#!/usr/bin/env python3
"""
Script para migrar automáticamente todas las semanas al nuevo framework
"""
import sys
from pathlib import Path
from typing import Dict, List

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent))

# Configuración de semanas y sus características
WEEKS_CONFIG = {
    3: {
        "title": "Base de Datos con SQLAlchemy",
        "description": "Integración de FastAPI con base de datos usando SQLAlchemy ORM",
        "dependencies": ["fastapi", "uvicorn", "sqlalchemy", "databases"],
        "main_topics": ["database_setup", "models", "crud_with_db", "migrations"],
        "checks": ["database_connection", "sqlalchemy_models", "crud_operations", "migrations"]
    },
    4: {
        "title": "Autenticación y Autorización",
        "description": "Implementación de JWT, OAuth2 y sistemas de autenticación",
        "dependencies": ["fastapi", "uvicorn", "python-jose", "passlib", "python-multipart"],
        "main_topics": ["authentication", "authorization", "jwt_tokens", "password_hashing"],
        "checks": ["jwt_implementation", "auth_endpoints", "protected_routes", "password_security"]
    },
    5: {
        "title": "Testing y Documentación",
        "description": "Pruebas unitarias, integración y documentación avanzada",
        "dependencies": ["fastapi", "uvicorn", "pytest", "httpx", "pytest-asyncio"],
        "main_topics": ["unit_testing", "integration_testing", "documentation", "api_versioning"],
        "checks": ["test_coverage", "test_quality", "documentation_completeness", "api_docs"]
    },
    6: {
        "title": "Background Tasks y WebSockets",
        "description": "Tareas en segundo plano y comunicación en tiempo real",
        "dependencies": ["fastapi", "uvicorn", "celery", "redis", "websockets"],
        "main_topics": ["background_tasks", "websockets", "real_time", "task_queues"],
        "checks": ["background_tasks", "websocket_endpoints", "task_queues", "real_time_features"]
    },
    7: {
        "title": "Deployment y Docker",
        "description": "Containerización y despliegue en producción",
        "dependencies": ["fastapi", "uvicorn", "gunicorn"],
        "main_topics": ["docker", "deployment", "production_config", "monitoring"],
        "checks": ["dockerfile", "docker_compose", "production_settings", "health_checks"]
    },
    8: {
        "title": "Microservicios y APIs",
        "description": "Arquitectura de microservicios y comunicación entre APIs",
        "dependencies": ["fastapi", "uvicorn", "httpx", "aiohttp"],
        "main_topics": ["microservices", "api_communication", "service_discovery", "load_balancing"],
        "checks": ["service_architecture", "api_communication", "error_handling", "service_discovery"]
    },
    9: {
        "title": "Performance y Caching",
        "description": "Optimización de rendimiento y estrategias de caché",
        "dependencies": ["fastapi", "uvicorn", "redis", "aioredis", "slow-query-log"],
        "main_topics": ["caching", "performance", "monitoring", "optimization"],
        "checks": ["caching_implementation", "performance_metrics", "query_optimization", "monitoring_setup"]
    },
    10: {
        "title": "GraphQL y Advanced APIs",
        "description": "Implementación de GraphQL y APIs avanzadas",
        "dependencies": ["fastapi", "uvicorn", "strawberry-graphql", "graphene"],
        "main_topics": ["graphql", "advanced_apis", "schema_design", "resolvers"],
        "checks": ["graphql_schema", "resolvers", "mutations", "subscriptions"]
    },
    11: {
        "title": "Proyecto Final",
        "description": "Integración de todos los conceptos en un proyecto completo",
        "dependencies": ["fastapi", "uvicorn", "sqlalchemy", "alembic", "pytest", "docker"],
        "main_topics": ["full_stack", "integration", "best_practices", "production_ready"],
        "checks": ["complete_application", "best_practices", "documentation", "deployment_ready"]
    }
}


