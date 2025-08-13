"""
Evaluador específico para Semana 4 - Bases de Datos Avanzadas con FastAPI
SQLAlchemy avanzado: migraciones, relaciones, consultas complejas
"""
import sys
from pathlib import Path
from typing import Dict, Any, List

# Agregar el directorio padre al path para importar core
sys.path.append(str(Path(__file__).parent.parent.parent))

from core.base_evaluator import BaseEvaluator
from core.common_checks import CommonChecks

# Import checks using absolute imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

try:
    from checks.alembic_migrations import check_alembic_migrations
    from checks.complex_relationships import check_complex_relationships
    from checks.advanced_queries import check_advanced_queries
    from checks.code_organization import check_code_organization
    from checks.performance_optimization import check_performance_optimization
except ImportError as e:
    print(f"Warning: Could not import some Week 4 checks: {e}")
    # Fallback functions
    def check_alembic_migrations(repo_path): return {"error": "Module not available"}
    def check_complex_relationships(repo_path): return {"error": "Module not available"}
    def check_advanced_queries(repo_path): return {"error": "Module not available"}
    def check_code_organization(repo_path): return {"error": "Module not available"}
    def check_performance_optimization(repo_path): return {"error": "Module not available"}


class Week04Evaluator(BaseEvaluator):
    """
    Evaluador para Semana 4: Bases de Datos Avanzadas con FastAPI
    
    Evalúa:
    - Advanced Database: Migraciones Alembic, relaciones complejas
    - Advanced CRUD: Queries complejas, operaciones en lote
    - Code Organization: Estructura profesional del código
    - Performance Optimization: Optimización y rendimiento
    """
    
    def __init__(self, student_repo_path: str):
        super().__init__(
            week_number=4,
            student_repo_path=student_repo_path
        )
        self.common_checks = CommonChecks(self.repo_path)

"""
Evaluador específico para Semana 4 - Bases de Datos Avanzadas con FastAPI
SQLAlchemy avanzado: migraciones, relaciones, consultas complejas
"""
import sys
from pathlib import Path
from typing import Dict, Any, List

# Agregar el directorio padre al path para importar core
sys.path.append(str(Path(__file__).parent.parent.parent))

from core.base_evaluator import BaseEvaluator
from core.common_checks import CommonChecks

# Import checks using absolute imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

try:
    from checks.alembic_migrations import check_alembic_migrations
    from checks.complex_relationships import check_complex_relationships
    from checks.advanced_queries import check_advanced_queries
    from checks.code_organization import check_code_organization
    from checks.performance_optimization import check_performance_optimization
except ImportError as e:
    print(f"Warning: Could not import some Week 4 checks: {e}")
    # Fallback functions
    def check_alembic_migrations(repo_path): return {"error": "Module not available"}
    def check_complex_relationships(repo_path): return {"error": "Module not available"}
    def check_advanced_queries(repo_path): return {"error": "Module not available"}
    def check_code_organization(repo_path): return {"error": "Module not available"}
    def check_performance_optimization(repo_path): return {"error": "Module not available"}


