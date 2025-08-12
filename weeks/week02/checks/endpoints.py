"""
Verificaciones de endpoints específicas para Week 2
Enfoque en endpoints CRUD y validación de datos
"""
import sys
from pathlib import Path
from typing import Dict, Any, List

# Importar las funciones del evaluador actual para reutilización
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "evaluator"))

try:
    from checks_endpoints import probe_endpoints
    from checks_app_import import try_import_app
except ImportError:
    def probe_endpoints(app_import_result):
        return {"ok": False, "error": "Could not import probe_endpoints"}
    
    def try_import_app(root):
        return {"import_ok": False, "error": "Could not import try_import_app"}


def check_endpoints(repo_path: str) -> Dict[str, Any]:
    """
    Verifica los endpoints específicos para Week 2
    
    Enfoque en:
    - Endpoints CRUD básicos
    - Validación de entrada y salida
    - Manejo de errores HTTP
    - Documentación automática
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de endpoints
    """
    repo_root = Path(repo_path)
    
    # Intentar importar la app
    app_import_result = try_import_app(repo_root)
    
    if not app_import_result.get("import_ok"):
        return {
            "app_importable": False,
            "endpoints_working": False,
            "crud_endpoints": {},
            "docs_accessible": False,
            "error": app_import_result.get("error", "Unknown import error")
        }
    
    # Probar endpoints usando el evaluador existente
    endpoint_results = probe_endpoints(app_import_result)
    
    # Análisis específico de endpoints CRUD
    crud_analysis = _analyze_crud_endpoints(endpoint_results)
    
    # Verificar documentación automática
    docs_analysis = _check_docs_endpoints(endpoint_results)
    
    # Análisis de validación en endpoints
    validation_analysis = _analyze_endpoint_validation(repo_root)
    
    return {
        "app_importable": True,
        "endpoints_working": len([r for r in endpoint_results.values() if isinstance(r, dict) and r.get("status") == 200]) > 0,
        "crud_endpoints": crud_analysis,
        "docs_accessible": docs_analysis["docs_working"],
        "validation_in_endpoints": validation_analysis,
        "endpoint_details": endpoint_results,
        "endpoint_score": _calculate_endpoint_score(crud_analysis, docs_analysis, validation_analysis)
    }