def create_week_evaluator_template(week_number: int, config: Dict) -> str:
    """
    Genera el template del evaluador para una semana específica
    """
    return f'''"""
Evaluador específico para Semana {week_number} - {config["title"]}
{config["description"]}
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
        print(f"Warning: Could not import {{module_name}} check: {{e}}")
        return None

# Obtener directorio actual del evaluador
current_dir = Path(__file__).parent

# Importar checks específicos
{_generate_check_imports(config["checks"])}


class Week{week_number:02d}Evaluator(BaseEvaluator):
    """
    Evaluador para Semana {week_number}: {config["title"]}
    
    Evalúa:
    {_generate_evaluation_points(config["main_topics"])}
    """
    
    def __init__(self, student_repo_path: str):
        super().__init__(
            week_number={week_number},
            student_repo_path=student_repo_path
        )
        self.common_checks = CommonChecks(self.repo_path)
    
    def run_specific_checks(self) -> Dict[str, Any]:
        """
        Ejecuta verificaciones específicas de la Semana {week_number}
        """
        results = {{}}
        
        # Checks básicos de estructura
        results["project_structure"] = self._check_week{week_number:02d}_structure()
        
        # Checks específicos de Week {week_number}
{_generate_specific_checks(config["checks"])}
        
        # Checks de calidad de código
        results["code_quality"] = self._check_code_quality()
        
        return results
    
    def _check_week{week_number:02d}_structure(self) -> Dict[str, Any]:
        """
        Verificaciones de estructura específicas para Week {week_number}
        """
        # Archivos requeridos para Week {week_number}
        required_files = ["main.py", "requirements.txt", "README.md"]
        file_checks = self.common_checks.check_required_files(required_files)
        
        # Verificar dependencias específicas de Week {week_number}
        required_packages = {config["dependencies"]}
        package_checks = self.common_checks.check_multiple_packages(required_packages)
        
        # Análisis de main.py
        main_syntax = self.common_checks.check_python_syntax("main.py")
        
        return {{
            "required_files": file_checks,
            "required_packages": package_checks,
            "main_syntax": main_syntax,
            "structure_score": self._calculate_structure_score(file_checks, package_checks, main_syntax)
        }}
    
    def _check_code_quality(self) -> Dict[str, Any]:
        """
        Verificaciones de calidad de código para Week {week_number}
        """
        readme_analysis = self.common_checks.check_readme_content("README.md")
        
        python_files = ["main.py"]
        syntax_checks = {{}}
        
        for py_file in python_files:
            if self.common_checks.check_file_exists(py_file):
                syntax_checks[py_file] = self.common_checks.check_python_syntax(py_file)
        
        return {{
            "readme_analysis": readme_analysis,
            "syntax_checks": syntax_checks,
            "overall_quality": self._assess_overall_quality(readme_analysis, syntax_checks)
        }}
    
    def _calculate_structure_score(self, file_checks: Dict[str, bool], 
                                 package_checks: Dict[str, bool], 
                                 main_syntax: Dict[str, Any]) -> float:
        """Calcula un score de estructura para Week {week_number}"""
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
        """Evalúa la calidad general del código para Week {week_number}"""
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
        Genera feedback específico para Week {week_number}
        """
        feedback = []
        
        structure = results.get("project_structure", {{}})
        if not structure.get("required_files", {{}}).get("main.py", False):
            feedback.append("• Crea el archivo main.py principal")
        
        missing_packages = [
            pkg for pkg, present in structure.get("required_packages", {{}}).items()
            if not present
        ]
        if missing_packages:
            feedback.append(f"• Agrega a requirements.txt: {{', '.join(missing_packages)}}")
        
        # TODO: Agregar feedback específico para Week {week_number}
        
        return feedback
    
    def get_week{week_number:02d}_summary(self) -> Dict[str, Any]:
        """
        Genera un resumen específico para Week {week_number}
        """
        if not self.results:
            return {{"error": "No evaluation results available"}}
        
        structure = self.results.get("project_structure", {{}})
        
        return {{
            "structure_complete": structure.get("structure_score", 0) >= 80,
            "ready_for_week{week_number + 1}": structure.get("structure_score", 0) >= 70
        }}


def create_evaluator(student_repo_path: str) -> Week{week_number:02d}Evaluator:
    """Factory function para crear el evaluador de Week {week_number}"""
    return Week{week_number:02d}Evaluator(student_repo_path)


def run_week{week_number:02d}_evaluation(student_repo_path: str) -> Dict[str, Any]:
    """
    Función de conveniencia para ejecutar evaluación completa de Week {week_number}
    
    Args:
        student_repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Resultado completo de evaluación
    """
    evaluator = create_evaluator(student_repo_path)
    return evaluator.evaluate()
'''


