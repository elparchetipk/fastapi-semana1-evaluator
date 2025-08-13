"""
Base evaluator class que sirve como foundation para todos los evaluadores semanales.
Proporciona funcionalidad común y define la interfaz que deben implementar los evaluadores específicos.
"""
import os
import sys
import yaml
import json
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime


class BaseEvaluator(ABC):
    """
    Clase base abstracta para todos los evaluadores semanales.
    
    Proporciona:
    - Carga de configuración desde criteria.yaml
    - Pipeline común de evaluación
    - Sistema de puntuación configurable
    - Generación de reportes
    - Manejo de errores estandarizado
    """
    
    def __init__(self, week_number: int, student_repo_path: str):
        """
        Inicializa el evaluador base.
        
        Args:
            week_number: Número de semana (1-11)
            student_repo_path: Ruta al repositorio del estudiante
        """
        self.week_number = week_number
        self.repo_path = Path(student_repo_path).resolve()
        self.week_dir = self._get_week_directory()
        
        # Cargar configuración de la semana
        self.criteria = self._load_criteria()
        self.config = self.criteria.get('automation', {})
        
        # Resultados de evaluación
        self.results = {}
        self.start_time = None
        self.end_time = None
        
        # Validar configuración básica
        self._validate_setup()
    
    def _get_week_directory(self) -> Path:
        """Obtiene el directorio de la semana actual"""
        base_dir = Path(__file__).parent.parent
        week_dir = base_dir / "weeks" / f"week{self.week_number:02d}"
        
        if not week_dir.exists():
            raise FileNotFoundError(f"Week directory not found: {week_dir}")
        
        return week_dir
    
    def _load_criteria(self) -> Dict[str, Any]:
        """Carga los criterios de evaluación desde criteria.yaml"""
        criteria_file = self.week_dir / "criteria.yaml"
        
        if not criteria_file.exists():
            raise FileNotFoundError(f"Criteria file not found: {criteria_file}")
        
        try:
            with open(criteria_file, 'r', encoding='utf-8') as f:
                criteria = yaml.safe_load(f)
            
            # Validar estructura básica
            required_keys = ['week_info', 'categories']
            for key in required_keys:
                if key not in criteria:
                    raise ValueError(f"Missing required key '{key}' in criteria.yaml")
            
            return criteria
            
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in criteria file: {e}")
    
    def _validate_setup(self):
        """Valida que el setup básico sea correcto"""
        # Verificar que el repositorio existe
        if not self.repo_path.exists():
            raise FileNotFoundError(f"Student repository not found: {self.repo_path}")
        
        # Verificar week_info
        week_info = self.criteria.get('week_info', {})
        if week_info.get('number') != self.week_number:
            raise ValueError(f"Week number mismatch: expected {self.week_number}, got {week_info.get('number')}")
    
    def evaluate(self) -> Dict[str, Any]:
        """
        Ejecuta el pipeline completo de evaluación.
        
        Returns:
            Dict con resultados completos de evaluación
        """
        self.start_time = datetime.now()
        
        try:
            # 1. Ejecutar checks comunes
            self.results.update(self._run_common_checks())
            
            # 2. Ejecutar checks específicos de la semana
            specific_results = self.run_specific_checks()
            self.results.update(specific_results)
            
            # 3. Calcular puntuación
            scoring = self._calculate_score()
            
            # 4. Generar reporte
            report = self._generate_report(scoring)
            
            # 5. Determinar si aprobó
            passed = self._determine_pass_status(scoring)
            
            self.end_time = datetime.now()
            
            # Extraer el score final para fácil acceso
            final_score = scoring.get('total', {})
            if isinstance(final_score, dict):
                final_score = final_score.get('percentage', 0)
            
            # Redondear score a 1 decimal para consistencia
            final_score = round(float(final_score), 1)
            
            return {
                "week": self.week_number,
                "student_repo": str(self.repo_path),
                "evaluation_time": self.end_time.isoformat(),
                "duration_seconds": (self.end_time - self.start_time).total_seconds(),
                "final_score": final_score,
                "results": self.results,
                "scoring": scoring,
                "report": report,
                "passed": passed,
                "passing_threshold": self.criteria['week_info'].get('passing_threshold', 70)
            }
            
        except Exception as e:
            self.end_time = datetime.now()
            return self._handle_evaluation_error(e)
    
    def _run_common_checks(self) -> Dict[str, Any]:
        """
        Ejecuta checks comunes que aplican a todas las semanas.
        Puede ser sobrescrito por evaluadores específicos.
        """
        # Los evaluadores específicos pueden implementar sus propios common checks
        # o usar CommonChecks del core
        try:
            from core.common_checks import CommonChecks
            common_checks = CommonChecks(self.repo_path)
            
            common_results = {}
            # Los common checks básicos se pueden implementar aquí si es necesario
            # Por ahora, devolvemos un resultado vacío para que no afecte la evaluación
            return common_results
            
        except ImportError:
            # Si no hay common checks disponibles, devolver resultado vacío
            return {}
    
    @abstractmethod
    def run_specific_checks(self) -> Dict[str, Any]:
        """
        Ejecuta verificaciones específicas de la semana.
        Debe ser implementado por cada evaluador específico.
        
        Returns:
            Dict con resultados de checks específicos
        """
        pass
    
    def _calculate_score(self) -> Dict[str, Any]:
        """
        Calcula la puntuación basada en los criterios configurados.
        """
        categories = self.criteria.get('categories', {})
        category_scores = {}
        total_possible = 0
        total_earned = 0
        
        for category_name, category_config in categories.items():
            category_weight = category_config.get('weight', 0)
            category_earned = self._calculate_category_score(category_name, category_config)
            
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
    
    def _calculate_category_score(self, category_name: str, category_config: Dict) -> float:
        """
        Calcula la puntuación para una categoría específica.
        
        Args:
            category_name: Nombre de la categoría
            category_config: Configuración de la categoría
            
        Returns:
            Puntuación obtenida para la categoría
        """
        checks = category_config.get('checks', [])
        earned_points = 0
        
        for check in checks:
            check_name = check.get('name')
            check_points = check.get('points', 0)
            check_required = check.get('required', True)
            
            # Obtener resultado del check
            check_result = self._get_check_result(check_name)
            
            if check_result:
                earned_points += check_points
            elif check_required:
                # Si es requerido y falló, penalización completa
                pass  # 0 puntos
            else:
                # Si es opcional y falló, penalización parcial
                earned_points += check_points * 0.1  # 10% por el intento
        
        # No exceder el peso máximo de la categoría
        max_points = category_config.get('weight', 0)
        return min(earned_points, max_points)
    
    def _get_check_result(self, check_name: str) -> bool:
        """
        Obtiene el resultado de un check específico desde los resultados.
        
        Args:
            check_name: Nombre del check a evaluar
            
        Returns:
            True si el check pasó, False si falló
        """
        # Mapeo de nombres de checks a rutas en results
        check_mappings = {
            # Checks de estructura (Week 1)
            "requirements_txt": lambda r: r.get("structure", {}).get("files", {}).get("requirements_txt", False),
            "main_py_exists": lambda r: r.get("structure", {}).get("files", {}).get("main_py", False),
            "readme_exists": lambda r: r.get("structure", {}).get("files", {}).get("readme_md", False),
            
            # Checks de dependencias (Week 1)
            "fastapi_dependency": lambda r: r.get("requirements", {}).get("fastapi", False),
            "uvicorn_dependency": lambda r: r.get("requirements", {}).get("uvicorn", False),
            
            # Checks de app (Week 1)
            "app_import": lambda r: r.get("app_import", {}).get("import_ok", False) and r.get("app_import", {}).get("has_app", False),
            
            # Checks de endpoints (Week 1)
            "root_endpoint": lambda r: r.get("endpoints", {}).get("root_working", False),
            "docs_accessible": lambda r: r.get("endpoints", {}).get("docs_accessible", False),
            "parametric_endpoint": lambda r: r.get("endpoints", {}).get("parametric_endpoint", False),
            
            # Checks de documentación (Week 1)
            "json_responses": lambda r: r.get("endpoints", {}).get("root_returns_json", False),
            "readme_reflection": lambda r: r.get("readme", {}).get("has_reflection", False),
            "setup_commands": lambda r: r.get("readme", {}).get("has_commands", False),
            
            # Checks generales (Week 1)
            "project_structure": lambda r: r.get("structure", {}).get("ok", False),
            "code_quality": lambda r: r.get("app_import", {}).get("import_ok", False),
            
            # Week 3 mappings
            "sqlalchemy_dependencies": lambda r: r.get("sqlalchemy_dependencies", {}).get("passed", False),
            "database_connection": lambda r: r.get("database_connection", {}).get("passed", False),
            "models_definition": lambda r: r.get("models_definition", {}).get("passed", False),
            "create_with_db": lambda r: r.get("create_with_db", {}).get("passed", False),
            "read_with_db": lambda r: r.get("read_with_db", {}).get("passed", False),
            "update_with_db": lambda r: r.get("update_with_db", {}).get("passed", False),
            "delete_with_db": lambda r: r.get("delete_with_db", {}).get("passed", False),
            "relationships": lambda r: r.get("relationships", {}).get("passed", False),
            "constraints": lambda r: r.get("constraints", {}).get("passed", False),
            "migrations": lambda r: r.get("migrations", {}).get("passed", False),
            "session_handling": lambda r: r.get("session_handling", {}).get("passed", False),
            "connection_pooling": lambda r: r.get("connection_pooling", {}).get("passed", False),
            
            # Week 5 mappings - using score-based checks
            "pytest_configuration": lambda r: self._score_based_check(r, "pytest_configuration"),
            "test_dependencies": lambda r: self._score_based_check(r, "test_dependencies"),
            "test_structure": lambda r: self._score_based_check(r, "test_structure"),
            "test_database_config": lambda r: self._score_based_check(r, "test_database_config"),
            "model_tests": lambda r: self._score_based_check(r, "model_tests"),
            "utility_function_tests": lambda r: self._score_based_check(r, "utility_function_tests"),
            "business_logic_tests": lambda r: self._score_based_check(r, "business_logic_tests"),
            "endpoint_tests": lambda r: self._score_based_check(r, "endpoint_tests"),
            "database_integration_tests": lambda r: self._score_based_check(r, "database_integration_tests"),
            "error_handling_tests": lambda r: self._score_based_check(r, "error_handling_tests"),
            "openapi_customization": lambda r: self._score_based_check(r, "openapi_customization"),
            "api_examples": lambda r: self._score_based_check(r, "api_examples"),
            "deployment_readme": lambda r: self._score_based_check(r, "deployment_readme"),
        }
        
        # Buscar el mapping correspondiente
        if check_name in check_mappings:
            try:
                return check_mappings[check_name](self.results)
            except (KeyError, TypeError):
                return False
        
        # Si no hay mapping específico, buscar directamente en results
        return self._search_result_by_name(check_name)
    
    def _search_result_by_name(self, check_name: str) -> bool:
        """
        Busca un resultado por nombre en toda la estructura de results.
        """
        def search_recursive(obj, target):
            if isinstance(obj, dict):
                if target in obj:
                    return bool(obj[target])
                for value in obj.values():
                    result = search_recursive(value, target)
                    if result is not None:
                        return result
            return None
        
        result = search_recursive(self.results, check_name)
        return result if result is not None else False
    
    def _generate_report(self, scoring: Dict[str, Any]) -> str:
        """
        Genera el reporte final de evaluación.
        
        Args:
            scoring: Resultados de puntuación
            
        Returns:
            Reporte formateado en Markdown
        """
        try:
            # Intentar cargar template personalizado
            template_path = self.week_dir / "templates" / "feedback.md"
            if template_path.exists():
                return self._generate_custom_report(template_path, scoring)
        except Exception:
            pass
        
        # Fallback a reporte básico
        return self._generate_basic_report(scoring)
    
    def _generate_custom_report(self, template_path: Path, scoring: Dict[str, Any]) -> str:
        """Genera reporte usando template personalizado"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template = f.read()
            
            # Variables para el template
            week_info = self.criteria.get('week_info', {})
            total_score = scoring['total']['earned']
            max_score = scoring['total']['possible']
            passed = total_score >= self.criteria['week_info'].get('passing_threshold', 70)
            
            # Feedback específico
            positive_feedback = self._generate_positive_feedback()
            improvement_feedback = self._generate_improvement_feedback()
            next_steps = self._generate_next_steps()
            
            # Reemplazar variables en el template
            template = template.format(
                status="✅ APROBADO" if passed else "🕐 PENDIENTE",
                total_score=int(total_score),
                pass_status="APROBADO" if passed else "PENDIENTE",
                # Scores por categoría
                **{f"{cat}_score": int(scores['earned']) for cat, scores in scoring['categories'].items()},
                **{f"{cat}_status": "✅" if scores['earned'] >= scores['possible'] * 0.7 else "⚠️" for cat, scores in scoring['categories'].items()},
                # Feedback sections
                positive_feedback=positive_feedback,
                improvement_feedback=improvement_feedback,
                next_steps=next_steps,
                evaluation_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            return template
            
        except Exception as e:
            return self._generate_basic_report(scoring)
    
    def _generate_basic_report(self, scoring: Dict[str, Any]) -> str:
        """Genera un reporte básico si no hay template personalizado"""
        week_info = self.criteria.get('week_info', {})
        total_score = scoring['total']['earned']
        threshold = self.criteria['week_info'].get('passing_threshold', 70)
        passed = total_score >= threshold
        
        status = "✅ **APROBADO**" if passed else "🕐 **PENDIENTE**"
        
        report = f"""{status} — Puntaje: **{int(total_score)}/100**

