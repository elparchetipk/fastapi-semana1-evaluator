"""
Evaluador específico para Semana 1 - Hello World API
"""
import sys
from pathlib import Path

# Agregar el directorio padre al path para importar core
sys.path.append(str(Path(__file__).parent.parent.parent))

from core.base_evaluator import BaseEvaluator
from .checks.endpoints import check_endpoints
from .checks.documentation import check_documentation
from .checks.structure import check_project_structure


class Week01Evaluator(BaseEvaluator):
    """
    Evaluador para Semana 1: Hello World API
    
    Evalúa:
    - Configuración básica del proyecto
    - Endpoints fundamentales
    - Documentación automática
    - Estructura del proyecto
    """
    
    def __init__(self, student_repo_path: str):
        super().__init__(
            week_number=1,
            student_repo_path=student_repo_path
        )
    
    def run_specific_checks(self) -> dict:
        """
        Ejecuta verificaciones específicas de la Semana 1
        """
        results = {}
        
        # Check de endpoints específicos
        results["endpoints"] = check_endpoints(self.repo_path)
        
        # Check de documentación
        results["documentation"] = check_documentation(self.repo_path)
        
        # Check de estructura del proyecto
        results["project_structure"] = check_project_structure(self.repo_path)
        
        return results
    
    def get_week_specific_feedback(self, results: dict) -> list:
        """
        Genera feedback específico para Week 1
        """
        feedback = []
        
        # Feedback sobre endpoints
        if not results.get("endpoints", {}).get("root_working"):
            feedback.append(
                "• Implementa un endpoint GET / que retorne un diccionario JSON simple"
            )
        
        if not results.get("endpoints", {}).get("docs_accessible"):
            feedback.append(
                "• Asegúrate de que /docs sea accesible. Esto indica que tu app FastAPI está configurada correctamente"
            )
        
        # Feedback sobre estructura
        if not results.get("app_import", {}).get("import_ok"):
            feedback.append(
                "• Revisa que main.py tenga 'app = FastAPI()' y no tenga errores de sintaxis"
            )
        
        # Feedback sobre documentación
        if not results.get("readme", {}).get("has_commands"):
            feedback.append(
                "• Agrega comandos de instalación (pip install -r requirements.txt) y ejecución (uvicorn main:app --reload) al README"
            )
        
        return feedback


def create_evaluator(student_repo_path: str) -> Week01Evaluator:
    """Factory function para crear el evaluador de Week 1"""
    return Week01Evaluator(student_repo_path)