def _analyze_crud_endpoints(endpoint_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analiza específicamente los endpoints CRUD
    """
    crud_endpoints = {
        "create_items": False,
        "read_items": False,
        "read_item": False,
        "update_item": False,
        "delete_item": False,
        "items_list": False
    }
    
    status_details = {}
    
    # Patrones de endpoints CRUD esperados para Week 2
    crud_patterns = {
        "create_items": ["/items", "/item"],  # POST
        "read_items": ["/items", "/"],  # GET lista
        "read_item": ["/items/", "/item/"],  # GET específico
        "update_item": ["/items/", "/item/"],  # PUT específico
        "delete_item": ["/items/", "/item/"],  # DELETE específico
        "items_list": ["/items", "/all", "/list"]  # GET lista alternativo
    }
    
    # Analizar cada endpoint probado
    for endpoint_path, result in endpoint_results.items():
        if isinstance(result, dict):
            status = result.get("status", 0)
            method = result.get("method", "GET").upper()
            
            status_details[endpoint_path] = {
                "status": status,
                "method": method,
                "working": status in [200, 201, 204]
            }
            
            # Verificar patrones CRUD
            endpoint_lower = endpoint_path.lower()
            
            for crud_op, patterns in crud_patterns.items():
                if any(pattern in endpoint_lower for pattern in patterns):
                    if status in [200, 201, 204]:
                        crud_endpoints[crud_op] = True
    
    return {
        **crud_endpoints,
        "status_details": status_details,
        "total_working": sum(crud_endpoints.values()),
        "crud_coverage": sum(crud_endpoints.values()) / len(crud_endpoints) * 100
    }


def _check_docs_endpoints(endpoint_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verifica la accesibilidad de la documentación automática
    """
    docs_endpoints = ["/docs", "/redoc", "/openapi.json"]
    docs_status = {}
    
    for docs_endpoint in docs_endpoints:
        if docs_endpoint in endpoint_results:
            result = endpoint_results[docs_endpoint]
            if isinstance(result, dict):
                docs_status[docs_endpoint] = {
                    "accessible": result.get("status") in [200, 307, 308],
                    "status": result.get("status", 0)
                }
        else:
            docs_status[docs_endpoint] = {"accessible": False, "status": 0}
    
    docs_working = any(status["accessible"] for status in docs_status.values())
    
    return {
        "docs_working": docs_working,
        "docs_status": docs_status,
        "swagger_ui": docs_status.get("/docs", {}).get("accessible", False),
        "redoc": docs_status.get("/redoc", {}).get("accessible", False),
        "openapi_schema": docs_status.get("/openapi.json", {}).get("accessible", False)
    }


def _analyze_endpoint_validation(repo_root: Path) -> Dict[str, Any]:
    """
    Analiza la implementación de validación en endpoints
    """
    validation_analysis = {
        "uses_pydantic_models": False,
        "has_request_validation": False,
        "has_response_validation": False,
        "has_path_parameters": False,
        "has_query_parameters": False,
        "has_error_handling": False
    }
    
    # Archivos a analizar
    files_to_check = ["main.py", "routers/*.py", "routes/*.py"]
    
    code_content = ""
    for file_pattern in files_to_check:
        if "*" in file_pattern:
            # Pattern matching para routers/routes
            for subdir in ["routers", "routes"]:
                router_dir = repo_root / subdir
                if router_dir.exists():
                    for py_file in router_dir.glob("*.py"):
                        try:
                            with open(py_file, 'r', encoding='utf-8') as f:
                                code_content += f.read() + "\n"
                        except:
                            continue
        else:
            file_path = repo_root / file_pattern
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        code_content += f.read() + "\n"
                except:
                    continue
    
    if code_content:
        # Analizar patrones de validación
        validation_analysis.update({
            "uses_pydantic_models": "BaseModel" in code_content,
            "has_request_validation": any(pattern in code_content for pattern in [
                "request:", "body:", "item:", "data:", "payload:"
            ]),
            "has_response_validation": any(pattern in code_content for pattern in [
                "response_model=", "return {", "-> dict", "-> Dict"
            ]),
            "has_path_parameters": "{" in code_content and "}" in code_content,
            "has_query_parameters": any(pattern in code_content for pattern in [
                "Query(", "query:", "params:"
            ]),
            "has_error_handling": any(pattern in code_content for pattern in [
                "HTTPException", "raise", "404", "400", "422", "status_code"
            ])
        })
    
    return validation_analysis


def _calculate_endpoint_score(crud_analysis: Dict[str, Any], 
                            docs_analysis: Dict[str, Any],
                            validation_analysis: Dict[str, Any]) -> float:
    """
    Calcula el score total de endpoints para Week 2
    """
    score = 0
    
    # CRUD endpoints (50% del score)
    crud_coverage = crud_analysis.get("crud_coverage", 0)
    score += crud_coverage * 0.5
    
    # Documentación (20% del score)
    if docs_analysis.get("docs_working", False):
        score += 20
    
    # Validación (30% del score)
    validation_indicators = [
        validation_analysis.get("uses_pydantic_models", False),
        validation_analysis.get("has_request_validation", False),
        validation_analysis.get("has_response_validation", False),
        validation_analysis.get("has_path_parameters", False),
        validation_analysis.get("has_error_handling", False)
    ]
    
    validation_score = sum(validation_indicators) / len(validation_indicators) * 30
    score += validation_score
    
    return score


def check_specific_endpoint(repo_path: str, endpoint_path: str, method: str = "GET") -> Dict[str, Any]:
    """
    Verifica un endpoint específico
    
    Args:
        repo_path: Ruta al repositorio
        endpoint_path: Path del endpoint (ej: "/items", "/items/1")
        method: Método HTTP (GET, POST, PUT, DELETE)
    """
    endpoint_results = check_endpoints(repo_path)
    
    if not endpoint_results.get("app_importable", False):
        return {
            "endpoint": endpoint_path,
            "method": method,
            "working": False,
            "error": "App not importable"
        }
    
    # Buscar el endpoint en los resultados
    endpoint_details = endpoint_results.get("endpoint_details", {})
    
    # Verificar diferentes variaciones del endpoint
    possible_keys = [endpoint_path, f"{endpoint_path}/", endpoint_path.rstrip("/")]
    
    for key in possible_keys:
        if key in endpoint_details:
            result = endpoint_details[key]
            if isinstance(result, dict):
                return {
                    "endpoint": endpoint_path,
                    "method": method,
                    "working": result.get("status") in [200, 201, 204],
                    "status": result.get("status", 0),
                    "details": result
                }
    
    return {
        "endpoint": endpoint_path,
        "method": method,
        "working": False,
        "status": 0,
        "error": "Endpoint not found or not tested"
    }


def get_endpoint_recommendations(repo_path: str) -> List[str]:
    """
    Genera recomendaciones específicas para endpoints de Week 2
    """
    endpoint_results = check_endpoints(repo_path)
    recommendations = []
    
    if not endpoint_results.get("app_importable", False):
        recommendations.append("Asegúrate de que la aplicación FastAPI sea importable")
        return recommendations
    
    # Recomendaciones para CRUD endpoints
    crud_endpoints = endpoint_results.get("crud_endpoints", {})
    
    if not crud_endpoints.get("create_items", False):
        recommendations.append("Implementa POST /items para crear nuevos items")
    
    if not crud_endpoints.get("read_items", False):
        recommendations.append("Implementa GET /items para listar todos los items")
    
    if not crud_endpoints.get("read_item", False):
        recommendations.append("Implementa GET /items/{item_id} para obtener un item específico")
    
    if not crud_endpoints.get("update_item", False):
        recommendations.append("Implementa PUT /items/{item_id} para actualizar items")
    
    if not crud_endpoints.get("delete_item", False):
        recommendations.append("Implementa DELETE /items/{item_id} para eliminar items")
    
    # Recomendaciones para documentación
    docs_analysis = endpoint_results.get("docs_accessible", False)
    if not docs_analysis:
        recommendations.append("Asegúrate de que /docs sea accesible para la documentación automática")
    
    # Recomendaciones para validación
    validation = endpoint_results.get("validation_in_endpoints", {})
    
    if not validation.get("uses_pydantic_models", False):
        recommendations.append("Usa modelos Pydantic para validar datos de entrada y salida")
    
    if not validation.get("has_error_handling", False):
        recommendations.append("Implementa manejo de errores con HTTPException")
    
    if not validation.get("has_path_parameters", False):
        recommendations.append("Usa parámetros de path para identificar recursos específicos")
    
    return recommendations
