"""
Evaluador específico para Semana 11 - Proyecto Final
Integración de todos los conceptos en un proyecto completo
"""
import sys
import importlib.util
import os
from pathlib import Path
from typing import Dict, Any, List

# Agregar el directorio padre al path para importar core
sys.path.append(str(Path(__file__).parent.parent.parent))

from core import BaseEvaluator, CommonChecks

def import_check_module(module_name: str, file_path: str):
    """Helper para importar módulos de checks"""
    try:
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print(f"Warning: Could not import {module_name} check: {e}")
        return None

# Obtener directorio actual del evaluador
current_dir = Path(__file__).parent

# Importar checks específicos

try:
    complete_application_module = import_check_module("complete_application", str(current_dir / "checks" / "complete_application.py"))
    check_complete_application = complete_application_module.check_complete_application if complete_application_module else lambda repo_path: {"error": "Module not available"}
except Exception as e:
    print(f"Warning: Could not import complete_application check: {e}")
    def check_complete_application(repo_path): return {"error": "Module not available"}

try:
    best_practices_module = import_check_module("best_practices", str(current_dir / "checks" / "best_practices.py"))
    check_best_practices = best_practices_module.check_best_practices if best_practices_module else lambda repo_path: {"error": "Module not available"}
except Exception as e:
    print(f"Warning: Could not import best_practices check: {e}")
    def check_best_practices(repo_path): return {"error": "Module not available"}

try:
    documentation_module = import_check_module("documentation", str(current_dir / "checks" / "documentation.py"))
    check_documentation = documentation_module.check_documentation if documentation_module else lambda repo_path: {"error": "Module not available"}
except Exception as e:
    print(f"Warning: Could not import documentation check: {e}")
    def check_documentation(repo_path): return {"error": "Module not available"}

try:
    deployment_ready_module = import_check_module("deployment_ready", str(current_dir / "checks" / "deployment_ready.py"))
    check_deployment_ready = deployment_ready_module.check_deployment_ready if deployment_ready_module else lambda repo_path: {"error": "Module not available"}
except Exception as e:
    print(f"Warning: Could not import deployment_ready check: {e}")
    def check_deployment_ready(repo_path): return {"error": "Module not available"}


class Week11Evaluator(BaseEvaluator):
    """
    Evaluador para Semana 11: Proyecto Final
    
    Evalúa:
    - Full Stack
    - Integration
    - Best Practices
    - Production Ready
    """
    
    def __init__(self, student_repo_path: str):
        super().__init__(
            week_number=11,
            student_repo_path=student_repo_path
        )
        self.common_checks = CommonChecks(self.repo_path)
    
    def run_specific_checks(self) -> Dict[str, Any]:
        """
        Ejecuta verificaciones específicas de la Semana 11
        """
        results = {}
        
        # Checks básicos de estructura
        results["project_structure"] = self._check_week11_structure()
        results["complete_application"] = check_complete_application(str(self.repo_path))
        results["best_practices"] = check_best_practices(str(self.repo_path))
        results["documentation"] = check_documentation(str(self.repo_path))
        results["deployment_ready"] = check_deployment_ready(str(self.repo_path))
        
        # Checks de calidad de código
        results["code_quality"] = self._check_code_quality()
        
        return results
    
    def _check_week11_structure(self) -> Dict[str, Any]:
        """
        Verificaciones de estructura específicas para Week 11
        """
        # Archivos requeridos para Week 11
        required_files = ["main.py", "requirements.txt", "README.md"]
        file_checks = self.common_checks.check_required_files(required_files)
        
        # Verificar dependencias específicas de Week 11
        required_packages = ['fastapi', 'uvicorn', 'sqlalchemy', 'alembic', 'pytest', 'docker']
        package_checks = self.common_checks.check_multiple_packages(required_packages)
        
        # Análisis de main.py
        main_syntax = self.common_checks.check_python_syntax("main.py")
        
        return {
            "required_files": file_checks,
            "required_packages": package_checks,
            "main_syntax": main_syntax,
            "structure_score": self._calculate_structure_score(file_checks, package_checks, main_syntax)
        }
    
    def _check_code_quality(self) -> Dict[str, Any]:
        """
        Verificaciones de calidad de código para Week 11
        """
        readme_analysis = self.common_checks.check_readme_content("README.md")
        
        python_files = ["main.py"]
        syntax_checks = {}
        
        for py_file in python_files:
            if self.common_checks.check_file_exists(py_file):
                syntax_checks[py_file] = self.common_checks.check_python_syntax(py_file)
        
        return {
            "readme_analysis": readme_analysis,
            "syntax_checks": syntax_checks,
            "overall_quality": self._assess_overall_quality(readme_analysis, syntax_checks)
        }
    
    def _calculate_structure_score(self, file_checks: Dict[str, bool], 
                                 package_checks: Dict[str, bool], 
                                 main_syntax: Dict[str, Any]) -> float:
        """Calcula un score de estructura para Week 11"""
        score = 0
        total = 0
        
        for file_present in file_checks.values():
            total += 1
            if file_present:
                score += 1
        
        for package_present in package_checks.values():
            total += 1
            if package_present:
                score += 1
        
        total += 1
        if main_syntax.get("syntax_valid", False):
            score += 1
        
        return (score / total * 100) if total > 0 else 0
    
    def _assess_overall_quality(self, readme_analysis: Dict[str, Any], 
                               syntax_checks: Dict[str, Any]) -> str:
        """Evalúa la calidad general del código para Week 11"""
        quality_score = 0
        
        readme_completeness = readme_analysis.get("estimated_completeness", 0)
        if readme_completeness > 80:
            quality_score += 50
        elif readme_completeness > 60:
            quality_score += 30
        elif readme_completeness > 40:
            quality_score += 15
        
        syntax_valid = all(
            check.get("syntax_valid", False) 
            for check in syntax_checks.values()
        )
        if syntax_valid:
            quality_score += 50
        
        if quality_score >= 85:
            return "excellent"
        elif quality_score >= 70:
            return "good"
        elif quality_score >= 50:
            return "acceptable"
        else:
            return "needs_improvement"
    
    def get_week_specific_feedback(self, results: Dict[str, Any]) -> List[str]:
        """
        Genera feedback específico para Week 11
        """
        feedback = []
        
        structure = results.get("project_structure", {})
        if not structure.get("required_files", {}).get("main.py", False):
            feedback.append("• Crea el archivo main.py principal")
        
        missing_packages = [
            pkg for pkg, present in structure.get("required_packages", {}).items()
            if not present
        ]
        if missing_packages:
            feedback.append(f"• Agrega a requirements.txt: {', '.join(missing_packages)}")
        
        # TODO: Agregar feedback específico para Week 11
        
        return feedback
    
    def get_week11_summary(self) -> Dict[str, Any]:
        """
        Genera un resumen específico para Week 11
        """
        if not self.results:
            return {"error": "No evaluation results available"}
        
        structure = self.results.get("project_structure", {})
        
        return {
            "structure_complete": structure.get("structure_score", 0) >= 80,
            "ready_for_week12": structure.get("structure_score", 0) >= 70
        }


def create_evaluator(student_repo_path: str) -> Week11Evaluator:
    """Factory function para crear el evaluador de Week 11"""
    return Week11Evaluator(student_repo_path)


def run_week11_evaluation(student_repo_path: str) -> Dict[str, Any]:
    """
    Función de conveniencia para ejecutar evaluación completa de Week 11
    
    Args:
        student_repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Resultado completo de evaluación
    """
    evaluator = create_evaluator(student_repo_path)
    return evaluator.evaluate()