## Week {self.week_number}: {week_info.get('title', 'Evaluación')}

### 📊 Desglose por categorías

| Categoría | Puntaje | Estado |
|-----------|---------|---------|
"""
        
        for cat_name, cat_scores in scoring['categories'].items():
            earned = int(cat_scores['earned'])
            possible = int(cat_scores['possible'])
            status_icon = "✅" if earned >= possible * 0.7 else "⚠️"
            report += f"| {cat_name.title()} | {earned}/{possible} | {status_icon} |\n"
        
        report += f"""
### 🎯 Umbral de aprobación: {threshold}%

### 📋 Feedback específico:
{self._generate_improvement_feedback()}

---
> 🤖 Evaluación automática generada el {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
        
        return report
    
    def _generate_positive_feedback(self) -> str:
        """Genera feedback positivo basado en resultados"""
        feedback = []
        
        if self.results.get("app_import", {}).get("import_ok"):
            feedback.append("✅ Tu aplicación FastAPI se importa correctamente")
        
        if self.results.get("endpoints", {}).get("root_working"):
            feedback.append("✅ El endpoint raíz (/) está funcionando")
        
        if self.results.get("endpoints", {}).get("docs_accessible"):
            feedback.append("✅ La documentación automática (/docs) es accesible")
        
        if self.results.get("structure", {}).get("ok"):
            feedback.append("✅ La estructura del proyecto es correcta")
        
        return "\n".join(feedback) if feedback else "Continúa trabajando en los aspectos fundamentales."
    
    def _generate_improvement_feedback(self) -> str:
        """Genera feedback estructurado de mejora basado en checks"""
        
        # Separar elementos exitosos y fallidos
        successful_items = []
        improvement_items = []
        
        # Analizar resultados para identificar éxitos y mejoras
        self._analyze_results_for_feedback(successful_items, improvement_items)
        
        # Construir feedback estructurado
        feedback_parts = []
        
        if successful_items:
            feedback_parts.append("✅ **Lo que está bien:**")
            for i, item in enumerate(successful_items, 1):
                feedback_parts.append(f"{i}. {item}")
            feedback_parts.append("")  # Línea en blanco
        
        if improvement_items:
            feedback_parts.append("🔧 **Lo que se debe mejorar:**")
            for i, item in enumerate(improvement_items, 1):
                feedback_parts.append(f"{i}. {item}")
        
        if not improvement_items and successful_items:
            feedback_parts.append("🎉 **¡Excelente trabajo!** No hay mejoras críticas necesarias.")
        
        # Agregar feedback específico de la semana si existe
        try:
            specific_feedback = self.get_week_specific_feedback(self.results)
            if specific_feedback:
                feedback_parts.append("")
                feedback_parts.extend(specific_feedback)  # Agregar directamente, ya que viene formateado
        except:
            pass
        
        return "\n".join(feedback_parts)
    
    def _generate_next_steps(self) -> str:
        """Genera recomendaciones para próximos pasos"""
        if self.week_number < 11:
            next_week = self.week_number + 1
            return f"🚀 Prepárate para la Week {next_week}. Revisa los materiales de la siguiente semana."
        else:
            return "🎓 ¡Felicitaciones! Has completado el bootcamp de FastAPI."
    
    def get_week_specific_feedback(self, results: Dict[str, Any]) -> List[str]:
        """
        Genera feedback específico de la semana.
        Puede ser implementado por evaluadores específicos.
        
        Args:
            results: Resultados de evaluación
            
        Returns:
            Lista de mensajes de feedback específicos
        """
        return []
    
    def _determine_pass_status(self, scoring: Dict[str, Any]) -> bool:
        """Determina si el estudiante aprobó basado en la puntuación"""
        threshold = self.criteria['week_info'].get('passing_threshold', 70)
        return scoring['total']['earned'] >= threshold
    
    def _handle_evaluation_error(self, error: Exception) -> Dict[str, Any]:
        """Maneja errores durante la evaluación"""
        return {
            "week": self.week_number,
            "student_repo": str(self.repo_path),
            "evaluation_time": datetime.now().isoformat(),
            "error": True,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "passed": False,
            "results": {},
            "scoring": {"total": {"earned": 0, "possible": 100}},
            "report": f"❌ **ERROR EN EVALUACIÓN**\n\nTipo: {type(error).__name__}\nMensaje: {str(error)}\n\nContacta al instructor para revisión manual."
        }
    
    def get_criteria(self) -> Dict[str, Any]:
        """Retorna los criterios de evaluación cargados"""
        return self.criteria
    
    def get_results(self) -> Dict[str, Any]:
        """Retorna los resultados de evaluación"""
        return self.results
    
    def _analyze_results_for_feedback(self, successful_items: List[str], improvement_items: List[str]) -> None:
        """Analiza los resultados para categorizar elementos exitosos y mejoras necesarias"""
        
        # Detectar estructura de archivos (diferentes evaluadores usan diferentes claves)
        file_structure = None
        dependencies = None
        syntax_validation = None
        documentation = None
        
        # Week 1 usa project_structure
        if "project_structure" in self.results:
            project_struct = self.results["project_structure"]
            if isinstance(project_struct, dict):
                file_structure = project_struct.get("required_files", {})
                dependencies = project_struct.get("required_packages", {})
                syntax_info = project_struct.get("main_syntax", {})
                if syntax_info and syntax_info.get("syntax_valid", False):
                    successful_items.append("Sintaxis correcta en main.py")
        
        # Week 2 usa structure y requirements
        elif "structure" in self.results and "requirements" in self.results:
            struct = self.results["structure"]
            if isinstance(struct, dict):
                files = struct.get("files", {})
                # Convertir a formato estándar
                file_structure = {}
                if files.get("main_py", False):
                    file_structure["main.py"] = True
                if files.get("requirements_txt", False):
                    file_structure["requirements.txt"] = True
                if files.get("readme_md", False):
                    file_structure["README.md"] = True
                    
            dependencies = self.results.get("requirements", {})
        
        # Week 3 usa file_structure, dependencies, etc.
        else:
            file_structure = self.results.get("file_structure", {})
            dependencies = self.results.get("dependencies", {})
            syntax_validation = self.results.get("syntax_validation", {})
            documentation = self.results.get("documentation", {})
        
        # Analizar estructura de archivos
        if file_structure:
            if isinstance(file_structure, dict):
                for file_name, exists in file_structure.items():
                    if exists:
                        if file_name == "main.py":
                            successful_items.append("Archivo main.py presente y accesible")
                        elif file_name == "requirements.txt":
                            successful_items.append("Archivo requirements.txt presente")
                        elif file_name == "README.md":
                            successful_items.append("Documentación README.md presente")
                    else:
                        if file_name == "main.py":
                            improvement_items.append("Crear archivo main.py en la raíz del proyecto")
                        elif file_name == "requirements.txt":
                            improvement_items.append("Crear archivo requirements.txt con dependencias")
                        elif file_name == "README.md":
                            improvement_items.append("Crear archivo README.md con documentación del proyecto")
        
        # Analizar dependencias
        if dependencies:
            if isinstance(dependencies, dict):
                for package, exists in dependencies.items():
                    if exists:
                        if package == "fastapi":
                            successful_items.append("FastAPI correctamente instalado y configurado")
                        elif package == "uvicorn":
                            successful_items.append("Uvicorn disponible para ejecutar la aplicación")
                        elif package == "pydantic":
                            successful_items.append("Pydantic disponible para validación de datos")
                    else:
                        if package == "fastapi":
                            improvement_items.append("Agregar 'fastapi' a requirements.txt")
                        elif package == "uvicorn":
                            improvement_items.append("Agregar 'uvicorn' a requirements.txt para ejecutar la app")
                        elif package == "pydantic":
                            improvement_items.append("Agregar 'pydantic' a requirements.txt para validación")
        
        # Analizar sintaxis (Week 2 y 3)
        if syntax_validation:
            syntax_errors = []
            for file_name, syntax_result in syntax_validation.items():
                if isinstance(syntax_result, dict):
                    if syntax_result.get("syntax_valid", False):
                        successful_items.append(f"Sintaxis correcta en {file_name}")
                    else:
                        syntax_errors.append(file_name)
                        
            if syntax_errors:
                improvement_items.append(f"Corregir errores de sintaxis en: {', '.join(syntax_errors)}")
        
        # Analizar documentación (Week 2 y 3)
        if documentation and isinstance(documentation, dict):
            if documentation.get("score", 0) > 0:
                successful_items.append("Documentación básica presente en README")
            if documentation.get("score", 0) >= 5:
                successful_items.append("README con buena estructura y contenido")
    
    def _score_based_check(self, results: Dict, check_name: str) -> bool:
        """
        Evalúa un check basado en score/max_score.
        
        Args:
            results: Resultados de los checks
            check_name: Nombre del check
            
        Returns:
            True si el check tiene una puntuación > 0
        """
        check_result = results.get(check_name, {})
        if isinstance(check_result, dict):
            score = check_result.get('score', 0)
            return score > 0
        return False
