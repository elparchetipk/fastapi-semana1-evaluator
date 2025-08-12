"""
Verificaciones de documentación específicas para Week 1 - Versión autocontenida
"""
from pathlib import Path
from typing import Dict, Any


def check_readme_exists_and_content(repo_path: str) -> Dict[str, Any]:
    """
    Verifica que README.md existe y tiene contenido adecuado
    """
    repo_root = Path(repo_path)
    readme_path = repo_root / "README.md"
    
    if not readme_path.exists():
        return {
            "exists": False,
            "has_content": False,
            "estimated_completeness": 0,
            "error": "README.md no encontrado"
        }
    
    try:
        content = readme_path.read_text(encoding="utf-8", errors="ignore")
        content_lower = content.lower()
        
        # Verificaciones básicas de contenido
        checks = {
            "has_title": any(line.startswith('#') for line in content.split('\n')),
            "has_description": len(content) > 50,
            "mentions_fastapi": "fastapi" in content_lower,
            "has_installation": any(word in content_lower for word in ["instalación", "install", "pip"]),
            "has_usage": any(word in content_lower for word in ["uso", "usage", "ejecutar", "run"]),
            "has_endpoints": any(word in content_lower for word in ["endpoint", "api", "get /"]),
            "has_uvicorn_command": "uvicorn" in content_lower and "main:app" in content_lower
        }
        
        # Calcular completeness score
        completeness = sum(checks.values()) / len(checks) * 100
        
        return {
            "exists": True,
            "has_content": len(content.strip()) > 0,
            "content_length": len(content),
            "estimated_completeness": completeness,
            "checks": checks,
            "passed": completeness >= 60,  # 60% de los checks deben pasar
            "score": min(100, completeness * 1.2)  # Bonus por completeness
        }
        
    except Exception as e:
        return {
            "exists": True,
            "has_content": False,
            "estimated_completeness": 0,
            "error": f"Error leyendo README.md: {str(e)}",
            "passed": False,
            "score": 0
        }


def check_documentation(repo_path: str) -> Dict[str, Any]:
    """
    Verifica la documentación específica para Week 1
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de documentación
    """
    # Usar el check de README autocontenido
    readme_results = check_readme_exists_and_content(repo_path)
    
    # Verificaciones adicionales específicas de Week 1
    additional_checks = check_week1_specific_docs(repo_path)
    
    # Combinar resultados
    return {
        "readme_exists": readme_results.get("exists", False),
        "has_setup_commands": additional_checks.get("has_uvicorn_command", False),
        "has_reflection": additional_checks.get("has_fastapi_explanation", False),
        "has_screenshot": False,  # No verificamos screenshots en Week 1
        "week1_specific": additional_checks,
        "readme_analysis": readme_results,
        "passed": readme_results.get("passed", False),
        "score": readme_results.get("score", 0)
    }


def check_week1_specific_docs(repo_path: str) -> Dict[str, Any]:
    """
    Verificaciones específicas de documentación para Week 1
    """
    repo_root = Path(repo_path)
    readme_path = repo_root / "README.md"
    
    if not readme_path.exists():
        return {
            "has_fastapi_explanation": False,
            "has_endpoint_examples": False,
            "has_uvicorn_command": False,
            "appears_complete": False
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
            "error": str(e),
            "appears_complete": False
        }


def check_docs_endpoint_accessibility(repo_path: str) -> Dict[str, Any]:
    """
    Verifica que el endpoint /docs sea accesible (integración con checks de endpoints)
    """
    try:
        # Importar desde el mismo directorio
        from .endpoints import safe_import_app
        
        app_import_result = safe_import_app(repo_path)
        
        docs_accessible = app_import_result.get("import_ok", False)
        
        return {
            "docs_accessible": docs_accessible,
            "message": "Documentación automática accesible" if docs_accessible else "Documentación automática no accesible",
            "suggestion": "" if docs_accessible else "Verifica que tu app FastAPI esté configurada correctamente y no tenga errores",
            "passed": docs_accessible,
            "score": 100 if docs_accessible else 0
        }
        
    except Exception as e:
        return {
            "docs_accessible": False,
            "message": f"Error verificando /docs: {str(e)}",
            "suggestion": "Revisa la configuración de tu aplicación FastAPI",
            "passed": False,
            "score": 0
        }
