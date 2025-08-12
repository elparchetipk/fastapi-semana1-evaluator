#!/usr/bin/env python3
"""
CLI principal para el sistema de evaluación automática de FastAPI
Soporta evaluación de todas las semanas usando el framework core.
"""
import argparse
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent))

from core import BaseEvaluator, ReportGenerator


def load_week_evaluator(week_number: int, student_repo_path: str) -> Optional[BaseEvaluator]:
    """
    Carga dinámicamente el evaluador para una semana específica
    
    Args:
        week_number: Número de semana (1-11)
        student_repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Instancia del evaluador o None si no existe
    """
    week_dir = Path(__file__).parent / "weeks" / f"week{week_number:02d}"
    evaluator_file = week_dir / "evaluator.py"
    
    if not evaluator_file.exists():
        print(f"❌ Evaluador para semana {week_number} no encontrado en {evaluator_file}")
        return None
    
    try:
        # Importar dinámicamente el módulo del evaluador
        import importlib.util
        spec = importlib.util.spec_from_file_location(f"week{week_number:02d}_evaluator", evaluator_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Buscar la función create_evaluator o la clase principal
        if hasattr(module, 'create_evaluator'):
            return module.create_evaluator(student_repo_path)
        else:
            # Buscar la clase evaluador automáticamente
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, BaseEvaluator) and 
                    attr != BaseEvaluator):
                    return attr(student_repo_path)
        
        print(f"❌ No se encontró evaluador válido en {evaluator_file}")
        return None
        
    except Exception as e:
        print(f"❌ Error cargando evaluador para semana {week_number}: {e}")
        return None


def run_evaluation(week_number: int, student_repo_path: str, output_format: str = "markdown") -> Dict[str, Any]:
    """
    Ejecuta la evaluación para una semana específica
    
    Args:
        week_number: Número de semana a evaluar
        student_repo_path: Ruta al repositorio del estudiante
        output_format: Formato de salida ('json', 'markdown', 'summary')
        
    Returns:
        Resultados de la evaluación
    """
    print(f"🚀 Iniciando evaluación de Semana {week_number}")
    print(f"📁 Repositorio: {student_repo_path}")
    
    # Verificar que el repositorio existe
    repo_path = Path(student_repo_path)
    if not repo_path.exists():
        return {
            "success": False,
            "error": f"Repositorio no encontrado: {student_repo_path}"
        }
    
    # Cargar evaluador para la semana
    evaluator = load_week_evaluator(week_number, student_repo_path)
    if not evaluator:
        return {
            "success": False,
            "error": f"No se pudo cargar el evaluador para semana {week_number}"
        }
    
    try:
        # Ejecutar evaluación
        print("⚡ Ejecutando verificaciones...")
        results = evaluator.evaluate()
        
        # Generar reporte según el formato solicitado
        if output_format == "json":
            return results
        elif output_format == "summary":
            return _generate_summary_report(results, week_number)
        else:  # markdown por defecto
            return _generate_markdown_report(results, week_number)
            
    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": f"Error durante la evaluación: {str(e)}",
            "traceback": traceback.format_exc()
        }


def _generate_summary_report(results: Dict[str, Any], week_number: int) -> Dict[str, Any]:
    """Genera un reporte resumido"""
    # Obtener scoring directamente de los resultados
    scoring = results.get("scoring", {})
    final_score = scoring.get("total", {}).get("percentage", 0)
    
    # Redondear score a 1 decimal
    final_score = round(float(final_score), 1)
    
    return {
        "success": True,
        "week": week_number,
        "final_score": final_score,
        "passed": final_score >= 70,
        "total_checks": len(results.get("results", {})),
        "passed_checks": sum(1 for check in results.get("results", {}).values() 
                           if isinstance(check, dict) and check.get("passed", False)),
        "feedback_items": len(results.get("feedback", []))
    }