class Week04Evaluator(BaseEvaluator):
    """
    Evaluador para Semana 4: Bases de Datos Avanzadas con FastAPI
    
    Evalúa:
    - Advanced Database: Migraciones Alembic, relaciones complejas
    - Advanced CRUD: Queries complejas, operaciones en lote
    - Code Organization: Estructura profesional del código
    - Performance Optimization: Optimización y rendimiento
    """
    
    def __init__(self, student_repo_path: str):
        super().__init__(
            week_number=4,
            student_repo_path=student_repo_path
        )
        self.common_checks = CommonChecks(self.repo_path)
    
    def run_specific_checks(self) -> Dict[str, Any]:
        """
        Ejecuta verificaciones específicas de la Semana 4 - Bases de Datos Avanzadas
        """
        results = {}
        
        # Checks básicos de estructura
        results["project_structure"] = self._check_week04_structure()
        
        # Checks específicos de Week 4 - Bases de Datos Avanzadas
        results["alembic_migrations"] = check_alembic_migrations(str(self.repo_path))
        results["complex_relationships"] = check_complex_relationships(str(self.repo_path))
        results["advanced_queries"] = check_advanced_queries(str(self.repo_path))
        results["code_organization"] = check_code_organization(str(self.repo_path))
        results["performance_optimization"] = check_performance_optimization(str(self.repo_path))
        
        # Checks de calidad de código
        results["code_quality"] = self._check_code_quality()
        
        return results
    
    def _check_week04_structure(self) -> Dict[str, Any]:
        """
        Verificaciones de estructura específicas para Week 4 - Bases de Datos Avanzadas
        """
        # Archivos requeridos para Week 4
        required_files = ["main.py", "requirements.txt", "README.md", "alembic.ini"]
        file_checks = self.common_checks.check_required_files(required_files)
        
        # Directorios requeridos para Week 4
        required_dirs = ["models", "schemas", "alembic"]
        dir_checks = {}
        for dir_name in required_dirs:
            dir_checks[dir_name] = self.common_checks.check_file_exists(dir_name)
        
        # Verificar dependencias específicas de Week 4
        required_packages = ['fastapi', 'uvicorn', 'sqlalchemy', 'alembic', 'psycopg2-binary']
        package_checks = self.common_checks.check_multiple_packages(required_packages)
        
        # Análisis de main.py
        main_syntax = self.common_checks.check_python_syntax("main.py")
        
        return {
            "required_files": file_checks,
            "required_directories": dir_checks,
            "required_packages": package_checks,
            "main_syntax": main_syntax,
            "structure_score": self._calculate_structure_score(file_checks, dir_checks, package_checks, main_syntax)
        }
    
    def _check_code_quality(self) -> Dict[str, Any]:
        """
        Verificaciones de calidad de código para Week 4
        """
        readme_analysis = self.common_checks.check_readme_content("README.md")
        
        python_files = ["main.py"]
        # Buscar archivos Python en models/ y schemas/
        models_path = self.repo_path / "models"
        schemas_path = self.repo_path / "schemas"
        
        if models_path.exists():
            python_files.extend([f"models/{f.name}" for f in models_path.glob("*.py")])
        if schemas_path.exists():
            python_files.extend([f"schemas/{f.name}" for f in schemas_path.glob("*.py")])
        
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
                                 dir_checks: Dict[str, bool],
                                 package_checks: Dict[str, bool], 
                                 main_syntax: Dict[str, Any]) -> float:
        """Calcula un score de estructura para Week 4"""
        score = 0
        total = 0
        
        # Archivos requeridos
        for file_present in file_checks.values():
            total += 1
            if file_present:
                score += 1
        
        # Directorios requeridos
        for dir_present in dir_checks.values():
            total += 1
            if dir_present:
                score += 1
        
        # Paquetes requeridos
        for package_present in package_checks.values():
            total += 1
            if package_present:
                score += 1
        
        # Sintaxis válida de main.py
        total += 1
        if main_syntax.get("syntax_valid", False):
            score += 1
        
        return (score / total * 100) if total > 0 else 0
    
    def _assess_overall_quality(self, readme_analysis: Dict[str, Any], 
                               syntax_checks: Dict[str, Any]) -> str:
        """Evalúa la calidad general del código para Week 4"""
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
        Genera feedback específico para Week 4 - Bases de Datos Avanzadas
        """
        feedback = []
        
        structure = results.get("project_structure", {})
        
        # Feedback sobre archivos requeridos
        if not structure.get("required_files", {}).get("main.py", False):
            feedback.append("• Crea el archivo main.py principal")
        if not structure.get("required_files", {}).get("alembic.ini", False):
            feedback.append("• Configura Alembic con alembic.ini")
        
        # Feedback sobre directorios
        missing_dirs = [
            dir_name for dir_name, present in structure.get("required_directories", {}).items()
            if not present
        ]
        if missing_dirs:
            feedback.append(f"• Crea las carpetas: {', '.join(missing_dirs)}")
        
        # Feedback sobre paquetes
        missing_packages = [
            pkg for pkg, present in structure.get("required_packages", {}).items()
            if not present
        ]
        if missing_packages:
            feedback.append(f"• Agrega a requirements.txt: {', '.join(missing_packages)}")
        
        # Feedback específico de checks de Week 4
        alembic_result = results.get("alembic_migrations", {})
        if not alembic_result.get("alembic_configured", False):
            feedback.append("• Configura Alembic para migraciones de base de datos")
        
        relationships_result = results.get("complex_relationships", {})
        if not relationships_result.get("has_relationships", False):
            feedback.append("• Implementa relaciones entre modelos (ForeignKey, relationship)")
        
        queries_result = results.get("advanced_queries", {})
        if not queries_result.get("has_complex_queries", False):
            feedback.append("• Desarrolla queries avanzadas con joins y filtros")
        
        organization_result = results.get("code_organization", {})
        if not organization_result.get("models_separated", False):
            feedback.append("• Organiza modelos en archivos separados en models/")
        
        return feedback
    
    def get_week04_summary(self) -> Dict[str, Any]:
        """
        Genera un resumen específico para Week 4
        """
        if not self.results:
            return {"error": "No evaluation results available"}
        
        structure = self.results.get("project_structure", {})
        alembic_result = self.results.get("alembic_migrations", {})
        relationships_result = self.results.get("complex_relationships", {})
        
        return {
            "structure_complete": structure.get("structure_score", 0) >= 80,
            "alembic_configured": alembic_result.get("alembic_configured", False),
            "relationships_implemented": relationships_result.get("has_relationships", False),
            "ready_for_week5": structure.get("structure_score", 0) >= 70 and alembic_result.get("alembic_configured", False)
        }


def create_evaluator(student_repo_path: str) -> Week04Evaluator:
    """Factory function para crear el evaluador de Week 4"""
    return Week04Evaluator(student_repo_path)


def run_week04_evaluation(student_repo_path: str) -> Dict[str, Any]:
    """
    Función de conveniencia para ejecutar evaluación completa de Week 4
    
    Args:
        student_repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Resultado completo de evaluación
    """
    evaluator = create_evaluator(student_repo_path)
    return evaluator.evaluate()
