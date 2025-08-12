"""
Verificaciones de operaciones CRUD específicas para Week 2
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


def check_crud_operations(repo_path: str) -> Dict[str, Any]:
    """
    Verifica que las operaciones CRUD básicas estén implementadas y funcionen
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de operaciones CRUD
    """
    repo_root = Path(repo_path)
    
    # Primero intentar importar la app
    app_import_result = try_import_app(repo_root)
    
    if not app_import_result.get("import_ok"):
        return {
            "app_importable": False,
            "create_operation": False,
            "read_operation": False,
            "read_all_operation": False,
            "update_operation": False,
            "delete_operation": False,
            "crud_score": 0,
            "error": app_import_result.get("error", "Unknown import error")
        }
    
    # Probar endpoints CRUD
    endpoint_results = probe_endpoints(app_import_result)
    
    # Analizar el código para buscar operaciones CRUD
    crud_analysis = _analyze_crud_code(repo_root)
    
    # Verificar endpoints CRUD típicos
    crud_endpoints = _check_crud_endpoints(endpoint_results)
    
    # Calcular score de CRUD
    crud_score = _calculate_crud_score(crud_endpoints, crud_analysis)
    
    return {
        "app_importable": True,
        "create_operation": crud_endpoints.get("create", False),
        "read_operation": crud_endpoints.get("read", False),
        "read_all_operation": crud_endpoints.get("read_all", False),
        "update_operation": crud_endpoints.get("update", False),
        "delete_operation": crud_endpoints.get("delete", False),
        "crud_in_code": crud_analysis,
        "crud_endpoints": crud_endpoints,
        "crud_score": crud_score,
        "endpoint_details": endpoint_results
    }


def _analyze_crud_code(repo_root: Path) -> Dict[str, Any]:
    """
    Analiza el código para detectar patrones de operaciones CRUD
    """
    analysis = {
        "has_post_decorator": False,
        "has_get_decorator": False,
        "has_put_decorator": False,
        "has_delete_decorator": False,
        "has_data_storage": False,
        "has_item_model": False,
        "uses_path_parameters": False,
        "uses_request_body": False
    }
    
    # Archivos a analizar
    files_to_check = ["main.py", "models.py", "schemas.py", "routers/*.py"]
    
    code_content = ""
    for file_pattern in files_to_check:
        if "*" in file_pattern:
            # Pattern matching para routers
            router_dir = repo_root / "routers"
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
        # Analizar patrones CRUD
        analysis.update({
            "has_post_decorator": "@app.post(" in code_content or "@router.post(" in code_content,
            "has_get_decorator": "@app.get(" in code_content or "@router.get(" in code_content,
            "has_put_decorator": "@app.put(" in code_content or "@router.put(" in code_content,
            "has_delete_decorator": "@app.delete(" in code_content or "@router.delete(" in code_content,
            "has_data_storage": any(keyword in code_content.lower() for keyword in ["items = ", "data = ", "database", "storage"]),
            "has_item_model": "BaseModel" in code_content,
            "uses_path_parameters": "{" in code_content and "}" in code_content,
            "uses_request_body": any(param in code_content for param in ["request:", "body:", "item:", "data:"])
        })
    
    return analysis


def _check_crud_endpoints(endpoint_results: Dict[str, Any]) -> Dict[str, bool]:
    """
    Verifica endpoints CRUD específicos basándose en los resultados de pruebas
    """
    crud_endpoints = {
        "create": False,
        "read": False,
        "read_all": False,
        "update": False,
        "delete": False
    }
    
    # Patrones comunes de endpoints CRUD
    crud_patterns = {
        "create": ["items", "item", "create", "add"],
        "read": ["items/{", "item/{", "get/"],
        "read_all": ["items", "all", "list"],
        "update": ["items/{", "item/{", "update/", "put/"],
        "delete": ["items/{", "item/{", "delete/", "remove/"]
    }
    
    # Analizar los resultados de endpoints
    for endpoint_path, result in endpoint_results.items():
        if isinstance(result, dict) and result.get("status") in [200, 201, 204]:
            endpoint_lower = endpoint_path.lower()
            
            # Verificar patrones para cada operación CRUD
            for operation, patterns in crud_patterns.items():
                if any(pattern in endpoint_lower for pattern in patterns):
                    crud_endpoints[operation] = True
    
    return crud_endpoints


def _calculate_crud_score(crud_endpoints: Dict[str, bool], crud_analysis: Dict[str, Any]) -> float:
    """
    Calcula el score total de las operaciones CRUD
    """
    # Score por endpoints funcionando (60% del total)
    endpoint_score = sum(crud_endpoints.values()) / len(crud_endpoints) * 60
    
    # Score por implementación en código (40% del total)
    code_indicators = [
        crud_analysis.get("has_post_decorator", False),
        crud_analysis.get("has_get_decorator", False),
        crud_analysis.get("has_put_decorator", False) or crud_analysis.get("has_delete_decorator", False),
        crud_analysis.get("has_data_storage", False),
        crud_analysis.get("has_item_model", False),
        crud_analysis.get("uses_path_parameters", False),
        crud_analysis.get("uses_request_body", False)
    ]
    
    code_score = sum(code_indicators) / len(code_indicators) * 40
    
    return endpoint_score + code_score


def check_specific_crud_operation(repo_path: str, operation: str) -> Dict[str, Any]:
    """
    Verifica una operación CRUD específica
    
    Args:
        repo_path: Ruta al repositorio
        operation: Operación a verificar ('create', 'read', 'update', 'delete')
    """
    crud_result = check_crud_operations(repo_path)
    
    operation_map = {
        "create": "create_operation",
        "read": "read_operation", 
        "update": "update_operation",
        "delete": "delete_operation"
    }
    
    if operation not in operation_map:
        return {"error": f"Unknown operation: {operation}"}
    
    operation_key = operation_map[operation]
    working = crud_result.get(operation_key, False)
    
    suggestions = {
        "create": "Implementa un endpoint POST para crear nuevos items",
        "read": "Implementa un endpoint GET para leer items específicos",
        "update": "Implementa un endpoint PUT para actualizar items existentes", 
        "delete": "Implementa un endpoint DELETE para eliminar items"
    }
    
    return {
        "operation": operation,
        "working": working,
        "suggestion": suggestions.get(operation, ""),
        "details": crud_result.get("crud_endpoints", {}).get(operation, False)
    }


def get_crud_recommendations(repo_path: str) -> List[str]:
    """
    Genera recomendaciones específicas para mejorar las operaciones CRUD
    """
    crud_result = check_crud_operations(repo_path)
    recommendations = []
    
    if not crud_result.get("app_importable", False):
        recommendations.append("Asegúrate de que la aplicación FastAPI sea importable y ejecutable")
        return recommendations
    
    # Verificar cada operación CRUD
    operations = {
        "create_operation": "Implementa un endpoint POST para crear items (ej: @app.post('/items/'))",
        "read_operation": "Implementa un endpoint GET para leer un item específico (ej: @app.get('/items/{item_id}'))",
        "read_all_operation": "Implementa un endpoint GET para listar todos los items (ej: @app.get('/items/'))",
        "update_operation": "Implementa un endpoint PUT para actualizar items (ej: @app.put('/items/{item_id}'))",
        "delete_operation": "Implementa un endpoint DELETE para eliminar items (ej: @app.delete('/items/{item_id}'))"
    }
    
    for operation, recommendation in operations.items():
        if not crud_result.get(operation, False):
            recommendations.append(f"• {recommendation}")
    
    # Recomendaciones adicionales basadas en el análisis de código
    crud_analysis = crud_result.get("crud_in_code", {})
    
    if not crud_analysis.get("has_item_model", False):
        recommendations.append("• Define un modelo Pydantic para representar tus items")
    
    if not crud_analysis.get("has_data_storage", False):
        recommendations.append("• Crea una estructura de datos en memoria para almacenar los items")
    
    if not crud_analysis.get("uses_path_parameters", False):
        recommendations.append("• Usa parámetros de path para identificar items específicos")
    
    if not crud_analysis.get("uses_request_body", False):
        recommendations.append("• Usa el cuerpo de la petición para recibir datos en POST/PUT")
    
    return recommendations
