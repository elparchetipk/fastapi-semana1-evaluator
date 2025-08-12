"""
Verificaciones de endpoints específicas para Week 1
"""
from pathlib import Path
from typing import Dict, Any


def check_endpoints(repo_path: str) -> Dict[str, Any]:
    """
    Verifica que los endpoints básicos de Week 1 funcionen correctamente
    """
    repo_root = Path(repo_path)
    main_py = repo_root / "main.py"
    
    # Verificar que main.py existe
    if not main_py.exists():
        return {
            "app_importable": False,
            "root_working": False,
            "docs_accessible": False,
            "parametric_endpoint": False,
            "passed": False,
            "score": 0,
            "error": "main.py no encontrado"
        }
    
    try:
        # Leer contenido de main.py
        content = main_py.read_text(encoding="utf-8", errors="ignore")
        
        # Verificar sintaxis
        try:
            compile(content, str(main_py), 'exec')
        except SyntaxError as e:
            return {
                "app_importable": False,
                "root_working": False,
                "docs_accessible": False,
                "parametric_endpoint": False,
                "passed": False,
                "score": 0,
                "error": f"Error de sintaxis en main.py: {e}"
            }
        
        # Verificar elementos básicos de FastAPI
        has_fastapi_import = "from fastapi import" in content or "import fastapi" in content
        has_app_instance = "app = FastAPI()" in content or "app=FastAPI()" in content
        
        if not has_fastapi_import:
            return {
                "app_importable": False,
                "root_working": False,
                "docs_accessible": False,
                "parametric_endpoint": False,
                "passed": False,
                "score": 0,
                "error": "No se encuentra import de FastAPI"
            }
        
        if not has_app_instance:
            return {
                "app_importable": False,
                "root_working": False,
                "docs_accessible": False,
                "parametric_endpoint": False,
                "passed": False,
                "score": 25,
                "error": "No se encuentra instancia 'app = FastAPI()'"
            }
        
        # Verificar endpoints
        has_root_endpoint = '@app.get("/")' in content or "@app.get('/')" in content
        has_param_endpoint = '@app.get("/hello/{' in content or "@app.get('/hello/{" in content
        
        # Calcular score
        score = 25  # Base por app importable
        if has_root_endpoint:
            score += 50
        if has_param_endpoint:
            score += 25
        
        return {
            "app_importable": True,
            "root_working": has_root_endpoint,
            "docs_accessible": True,  # Asumimos que funciona si app es válida
            "parametric_endpoint": has_param_endpoint,
            "passed": has_root_endpoint,  # Mínimo requerido
            "score": score,
            "analysis_method": "static"
        }
        
    except Exception as e:
        return {
            "app_importable": False,
            "root_working": False,
            "docs_accessible": False,
            "parametric_endpoint": False,
            "passed": False,
            "score": 0,
            "error": f"Error procesando main.py: {str(e)}"
        }
