"""
Verificaciones de endpoints específicas para Week 2 - Versión autocontenida (análisis estático)
"""
from pathlib import Path
from typing import Dict, Any, List
import ast

HTTP_METHODS = {"get", "post", "put", "patch", "delete"}


def _collect_source(repo_root: Path) -> Dict[str, str]:
    files: List[Path] = []
    for base in ["main.py", "models.py", "schemas.py"]:
        p = repo_root / base
        if p.exists():
            files.append(p)
    for sub in ["routers", "routes"]:
        d = repo_root / sub
        if d.exists():
            files.extend(sorted(d.glob("*.py")))
    out = {}
    for f in files:
        try:
            out[str(f.relative_to(repo_root))] = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            pass
    return out


def _parse_functions(all_code: str) -> List[Dict[str, Any]]:
    endpoints: List[Dict[str, Any]] = []
    try:
        tree = ast.parse(all_code)
    except SyntaxError:
        return endpoints
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for dec in node.decorator_list:
                if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                    method = dec.func.attr.lower()
                    if method in HTTP_METHODS:
                        path = ""
                        if dec.args:
                            a0 = dec.args[0]
                            if isinstance(a0, ast.Constant) and isinstance(a0.value, str):
                                path = a0.value
                        endpoints.append({
                            "function": node.name,
                            "method": method.upper(),
                            "path": path
                        })
    return endpoints


def _classify_crud(endpoints: List[Dict[str, Any]]) -> Dict[str, bool]:
    flags = {"create_items": False, "read_items": False, "read_item": False, "update_item": False, "delete_item": False, "items_list": False}
    for ep in endpoints:
        path = ep["path"].lower()
        method = ep["method"]
        has_param = "{" in path and "}" in path
        if method == "POST" and not has_param:
            flags["create_items"] = True
        if method == "GET" and not has_param:
            flags["read_items"] = True
        if method == "GET" and has_param:
            flags["read_item"] = True
        if method in {"PUT", "PATCH"} and has_param:
            flags["update_item"] = True
        if method == "DELETE" and has_param:
            flags["delete_item"] = True
    # items_list es sinónimo de read_items
    flags["items_list"] = flags["read_items"]
    return flags


def _detect_validation(all_code: str) -> Dict[str, bool]:
    return {
        "uses_pydantic_models": "BaseModel" in all_code,
        "has_request_validation": any(k in all_code for k in ["BaseModel", "Field(", ": str", ": int", ": float"]),
        "has_response_validation": "response_model=" in all_code,
        "has_path_parameters": "{" in all_code and "}" in all_code,
        "has_query_parameters": any(q in all_code for q in ["Query(", "Depends("]),
        "has_error_handling": any(e in all_code for e in ["HTTPException", "404", "422", "400", "status_code="])
    }


def _docs_indicators(all_code: str) -> Dict[str, bool]:
    # Si la app crea FastAPI() asumimos docs habilitadas
    return {
        "docs_working": "FastAPI(" in all_code,
        "swagger_ui": "FastAPI(" in all_code,
        "redoc": "FastAPI(" in all_code,
        "openapi_schema": "FastAPI(" in all_code
    }


def _endpoint_score(crud_flags: Dict[str, bool], docs: Dict[str, bool], validation: Dict[str, bool]) -> float:
    crud_cov = sum(crud_flags.values()) - int(crud_flags.get("items_list", False))  # evitar doble conteo
    crud_total = 5  # create, read_items, read_item, update, delete
    crud_score = (crud_cov / crud_total) * 50
    validation_keys = ["uses_pydantic_models", "has_request_validation", "has_response_validation", "has_path_parameters", "has_error_handling"]
    val_score = (sum(validation[k] for k in validation_keys) / len(validation_keys)) * 30
    docs_score = 20 if docs.get("docs_working") else 0
    return crud_score + val_score + docs_score


def check_endpoints(repo_path: str) -> Dict[str, Any]:
    repo_root = Path(repo_path)
    if not repo_root.exists():
        return {"error": "Ruta no encontrada", "endpoint_score": 0, "app_importable": False}

    sources = _collect_source(repo_root)
    all_code = "\n".join(sources.values())
    if not all_code:
        return {"error": "No se encontraron archivos fuente", "endpoint_score": 0, "app_importable": False}

    endpoints = _parse_functions(all_code)
    crud_flags = _classify_crud(endpoints)
    validation = _detect_validation(all_code)
    docs = _docs_indicators(all_code)
    score = _endpoint_score(crud_flags, docs, validation)

    return {
        "app_importable": "FastAPI(" in all_code,
        "endpoints_working": any(endpoints),
        "crud_endpoints": {**crud_flags, "crud_coverage": (sum(crud_flags.values()) - int(crud_flags.get("items_list", False))) / 5 * 100},
        "docs_accessible": docs.get("docs_working", False),
        "validation_in_endpoints": validation,
        "endpoint_details": endpoints,
        "endpoint_score": round(score, 2)
    }


def check_specific_endpoint(repo_path: str, endpoint_path: str, method: str = "GET") -> Dict[str, Any]:
    result = check_endpoints(repo_path)
    eps = result.get("endpoint_details", [])
    method = method.upper()
    found = any(e.get("path") == endpoint_path and e.get("method") == method for e in eps)
    return {"endpoint": endpoint_path, "method": method, "working": found}


def get_endpoint_recommendations(repo_path: str) -> List[str]:
    result = check_endpoints(repo_path)
    if result.get("error"):
        return ["No se pudo analizar endpoints: " + str(result.get("error"))]
    rec: List[str] = []
    crud = result.get("crud_endpoints", {})
    if not crud.get("create_items"):
        rec.append("Agregar POST para crear recursos.")
    if not crud.get("read_items"):
        rec.append("Agregar GET colección.")
    if not crud.get("read_item"):
        rec.append("Agregar GET /recurso/{id}.")
    if not crud.get("update_item"):
        rec.append("Agregar PUT/PATCH /recurso/{id}.")
    if not crud.get("delete_item"):
        rec.append("Agregar DELETE /recurso/{id}.")
    val = result.get("validation_in_endpoints", {})
    if not val.get("uses_pydantic_models"):
        rec.append("Definir modelos Pydantic para validación.")
    if not val.get("has_error_handling"):
        rec.append("Agregar manejo de errores con HTTPException.")
    return rec
