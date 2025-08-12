"""
Verificaciones de estructura de proyecto específicas para Week 1
"""
import sys
from pathlib import Path
from typing import Dict, Any, List

# Importar las funciones del evaluador actual
sys.path.append(str(Path(__file__).parent.parent.parent.parent / "evaluator"))

try:
    from checks_structure import check_structure
    from checks_requirements import check_requirements
except ImportError:
    def check_structure(root):
        return {"ok": False, "error": "Could not import check_structure"}
    
    def check_requirements(root):
        return {"ok": False, "error": "Could not import check_requirements"}


def check_project_structure(repo_path: str) -> Dict[str, Any]:
    """
    Verifica la estructura del proyecto específica para Week 1
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de estructura
    """
    repo_root = Path(repo_path)
    
    # Usar checks existentes
    structure_results = check_structure(repo_root)
    requirements_results = check_requirements(repo_root)
    
    # Verificaciones adicionales específicas de Week 1
    week1_structure = check_week1_structure(repo_root)
    
    return {
        "basic_files": structure_results.get("files", {}),
        "requirements_ok": requirements_results.get("ok", False),
        "has_fastapi": requirements_results.get("fastapi", False),
        "has_uvicorn": requirements_results.get("uvicorn", False),
        "week1_specific": week1_structure,
        "overall_ok": (
            structure_results.get("ok", False) and 
            requirements_results.get("fastapi", False) and 
            requirements_results.get("uvicorn", False)
        )
    }


def check_week1_structure(repo_root: Path) -> Dict[str, Any]:
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


def analyze_main_py(main_py_path: Path) -> Dict[str, Any]:
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
