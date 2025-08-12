"""
Verificaciones de estructura de proyecto específicas para Week 1 - Versión autocontenida
"""
from pathlib import Path
from typing import Dict, Any, List


def check_required_files(repo_path: str) -> Dict[str, Any]:
    """
    Verifica que los archivos requeridos estén presentes
    """
    repo_root = Path(repo_path)
    required_files = ["main.py", "requirements.txt", "README.md"]
    
    file_status = {}
    missing_files = []
    present_files = []
    
    for file_name in required_files:
        file_path = repo_root / file_name
        exists = file_path.exists()
        file_status[file_name] = exists
        
        if exists:
            present_files.append(file_name)
        else:
            missing_files.append(file_name)
    
    return {
        "file_status": file_status,
        "present_files": present_files,
        "missing_files": missing_files,
        "all_present": len(missing_files) == 0,
        "score": (len(present_files) / len(required_files)) * 100
    }


def check_requirements_dependencies(repo_path: str) -> Dict[str, Any]:
    """
    Verifica que requirements.txt tenga las dependencias necesarias
    """
    repo_root = Path(repo_path)
    requirements_file = repo_root / "requirements.txt"
    
    if not requirements_file.exists():
        return {
            "file_exists": False,
            "fastapi": False,
            "uvicorn": False,
            "all_dependencies": False,
            "error": "requirements.txt no encontrado",
            "score": 0
        }
    
    try:
        content = requirements_file.read_text(encoding="utf-8", errors="ignore").lower()
        
        has_fastapi = "fastapi" in content
        has_uvicorn = "uvicorn" in content
        
        # Verificar versiones mínimas (opcional)
        version_warnings = []
        if has_fastapi and "fastapi>=" not in content and "fastapi==" not in content:
            version_warnings.append("Considera especificar versión de FastAPI")
        
        return {
            "file_exists": True,
            "fastapi": has_fastapi,
            "uvicorn": has_uvicorn,
            "all_dependencies": has_fastapi and has_uvicorn,
            "version_warnings": version_warnings,
            "content": content[:200],  # Primeros 200 caracteres para debug
            "score": (sum([has_fastapi, has_uvicorn]) / 2) * 100
        }
        
    except Exception as e:
        return {
            "file_exists": True,
            "fastapi": False,
            "uvicorn": False,
            "all_dependencies": False,
            "error": f"Error leyendo requirements.txt: {str(e)}",
            "score": 0
        }


def check_project_structure(repo_path: str) -> Dict[str, Any]:
    """
    Verifica la estructura del proyecto específica para Week 1
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de estructura
    """
    # Usar checks autocontenidos
    files_check = check_required_files(repo_path)
    requirements_check = check_requirements_dependencies(repo_path)
    
    # Verificaciones adicionales específicas de Week 1
    week1_structure = check_week1_structure_details(repo_path)
    
    # Calcular score general
    overall_score = (
        files_check.get("score", 0) * 0.4 +  # 40% archivos
        requirements_check.get("score", 0) * 0.4 +  # 40% dependencias
        week1_structure.get("score", 0) * 0.2  # 20% estructura específica
    )
    
    return {
        "basic_files": files_check,
        "requirements": requirements_check,
        "has_fastapi": requirements_check.get("fastapi", False),
        "has_uvicorn": requirements_check.get("uvicorn", False),
        "week1_specific": week1_structure,
        "overall_ok": (
            files_check.get("all_present", False) and 
            requirements_check.get("all_dependencies", False) and
            week1_structure.get("main_py_valid", False)
        ),
        "passed": overall_score >= 70,
        "score": overall_score
    }


def check_week1_structure_details(repo_path: str) -> Dict[str, Any]:
    """
    Verificaciones específicas de estructura para Week 1
    """
    repo_root = Path(repo_path)
    optional_files = [".gitignore", "Dockerfile", "docker-compose.yml"]
    
    # Verificar archivos opcionales
    present_optional = []
    for file_name in optional_files:
        file_path = repo_root / file_name
        if file_path.exists():
            present_optional.append(file_name)
    
    # Verificar estructura de directorios (debe ser simple para Week 1)
    unexpected_dirs = []
    allowed_dirs = {".git", ".vscode", "__pycache__", ".pytest_cache", "venv", ".env"}
    
    for item in repo_root.iterdir():
        if item.is_dir() and item.name not in allowed_dirs:
            unexpected_dirs.append(item.name)
    
    # Verificar contenido de main.py
    main_py_analysis = analyze_main_py_content(repo_root / "main.py")
    
    # Calcular score
    structure_score = 50  # Base score
    if main_py_analysis.get("syntax_valid", False):
        structure_score += 30
    if main_py_analysis.get("has_fastapi_import", False):
        structure_score += 10
    if main_py_analysis.get("has_app_instance", False):
        structure_score += 10
    
    return {
        "optional_files": present_optional,
        "unexpected_directories": unexpected_dirs,
        "is_simple_structure": len(unexpected_dirs) == 0,
        "main_py_analysis": main_py_analysis,
        "main_py_valid": main_py_analysis.get("syntax_valid", False),
        "score": min(100, structure_score)
    }
    """
    Verificaciones específicas de estructura para Week 1
    """
    required_files = ["main.py", "requirements.txt", "README.md"]
    optional_files = [".gitignore", "Dockerfile", "docker-compose.yml"]
    
    # Verificar archivos requeridos
    missing_required = []
    present_required = []
    
    for file_name in required_files:
        file_path = repo_root / file_name
        if file_path.exists():
            present_required.append(file_name)
        else:
            missing_required.append(file_name)
    
    # Verificar archivos opcionales
    present_optional = []
    for file_name in optional_files:
        file_path = repo_root / file_name
        if file_path.exists():
            present_optional.append(file_name)
    
    # Verificar estructura de directorios (debe ser simple para Week 1)
    unexpected_dirs = []
    for item in repo_root.iterdir():
        if item.is_dir() and item.name not in [".git", ".vscode", "__pycache__", ".pytest_cache"]:
            unexpected_dirs.append(item.name)
    
    # Verificar contenido de main.py
    main_py_analysis = analyze_main_py(repo_root / "main.py")
    
    return {
        "required_files": {
            "present": present_required,
            "missing": missing_required,
            "all_present": len(missing_required) == 0
        },
        "optional_files": present_optional,
        "unexpected_directories": unexpected_dirs,
        "is_simple_structure": len(unexpected_dirs) == 0,
        "main_py_analysis": main_py_analysis
    }