def _generate_check_imports(checks: List[str]) -> str:
    """Genera los imports de checks específicos"""
    imports = []
    for check in checks:
        imports.append(f'''
try:
    {check}_module = import_check_module("{check}", str(current_dir / "checks" / "{check}.py"))
    check_{check} = {check}_module.check_{check} if {check}_module else lambda repo_path: {{"error": "Module not available"}}
except Exception as e:
    print(f"Warning: Could not import {check} check: {{e}}")
    def check_{check}(repo_path): return {{"error": "Module not available"}}''')
    
    return '\n'.join(imports)


def _generate_evaluation_points(topics: List[str]) -> str:
    """Genera los puntos de evaluación"""
    return '\n    '.join([f"- {topic.replace('_', ' ').title()}" for topic in topics])


def _generate_specific_checks(checks: List[str]) -> str:
    """Genera las llamadas a checks específicos"""
    check_calls = []
    for check in checks:
        check_calls.append(f'        results["{check}"] = check_{check}(str(self.repo_path))')
    
    return '\n'.join(check_calls)


def create_basic_check_template(check_name: str, week_number: int) -> str:
    """
    Genera un template básico para un check específico
    """
    return f'''"""
Verificaciones de {check_name.replace("_", " ")} específicas para Week {week_number}
"""
import sys
from pathlib import Path
from typing import Dict, Any, List


def check_{check_name}(repo_path: str) -> Dict[str, Any]:
    """
    Verifica {check_name.replace("_", " ")} para Week {week_number}
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de {check_name.replace("_", " ")}
    """
    repo_root = Path(repo_path)
    
    # TODO: Implementar verificaciones específicas para {check_name}
    
    return {{
        "{check_name}_implemented": False,
        "{check_name}_score": 0,
        "recommendations": [
            "Implementar {check_name.replace('_', ' ')}"
        ],
        "error": "Check not implemented yet"
    }}


def get_{check_name}_recommendations(repo_path: str) -> List[str]:
    """
    Genera recomendaciones específicas para {check_name.replace("_", " ")}
    """
    return [
        f"Implementar {check_name.replace('_', ' ')} según los requisitos de Week {week_number}"
    ]
'''


