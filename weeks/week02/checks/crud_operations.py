"""
Verificaciones de operaciones CRUD específicas para Week 2 - Versión autocontenida (análisis estático)
"""
from pathlib import Path
from typing import Dict, Any, List
import ast

# Métodos HTTP que nos interesan
HTTP_METHODS = {"get", "post", "put", "patch", "delete"}


def _collect_code(repo_root: Path) -> Dict[str, str]:
    """Recolecta contenido de archivos potencialmente relevantes."""
    targets: List[Path] = []
    for name in ["main.py", "models.py", "schemas.py"]:
        p = repo_root / name
        if p.exists():
            targets.append(p)
    for sub in ["routers", "routes"]:
        d = repo_root / sub
        if d.exists():
            targets.extend(sorted(d.glob("*.py")))
    contents = {}
    for p in targets:
        try:
            contents[str(p.relative_to(repo_root))] = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            pass
    return contents


def _parse_endpoints(all_code: str) -> List[Dict[str, Any]]:
    """Extrae endpoints usando AST buscando decoradores @app.<method>("/path")."""
    endpoints: List[Dict[str, Any]] = []
    try:
        tree = ast.parse(all_code)
    except SyntaxError:
        return endpoints
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for dec in node.decorator_list:
                # Formas posibles: @app.get("/items") o @router.post("/items/")
                if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                    method = dec.func.attr.lower()
                    if method in HTTP_METHODS:
                        path = None
                        if dec.args:
                            arg0 = dec.args[0]
                            if isinstance(arg0, ast.Constant) and isinstance(arg0.value, str):
                                path = arg0.value
                        # Extraer parámetros de path {param}
                        path_params = []
                        if path:
                            path_params = [seg[1:-1] for seg in path.split('/') if seg.startswith('{') and seg.endswith('}')]
                        endpoints.append({
                            "function": node.name,
                            "method": method.upper(),
                            "path": path or "",
                            "path_params": path_params
                        })
    return endpoints


def _detect_storage_patterns(all_code: str) -> bool:
    patterns = ["items =", "data =", "database", "storage", "_db", "memory_store"]
    low = all_code.lower()
    return any(p in low for p in patterns)


def _detect_model_usage(all_code: str) -> bool:
    return "BaseModel" in all_code


def _has_request_body_indicator(fn_src: str) -> bool:
    # Heurística simple: anotación de parámetro con BaseModel o dict
    return any(token in fn_src for token in [":", "BaseModel", "dict", "Request"])


def _split_functions_source(all_code: str) -> Dict[str, str]:
    mapping: Dict[str, str] = {}
    try:
        tree = ast.parse(all_code)
    except SyntaxError:
        return mapping
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            try:
                start = node.lineno - 1
                end = node.end_lineno  # type: ignore[attr-defined]
                lines = all_code.splitlines()
                mapping[node.name] = "\n".join(lines[start:end])
            except Exception:
                pass
    return mapping


def _classify_crud(endpoints: List[Dict[str, Any]]) -> Dict[str, bool]:
    """Clasifica presencia de operaciones CRUD basándose en método + path."""
    presence = {
        "create": False,
        "read": False,        # GET individual
        "read_all": False,    # GET colección
        "update": False,
        "delete": False
    }
    for ep in endpoints:
        path = ep.get("path", "").lower()
        method = ep.get("method")
        params = ep.get("path_params", [])
        if method == "POST":
            presence["create"] = True
        if method == "GET" and params:
            presence["read"] = True
        if method == "GET" and not params:
            presence["read_all"] = True
        if method in {"PUT", "PATCH"} and params:
            presence["update"] = True
        if method == "DELETE" and params:
            presence["delete"] = True
    return presence


def _calculate_crud_score(presence: Dict[str, bool], indicators: Dict[str, bool]) -> float:
    # 60% endpoints + 40% indicadores de implementación
    endpoint_score = sum(presence.values()) / 5 * 60
    impl_flags = [
        indicators.get("has_post", False),
        indicators.get("has_get", False),
        indicators.get("has_put_or_patch", False),
        indicators.get("has_delete", False),
        indicators.get("has_storage", False),
        indicators.get("has_model", False),
        indicators.get("has_request_body", False),
    ]
    impl_score = sum(impl_flags) / len(impl_flags) * 40
    return endpoint_score + impl_score


def check_crud_operations(repo_path: str) -> Dict[str, Any]:
    """Verifica operaciones CRUD mediante análisis estático (sin ejecutar código del estudiante)."""
    repo_root = Path(repo_path)
    if not repo_root.exists():
        return {"error": "Ruta no encontrada", "crud_score": 0}

    contents = _collect_code(repo_root)
    all_code = "\n".join(contents.values())
    endpoints = _parse_endpoints(all_code)
    functions_src = _split_functions_source(all_code)

    presence = _classify_crud(endpoints)

    # Indicadores de implementación
    indicators = {
        "has_post": any(ep["method"] == "POST" for ep in endpoints),
        "has_get": any(ep["method"] == "GET" for ep in endpoints),
        "has_put_or_patch": any(ep["method"] in {"PUT", "PATCH"} for ep in endpoints),
        "has_delete": any(ep["method"] == "DELETE" for ep in endpoints),
        "has_storage": _detect_storage_patterns(all_code),
        "has_model": _detect_model_usage(all_code),
        "has_request_body": any(_has_request_body_indicator(src) for src in functions_src.values()),
    }

    crud_score = _calculate_crud_score(presence, indicators)

    return {
        "analysis_method": "static",
        "endpoints_detected": endpoints,
        "presence": presence,
        "indicators": indicators,
        "create_operation": presence["create"],
        "read_operation": presence["read"],
        "read_all_operation": presence["read_all"],
        "update_operation": presence["update"],
        "delete_operation": presence["delete"],
        "crud_score": round(crud_score, 2)
    }


def check_specific_crud_operation(repo_path: str, operation: str) -> Dict[str, Any]:
    result = check_crud_operations(repo_path)
    mapping = {
        "create": "create_operation",
        "read": "read_operation",
        "read_all": "read_all_operation",
        "update": "update_operation",
        "delete": "delete_operation"
    }
    key = mapping.get(operation)
    if not key:
        return {"error": f"Operación desconocida: {operation}"}
    return {
        "operation": operation,
        "implemented": bool(result.get(key)),
        "crud_score": result.get("crud_score")
    }


def get_crud_recommendations(repo_path: str) -> List[str]:
    result = check_crud_operations(repo_path)
    rec: List[str] = []
    if result.get("error"):
        return ["No se pudo analizar CRUD: " + str(result.get("error"))]
    if not result.get("create_operation"):
        rec.append("Implementa un endpoint POST (crear recurso).")
    if not result.get("read_all_operation"):
        rec.append("Implementa GET colección (listar recursos).")
    if not result.get("read_operation"):
        rec.append("Implementa GET /recurso/{id} (obtener recurso individual).")
    if not result.get("update_operation"):
        rec.append("Implementa PUT/PATCH /recurso/{id} (actualizar).")
    if not result.get("delete_operation"):
        rec.append("Implementa DELETE /recurso/{id} (eliminar).")
    if not result.get("indicators", {}).get("has_model"):
        rec.append("Define modelos Pydantic (BaseModel) para validar datos.")
    if not result.get("indicators", {}).get("has_storage"):
        rec.append("Agrega una estructura de almacenamiento en memoria (lista o dict).")
    return rec