def _generate_markdown_report(results: Dict[str, Any], week_number: int) -> Dict[str, Any]:
    """Genera un reporte en formato markdown"""
    generator = ReportGenerator()
    
    # Usar el generador de reportes del core
    markdown_report = generator.generate_markdown_report(results)
    
    return {
        "success": True,
        "week": week_number,
        "format": "markdown",
        "report": markdown_report,
        "results": results
    }


def save_report_to_file(report_data: Dict[str, Any], output_file: str, format_type: str = "markdown"):
    """
    Guarda el reporte en un archivo
    
    Args:
        report_data: Datos del reporte
        output_file: Archivo de salida
        format_type: Tipo de formato ('json', 'markdown')
    """
    output_path = Path(output_file)
    
    try:
        if format_type == "json":
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
        else:  # markdown
            with open(output_path, 'w', encoding='utf-8') as f:
                if "report" in report_data:
                    f.write(report_data["report"])
                else:
                    f.write("# Reporte de Evaluación\n\n")
                    f.write(f"**Semana:** {report_data.get('week', 'N/A')}\n")
                    f.write(f"**Score:** {report_data.get('final_score', 'N/A')}\n\n")
                    f.write("```json\n")
                    f.write(json.dumps(report_data, indent=2, ensure_ascii=False))
                    f.write("\n```\n")
        
        print(f"✅ Reporte guardado en: {output_path}")
        
    except Exception as e:
        print(f"❌ Error guardando reporte: {e}")


def main():
    """Función principal del CLI"""
    parser = argparse.ArgumentParser(
        description="Evaluador automático para el bootcamp de FastAPI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python evaluate.py --week 1 --repo ./student-repo
  python evaluate.py --week 1 --repo ./student-repo --format json --output results.json
  python evaluate.py --week 1 --repo ./student-repo --format summary
        """
    )
    
    parser.add_argument(
        "--week", "-w",
        type=int,
        required=True,
        choices=range(1, 12),
        help="Número de semana a evaluar (1-11)"
    )
    
    parser.add_argument(
        "--repo", "-r",
        type=str,
        required=True,
        help="Ruta al repositorio del estudiante"
    )
    
    parser.add_argument(
        "--format", "-f",
        type=str,
        choices=["json", "markdown", "summary"],
        default="markdown",
        help="Formato de salida del reporte (default: markdown)"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Archivo donde guardar el reporte (opcional)"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Mostrar información detallada durante la evaluación"
    )
    
    args = parser.parse_args()
    
    # Configurar verbosidad
    if args.verbose:
        print(f"🔧 Configuración:")
        print(f"   Semana: {args.week}")
        print(f"   Repositorio: {args.repo}")
        print(f"   Formato: {args.format}")
        print(f"   Salida: {args.output or 'consola'}")
        print()
    
    # Ejecutar evaluación
    results = run_evaluation(args.week, args.repo, args.format)
    
    # Verificar si hubo errores
    if not results.get("success", False):
        print(f"❌ Error: {results.get('error', 'Error desconocido')}")
        sys.exit(1)
    
    # Mostrar resultados en consola
    if args.format == "summary":
        print("\n📊 RESUMEN DE EVALUACIÓN")
        print("=" * 50)
        print(f"Semana: {results['week']}")
        print(f"Score Final: {results['final_score']:.1f}/100")
        print(f"Estado: {'✅ APROBADO' if results['passed'] else '❌ REPROBADO'}")
        print(f"Checks: {results['passed_checks']}/{results['total_checks']} pasaron")
        print(f"Feedback: {results['feedback_items']} elementos")
    elif args.format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:  # markdown
        if "report" in results:
            print(results["report"])
        else:
            print("Error: No se pudo generar el reporte markdown")
    
    # Guardar archivo si se especificó
    if args.output:
        save_report_to_file(results, args.output, args.format)
    
    # Exit code basado en el resultado
    if args.format != "summary":
        # Para formatos completos, verificar el score en los resultados
        final_score = results.get("scoring", {}).get("total", {}).get("percentage", 0)
        if final_score < 70:
            sys.exit(1)
    else:
        # Para summary, usar el campo 'passed'
        if not results.get("passed", False):
            sys.exit(1)


if __name__ == "__main__":
    main()
