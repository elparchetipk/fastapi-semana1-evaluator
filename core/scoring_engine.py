"""
Motor de puntuación configurable que calcula scores basado en criterios YAML.
Proporciona flexibilidad para diferentes tipos de evaluación y pesos.
"""
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path
import yaml


class ScoringEngine:
    """
    Motor de puntuación que evalúa resultados contra criterios configurables.
    """
    
    def __init__(self, criteria: Dict[str, Any]):
        """
        Inicializa el motor de puntuación.
        
        Args:
            criteria: Criterios de evaluación cargados desde YAML
        """
        self.criteria = criteria
        self.categories = criteria.get('categories', {})
        self.total_possible = self._calculate_total_possible()
        
        # Validar criterios
        self._validate_criteria()
    
    def _validate_criteria(self):
        """Valida que los criterios tengan la estructura correcta"""
        if not self.categories:
            raise ValueError("No categories found in criteria")
        
        total_weight = sum(cat.get('weight', 0) for cat in self.categories.values())
        if total_weight == 0:
            raise ValueError("Total weight of categories is 0")
        
        if total_weight > 110:  # Permite un pequeño margen
            raise ValueError(f"Total weight ({total_weight}) exceeds 100")
    
    def _calculate_total_possible(self) -> float:
        """Calcula el puntaje total posible"""
        return sum(cat.get('weight', 0) for cat in self.categories.values())
    
    def calculate_score(self, results: Dict[str, Any], 
                       result_evaluator: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Calcula la puntuación basada en los resultados de evaluación.
        
        Args:
            results: Resultados de todos los checks ejecutados
            result_evaluator: Función personalizada para evaluar resultados
            
        Returns:
            Dict con puntuación detallada por categorías y total
        """
        category_scores = {}
        total_earned = 0
        
        for category_name, category_config in self.categories.items():
            category_score = self._calculate_category_score(
                category_name, 
                category_config, 
                results,
                result_evaluator
            )
            
            category_scores[category_name] = category_score
            total_earned += category_score['earned']
        
        # Calcular porcentajes y estadísticas
        total_percentage = (total_earned / self.total_possible * 100) if self.total_possible > 0 else 0
        
        # Redondear percentage a 1 decimal
        total_percentage = round(total_percentage, 1)
        
        return {
            "categories": category_scores,
            "total": {
                "earned": total_earned,
                "possible": self.total_possible,
                "percentage": total_percentage
            },
            "breakdown": {cat: scores['earned'] for cat, scores in category_scores.items()},
            "passed": total_earned >= self.criteria.get('week_info', {}).get('passing_threshold', 70),
            "grade": self._calculate_letter_grade(total_percentage)
        }
    
    def _calculate_category_score(self, category_name: str, category_config: Dict,
                                 results: Dict[str, Any], 
                                 result_evaluator: Optional[Callable] = None) -> Dict[str, Any]:
        """
        Calcula la puntuación para una categoría específica.
        
        Args:
            category_name: Nombre de la categoría
            category_config: Configuración de la categoría
            results: Resultados de evaluación
            result_evaluator: Evaluador personalizado de resultados
            
        Returns:
            Dict con puntuación de la categoría
        """
        checks = category_config.get('checks', [])
        category_weight = category_config.get('weight', 0)
        
        earned_points = 0
        max_points_available = sum(check.get('points', 0) for check in checks)
        check_results = {}
        
        for check in checks:
            check_name = check.get('name')
            check_points = check.get('points', 0)
            check_required = check.get('required', True)
            
            # Evaluar el check
            if result_evaluator:
                check_passed = result_evaluator(check_name, results)
            else:
                check_passed = self._default_check_evaluator(check_name, results)
            
            check_results[check_name] = {
                "passed": check_passed,
                "points_possible": check_points,
                "points_earned": 0,
                "required": check_required
            }
            
            # Calcular puntos ganados
            if check_passed:
                points_earned = check_points
            elif not check_required:
                # Para checks opcionales, dar puntos parciales por el intento
                points_earned = check_points * 0.2  # 20% por el intento
            else:
                points_earned = 0
            
            check_results[check_name]["points_earned"] = points_earned
            earned_points += points_earned
        
        # Aplicar el peso de la categoría
        if max_points_available > 0:
            # Normalizar a la escala del peso de la categoría
            normalized_score = (earned_points / max_points_available) * category_weight
        else:
            normalized_score = 0
        
        # No exceder el peso máximo de la categoría
        final_score = min(normalized_score, category_weight)
        
        return {
            "earned": final_score,
            "possible": category_weight,
            "percentage": round((final_score / category_weight * 100) if category_weight > 0 else 0, 1),
            "checks": check_results,
            "raw_points": {
                "earned": earned_points,
                "possible": max_points_available
            }
        }
    
    def _default_check_evaluator(self, check_name: str, results: Dict[str, Any]) -> bool:
        """
        Evaluador por defecto que mapea nombres de checks a resultados.
        
        Args:
            check_name: Nombre del check
            results: Resultados de evaluación
            
        Returns:
            True si el check pasó
        """
        # Mapeos predefinidos para checks comunes
        check_mappings = {
            # Estructura básica
            "requirements_txt": lambda r: r.get("structure", {}).get("files", {}).get("requirements_txt", False),
            "main_py_exists": lambda r: r.get("structure", {}).get("files", {}).get("main_py", False),
            "readme_exists": lambda r: r.get("structure", {}).get("files", {}).get("readme_md", False),
            
            # Dependencias
            "fastapi_dependency": lambda r: r.get("requirements", {}).get("fastapi", False),
            "uvicorn_dependency": lambda r: r.get("requirements", {}).get("uvicorn", False),
            "sqlalchemy_installed": lambda r: r.get("requirements", {}).get("sqlalchemy", False),
            "pytest_setup": lambda r: r.get("requirements", {}).get("pytest", False),
            
            # App y funcionalidad
            "app_import": lambda r: r.get("app_import", {}).get("import_ok", False) and r.get("app_import", {}).get("has_app", False),
            "root_endpoint": lambda r: r.get("endpoints", {}).get("root_working", False),
            "docs_accessible": lambda r: r.get("endpoints", {}).get("docs_accessible", False),
            "parametric_endpoint": lambda r: r.get("endpoints", {}).get("parametric_endpoint", False),
            
            # Documentación
            "json_responses": lambda r: r.get("endpoints", {}).get("root_returns_json", False),
            "readme_reflection": lambda r: r.get("readme", {}).get("has_reflection", False),
            "setup_commands": lambda r: r.get("readme", {}).get("has_commands", False),
            
            # Calidad general
            "project_structure": lambda r: r.get("structure", {}).get("ok", False),
            "code_quality": lambda r: r.get("app_import", {}).get("import_ok", False),
            
            # Checks avanzados
            "database_config": lambda r: r.get("database", {}).get("connection_ok", False),
            "models_created": lambda r: r.get("database", {}).get("models_exist", False),
            "crud_operations": lambda r: r.get("crud", {}).get("all_operations", False),
            "authentication_system": lambda r: r.get("auth", {}).get("jwt_working", False),
            "containerization": lambda r: r.get("docker", {}).get("dockerfile_exists", False),
            "testing_coverage": lambda r: r.get("testing", {}).get("coverage_percentage", 0) >= 70,
        }
        
        # Intentar mapeo directo
        if check_name in check_mappings:
            try:
                return check_mappings[check_name](results)
            except (KeyError, TypeError, AttributeError):
                return False
        
        # Búsqueda recursiva en resultados
        return self._search_result_recursively(check_name, results)
    
    def _search_result_recursively(self, check_name: str, obj: Any, 
                                  max_depth: int = 5, current_depth: int = 0) -> bool:
        """
        Busca recursivamente un resultado por nombre en la estructura de datos.
        
        Args:
            check_name: Nombre del check a buscar
            obj: Objeto donde buscar
            max_depth: Profundidad máxima de búsqueda
            current_depth: Profundidad actual
            
        Returns:
            True si encuentra el resultado y es truthy
        """
        if current_depth >= max_depth:
            return False
        
        if isinstance(obj, dict):
            # Búsqueda directa
            if check_name in obj:
                return bool(obj[check_name])
            
            # Búsqueda por claves similares
            for key, value in obj.items():
                if check_name.lower() in key.lower() or key.lower() in check_name.lower():
                    if isinstance(value, bool):
                        return value
                    elif isinstance(value, (int, float)):
                        return value > 0
                
                # Búsqueda recursiva
                result = self._search_result_recursively(
                    check_name, value, max_depth, current_depth + 1
                )
                if result:
                    return result
        
        elif isinstance(obj, list):
            for item in obj:
                result = self._search_result_recursively(
                    check_name, item, max_depth, current_depth + 1
                )
                if result:
                    return result
        
        return False
    
    def _calculate_letter_grade(self, percentage: float) -> str:
        """
        Calcula la calificación en letras basada en el porcentaje.
        
        Args:
            percentage: Porcentaje obtenido
            
        Returns:
            Calificación en letra
        """
        if percentage >= 95:
            return "A+"
        elif percentage >= 90:
            return "A"
        elif percentage >= 85:
            return "A-"
        elif percentage >= 80:
            return "B+"
        elif percentage >= 75:
            return "B"
        elif percentage >= 70:
            return "B-"
        elif percentage >= 65:
            return "C+"
        elif percentage >= 60:
            return "C"
        elif percentage >= 55:
            return "C-"
        elif percentage >= 50:
            return "D"
        else:
            return "F"
    
    def get_category_feedback(self, category_name: str, category_score: Dict[str, Any]) -> List[str]:
        """
        Genera feedback específico para una categoría.
        
        Args:
            category_name: Nombre de la categoría
            category_score: Puntuación de la categoría
            
        Returns:
            Lista de mensajes de feedback
        """
        feedback = []
        checks = category_score.get('checks', {})
        
        # Feedback para checks fallidos
        failed_checks = [
            check_name for check_name, check_data in checks.items()
            if not check_data.get('passed', False) and check_data.get('required', True)
        ]
        
        if failed_checks:
            feedback.append(f"❌ **{category_name.title()}**: Checks fallidos: {', '.join(failed_checks)}")
        
        # Feedback para checks opcionales
        optional_failed = [
            check_name for check_name, check_data in checks.items()
            if not check_data.get('passed', False) and not check_data.get('required', True)
        ]
        
        if optional_failed:
            feedback.append(f"⚠️ **{category_name.title()}**: Mejoras opcionales: {', '.join(optional_failed)}")
        
        # Feedback positivo
        passed_checks = [
            check_name for check_name, check_data in checks.items()
            if check_data.get('passed', False)
        ]
        
        if passed_checks:
            feedback.append(f"✅ **{category_name.title()}**: Completado: {', '.join(passed_checks)}")
        
        return feedback
    
    def get_improvement_suggestions(self, scoring_result: Dict[str, Any]) -> List[str]:
        """
        Genera sugerencias de mejora basadas en la puntuación.
        
        Args:
            scoring_result: Resultado completo de puntuación
            
        Returns:
            Lista de sugerencias de mejora
        """
        suggestions = []
        categories = scoring_result.get('categories', {})
        
        # Ordenar categorías por performance (peor primero)
        sorted_categories = sorted(
            categories.items(),
            key=lambda x: x[1]['percentage']
        )
        
        for category_name, category_data in sorted_categories:
            percentage = category_data['percentage']
            
            if percentage < 50:
                suggestions.append(f"🔴 **{category_name.title()}**: Necesita atención urgente ({percentage:.1f}%)")
            elif percentage < 70:
                suggestions.append(f"🟡 **{category_name.title()}**: Requiere mejoras ({percentage:.1f}%)")
            elif percentage < 90:
                suggestions.append(f"🟢 **{category_name.title()}**: Buen trabajo, pequeñas mejoras posibles ({percentage:.1f}%)")
        
        return suggestions
    
    def export_detailed_report(self, scoring_result: Dict[str, Any]) -> str:
        """
        Exporta un reporte detallado de la puntuación.
        
        Args:
            scoring_result: Resultado de puntuación
            
        Returns:
            Reporte formateado en texto
        """
        total = scoring_result['total']
        categories = scoring_result['categories']
        
        report = f"""
REPORTE DETALLADO DE EVALUACIÓN
===============================

Puntuación Total: {total['earned']:.1f}/{total['possible']:.1f} ({total['percentage']:.1f}%)
Calificación: {scoring_result['grade']}
Estado: {'✅ APROBADO' if scoring_result['passed'] else '❌ PENDIENTE'}

DESGLOSE POR CATEGORÍAS:
"""
        
        for category_name, category_data in categories.items():
            report += f"""
{category_name.upper()}:
  Puntuación: {category_data['earned']:.1f}/{category_data['possible']:.1f} ({category_data['percentage']:.1f}%)
  
  Checks individuales:
"""
            
            for check_name, check_data in category_data['checks'].items():
                status = "✅" if check_data['passed'] else "❌"
                required = "Requerido" if check_data['required'] else "Opcional"
                points = f"{check_data['points_earned']:.1f}/{check_data['points_possible']}"
                
                report += f"    {status} {check_name} ({required}): {points} pts\n"
        
        return report


def create_scoring_engine(criteria_path: Path) -> ScoringEngine:
    """
    Factory function para crear un motor de puntuación desde archivo YAML.
    
    Args:
        criteria_path: Ruta al archivo criteria.yaml
        
    Returns:
        Motor de puntuación configurado
    """
    with open(criteria_path, 'r', encoding='utf-8') as f:
        criteria = yaml.safe_load(f)
    
    return ScoringEngine(criteria)
