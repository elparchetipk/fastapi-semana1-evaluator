"""
Generador de reportes que crea feedback formateado basado en templates y resultados.
Soporta templates personalizados y generación automática de reportes.
"""
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from string import Template


class ReportGenerator:
    """
    Generador de reportes flexible que puede usar templates personalizados o generar reportes automáticamente.
    """
    
    def __init__(self, week_number: int, week_dir: Path):
        """
        Inicializa el generador de reportes.
        
        Args:
            week_number: Número de semana
            week_dir: Directorio de la semana con templates
        """
        self.week_number = week_number
        self.week_dir = week_dir
        self.templates_dir = week_dir / "templates"
    
    def generate_report(self, evaluation_result: Dict[str, Any], 
                       template_name: str = "feedback.md") -> str:
        """
        Genera un reporte de evaluación.
        
        Args:
            evaluation_result: Resultado completo de evaluación
            template_name: Nombre del template a usar
            
        Returns:
            Reporte formateado en Markdown
        """
        # Intentar usar template personalizado
        custom_template_path = self.templates_dir / template_name
        if custom_template_path.exists():
            try:
                return self._generate_from_template(custom_template_path, evaluation_result)
            except Exception as e:
                # Fallback a reporte automático si el template falla
                pass
        
        # Generar reporte automático
        return self._generate_automatic_report(evaluation_result)
    
    def _generate_from_template(self, template_path: Path, 
                               evaluation_result: Dict[str, Any]) -> str:
        """
        Genera reporte usando un template personalizado.
        
        Args:
            template_path: Ruta al template
            evaluation_result: Resultado de evaluación
            
        Returns:
            Reporte renderizado
        """
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Preparar variables para el template
        template_vars = self._prepare_template_variables(evaluation_result)
        
        # Usar Template de Python para reemplazos seguros
        template = Template(template_content)
        
        try:
            # Intentar reemplazo con Template
            return template.safe_substitute(template_vars)
        except Exception:
            # Fallback a format string
            return template_content.format(**template_vars)
    
    def _prepare_template_variables(self, evaluation_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepara todas las variables disponibles para los templates.
        
        Args:
            evaluation_result: Resultado de evaluación
            
        Returns:
            Dict con variables para templates
        """
        scoring = evaluation_result.get('scoring', {})
        total = scoring.get('total', {})
        categories = scoring.get('categories', {})
        results = evaluation_result.get('results', {})
        
        # Variables básicas
        template_vars = {
            # Información básica
            'week_number': self.week_number,
            'total_score': int(total.get('earned', 0)),
            'max_score': int(total.get('possible', 100)),
            'percentage': f"{total.get('percentage', 0):.1f}",
            'passed': evaluation_result.get('passed', False),
            'status': "✅ APROBADO" if evaluation_result.get('passed', False) else "🕐 PENDIENTE",
            'pass_status': "APROBADO" if evaluation_result.get('passed', False) else "PENDIENTE",
            'grade': scoring.get('grade', 'F'),
            'evaluation_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'duration': f"{evaluation_result.get('duration_seconds', 0):.1f}",
            
            # Umbrales
            'passing_threshold': evaluation_result.get('passing_threshold', 70),
            
            # Feedback sections
            'positive_feedback': self._generate_positive_feedback(results),
            'improvement_feedback': self._generate_improvement_feedback(results, scoring),
            'next_steps': self._generate_next_steps(),
        }
        
        # Variables por categoría
        for category_name, category_data in categories.items():
            safe_name = self._safe_variable_name(category_name)
            template_vars.update({
                f'{safe_name}_score': int(category_data.get('earned', 0)),
                f'{safe_name}_max': int(category_data.get('possible', 0)),
                f'{safe_name}_percentage': f"{category_data.get('percentage', 0):.1f}",
                f'{safe_name}_status': "✅" if category_data.get('percentage', 0) >= 70 else "⚠️",
                f'{safe_name}_details': self._generate_category_details(category_name, category_data),
            })
        
        # Variables de análisis detallado
        template_vars.update({
            'failed_checks': self._get_failed_checks(scoring),
            'passed_checks': self._get_passed_checks(scoring),
            'critical_issues': self._get_critical_issues(results),
            'suggestions': self._get_suggestions(scoring),
            'technical_details': self._get_technical_details(results),
        })
        
        return template_vars
    
    def _safe_variable_name(self, name: str) -> str:
        """Convierte un nombre a un nombre de variable seguro"""
        return re.sub(r'[^a-zA-Z0-9_]', '_', name.lower())
    
    def _generate_automatic_report(self, evaluation_result: Dict[str, Any]) -> str:
        """
        Genera un reporte automático cuando no hay template personalizado.
        
        Args:
            evaluation_result: Resultado de evaluación
            
        Returns:
            Reporte automático en Markdown
        """
        scoring = evaluation_result.get('scoring', {})
        total = scoring.get('total', {})
        categories = scoring.get('categories', {})
        results = evaluation_result.get('results', {})
        
        total_score = int(total.get('earned', 0))
        passed = evaluation_result.get('passed', False)
        status = "✅ **APROBADO**" if passed else "🕐 **PENDIENTE**"
        
        # Header del reporte
        report = f"""{status} — Puntaje: **{total_score}/100**

# Week {self.week_number} - Evaluación Automática

**Estado:** {status}  
**Calificación:** {scoring.get('grade', 'F')}  
**Fecha:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 📊 Desglose por Categorías

| Categoría | Puntaje | Porcentaje | Estado |
|-----------|---------|------------|---------|
"""
        
        # Tabla de categorías
        for category_name, category_data in categories.items():
            earned = int(category_data.get('earned', 0))
            possible = int(category_data.get('possible', 0))
            percentage = f"{category_data.get('percentage', 0):.1f}%"
            status_icon = "✅" if category_data.get('percentage', 0) >= 70 else "⚠️"
            
            report += f"| {category_name.title()} | {earned}/{possible} | {percentage} | {status_icon} |\n"
        
        # Feedback positivo
        positive_feedback = self._generate_positive_feedback(results)
        if positive_feedback:
            report += f"""
---

## ✅ Lo que está funcionando bien

{positive_feedback}
"""
        
        # Áreas de mejora
        improvement_feedback = self._generate_improvement_feedback(results, scoring)
        if improvement_feedback:
            report += f"""
---

## 🔧 Áreas de mejora

{improvement_feedback}
"""
        
        # Detalles por categoría
        report += "\n---\n\n## 📋 Detalles por Categoría\n"
        
        for category_name, category_data in categories.items():
            details = self._generate_category_details(category_name, category_data)
            if details:
                earned = int(category_data.get('earned', 0))
                possible = int(category_data.get('possible', 0))
                report += f"\n### {category_name.title()} ({earned}/{possible})\n\n{details}\n"
        
        # Próximos pasos
        next_steps = self._generate_next_steps()
        if next_steps:
            report += f"""
---

## 🚀 Próximos pasos

{next_steps}
"""
        
        # Footer
        report += f"""
---

## 🔄 ¿Cómo mejorar?

1. **Revisa** los puntos mencionados en "Áreas de mejora"
2. **Implementa** las correcciones necesarias
3. **Actualiza** tu repositorio con los cambios
4. **Edita este issue** para solicitar una nueva evaluación

---

> 🤖 **Evaluación automática** - Si tienes dudas, consulta con tu instructor
"""
        
        return report
    
    def _generate_positive_feedback(self, results: Dict[str, Any]) -> str:
        """Genera feedback positivo basado en resultados exitosos"""
        feedback_items = []
        
        # Checks básicos exitosos
        if results.get("app_import", {}).get("import_ok"):
            feedback_items.append("✅ Tu aplicación FastAPI se importa correctamente")
        
        if results.get("endpoints", {}).get("root_working"):
            feedback_items.append("✅ El endpoint raíz (/) está funcionando")
        
        if results.get("endpoints", {}).get("docs_accessible"):
            feedback_items.append("✅ La documentación automática (/docs) es accesible")
        
        if results.get("structure", {}).get("ok"):
            feedback_items.append("✅ La estructura del proyecto es adecuada")
        
        if results.get("requirements", {}).get("fastapi") and results.get("requirements", {}).get("uvicorn"):
            feedback_items.append("✅ Las dependencias básicas están configuradas")
        
        if results.get("readme", {}).get("exists"):
            feedback_items.append("✅ Documentación del proyecto presente")
        
        # Checks avanzados
        if results.get("testing", {}).get("coverage_percentage", 0) > 70:
            feedback_items.append("✅ Excelente cobertura de testing")
        
        if results.get("docker", {}).get("dockerfile_exists"):
            feedback_items.append("✅ Aplicación containerizada con Docker")
        
        if results.get("auth", {}).get("jwt_working"):
            feedback_items.append("✅ Sistema de autenticación funcionando")
        
        return "\n".join(feedback_items) if feedback_items else "Continúa trabajando en los fundamentos básicos."
    
    def _generate_improvement_feedback(self, results: Dict[str, Any], 
                                     scoring: Dict[str, Any]) -> str:
        """Genera feedback de mejora basado en checks fallidos"""
        feedback_items = []
        
        # Análisis de categorías con bajo rendimiento
        categories = scoring.get('categories', {})
        for category_name, category_data in categories.items():
            if category_data.get('percentage', 0) < 70:
                failed_checks = [
                    check_name for check_name, check_info in category_data.get('checks', {}).items()
                    if not check_info.get('passed', False) and check_info.get('required', True)
                ]
                
                if failed_checks:
                    feedback_items.append(f"🔴 **{category_name.title()}**: {', '.join(failed_checks)}")
        
        # Feedback específico común
        if not results.get("structure", {}).get("files", {}).get("main_py"):
            feedback_items.append("• Crea el archivo `main.py` en la raíz del proyecto")
        
        if not results.get("requirements", {}).get("fastapi"):
            feedback_items.append("• Agrega `fastapi` a `requirements.txt`")
        
        if not results.get("requirements", {}).get("uvicorn"):
            feedback_items.append("• Agrega `uvicorn[standard]` a `requirements.txt`")
        
        if not results.get("app_import", {}).get("import_ok"):
            feedback_items.append("• Revisa errores de sintaxis en `main.py`")
        
        if not results.get("endpoints", {}).get("root_working"):
            feedback_items.append("• Implementa un endpoint `GET /` que retorne JSON")
        
        if not results.get("endpoints", {}).get("docs_accessible"):
            feedback_items.append("• Asegúrate de que `/docs` sea accesible")
        
        return "\n".join(feedback_items) if feedback_items else "¡Excelente trabajo! No hay mejoras críticas necesarias."
    
    def _generate_next_steps(self) -> str:
        """Genera recomendaciones para próximos pasos"""
        if self.week_number < 11:
            next_week = self.week_number + 1
            week_topics = {
                2: "CRUD Operations y Modelos de Datos",
                3: "Validación de Datos y Error Handling",
                4: "Base de Datos con SQLAlchemy",
                5: "Autenticación y Autorización",
                6: "Middleware y Configuración Avanzada",
                7: "Testing y Calidad de Código",
                8: "Deployment y Containerización",
                9: "WebSockets y Comunicación en Tiempo Real",
                10: "Background Tasks y Async Processing",
                11: "Proyecto Final Integrador"
            }
            
            topic = week_topics.get(next_week, "Siguiente tema")
            return f"🚀 **Prepárate para Week {next_week}**: {topic}"
        else:
            return "🎓 **¡Felicitaciones!** Has completado el bootcamp de FastAPI."
    
    def _generate_category_details(self, category_name: str, 
                                  category_data: Dict[str, Any]) -> str:
        """Genera detalles específicos para una categoría"""
        checks = category_data.get('checks', {})
        if not checks:
            return ""
        
        details = []
        
        for check_name, check_info in checks.items():
            status_icon = "✅" if check_info.get('passed', False) else "❌"
            points_earned = check_info.get('points_earned', 0)
            points_possible = check_info.get('points_possible', 0)
            required_text = " (Requerido)" if check_info.get('required', True) else " (Opcional)"
            
            details.append(f"{status_icon} **{check_name}**{required_text}: {points_earned:.1f}/{points_possible} pts")
        
        return "\n".join(details)
    
    def _get_failed_checks(self, scoring: Dict[str, Any]) -> List[str]:
        """Obtiene lista de checks fallidos"""
        failed = []
        categories = scoring.get('categories', {})
        
        for category_data in categories.values():
            for check_name, check_info in category_data.get('checks', {}).items():
                if not check_info.get('passed', False) and check_info.get('required', True):
                    failed.append(check_name)
        
        return failed
    
    def _get_passed_checks(self, scoring: Dict[str, Any]) -> List[str]:
        """Obtiene lista de checks exitosos"""
        passed = []
        categories = scoring.get('categories', {})
        
        for category_data in categories.values():
            for check_name, check_info in category_data.get('checks', {}).items():
                if check_info.get('passed', False):
                    passed.append(check_name)
        
        return passed
    
    def _get_critical_issues(self, results: Dict[str, Any]) -> List[str]:
        """Identifica issues críticos que impiden el funcionamiento básico"""
        critical = []
        
        if not results.get("app_import", {}).get("import_ok"):
            critical.append("La aplicación no se puede importar")
        
        if not results.get("structure", {}).get("files", {}).get("main_py"):
            critical.append("Falta archivo main.py")
        
        if not results.get("requirements", {}).get("fastapi"):
            critical.append("FastAPI no está en requirements.txt")
        
        return critical
    
    def _get_suggestions(self, scoring: Dict[str, Any]) -> List[str]:
        """Genera sugerencias específicas basadas en la puntuación"""
        suggestions = []
        total_percentage = scoring.get('total', {}).get('percentage', 0)
        
        if total_percentage < 50:
            suggestions.append("Enfócate en completar los requisitos básicos primero")
        elif total_percentage < 70:
            suggestions.append("Estás cerca del objetivo, revisa los checks fallidos")
        elif total_percentage < 90:
            suggestions.append("Buen trabajo, considera implementar features opcionales")
        else:
            suggestions.append("¡Excelente trabajo! Podrías ser mentor de otros estudiantes")
        
        return suggestions
    
    def _get_technical_details(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Extrae detalles técnicos para debugging"""
        return {
            "import_successful": results.get("app_import", {}).get("import_ok", False),
            "endpoints_working": results.get("endpoints", {}).get("root_working", False),
            "docs_accessible": results.get("endpoints", {}).get("docs_accessible", False),
            "structure_valid": results.get("structure", {}).get("ok", False),
            "dependencies_ok": results.get("requirements", {}).get("ok", False)
        }


def create_report_generator(week_number: int, week_dir: Path) -> ReportGenerator:
    """
    Factory function para crear un generador de reportes.
    
    Args:
        week_number: Número de semana
        week_dir: Directorio de la semana
        
    Returns:
        Generador de reportes configurado
    """
    return ReportGenerator(week_number, week_dir)
