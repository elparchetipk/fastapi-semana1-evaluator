"""
Verificaciones de endpoints específicas para Week 1
"""
import sys
from pathlib import Path
from typing import Dict, Any

# Importar las funciones del evaluador actual para reutilización
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "evaluator"))

try:
    from checks_endpoints import probe_endpoints
    from checks_app_import import try_import_app
except ImportError:
    # Fallback si no se pueden importar
    def probe_endpoints(app_import_result):
        return {"ok": False, "error": "Could not import probe_endpoints"}
    
    def try_import_app(root):
        return {"import_ok": False, "error": "Could not import try_import_app"}


def check_endpoints(repo_path: str) -> Dict[str, Any]:
    """
    Verifica que los endpoints básicos de Week 1 funcionen correctamente
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de endpoints
    """
    repo_root = Path(repo_path)
    
    # Primero intentar importar la app
    app_import_result = try_import_app(repo_root)
    
    if not app_import_result.get("import_ok"):
        return {
            "app_importable": False,
            "root_working": False,
            "docs_accessible": False,
            "parametric_endpoint": False,
            "error": app_import_result.get("error", "Unknown import error")
        }
    
    # Probar endpoints usando el evaluador existente
    endpoint_results = probe_endpoints(app_import_result)
    
    return {
        "app_importable": True,
        "root_working": endpoint_results.get("root", {}).get("status") == 200,
        "root_returns_json": endpoint_results.get("root", {}).get("json_like", False),
        "docs_accessible": endpoint_results.get("docs", {}).get("status") in [200, 307, 308],
        "parametric_endpoint": endpoint_results.get("hello_param", False),
        "endpoint_details": endpoint_results
    }


def check_hello_world_endpoint(repo_path: str) -> Dict[str, Any]:
    """
    Verificación específica del endpoint raíz (Hello World)
    """
    try:
        endpoint_results = check_endpoints(repo_path)
        
        if not endpoint_results.get("root_working"):
            return {
                "working": False,
                "message": "Endpoint GET / no responde correctamente",
                "suggestion": "Implementa @app.get('/') def root(): return {'message': 'Hello World'}"
            }
        
        if not endpoint_results.get("root_returns_json"):
            return {
                "working": False,
                "message": "Endpoint GET / no retorna JSON válido",
                "suggestion": "Asegúrate de retornar un diccionario o usar JSONResponse"
            }
        
        return {
            "working": True,
            "message": "Endpoint Hello World funcionando correctamente"
        }
        
    except Exception as e:
        return {
            "working": False,
            "message": f"Error verificando endpoint: {str(e)}",
            "suggestion": "Revisa que tu aplicación FastAPI esté configurada correctamente"
        }
