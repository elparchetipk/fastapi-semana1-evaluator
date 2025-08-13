"""
Evaluador específico para Semana 3 - Base de Datos con SQLAlchemy (versión segura análisis estático)
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
    from checks.database_connection import check_database_connection
    from checks.sqlalchemy_models import check_sqlalchemy_models
    from checks.crud_operations import check_crud_operations
    from checks.migrations import check_migrations
except ImportError as e:
    print(f"Warning: Could not import some Week 3 checks: {e}")
    # Fallback functions
    def check_database_connection(repo_path): return {"error": "Module not available"}
    def check_sqlalchemy_models(repo_path): return {"error": "Module not available"}
    def check_crud_operations(repo_path): return {"error": "Module not available"}
    def check_migrations(repo_path): return {"error": "Module not available"}


class Week03Evaluator(BaseEvaluator):
    """
    Evaluador para Semana 3: Base de Datos con SQLAlchemy
    
    Evalúa:
    - Database Setup: Configuración de base de datos
    - CRUD with DB: Operaciones CRUD con base de datos
    - Data Integrity: Integridad y relaciones de datos
    - Session Management: Manejo de sesiones de BD
    """
    
    def __init__(self, student_repo_path: str):
        super().__init__(
            week_number=3,
            student_repo_path=student_repo_path
        )
        
    def _run_common_checks(self) -> Dict[str, Any]:
        """
        Ejecuta verificaciones comunes usando CommonChecks
        """
        common_checks = CommonChecks(str(self.repo_path))
        
        # Verificaciones básicas de estructura
        required_files = ["main.py", "requirements.txt", "README.md"]
        file_checks = common_checks.check_required_files(required_files)
        
        # Verificaciones de dependencias específicas de Week 3
        required_packages = ['fastapi', 'uvicorn', 'sqlalchemy']
        package_checks = common_checks.check_multiple_packages(required_packages)
        
        # Verificaciones de sintaxis Python
        syntax_checks = {}
        python_files = ["main.py"]
        
        for py_file in python_files:
            if common_checks.check_file_exists(py_file):
                syntax_checks[py_file] = common_checks.check_python_syntax(py_file)
        
        # Análisis de README
        readme_analysis = common_checks.check_readme_content("README.md")
        
        return {
            "file_structure": file_checks,
            "dependencies": package_checks,
            "syntax_validation": syntax_checks,
            "documentation": readme_analysis
        }
    
    def run_specific_checks(self) -> Dict[str, Any]:
        """
        Ejecuta verificaciones específicas de la Semana 3
        """
        repo_path_str = str(self.repo_path)
        
        return {
            "sqlalchemy_dependencies": self._check_sqlalchemy_dependencies(),
            "database_connection": self._execute_check_safely(check_database_connection, repo_path_str),
            "models_definition": self._execute_check_safely(check_sqlalchemy_models, repo_path_str),
            "create_with_db": self._execute_check_safely(check_crud_operations, repo_path_str),
            "read_with_db": self._execute_check_safely(check_crud_operations, repo_path_str),
            "update_with_db": self._execute_check_safely(check_crud_operations, repo_path_str),
            "delete_with_db": self._execute_check_safely(check_crud_operations, repo_path_str),
            "relationships": self._execute_check_safely(check_sqlalchemy_models, repo_path_str),
            "constraints": self._execute_check_safely(check_sqlalchemy_models, repo_path_str),
            "migrations": self._execute_check_safely(check_migrations, repo_path_str),
            "session_handling": self._execute_check_safely(check_database_connection, repo_path_str),
            "connection_pooling": self._execute_check_safely(check_database_connection, repo_path_str)
        }
    
    def _execute_check_safely(self, check_function, repo_path: str) -> Dict[str, Any]:
        """
        Ejecuta una función de check de forma segura
        """
        try:
            result = check_function(repo_path)
            return {
                "passed": result.get("passed", False),
                "score": result.get("score", 0),
                "feedback": result.get("feedback", []),
                "details": result
            }
        except Exception as e:
            return {
                "passed": False,
                "score": 0,
                "feedback": [f"Error en verificación: {str(e)}"],
                "details": {"error": str(e)}
            }
    
    def _check_sqlalchemy_dependencies(self) -> Dict[str, Any]:
        """
        Verifica dependencias de SQLAlchemy
        """
        common_checks = CommonChecks(str(self.repo_path))
        
        # Verificar SQLAlchemy y driver de BD
        sqlalchemy_packages = ['sqlalchemy']
        db_drivers = ['psycopg2', 'psycopg2-binary', 'pymysql']
        
        sqlalchemy_check = common_checks.check_multiple_packages(sqlalchemy_packages)
        driver_check = common_checks.check_any_package(db_drivers)
        
        # SQLite no requiere driver externo, así que verificamos si usa SQLite
        uses_sqlite = self._check_sqlite_usage()
        
        # Se considera válido si tiene SQLAlchemy y (usa SQLite o tiene otro driver)
        has_sqlalchemy = sqlalchemy_check.get('sqlalchemy', False)
        has_driver = any(driver_check.values()) or uses_sqlite
        
        passed = has_sqlalchemy and has_driver
        score = 8 if passed else 0
        
        feedback = []
        if not has_sqlalchemy:
            feedback.append("Agrega 'sqlalchemy' a requirements.txt")
        if not has_driver and not uses_sqlite:
            feedback.append("Define una base de datos (SQLite incluido o agrega driver como psycopg2)")
        
        return {
            "passed": passed,
            "score": score,
            "feedback": feedback,
            "details": {
                "sqlalchemy_present": has_sqlalchemy,
                "db_driver_present": any(driver_check.values()),
                "uses_sqlite": uses_sqlite,
                "available_drivers": [k for k, v in driver_check.items() if v]
            }
        }
    
    def _check_sqlite_usage(self) -> bool:
        """
        Verifica si el proyecto usa SQLite basándose en el código
        """
        try:
            for py_file in self.repo_path.glob("**/*.py"):
                if py_file.name.startswith('.') or '__pycache__' in str(py_file):
                    continue
                
                try:
                    content = py_file.read_text(encoding='utf-8')
                    if 'sqlite://' in content.lower():
                        return True
                except Exception:
                    continue
            return False
        except Exception:
            return False
    
    def get_week_specific_feedback(self, results: Dict[str, Any]) -> List[str]:
        """
        Genera feedback específico para Week 3 - Base de Datos con SQLAlchemy
        Incluye tanto aspectos positivos como mejoras necesarias
        """
        feedback = []
        successful_aspects = []
        
        # Analizar dependencias de SQLAlchemy
        sqlalchemy_deps = results.get("sqlalchemy_dependencies", {})
        if sqlalchemy_deps.get("passed", False):
            successful_aspects.append("SQLAlchemy correctamente configurado y disponible")
        else:
            feedback.append("Configurar SQLAlchemy: agregar 'sqlalchemy' a requirements.txt")
        
        # Analizar conexión a base de datos
        db_connection = results.get("database_connection", {})
        if db_connection.get("passed", False):
            successful_aspects.append("Configuración de base de datos implementada (engine, session)")
        else:
            feedback.append("Implementar configuración de base de datos (create_engine, SessionLocal)")
        
        # Analizar definición de modelos
        models = results.get("models_definition", {})
        if models.get("passed", False):
            successful_aspects.append("Modelos SQLAlchemy definidos con tablas y columnas")
        else:
            feedback.append("Definir modelos SQLAlchemy con Base, columnas y tipos de datos")
        
        # Analizar operaciones CRUD
        crud_operations = {
            "create_with_db": ("CREATE", "endpoint POST que inserte datos en BD"),
            "read_with_db": ("READ", "endpoint GET que consulte datos de BD"), 
            "update_with_db": ("UPDATE", "endpoint PUT que actualice registros"),
            "delete_with_db": ("DELETE", "endpoint DELETE que elimine registros")
        }
        
        successful_crud = []
        missing_crud = []
        for operation, (label, description) in crud_operations.items():
            operation_result = results.get(operation, {})
            if operation_result.get("passed", False):
                successful_crud.append(f"Operación {label}")
            else:
                missing_crud.append(f"Implementar {description}")
        
        if successful_crud:
            successful_aspects.append(f"Operaciones CRUD implementadas: {', '.join(successful_crud)}")
        
        if missing_crud:
            feedback.extend(missing_crud)
        
        # Analizar relaciones entre tablas
        relationships = results.get("relationships", {})
        if relationships.get("passed", False):
            successful_aspects.append("Relaciones entre modelos definidas correctamente")
        else:
            feedback.append("Definir relaciones entre modelos usando ForeignKey y relationship()")
        
        # Analizar manejo de sesiones
        session_handling = results.get("session_handling", {})
        if session_handling.get("passed", False):
            successful_aspects.append("Manejo de sesiones SQLAlchemy implementado correctamente")
        else:
            feedback.append("Implementar dependency injection para sesiones BD con get_db()")
        
        # Combinar aspectos exitosos y mejoras
        combined_feedback = []
        
        if successful_aspects:
            combined_feedback.append("✅ **Aspectos de Week 3 implementados correctamente:**")
            for aspect in successful_aspects:
                combined_feedback.append(f"• {aspect}")
            combined_feedback.append("")  # Línea en blanco
        
        if feedback:
            combined_feedback.append("🔧 **Mejoras específicas de Week 3:**")
            for improvement in feedback:
                combined_feedback.append(f"• {improvement}")
        
        return combined_feedback



def create_evaluator(student_repo_path: str) -> Week03Evaluator:
    """Factory function para crear el evaluador de Week 3"""
    return Week03Evaluator(student_repo_path)


def run_week03_evaluation(student_repo_path: str) -> Dict[str, Any]:
    """
    Función de conveniencia para ejecutar evaluación completa de Week 3
    
    Args:
        student_repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Resultado completo de evaluación
    """
    evaluator = create_evaluator(student_repo_path)
    return evaluator.evaluate()
