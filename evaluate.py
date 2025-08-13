#!/usr/bin/env python3
"""
Sistema de Evaluación Automática FastAPI Course
Punto de entrada principal para evaluaciones via CLI
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Dict, Any

# Agregar el directorio actual al Python path
sys.path.insert(0, str(Path(__file__).parent))

def get_evaluator_for_week(week_number: int, student_repo_path: str):
    """Obtiene el evaluador correcto para la semana especificada"""
    try:
        if week_number == 1:
            from weeks.week01.evaluator import Week01Evaluator
            return Week01Evaluator(student_repo_path)
        elif week_number == 2:
            from weeks.week02.evaluator import Week02Evaluator
            return Week02Evaluator(student_repo_path)
        elif week_number == 3:
            from weeks.week03.evaluator import Week03Evaluator
            return Week03Evaluator(student_repo_path)
        elif week_number == 4:
            from weeks.week04.evaluator import Week04Evaluator
            return Week04Evaluator(student_repo_path)
        elif week_number == 5:
            from weeks.week05.evaluator import Week05Evaluator
            return Week05Evaluator(student_repo_path)
        else:
            raise ValueError(f"Semana {week_number} no está implementada")
    except ImportError as e:
        raise ImportError(f"No se pudo cargar el evaluador para la semana {week_number}: {e}")

def format_output(result: Dict[str, Any], format_type: str) -> str:
    """Formatea el resultado según el tipo especificado"""
    if format_type == "json":
        return json.dumps(result, indent=2, ensure_ascii=False)
    elif format_type == "markdown":
        return result.get('report', '# Error: No se pudo generar el reporte')
    elif format_type == "summary":
        final_score = result.get('final_score', 0)
        passed = result.get('passed', False)
        status = "✅ APROBADO" if passed else "❌ NO APROBADO"
        
        return f"""
=== RESUMEN DE EVALUACIÓN ===
Semana: {result.get('week', 'N/A')}
Puntuación Final: {final_score:.1f}%
Estado: {status}
Umbral de Aprobación: {result.get('passing_threshold', 70)}%
Duración: {result.get('duration_seconds', 0):.2f} segundos
"""
    else:
        return str(result)

def main():
    """Función principal del CLI"""
    parser = argparse.ArgumentParser(
        description="Sistema de Evaluación Automática FastAPI Course",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python evaluate.py --week 1 --repo /path/to/student/repo
  python evaluate.py -w 5 -r /path/to/repo --format json
  python evaluate.py --week 3 --repo /path/to/repo --output results.md --format markdown
        """
    )
    
    parser.add_argument(
        '-w', '--week',
        type=int,
        required=True,
        help='Número de semana a evaluar (1-11)'
    )
    
    parser.add_argument(
        '-r', '--repo',
        type=str,
        required=True,
        help='Ruta al repositorio del estudiante'
    )
    
    parser.add_argument(
        '--format',
        choices=['json', 'markdown', 'summary'],
        default='summary',
        help='Formato de salida (default: summary)'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Archivo de salida (default: stdout)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar información detallada'
    )
    
    args = parser.parse_args()
    
    # Validar argumentos
    if not Path(args.repo).exists():
        print(f"❌ Error: El repositorio {args.repo} no existe", file=sys.stderr)
        sys.exit(1)
    
    if args.week < 1 or args.week > 11:
        print(f"❌ Error: Semana {args.week} no válida (debe ser 1-11)", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Mostrar información inicial si es verbose
        if args.verbose:
            print(f"🔍 Evaluando semana {args.week}")
            print(f"📁 Repositorio: {args.repo}")
            print(f"📄 Formato: {args.format}")
            print("-" * 50)
        
        # Obtener evaluador y ejecutar
        evaluator = get_evaluator_for_week(args.week, args.repo)
        result = evaluator.evaluate()
        
        # Formatear salida
        output = format_output(result, args.format)
        
        # Escribir resultado
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            if args.verbose:
                print(f"✅ Resultado guardado en: {args.output}")
        else:
            print(output)
        
        # Exit code basado en si pasó o no
        sys.exit(0 if result.get('passed', False) else 1)
        
    except Exception as e:
        print(f"❌ Error durante la evaluación: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(2)

if __name__ == "__main__":
    main()