def migrate_week(week_number: int):
    """
    Migra una semana específica al nuevo framework
    """
    if week_number not in WEEKS_CONFIG:
        print(f"❌ Week {week_number} no está configurada")
        return False
    
    config = WEEKS_CONFIG[week_number]
    week_dir = Path(__file__).parent / "weeks" / f"week{week_number:02d}"
    
    print(f"🔄 Migrando Week {week_number}: {config['title']}")
    
    # Crear directorios si no existen
    checks_dir = week_dir / "checks"
    templates_dir = week_dir / "templates"
    
    checks_dir.mkdir(exist_ok=True)
    templates_dir.mkdir(exist_ok=True)
    
    # Crear evaluator.py
    evaluator_file = week_dir / "evaluator.py"
    if not evaluator_file.exists():
        evaluator_content = create_week_evaluator_template(week_number, config)
        evaluator_file.write_text(evaluator_content)
        print(f"  ✅ Creado evaluator.py")
    else:
        print(f"  ⚠️  evaluator.py ya existe, saltando...")
    
    # Crear checks básicos
    for check_name in config["checks"]:
        check_file = checks_dir / f"{check_name}.py"
        if not check_file.exists():
            check_content = create_basic_check_template(check_name, week_number)
            check_file.write_text(check_content)
            print(f"  ✅ Creado checks/{check_name}.py")
        else:
            print(f"  ⚠️  checks/{check_name}.py ya existe, saltando...")
    
    # Crear templates básicos
    feedback_template = templates_dir / "feedback.md"
    if not feedback_template.exists():
        feedback_content = f"""# 📋 Feedback de Evaluación - Semana {week_number}: {config["title"]}

**Score Final**: {{{{final_score}}}}/100 ({{{{status}}}})

## 🔍 Análisis Detallado

### Resultados por Área:
{{{{#check_results}}}}
- **{{{{name}}}}**: {{{{score}}}}/100
{{{{/check_results}}}}

## 🎯 Recomendaciones

{{{{#recommendations}}}}
- {{{{.}}}}
{{{{/recommendations}}}}

## 📚 Recursos de Apoyo

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Week {week_number} Specific Resources]

**¡Sigue adelante! 🚀**
"""
        feedback_template.write_text(feedback_content)
        print(f"  ✅ Creado templates/feedback.md")
    
    issue_template = templates_dir / "issue_template.yml"
    if not issue_template.exists():
        issue_content = f'''name: "📋 Week {week_number}: {config["title"]} - Evaluación Automática"
description: "Reporte automático de evaluación para Semana {week_number}"
title: "[Week {week_number}] Evaluación Automática - {config["title"]}"
labels: ["week-{week_number}", "evaluation", "fastapi"]
body:
  - type: markdown
    attributes:
      value: |
        ## 📊 Resumen de Evaluación - Semana {week_number}
        
        **Tema**: {config["title"]}
        **Score Final**: ${{{{ final_score }}}}/100
        
  - type: textarea
    id: results
    attributes:
      label: "🎯 Resultados"
      value: |
        **Status**: ${{{{ status }}}}
        **Listo para Week {week_number + 1}**: ${{{{ ready_for_next_week }}}}
'''
        issue_template.write_text(issue_content)
        print(f"  ✅ Creado templates/issue_template.yml")
    
    print(f"✅ Week {week_number} migrada exitosamente")
    return True


def migrate_all_weeks():
    """
    Migra todas las semanas restantes
    """
    print("🚀 Iniciando migración de todas las semanas al nuevo framework")
    print("=" * 60)
    
    success_count = 0
    total_weeks = len(WEEKS_CONFIG)
    
    for week_number in sorted(WEEKS_CONFIG.keys()):
        try:
            if migrate_week(week_number):
                success_count += 1
            print()  # Línea en blanco entre semanas
        except Exception as e:
            print(f"❌ Error migrando Week {week_number}: {e}")
    
    print("=" * 60)
    print(f"🏁 Migración completada: {success_count}/{total_weeks} semanas migradas exitosamente")
    
    if success_count == total_weeks:
        print("🎉 ¡Todas las semanas fueron migradas correctamente!")
    else:
        print("⚠️  Algunas semanas tuvieron problemas. Revisa los errores arriba.")
    
    return success_count == total_weeks


def main():
    """
    Función principal
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Migrar semanas al nuevo framework")
    parser.add_argument("--week", "-w", type=int, choices=list(WEEKS_CONFIG.keys()),
                       help="Migrar una semana específica")
    parser.add_argument("--all", "-a", action="store_true",
                       help="Migrar todas las semanas")
    
    args = parser.parse_args()
    
    if args.week:
        success = migrate_week(args.week)
        sys.exit(0 if success else 1)
    elif args.all:
        success = migrate_all_weeks()
        sys.exit(0 if success else 1)
    else:
        print("🔧 MIGRADOR DE SEMANAS - FastAPI Evaluator")
        print("Uso:")
        print("  python migrate_weeks.py --week 3    # Migrar semana específica")
        print("  python migrate_weeks.py --all       # Migrar todas las semanas")
        print()
        print("Semanas disponibles para migrar:")
        for week_num, config in WEEKS_CONFIG.items():
            print(f"  Week {week_num}: {config['title']}")


if __name__ == "__main__":
    main()
