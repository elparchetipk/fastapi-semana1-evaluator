"""
Evaluador específico para Semana 1 - Hello World API
Migrado al nuevo framework core.
"""
import sys
import importlib.util
import os
from pathlib import Path
from typing import Dict, Any, List

# Agregar el directorio padre al path para importar core
sys.path.append(str(Path(__file__).parent.parent.parent))

from core import BaseEvaluator, CommonChecks

def safe_import_check(check_name: str, default_return: Dict[str, Any] = None):
    """Helper para importar checks de manera segura"""
    if default_return is None:
        default_return = {"error": f"Check {check_name} not available", "passed": False, "score": 0}
    
    try:
        current_dir = Path(__file__).parent
        check_file = current_dir / "checks" / f"{check_name}.py"
        
        if not check_file.exists():
            return lambda repo_path: default_return
        
        spec = importlib.util.spec_from_file_location(f"{check_name}_check", str(check_file))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Buscar la función principal del check
        function_name = f"check_{check_name}" if check_name != "endpoints" else "check_endpoints"
        if check_name == "structure":
            function_name = "check_project_structure"
        
        if hasattr(module, function_name):
            return getattr(module, function_name)
        else:
            # Buscar cualquier función que empiece con "check_"
            for attr_name in dir(module):
                if attr_name.startswith("check_") and callable(getattr(module, attr_name)):
                    return getattr(module, attr_name)
        
        return lambda repo_path: default_return
        
    except Exception as e:
        print(f"Warning: Could not import {check_name} check: {e}")
        return lambda repo_path: {**default_return, "error": str(e)}

