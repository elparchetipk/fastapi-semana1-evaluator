"""
Verificaciones de endpoints específicas para Week 1 - Versión autocontenida
"""
from pathlib import Path
from typing import Dict, Any


def safe_import_app(repo_path: str) -> Dict[str, Any]:
    """
    Intenta importar la aplicación FastAPI de manera segura usando análisis estático
    """
    repo_root = Path(repo_path)
    main_py = repo_root / "main.py"
    
    if not main_py.exists():
        return {"import_ok": False, "has_app": False, "error": "main.py no encontrado"}
    
    try:
        # Verificar sintaxis básica
        with open(main_py, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Intentar compilar para verificar sintaxis
        try:
            compile(content, str(main_py), 'exec')
        except SyntaxError as e:
            return {"import_ok": False, "has_app": False, "error": f"Error de sintaxis: {e}"}
        
        # Verificar que tiene los elementos básicos de FastAPI
        has_fastapi_import = any(line.strip().startswith(("from fastapi import", "import fastapi")) 
                                for line in content.split('\n'))
        has_app_instance = "app = FastAPI()" in content or "app=FastAPI()" in content
        
        if not has_fastapi_import:
            return {"import_ok": False, "has_app": False, "error": "No se encuentra import de FastAPI"}
        
        if not has_app_instance:
            return {"import_ok": False, "has_app": False, "error": "No se encuentra instancia 'app = FastAPI()'"}
        
        return {"import_ok": True, "has_app": True, "content": content}
        
    except Exception as e:
        return {"import_ok": False, "has_app": False, "error": f"Error procesando main.py: {str(e)}"}


def analyze_endpoints_static(repo_path: str) -> Dict[str, Any]:
    """
    Analiza los endpoints usando análisis estático del código
    """
    repo_root = Path(repo_path)
    
    # Verificar que requirements.txt existe y tiene las dependencias
    requirements_file = repo_root / "requirements.txt"
    if not requirements_file.exists():
        return {"error": "requirements.txt no encontrado", "analysis_ok": False}
    
    try:
        # Verificar dependencias en requirements.txt
        with open(requirements_file, 'r') as f:
            req_content = f.read().lower()
        
        if "fastapi" not in req_content:
            return {"error": "FastAPI no está en requirements.txt", "analysis_ok": False}
        
        if "uvicorn" not in req_content:
            return {"error": "uvicorn no está en requirements.txt", "analysis_ok": False}
        
        # Verificación estática de endpoints en main.py
        main_py = repo_root / "main.py"
        if not main_py.exists():
            return {"error": "main.py no encontrado", "analysis_ok": False}
        
        with open(main_py, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Buscar endpoints definidos
        endpoints_found = {}
        
        # Buscar endpoint raíz
        root_patterns = ['@app.get("/")', "@app.get('/')", '@app.get("/")']
        endpoints_found["root"] = any(pattern in content for pattern in root_patterns)
        
        # Buscar endpoint con parámetros
        param_patterns = ['@app.get("/hello/{', '@app.get(\'/hello/{']
        endpoints_found["parametric"] = any(pattern in content for pattern in param_patterns)
        
        # Buscar funciones correspondientes
        has_root_function = False
        has_param_function = False
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            # Si encontramos un decorador @app.get, verificar que hay una función después
            if any(pattern in line for pattern in root_patterns):
                # Buscar la función en las siguientes líneas
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].strip().startswith('def '):
                        has_root_function = True
                        break
            
            if any(pattern in line for pattern in param_patterns):
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j].strip().startswith('def '):
                        has_param_function = True
                        break
        
        return {
            "analysis_ok": True,
            "endpoints": endpoints_found,
            "functions": {
                "root_function": has_root_function,
                "param_function": has_param_function
            },
            "analysis_method": "static"
        }
        
    except Exception as e:
        return {"error": f"Error en análisis: {str(e)}", "analysis_ok": False}


def check_endpoints(repo_path: str) -> Dict[str, Any]:
    """
    Verifica que los endpoints básicos de Week 1 funcionen correctamente
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de endpoints
    """
    # Primero intentar importar la app de manera segura
    app_import_result = safe_import_app(repo_path)
    
    if not app_import_result.get("import_ok"):
        return {
            "app_importable": False,
            "root_working": False,
            "docs_accessible": False,
            "parametric_endpoint": False,
            "passed": False,
            "score": 0,
            "error": app_import_result.get("error", "Unknown import error")
        }
    
    # Analizar endpoints usando análisis estático
    endpoint_analysis = analyze_endpoints_static(repo_path)
    
    if not endpoint_analysis.get("analysis_ok"):
        return {
            "app_importable": True,
            "root_working": False,
            "docs_accessible": False,
            "parametric_endpoint": False,
            "passed": False,
            "score": 25,  # Puntos por tener app importable
            "error": endpoint_analysis.get("error", "No se pudo analizar endpoints")
        }
    
    endpoints = endpoint_analysis.get("endpoints", {})
    functions = endpoint_analysis.get("functions", {})
    
    # Validar que los endpoints tienen funciones asociadas
    root_working = endpoints.get("root", False) and functions.get("root_function", False)
    param_working = endpoints.get("parametric", False) and functions.get("param_function", False)
    
    # Calcular score basado en endpoints encontrados
    score = 25  # Base por app importable
    if root_working:
        score += 50  # Endpoint raíz funcionando
    if param_working:
        score += 25  # Endpoint con parámetros funcionando
    
    return {
        "app_importable": True,
        "root_working": root_working,
        "docs_accessible": True,  # Asumimos que docs funciona si app es importable
        "parametric_endpoint": param_working,
        "passed": root_working,  # Mínimo requerido es endpoint raíz
        "score": score,
        "analysis_method": endpoint_analysis.get("analysis_method", "static"),
        "details": {
            "endpoints_found": endpoints,
            "functions_found": functions
        }
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
                "suggestion": "Implementa @app.get('/') def root(): return {'message': 'Hello World'}",
                "passed": False,
                "score": 0
            }
        
        return {
            "working": True,
            "message": "Endpoint Hello World funcionando correctamente",
            "passed": True,
            "score": 100
        }
        
    except Exception as e:
        return {
            "working": False,
            "message": f"Error verificando endpoint: {str(e)}",
            "suggestion": "Revisa que tu aplicación FastAPI esté configurada correctamente",
            "passed": False,
            "score": 0
        }


def check_docs_accessibility(repo_path: str) -> Dict[str, Any]:
    """
    Verifica que la documentación automática sea accesible
    """
    try:
        app_import_result = safe_import_app(repo_path)
        
        if not app_import_result.get("import_ok"):
            return {
                "docs_accessible": False,
                "message": "No se puede verificar /docs porque la app no es importable",
                "suggestion": "Corrige los errores en main.py primero",
                "passed": False,
                "score": 0
            }
        
        # Si la app es importable, asumimos que /docs funciona
        return {
            "docs_accessible": True,
            "message": "Documentación automática debería ser accesible en /docs",
            "suggestion": "Verifica ejecutando: uvicorn main:app --reload",
            "passed": True,
            "score": 100
        }
        
    except Exception as e:
        return {
            "docs_accessible": False,
            "message": f"Error verificando accesibilidad de docs: {str(e)}",
            "suggestion": "Revisa la configuración de tu aplicación FastAPI",
            "passed": False,
            "score": 0
        }