def analyze_main_py_content(main_py_path: Path) -> Dict[str, Any]:
    """
    Analiza el contenido de main.py para Week 1
    """
    if not main_py_path.exists():
        return {
            "exists": False,
            "has_fastapi_import": False,
            "has_app_instance": False,
            "has_root_endpoint": False,
            "syntax_valid": False,
            "score": 0
        }
    
    try:
        content = main_py_path.read_text(encoding="utf-8", errors="ignore")
        
        # Verificaciones básicas de contenido
        has_fastapi_import = any(line.strip().startswith(("from fastapi import", "import fastapi")) 
                                for line in content.split('\n'))
        
        has_app_instance = "app = FastAPI()" in content or "app=FastAPI()" in content
        
        has_root_endpoint = "@app.get(\"/\")" in content or "@app.get('/')" in content
        
        # Verificar sintaxis básica
        syntax_valid = True
        syntax_error = None
        try:
            compile(content, str(main_py_path), 'exec')
        except SyntaxError as e:
            syntax_valid = False
            syntax_error = str(e)
        
        # Calcular score del main.py
        main_score = 0
        if syntax_valid:
            main_score += 40
        if has_fastapi_import:
            main_score += 20
        if has_app_instance:
            main_score += 20
        if has_root_endpoint:
            main_score += 20
        
        return {
            "exists": True,
            "has_fastapi_import": has_fastapi_import,
            "has_app_instance": has_app_instance,
            "has_root_endpoint": has_root_endpoint,
            "syntax_valid": syntax_valid,
            "syntax_error": syntax_error,
            "line_count": len(content.split('\n')),
            "appears_minimal": len(content.split('\n')) <= 20,  # Heurística para Week 1
            "score": main_score
        }
        
    except Exception as e:
        return {
            "exists": True,
            "has_fastapi_import": False,
            "has_app_instance": False,
            "has_root_endpoint": False,
            "syntax_valid": False,
            "error": str(e),
            "score": 0
        }
    """
    Analiza el contenido de main.py para Week 1
    """
    if not main_py_path.exists():
        return {
            "exists": False,
            "has_fastapi_import": False,
            "has_app_instance": False,
            "has_root_endpoint": False,
            "syntax_valid": False
        }
    
    try:
        content = main_py_path.read_text(encoding="utf-8", errors="ignore")
        
        # Verificaciones básicas de contenido
        has_fastapi_import = any(line.strip().startswith(("from fastapi import", "import fastapi")) 
                                for line in content.split('\n'))
        
        has_app_instance = "app = FastAPI()" in content or "app=FastAPI()" in content
        
        has_root_endpoint = "@app.get(\"/\")" in content or "@app.get('/')" in content
        
        # Verificar sintaxis básica
        syntax_valid = True
        try:
            compile(content, main_py_path, 'exec')
        except SyntaxError:
            syntax_valid = False
        
        return {
            "exists": True,
            "has_fastapi_import": has_fastapi_import,
            "has_app_instance": has_app_instance,
            "has_root_endpoint": has_root_endpoint,
            "syntax_valid": syntax_valid,
            "line_count": len(content.split('\n')),
            "appears_minimal": len(content.split('\n')) <= 20  # Heurística para Week 1
        }
        
    except Exception as e:
        return {
            "exists": True,
            "has_fastapi_import": False,
            "has_app_instance": False,
            "has_root_endpoint": False,
            "syntax_valid": False,
            "error": str(e)
        }


def get_structure_feedback(structure_results: Dict[str, Any]) -> List[str]:
    """
    Genera feedback específico sobre la estructura del proyecto
    """
    feedback = []
    
    # Feedback sobre archivos faltantes
    missing_files = structure_results.get("week1_specific", {}).get("required_files", {}).get("missing", [])
    if missing_files:
        feedback.append(f"• Faltan archivos requeridos: {', '.join(missing_files)}")
    
    # Feedback sobre main.py
    main_analysis = structure_results.get("week1_specific", {}).get("main_py_analysis", {})
    
    if not main_analysis.get("has_fastapi_import"):
        feedback.append("• Agrega 'from fastapi import FastAPI' en main.py")
    
    if not main_analysis.get("has_app_instance"):
        feedback.append("• Crea la instancia de la aplicación con 'app = FastAPI()' en main.py")
    
    if not main_analysis.get("has_root_endpoint"):
        feedback.append("• Implementa un endpoint raíz con '@app.get(\"/\")' en main.py")
    
    if not main_analysis.get("syntax_valid"):
        feedback.append("• Corrige errores de sintaxis en main.py")
    
    # Feedback sobre dependencias
    if not structure_results.get("has_fastapi"):
        feedback.append("• Agrega 'fastapi' a requirements.txt")
    
    if not structure_results.get("has_uvicorn"):
        feedback.append("• Agrega 'uvicorn[standard]' a requirements.txt")
    
    return feedback
