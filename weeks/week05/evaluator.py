"""
Evaluador específico para Semana 5 - Testing y Documentación
Pruebas unitarias, integración y documentación avanzada
"""
import sys
import os
import re
from pathlib import Path
from typing import Dict, Any, List

# Agregar el directorio padre al path para importar core
sys.path.append(str(Path(__file__).parent.parent.parent))

from core import BaseEvaluator, CommonChecks

# Obtener directorio actual del evaluador
current_dir = Path(__file__).parent

# Agregar checks al path
checks_dir = current_dir / "checks"
sys.path.insert(0, str(checks_dir))

# Importar checks específicos directamente
try:
    from pytest_config import check_pytest_configuration
except ImportError as e:
    print(f"Warning: Could not import pytest_config check: {e}")
    def check_pytest_configuration(repo_path): return {"error": "Module not available"}

try:
    from test_dependencies import check_test_dependencies
except ImportError as e:
    print(f"Warning: Could not import test_dependencies check: {e}")
    def check_test_dependencies(repo_path): return {"error": "Module not available"}

try:
    from test_structure import check_test_structure
except ImportError as e:
    print(f"Warning: Could not import test_structure check: {e}")
    def check_test_structure(repo_path): return {"error": "Module not available"}

try:
    from test_database_config import check_test_database_config
except ImportError as e:
    print(f"Warning: Could not import test_database_config check: {e}")
    def check_test_database_config(repo_path): return {"error": "Module not available"}

try:
    from model_tests import check_model_tests
except ImportError as e:
    print(f"Warning: Could not import model_tests check: {e}")
    def check_model_tests(repo_path): return {"error": "Module not available"}

try:
    from utility_function_tests import check_utility_function_tests
except ImportError as e:
    print(f"Warning: Could not import utility_function_tests check: {e}")
    def check_utility_function_tests(repo_path): return {"error": "Module not available"}

try:
    from business_logic_tests import check_business_logic_tests
except ImportError as e:
    print(f"Warning: Could not import business_logic_tests check: {e}")
    def check_business_logic_tests(repo_path): return {"error": "Module not available"}

try:
    from endpoint_tests import check_endpoint_tests
except ImportError as e:
    print(f"Warning: Could not import endpoint_tests check: {e}")
    def check_endpoint_tests(repo_path): return {"error": "Module not available"}


