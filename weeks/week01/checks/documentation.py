"""
Verificaciones de documentación específicas para Week 1
"""
import sys
from pathlib import Path
from typing import Dict, Any

# Importar las funciones del evaluador actual
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "evaluator"))

try:
    from checks_readme import check_readme
except ImportError:
    def check_readme(root):
        return {"exists": False, "error": "Could not import check_readme"}


def check_documentation(repo_path: str) -> Dict[str, Any]:
    """
    Verifica la documentación específica para Week 1
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de documentación
    """
    repo_root = Path(repo_path)
    
    # Usar el check existente de README
    readme_results = check_readme(repo_root)
    
    # Verificaciones adicionales específicas de Week 1
    additional_checks = check_week1_specific_docs(repo_root)
    
    return {
        "readme_exists": readme_results.get("exists", False),
        "has_setup_commands": readme_results.get("has_commands", False),
        "has_reflection": readme_results.get("has_reflection", False),
        "has_screenshot": readme_results.get("has_screenshot", False),
        "week1_specific": additional_checks
    }


def check_week1_specific_docs(repo_root: Path) -> Dict[str, Any]:
    """
    Verificaciones específicas de documentación para Week 1
    """
    readme_path = repo_root / "README.md"
    
    if not readme_path.exists():
        return {
            "has_fastapi_explanation": False,
            "has_endpoint_examples": False,
            "has_uvicorn_command": False
        }
    
    try:
        content = readme_path.read_text(encoding="utf-8", errors="ignore").lower()
        
        # Verificar explicación de FastAPI
        has_fastapi_explanation = any(term in content for term in [
            "fastapi", "api rest", "framework", "web api"
        ])
        
        # Verificar ejemplos de endpoints
        has_endpoint_examples = any(term in content for term in [
            "get /", "endpoint", "@app.get", "curl", "http://localhost"
        ])
        
        # Verificar comando uvicorn
        has_uvicorn_command = "uvicorn" in content and "main:app" in content
        
        return {
            "has_fastapi_explanation": has_fastapi_explanation,
            "has_endpoint_examples": has_endpoint_examples,
            "has_uvicorn_command": has_uvicorn_command,
            "content_length": len(content),
            "appears_complete": len(content) > 200  # Heurística básica
        }
        
    except Exception as e:
        return {
            "has_fastapi_explanation": False,
            "has_endpoint_examples": False,
            "has_uvicorn_command": False,
            "error": str(e)
        }


def check_docs_endpoint_accessibility(repo_path: str) -> Dict[str, Any]:
    """
    Verifica que el endpoint /docs sea accesible
    """
    try:
        # Esto se integra con el check de endpoints
        from .endpoints import check_endpoints
        
        endpoint_results = check_endpoints(repo_path)
        
        return {
            "docs_accessible": endpoint_results.get("docs_accessible", False),
            "message": "Documentación automática accesible" if endpoint_results.get("docs_accessible") else "Documentación automática no accesible",
            "suggestion": "" if endpoint_results.get("docs_accessible") else "Verifica que tu app FastAPI esté configurada correctamente y no tenga errores"
        }
        
    except Exception as e:
        return {
            "docs_accessible": False,
            "message": f"Error verificando /docs: {str(e)}",
            "suggestion": "Revisa la configuración de tu aplicación FastAPI"
        }