# Importar checks con manejo de errores
check_endpoints = safe_import_check("endpoints")
check_documentation = safe_import_check("documentation") 
check_project_structure = safe_import_check("structure")


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
        # Inicializar common checks para esta semana
        self.common_checks = CommonChecks(self.repo_path)
    
    def run_specific_checks(self) -> Dict[str, Any]:
        """
        Ejecuta verificaciones específicas de la Semana 1
        """
        results = {}
        
        # Check de endpoints específicos usando el nuevo framework
        try:
            results["endpoints"] = check_endpoints(str(self.repo_path))
        except Exception as e:
            results["endpoints"] = {"error": str(e), "passed": False, "score": 0}
        
        # Check de documentación
        try:
            results["documentation"] = check_documentation(str(self.repo_path))
        except Exception as e:
            results["documentation"] = {"error": str(e), "passed": False, "score": 0}
        
        # Check de estructura del proyecto usando common checks
        try:
            results["project_structure"] = self._check_week01_structure()
        except Exception as e:
            results["project_structure"] = {"error": str(e), "passed": False, "score": 0}
        
        # Checks adicionales con common checks
        try:
            results["fastapi_app"] = self._check_fastapi_app_setup()
        except Exception as e:
            results["fastapi_app"] = {"error": str(e), "passed": False, "score": 0}
            
        try:
            results["code_quality"] = self._check_code_quality()
        except Exception as e:
            results["code_quality"] = {"error": str(e), "passed": False, "score": 0}
        
        return results
    
    def _check_week01_structure(self) -> Dict[str, Any]:
        """
        Verificaciones de estructura específicas para Week 1 usando common checks
        """
        # Archivos requeridos para Week 1
        required_files = ["main.py", "requirements.txt", "README.md"]
        file_checks = self.common_checks.check_required_files(required_files)
        
        # Verificar dependencias específicas
        required_packages = ["fastapi", "uvicorn"]
        package_checks = self.common_checks.check_multiple_packages(required_packages)
        
        # Análisis de main.py
        main_syntax = self.common_checks.check_python_syntax("main.py")
        
        # Verificar imports específicos de FastAPI
        fastapi_imports = self.common_checks.check_imports_in_file("main.py", ["fastapi"])
        
        return {
            "required_files": file_checks,
            "required_packages": package_checks,
            "main_syntax": main_syntax,
            "fastapi_imports": fastapi_imports,
            "all_files_present": all(file_checks.values()),
            "all_packages_present": all(package_checks.values()),
            "structure_score": self._calculate_structure_score(file_checks, package_checks, main_syntax)
        }
    
    def _check_fastapi_app_setup(self) -> Dict[str, Any]:
        """
        Verificaciones específicas de la aplicación FastAPI usando common checks
        """
        # Verificar archivos y contenido sin importar
        main_py_exists = self.common_checks.check_file_exists("main.py")
        if not main_py_exists:
            return {
                "has_fastapi_import": False,
                "has_app_instance": False,
                "has_root_endpoint_function": False,
                "setup_complete": False,
                "error": "main.py no encontrado"
            }
        
        # Análisis estático del código (sin importar)
        try:
            main_content = (self.repo_path / "main.py").read_text(encoding='utf-8')
            
            has_fastapi_import = "from fastapi import" in main_content or "import fastapi" in main_content
            has_app_instance = "app = FastAPI" in main_content or "app=FastAPI" in main_content
            has_get_decorator = "@app.get" in main_content
            has_root_endpoint = "@app.get(\"/\")" in main_content or "@app.get('/')" in main_content
            
            return {
                "has_fastapi_import": has_fastapi_import,
                "has_app_instance": has_app_instance,
                "has_get_decorator": has_get_decorator,
                "has_root_endpoint": has_root_endpoint,
                "setup_complete": has_fastapi_import and has_app_instance and has_root_endpoint,
                "passed": has_fastapi_import and has_app_instance and has_root_endpoint,
                "score": sum([has_fastapi_import, has_app_instance, has_get_decorator, has_root_endpoint]) * 25
            }
            
        except Exception as e:
            return {
                "has_fastapi_import": False,
                "has_app_instance": False,
                "has_root_endpoint_function": False,
                "setup_complete": False,
                "error": f"Error analizando main.py: {str(e)}",
                "passed": False,
                "score": 0
            }
    
    def _check_code_quality(self) -> Dict[str, Any]:
        """
        Verificaciones de calidad de código para Week 1
        """
        # README analysis
        readme_analysis = self.common_checks.check_readme_content("README.md")
        
        # Sintaxis de archivos Python
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
        """Calcula un score de estructura para Week 1"""
        score = 0
        total = 0
        
        # Archivos (40% del score)
        for file_present in file_checks.values():
            total += 1
            if file_present:
                score += 1
        
        # Packages (40% del score)
        for package_present in package_checks.values():
            total += 1
            if package_present:
                score += 1
        
        # Sintaxis (20% del score)
        total += 1
        if main_syntax.get("syntax_valid", False):
            score += 1
        
        return (score / total * 100) if total > 0 else 0
    
    def _assess_overall_quality(self, readme_analysis: Dict[str, Any], 
                               syntax_checks: Dict[str, Any]) -> str:
        """Evalúa la calidad general del código"""
        quality_score = 0
        
        # README quality (50%)
        if readme_analysis.get("estimated_completeness", 0) > 75:
            quality_score += 50
        elif readme_analysis.get("estimated_completeness", 0) > 50:
            quality_score += 30
        elif readme_analysis.get("estimated_completeness", 0) > 25:
            quality_score += 15
        
        # Syntax quality (50%)
        syntax_valid = all(
            check.get("syntax_valid", False) 
            for check in syntax_checks.values()
        )
        if syntax_valid:
            quality_score += 50
        
        # Clasificar calidad
        if quality_score >= 80:
            return "excellent"
        elif quality_score >= 60:
            return "good"
        elif quality_score >= 40:
            return "acceptable"
        else:
            return "needs_improvement"
    
    def get_week_specific_feedback(self, results: Dict[str, Any]) -> List[str]:
        """
        Genera feedback específico para Week 1 - Hello World API
        Incluye tanto aspectos positivos como mejoras necesarias
        """
        feedback = []
        successful_aspects = []
        
        # Analizar estructura del proyecto
        structure = results.get("project_structure", {})
        if structure.get("all_files_present", False):
            successful_aspects.append("Estructura de archivos básica completa (main.py, requirements.txt, README.md)")
        
        if structure.get("all_packages_present", False):
            successful_aspects.append("Dependencias FastAPI correctamente especificadas en requirements.txt")
        
        # Analizar configuración de FastAPI
        app_setup = results.get("fastapi_app", {})
        if app_setup.get("has_fastapi_import", False):
            successful_aspects.append("FastAPI correctamente importado en main.py")
        else:
            feedback.append("Importar FastAPI: agregar 'from fastapi import FastAPI' en main.py")
        
        if app_setup.get("has_app_instance", False):
            successful_aspects.append("Instancia de aplicación FastAPI creada correctamente")
        else:
            feedback.append("Crear instancia de aplicación: agregar 'app = FastAPI()' en main.py")
        
        if app_setup.get("has_root_endpoint_function", False):
            successful_aspects.append("Función de endpoint raíz definida")
        else:
            feedback.append("Implementar función para endpoint raíz con decorador @app.get('/')")
        
        # Analizar endpoints
        endpoints = results.get("endpoints", {})
        if endpoints.get("root_working", False):
            successful_aspects.append("Endpoint GET / funcionando y retornando JSON válido")
        else:
            feedback.append("Asegurar que el endpoint GET / retorne JSON y responda con status 200")
        
        if endpoints.get("docs_accessible", False):
            successful_aspects.append("Documentación automática FastAPI accesible en /docs")
        else:
            feedback.append("Verificar que /docs sea accesible (indica configuración correcta de FastAPI)")
        
        # Analizar documentación
        documentation = results.get("documentation", {})
        if documentation.get("has_setup_commands", False):
            successful_aspects.append("README con comandos de instalación y ejecución")
        else:
            feedback.append("Agregar comandos de instalación (pip install -r requirements.txt) y ejecución (uvicorn main:app --reload) al README")
        
        # Analizar calidad general
        code_quality = results.get("code_quality", {})
        quality_level = code_quality.get("overall_quality", "needs_improvement")
        if quality_level in ["excellent", "good"]:
            successful_aspects.append("Código bien estructurado y documentado")
        elif quality_level == "acceptable":
            successful_aspects.append("Estructura de código básica aceptable")
        else:
            feedback.append("Mejorar documentación del proyecto y verificar sintaxis del código")
        
        # Combinar aspectos exitosos y mejoras
        combined_feedback = []
        
        if successful_aspects:
            combined_feedback.append("✅ **Aspectos de Week 1 implementados correctamente:**")
            for aspect in successful_aspects:
                combined_feedback.append(f"• {aspect}")
            combined_feedback.append("")  # Línea en blanco
        
        if feedback:
            combined_feedback.append("🔧 **Mejoras específicas de Week 1:**")
            for improvement in feedback:
                combined_feedback.append(f"• {improvement}")
        
        return combined_feedback
    
    def get_week01_summary(self) -> Dict[str, Any]:
        """
        Genera un resumen específico para Week 1
        """
        if not self.results:
            return {"error": "No evaluation results available"}
        
        structure = self.results.get("project_structure", {})
        app_setup = self.results.get("fastapi_app", {})
        endpoints = self.results.get("endpoints", {})
        
        return {
            "files_complete": structure.get("all_files_present", False),
            "dependencies_ok": structure.get("all_packages_present", False),
            "app_configured": app_setup.get("setup_complete", False),
            "api_working": endpoints.get("root_working", False),
            "docs_accessible": endpoints.get("docs_accessible", False),
            "ready_for_week2": all([
                structure.get("all_files_present", False),
                structure.get("all_packages_present", False),
                app_setup.get("setup_complete", False),
                endpoints.get("root_working", False)
            ])
        }
    
    def _get_check_result(self, check_name: str) -> bool:
        """
        Mapea los nombres de checks del criteria.yaml a los resultados reales
        """
        if not self.results:
            return False
        
        # Mapeo de checks del criteria.yaml a resultados del evaluador
        check_mappings = {
            # Setup category
            "requirements_txt": lambda: self.results.get("project_structure", {}).get("required_files", {}).get("requirements.txt", False),
            "fastapi_dependency": lambda: self.results.get("project_structure", {}).get("required_packages", {}).get("fastapi", False),
            "uvicorn_dependency": lambda: self.results.get("project_structure", {}).get("required_packages", {}).get("uvicorn", False),
            "main_py_exists": lambda: self.results.get("project_structure", {}).get("required_files", {}).get("main.py", False),
            "readme_exists": lambda: self.results.get("project_structure", {}).get("required_files", {}).get("README.md", False),
            
            # Functionality category
            "app_import": lambda: self.results.get("fastapi_app", {}).get("has_fastapi_import", False) and self.results.get("fastapi_app", {}).get("has_app_instance", False),
            "root_endpoint": lambda: self.results.get("endpoints", {}).get("root_working", False),
            "docs_accessible": lambda: self.results.get("endpoints", {}).get("docs_accessible", False),
            "parametric_endpoint": lambda: self.results.get("endpoints", {}).get("parametric_endpoint", False),
            
            # Documentation category
            "json_responses": lambda: self.results.get("endpoints", {}).get("root_working", False),  # Si funciona el endpoint, devuelve JSON
            "readme_reflection": lambda: self.results.get("documentation", {}).get("has_reflection", False),
            "setup_commands": lambda: self.results.get("documentation", {}).get("has_setup_commands", False),
            
            # Deliverables category  
            "project_structure": lambda: self.results.get("project_structure", {}).get("all_files_present", False),
            "code_quality": lambda: self.results.get("code_quality", {}).get("overall_quality") in ["excellent", "good"],
            
            # Understanding category
            "demonstrates_understanding": lambda: self.results.get("documentation", {}).get("week1_specific", {}).get("appears_complete", False),
        }
        
        if check_name in check_mappings:
            try:
                return bool(check_mappings[check_name]())
            except (KeyError, TypeError, AttributeError):
                return False
        
        # Fallback al método del padre
        return super()._get_check_result(check_name)

def create_evaluator(student_repo_path: str) -> Week01Evaluator:
    """Factory function para crear el evaluador de Week 1"""
    return Week01Evaluator(student_repo_path)


def run_week01_evaluation(student_repo_path: str) -> Dict[str, Any]:
    """
    Función de conveniencia para ejecutar evaluación completa de Week 1
    
    Args:
        student_repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Resultado completo de evaluación
    """
    evaluator = create_evaluator(student_repo_path)
    return evaluator.evaluate()