class Week05Evaluator(BaseEvaluator):
    """
    Evaluador para Semana 5: Testing y Documentación
    
    Evalúa:
    - Unit Testing
    - Integration Testing
    - Documentation
    - Api Versioning
    """
    
    def __init__(self, student_repo_path: str):
        super().__init__(
            week_number=5,
            student_repo_path=student_repo_path
        )
        self.common_checks = CommonChecks(self.repo_path)
    
    def run_specific_checks(self) -> Dict[str, Any]:
        """
        Ejecuta verificaciones específicas de la Semana 5
        """
        results = {}
        
        # Testing Setup (35 points total)
        results["pytest_configuration"] = check_pytest_configuration(str(self.repo_path))
        results["test_dependencies"] = check_test_dependencies(str(self.repo_path))
        results["test_structure"] = check_test_structure(str(self.repo_path))
        results["test_database_config"] = check_test_database_config(str(self.repo_path))
        
        # Unit Testing (25 points total)
        results["model_tests"] = check_model_tests(str(self.repo_path))
        results["utility_function_tests"] = check_utility_function_tests(str(self.repo_path))
        results["business_logic_tests"] = check_business_logic_tests(str(self.repo_path))
        
        # Integration Testing (25 points total)
        results["endpoint_tests"] = check_endpoint_tests(str(self.repo_path))
        results["database_integration_tests"] = self._check_database_integration_tests()
        results["error_handling_tests"] = self._check_error_handling_tests()
        
        # Documentation (15 points total)
        results["openapi_customization"] = self._check_openapi_customization()
        results["api_examples"] = self._check_api_examples()
        results["deployment_readme"] = self._check_deployment_readme()
        
        return results
    
    def _check_database_integration_tests(self) -> Dict[str, Any]:
        """
        Verificaciones de tests de integración de base de datos
        """
        tests_dir = self.repo_path / 'tests'
        
        if not tests_dir.exists():
            return {
                "db_integration_tests": 0,
                "score": 0,
                "max_score": 8,
                "recommendations": ["Crear tests de integración de base de datos"]
            }
        
        db_test_count = 0
        test_files = list(tests_dir.rglob('test*.py'))
        
        for test_file in test_files:
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Buscar indicios de tests de integración de DB
                    db_patterns = [
                        r'def test.*db',
                        r'def test.*database',
                        r'def test.*session',
                        r'def test.*commit',
                        r'def test.*transaction'
                    ]
                    
                    for pattern in db_patterns:
                        if re.search(pattern, content.lower()):
                            db_test_count += len(re.findall(pattern, content.lower()))
                            
            except Exception:
                continue
        
        score = min(db_test_count * 2, 8)
        
        recommendations = []
        if db_test_count == 0:
            recommendations.append("Crear tests de integración con base de datos")
        
        return {
            "db_integration_tests": db_test_count,
            "score": score,
            "max_score": 8,
            "recommendations": recommendations
        }
    
    def _check_error_handling_tests(self) -> Dict[str, Any]:
        """
        Verificaciones de tests de manejo de errores
        """
        tests_dir = self.repo_path / 'tests'
        
        if not tests_dir.exists():
            return {
                "error_handling_tests": 0,
                "score": 0,
                "max_score": 7,
                "recommendations": ["Crear tests de manejo de errores"]
            }
        
        error_test_count = 0
        test_files = list(tests_dir.rglob('test*.py'))
        
        for test_file in test_files:
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Buscar indicios de tests de manejo de errores
                    error_patterns = [
                        r'def test.*error',
                        r'def test.*exception',
                        r'def test.*invalid',
                        r'def test.*fail',
                        r'pytest\.raises',
                        r'status_code.*4\d\d',
                        r'status_code.*5\d\d'
                    ]
                    
                    for pattern in error_patterns:
                        matches = re.findall(pattern, content.lower())
                        error_test_count += len(matches)
                            
            except Exception:
                continue
        
        score = min(error_test_count * 1.5, 7)
        
        recommendations = []
        if error_test_count == 0:
            recommendations.append("Crear tests para manejo de errores")
        
        return {
            "error_handling_tests": error_test_count,
            "score": int(score),
            "max_score": 7,
            "recommendations": recommendations
        }
    
    def _check_openapi_customization(self) -> Dict[str, Any]:
        """
        Verificaciones de personalización de documentación OpenAPI
        """
        main_files = ['main.py', 'app.py', 'api.py']
        customization_found = False
        customizations = []
        
        for main_file in main_files:
            file_path = self.repo_path / main_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Buscar personalizaciones de OpenAPI
                        if 'title=' in content and 'FastAPI' not in content:
                            customizations.append("Custom title")
                            customization_found = True
                            
                        if 'description=' in content:
                            customizations.append("Custom description")
                            customization_found = True
                            
                        if 'version=' in content:
                            customizations.append("Custom version")
                            customization_found = True
                            
                        if 'tags_metadata' in content:
                            customizations.append("Tags metadata")
                            customization_found = True
                            
                except Exception:
                    continue
        
        score = 5 if customization_found else 0
        
        return {
            "openapi_customized": customization_found,
            "customizations": customizations,
            "score": score,
            "max_score": 5,
            "recommendations": ["Personalizar título, descripción y metadata de OpenAPI"] if not customization_found else []
        }
    
    def _check_api_examples(self) -> Dict[str, Any]:
        """
        Verificaciones de ejemplos en documentación de API
        """
        python_files = list(self.repo_path.rglob('*.py'))
        examples_found = False
        example_types = []
        
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Buscar ejemplos en Pydantic models
                    if 'example=' in content or 'examples=' in content:
                        example_types.append("Pydantic examples")
                        examples_found = True
                        
                    # Buscar ejemplos en FastAPI endpoints
                    if 'response_model_example' in content:
                        example_types.append("Response examples")
                        examples_found = True
                        
                    # Buscar documentación en docstrings
                    if '"""' in content and 'example' in content.lower():
                        example_types.append("Docstring examples")
                        examples_found = True
                        
            except Exception:
                continue
        
        score = 5 if examples_found else 0
        
        return {
            "api_examples_found": examples_found,
            "example_types": example_types,
            "score": score,
            "max_score": 5,
            "recommendations": ["Agregar ejemplos en modelos Pydantic y endpoints"] if not examples_found else []
        }
    
    def _check_deployment_readme(self) -> Dict[str, Any]:
        """
        Verificaciones de documentación para deployment
        """
        readme_file = self.repo_path / 'README.md'
        
        if not readme_file.exists():
            return {
                "deployment_readme": False,
                "deployment_sections": [],
                "score": 0,
                "max_score": 5,
                "recommendations": ["Crear README.md con información de deployment"]
            }
        
        try:
            with open(readme_file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                
                deployment_sections = []
                
                # Buscar secciones relacionadas con deployment
                if 'install' in content or 'instalación' in content:
                    deployment_sections.append("Installation")
                    
                if 'run' in content or 'ejecutar' in content:
                    deployment_sections.append("Run instructions")
                    
                if 'docker' in content:
                    deployment_sections.append("Docker")
                    
                if 'environment' in content or 'env' in content:
                    deployment_sections.append("Environment variables")
                    
                if 'deploy' in content or 'production' in content:
                    deployment_sections.append("Deployment")
                
                has_deployment_info = len(deployment_sections) >= 2
                score = 5 if has_deployment_info else 2 if deployment_sections else 0
                
                return {
                    "deployment_readme": has_deployment_info,
                    "deployment_sections": deployment_sections,
                    "score": score,
                    "max_score": 5,
                    "recommendations": ["Agregar más información sobre deployment en README.md"] if not has_deployment_info else []
                }
                
        except Exception:
            return {
                "deployment_readme": False,
                "deployment_sections": [],
                "score": 0,
                "max_score": 5,
                "recommendations": ["Mejorar README.md con información de deployment"]
            }
    
    def _calculate_score(self) -> Dict[str, Any]:
        """
        Calcula la puntuación basada en los scores de los checks individuales.
        Este método sobrescribe el cálculo del BaseEvaluator para usar scores numéricos.
        """
        categories = self.criteria.get('categories', {})
        category_scores = {}
        total_possible = 0
        total_earned = 0
        
        for category_name, category_config in categories.items():
            category_weight = category_config.get('weight', 0)
            category_earned = self._calculate_category_score_numeric(category_name, category_config)
            
            category_scores[category_name] = {
                "earned": category_earned,
                "possible": category_weight,
                "percentage": (category_earned / category_weight * 100) if category_weight > 0 else 0
            }
            
            total_possible += category_weight
            total_earned += category_earned
        
        return {
            "categories": category_scores,
            "total": {
                "earned": total_earned,
                "possible": total_possible,
                "percentage": (total_earned / total_possible * 100) if total_possible > 0 else 0
            },
            "breakdown": {cat: scores["earned"] for cat, scores in category_scores.items()}
        }
    
    def _calculate_category_score_numeric(self, category_name: str, category_config: Dict) -> float:
        """
        Calcula la puntuación para una categoría basándose en scores numéricos de checks.
        """
        checks = category_config.get('checks', [])
        earned_points = 0
        max_possible_points = 0
        
        for check in checks:
            check_name = check.get('name')
            check_points = check.get('points', 0)
            max_possible_points += check_points
            
            # Obtener resultado del check (score numérico)
            check_result = self.results.get(check_name, {})
            if isinstance(check_result, dict):
                score = check_result.get('score', 0)
                max_score = check_result.get('max_score', check_points)
                
                # Normalizar el score al peso del check en el criterio
                if max_score > 0:
                    normalized_score = (score / max_score) * check_points
                    earned_points += normalized_score
        
        # No exceder el peso máximo de la categoría
        max_points = category_config.get('weight', 0)
        return min(earned_points, max_points)
    
    def _generate_report(self, scoring: Dict[str, Any]) -> str:
        """
        Genera el reporte final de evaluación para Week 5.
        Sobrescribe el método del BaseEvaluator para generar un reporte específico.
        """
        # Información básica
        week_info = self.criteria.get('week_info', {})
        final_score = scoring['total']['percentage']
        passed = scoring['total']['earned'] >= self.criteria['week_info'].get('passing_threshold', 75)
        status = "APROBADO ✅" if passed else "NO APROBADO ❌"
        
        # Construir reporte markdown
        report = f"""# 📋 Feedback de Evaluación - Semana 5: Testing y Documentación Avanzada

**Score Final**: {final_score:.1f}% ({status})

## 🔍 Análisis Detallado

### Resultados por Categoría:
"""
        
        # Agregar resultados por categoría
        for category_name, category_data in scoring['categories'].items():
            category_title = category_name.replace('_', ' ').title()
            earned = category_data['earned']
            possible = category_data['possible']
            percentage = category_data['percentage']
            
            report += f"- **{category_title}**: {earned:.1f}/{possible} puntos ({percentage:.1f}%)\n"
        
        # Agregar detalles de checks individuales
        report += "\n### Resultados por Check:\n"
        for check_name, check_result in self.results.items():
            if isinstance(check_result, dict) and 'score' in check_result:
                score = check_result['score']
                max_score = check_result.get('max_score', 0)
                check_title = check_name.replace('_', ' ').title()
                report += f"- **{check_title}**: {score}/{max_score} puntos\n"
        
        # Agregar recomendaciones
        report += "\n## 🎯 Recomendaciones\n\n"
        
        # Recopilar recomendaciones de todos los checks
        all_recommendations = []
        for check_result in self.results.values():
            if isinstance(check_result, dict) and 'recommendations' in check_result:
                all_recommendations.extend(check_result['recommendations'])
        
        if all_recommendations:
            for rec in all_recommendations[:10]:  # Limitar a 10 recomendaciones
                report += f"- {rec}\n"
        else:
            report += "- ¡Excelente trabajo! Continúa mejorando tu implementación.\n"
        
        # Recursos adicionales
        report += f"""
## 📚 Recursos de Apoyo

- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pytest Documentation](https://docs.pytest.org/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)

## 📊 Resumen

- **Umbral de Aprobación**: {self.criteria['week_info'].get('passing_threshold', 75)}%
- **Tu Puntuación**: {final_score:.1f}%
- **Estado**: {status}

{'¡Felicitaciones! Has aprobado esta evaluación.' if passed else 'Revisa las recomendaciones y vuelve a intentar.'}

**¡Sigue adelante con tu aprendizaje! 🚀**
"""
        
        return report


def create_evaluator(student_repo_path: str) -> Week05Evaluator:
    """Factory function para crear el evaluador de Week 5"""
    return Week05Evaluator(student_repo_path)


def run_week05_evaluation(student_repo_path: str) -> Dict[str, Any]:
    """
    Función de conveniencia para ejecutar evaluación completa de Week 5
    
    Args:
        student_repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Resultado completo de evaluación
    """
    evaluator = create_evaluator(student_repo_path)
    return evaluator.evaluate()
