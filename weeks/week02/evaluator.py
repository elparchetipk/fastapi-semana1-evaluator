"""
Evaluador específico para Semana 2 - CRUD Básico con FastAPI
Operaciones Create, Read, Update, Delete con datos en memoria
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
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

# Obtener directorio actual del evaluador
current_dir = Path(__file__).parent

# Importar checks específicos
try:
    crud_module = import_check_module("crud_operations", str(current_dir / "checks" / "crud_operations.py"))
    check_crud_operations = crud_module.check_crud_operations
except Exception as e:
    print(f"Warning: Could not import crud_operations check: {e}")
    def check_crud_operations(repo_path): return {"error": "Module not available"}

try:
    models_module = import_check_module("models", str(current_dir / "checks" / "models.py"))
    check_models = models_module.check_models
except Exception as e:
    print(f"Warning: Could not import models check: {e}")
    def check_models(repo_path): return {"error": "Module not available"}

try:
    endpoints_module = import_check_module("endpoints", str(current_dir / "checks" / "endpoints.py"))
    check_endpoints = endpoints_module.check_endpoints
except Exception as e:
    print(f"Warning: Could not import endpoints check: {e}")
    def check_endpoints(repo_path): return {"error": "Module not available"}


class Week02Evaluator(BaseEvaluator):
    """
    Evaluador para Semana 2: CRUD Básico con FastAPI
    
    Evalúa:
    - Operaciones CRUD (Create, Read, Update, Delete)
    - Modelos Pydantic
    - Manejo de datos en memoria
    - Validación de entrada
    """
    
    def __init__(self, student_repo_path: str):
        super().__init__(
            week_number=2,
            student_repo_path=student_repo_path
        )
        self.common_checks = CommonChecks(self.repo_path)
    
    def run_specific_checks(self) -> Dict[str, Any]:
        """
        Ejecuta verificaciones específicas de la Semana 2
        """
        results = {}
        
        # Checks de estructura del proyecto
        results["project_structure"] = self._check_week02_structure()
        
        # Checks de modelos Pydantic
        results["models"] = check_models(str(self.repo_path))
        
        # Checks de operaciones CRUD
        results["crud_operations"] = check_crud_operations(str(self.repo_path))
        
        # Checks de endpoints
        results["endpoints"] = check_endpoints(str(self.repo_path))
        
        # Checks de calidad de código
        results["code_quality"] = self._check_code_quality()
        
        # Checks adicionales específicos de Week 2
        results["data_validation"] = self._check_data_validation()
        results["error_handling"] = self._check_error_handling()
        
        return results
    
    def _check_week02_structure(self) -> Dict[str, Any]:
        """
        Verificaciones de estructura específicas para Week 2
        """
        # Archivos requeridos para Week 2
        required_files = ["main.py", "requirements.txt", "README.md"]
        file_checks = self.common_checks.check_required_files(required_files)
        
        # Verificar dependencias específicas de Week 2
        required_packages = ["fastapi", "uvicorn", "pydantic"]
        package_checks = self.common_checks.check_multiple_packages(required_packages)
        
        # Verificar archivos opcionales pero recomendados
        optional_files = ["models.py", "schemas.py", "routers/", "routes/"]
        optional_checks = {}
        for file in optional_files:
            optional_checks[file] = self.common_checks.check_file_exists(file)
        
        # Análisis de main.py
        main_syntax = self.common_checks.check_python_syntax("main.py")
        
        # Verificar imports específicos
        required_imports = ["fastapi", "pydantic"]
        import_checks = {}
        for imp in required_imports:
            import_checks[imp] = self.common_checks.check_imports_in_file("main.py", [imp])
        
        return {
            "required_files": file_checks,
            "required_packages": package_checks,
            "optional_files": optional_checks,
            "main_syntax": main_syntax,
            "imports": import_checks,
            "structure_score": self._calculate_structure_score(file_checks, package_checks, main_syntax),
            "organization_score": self._calculate_organization_score(optional_checks)
        }
    
    def _check_data_validation(self) -> Dict[str, Any]:
        """
        Verifica el uso correcto de validación de datos con Pydantic
        """
        # Buscar modelos Pydantic
        pydantic_models = self.common_checks.check_imports_in_file("main.py", ["BaseModel"])
        
        # Verificar si hay archivos de modelos separados
        has_models_file = (
            self.common_checks.check_file_exists("models.py") or
            self.common_checks.check_file_exists("schemas.py")
        )
        
        # Verificar tipos de validación común
        validation_patterns = []
        if self.common_checks.check_file_exists("main.py"):
            # Buscar patrones de validación comunes
            main_content = ""
            try:
                with open(self.repo_path / "main.py", 'r') as f:
                    main_content = f.read()
                
                # Patrones de validación
                validation_patterns = [
                    ("str_validation", "str" in main_content),
                    ("int_validation", "int" in main_content),
                    ("optional_fields", "Optional" in main_content or "None" in main_content),
                    ("field_validation", "Field(" in main_content),
                ]
            except:
                pass
        
        return {
            "pydantic_used": pydantic_models,
            "has_separate_models": has_models_file,
            "validation_patterns": dict(validation_patterns),
            "validation_score": self._calculate_validation_score(pydantic_models, has_models_file, validation_patterns)
        }
    
    def _check_error_handling(self) -> Dict[str, Any]:
        """
        Verifica el manejo de errores en las operaciones CRUD
        """
        error_handling = {
            "has_http_exceptions": False,
            "handles_not_found": False,
            "handles_validation_errors": False,
            "custom_error_responses": False
        }
        
        if self.common_checks.check_file_exists("main.py"):
            try:
                with open(self.repo_path / "main.py", 'r') as f:
                    content = f.read()
                
                # Verificar patrones de manejo de errores
                error_handling.update({
                    "has_http_exceptions": "HTTPException" in content,
                    "handles_not_found": "404" in content or "not found" in content.lower(),
                    "handles_validation_errors": "422" in content or "ValidationError" in content,
                    "custom_error_responses": "status_code" in content
                })
            except:
                pass
        
        error_score = sum(error_handling.values()) / len(error_handling) * 100
        
        return {
            **error_handling,
            "error_handling_score": error_score
        }
    
    def _check_code_quality(self) -> Dict[str, Any]:
        """
        Verificaciones de calidad de código para Week 2
        """
        # README analysis
        readme_analysis = self.common_checks.check_readme_content("README.md")
        
        # Sintaxis de archivos Python principales
        python_files = ["main.py"]
        if self.common_checks.check_file_exists("models.py"):
            python_files.append("models.py")
        if self.common_checks.check_file_exists("schemas.py"):
            python_files.append("schemas.py")
        
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
        """Calcula un score de estructura para Week 2"""
        score = 0
        total = 0
        
        # Archivos requeridos (50% del score)
        for file_present in file_checks.values():
            total += 1
            if file_present:
                score += 1
        
        # Packages requeridos (30% del score)
        for package_present in package_checks.values():
            total += 1
            if package_present:
                score += 1
        
        # Sintaxis (20% del score)
        total += 1
        if main_syntax.get("syntax_valid", False):
            score += 1
        
        return (score / total * 100) if total > 0 else 0
    
    def _calculate_organization_score(self, optional_checks: Dict[str, bool]) -> float:
        """Calcula un score de organización basado en archivos opcionales"""
        # Dar puntos por tener archivos organizados
        organization_score = 0
        if optional_checks.get("models.py", False) or optional_checks.get("schemas.py", False):
            organization_score += 50
        if optional_checks.get("routers/", False) or optional_checks.get("routes/", False):
            organization_score += 50
        
        return organization_score
    
    def _calculate_validation_score(self, pydantic_used: bool, has_separate_models: bool, 
                                   validation_patterns: List) -> float:
        """Calcula score de validación de datos"""
        score = 0
        
        if pydantic_used:
            score += 40
        if has_separate_models:
            score += 30
        
        # Patrones de validación (30 puntos distribuidos)
        pattern_score = sum(1 for _, present in validation_patterns if present)
        score += (pattern_score / len(validation_patterns) * 30) if validation_patterns else 0
        
        return score
    
    def _assess_overall_quality(self, readme_analysis: Dict[str, Any], 
                               syntax_checks: Dict[str, Any]) -> str:
        """Evalúa la calidad general del código para Week 2"""
        quality_score = 0
        
        # README quality (40%)
        readme_completeness = readme_analysis.get("estimated_completeness", 0)
        if readme_completeness > 80:
            quality_score += 40
        elif readme_completeness > 60:
            quality_score += 25
        elif readme_completeness > 40:
            quality_score += 15
        
        # Syntax quality (60%)
        syntax_valid = all(
            check.get("syntax_valid", False) 
            for check in syntax_checks.values()
        )
        if syntax_valid:
            quality_score += 60
        else:
            # Puntuación parcial si algunos archivos están bien
            valid_files = sum(1 for check in syntax_checks.values() if check.get("syntax_valid", False))
            total_files = len(syntax_checks)
            if total_files > 0:
                quality_score += (valid_files / total_files * 60)
        
        # Clasificar calidad
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
        Genera feedback específico para Week 2
        """
        feedback = []
        
        # Feedback sobre estructura
        structure = results.get("project_structure", {})
        if not structure.get("required_files", {}).get("main.py", False):
            feedback.append("• Crea el archivo main.py principal")
        
        missing_packages = [
            pkg for pkg, present in structure.get("required_packages", {}).items()
            if not present
        ]
        if missing_packages:
            feedback.append(f"• Agrega a requirements.txt: {', '.join(missing_packages)}")
        
        # Feedback sobre modelos
        models_result = results.get("models", {})
        if "error" in models_result:
            feedback.append("• Define modelos Pydantic para estructurar tus datos")
        
        # Feedback sobre validación
        validation = results.get("data_validation", {})
        if not validation.get("pydantic_used", False):
            feedback.append("• Usa Pydantic BaseModel para validación de datos")
        
        if not validation.get("has_separate_models", False):
            feedback.append("• Considera crear un archivo models.py o schemas.py para organizar mejor")
        
        # Feedback sobre CRUD operations
        crud = results.get("crud_operations", {})
        if "error" in crud:
            feedback.append("• Implementa las operaciones CRUD básicas: Create, Read, Update, Delete")
        
        # Feedback sobre manejo de errores
        error_handling = results.get("error_handling", {})
        if not error_handling.get("has_http_exceptions", False):
            feedback.append("• Usa HTTPException para manejar errores apropiadamente")
        
        if not error_handling.get("handles_not_found", False):
            feedback.append("• Maneja el caso cuando un item no existe (404 Not Found)")
        
        # Feedback sobre calidad
        code_quality = results.get("code_quality", {})
        if code_quality.get("overall_quality") == "needs_improvement":
            feedback.append("• Mejora la documentación y verifica la sintaxis del código")
        
        # Feedback sobre organización
        organization_score = structure.get("organization_score", 0)
        if organization_score < 50:
            feedback.append("• Organiza tu código en módulos separados (models.py, routes/)")
        
        return feedback
    
    def get_week02_summary(self) -> Dict[str, Any]:
        """
        Genera un resumen específico para Week 2
        """
        if not self.results:
            return {"error": "No evaluation results available"}
        
        structure = self.results.get("project_structure", {})
        crud = self.results.get("crud_operations", {})
        validation = self.results.get("data_validation", {})
        error_handling = self.results.get("error_handling", {})
        
        return {
            "structure_complete": structure.get("structure_score", 0) >= 80,
            "models_implemented": validation.get("pydantic_used", False),
            "crud_working": "error" not in crud,
            "error_handling_ok": error_handling.get("error_handling_score", 0) >= 50,
            "well_organized": structure.get("organization_score", 0) >= 50,
            "ready_for_week3": all([
                structure.get("structure_score", 0) >= 70,
                validation.get("pydantic_used", False),
                "error" not in crud,
                error_handling.get("error_handling_score", 0) >= 40
            ])
        }


def create_evaluator(student_repo_path: str) -> Week02Evaluator:
    """Factory function para crear el evaluador de Week 2"""
    return Week02Evaluator(student_repo_path)


def run_week02_evaluation(student_repo_path: str) -> Dict[str, Any]:
    """
    Función de conveniencia para ejecutar evaluación completa de Week 2
    
    Args:
        student_repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Resultado completo de evaluación
    """
    evaluator = create_evaluator(student_repo_path)
    return evaluator.evaluate()
