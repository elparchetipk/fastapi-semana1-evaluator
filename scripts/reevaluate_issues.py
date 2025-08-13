#!/usr/bin/env python3
"""
Script para re-evaluar issues existentes en GitHub
Útil para activar re-evaluaciones masivas después de correcciones en el sistema
"""
import os
import sys
import json
import requests
import argparse
from typing import List, Dict, Any

def get_github_token() -> str:
    """Obtiene el token de GitHub desde variables de entorno"""
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ Error: Variable de entorno GITHUB_TOKEN no encontrada")
        print("Exporta tu token: export GITHUB_TOKEN=ghp_xxxxxxxxxxxx")
        sys.exit(1)
    return token

def get_issues(owner: str, repo: str, week: int, token: str, additional_labels: List[str] = None) -> List[Dict[str, Any]]:
    """Obtiene issues que necesitan re-evaluación"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Labels base para la búsqueda
    labels = ['evaluacion', f'semana-{week}']
    if additional_labels:
        labels.extend(additional_labels)
    
    url = f'https://api.github.com/repos/{owner}/{repo}/issues'
    params = {
        'labels': ','.join(labels),
        'state': 'open',
        'per_page': 100
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"❌ Error obteniendo issues: {response.status_code}")
        print(response.text)
        sys.exit(1)
    
    return response.json()

def trigger_reevaluation(owner: str, repo: str, issue_number: int, token: str, dry_run: bool = False) -> bool:
    """Activa la re-evaluación de un issue específico"""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    comment_body = (
        "🔄 **Re-evaluación solicitada**\n\n"
        "Esta evaluación fue activada por el script de re-evaluación.\n\n"
        "/evaluar"
    )
    
    if dry_run:
        print(f"  🧪 [DRY RUN] Comentaría en issue #{issue_number}")
        return True
    
    url = f'https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments'
    data = {'body': comment_body}
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"  ✅ Re-evaluación activada para issue #{issue_number}")
        return True
    else:
        print(f"  ❌ Error en issue #{issue_number}: {response.status_code}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Re-evalúa issues existentes en GitHub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python scripts/reevaluate_issues.py --owner epti --repo bc-channel --week 1
  python scripts/reevaluate_issues.py --owner epti --repo bc-channel --week 1 --dry-run
  python scripts/reevaluate_issues.py --owner epti --repo bc-channel --week 1 --labels revisar,pendiente
        """
    )
    
    parser.add_argument('--owner', required=True, help='Owner del repositorio de GitHub')
    parser.add_argument('--repo', required=True, help='Nombre del repositorio')
    parser.add_argument('--week', type=int, required=True, choices=range(1, 12), 
                       help='Semana a re-evaluar (1-11)')
    parser.add_argument('--labels', help='Labels adicionales separados por coma')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Modo de prueba (no realizar cambios reales)')
    parser.add_argument('--max-issues', type=int, default=50,
                       help='Máximo número de issues a procesar (default: 50)')
    
    args = parser.parse_args()
    
    print(f"🔄 Re-evaluación de Issues - Semana {args.week}")
    print("=" * 50)
    
    # Verificar token
    token = get_github_token()
    
    # Labels adicionales
    additional_labels = []
    if args.labels:
        additional_labels = [label.strip() for label in args.labels.split(',')]
    
    # Obtener issues
    print(f"🔍 Buscando issues en {args.owner}/{args.repo}")
    print(f"📋 Labels: evaluacion, semana-{args.week}" + 
          (f", {', '.join(additional_labels)}" if additional_labels else ""))
    
    issues = get_issues(args.owner, args.repo, args.week, token, additional_labels)
    
    if not issues:
        print("📭 No se encontraron issues para re-evaluar")
        return
    
    print(f"📊 Encontrados {len(issues)} issues")
    
    if args.dry_run:
        print("🧪 MODO DE PRUEBA - No se realizarán cambios reales")
    
    # Procesar issues
    issues_to_process = issues[:args.max_issues]
    success_count = 0
    
    print(f"\n🚀 Procesando {len(issues_to_process)} issues...")
    
    for i, issue in enumerate(issues_to_process, 1):
        issue_number = issue['number']
        title = issue['title'][:50] + "..." if len(issue['title']) > 50 else issue['title']
        
        print(f"\n📝 [{i}/{len(issues_to_process)}] Issue #{issue_number}: {title}")
        
        if trigger_reevaluation(args.owner, args.repo, issue_number, token, args.dry_run):
            success_count += 1
        
        # Pausa para evitar rate limiting
        if not args.dry_run and i < len(issues_to_process):
            import time
            time.sleep(1)
    
    print(f"\n✅ Resumen:")
    print(f"   📊 Issues procesados: {len(issues_to_process)}")
    print(f"   ✅ Exitosos: {success_count}")
    print(f"   ❌ Fallidos: {len(issues_to_process) - success_count}")
    
    if args.dry_run:
        print(f"\n💡 Para ejecutar realmente, quita el flag --dry-run")
    else:
        print(f"\n🎉 Re-evaluación completada!")

if __name__ == "__main__":
    main()
