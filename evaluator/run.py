#!/usr/bin/env python3
"""
Script de compatibilidad para GitHub Actions
Redirige al evaluate.py principal con los argumentos correctos
"""
import sys
import subprocess
from pathlib import Path

def main():
    """Redirige al evaluate.py principal"""
    # Ruta al script principal
    main_script = Path(__file__).parent.parent / "evaluate.py"
    
    # Argumentos por defecto para Semana 1 si no se especifican
    args = []
    
    # Procesar argumentos del estilo GitHub Actions
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == "--repo-url":
            # Convertir URL de repo a path local (si es file://) o clonar
            repo_url = sys.argv[i + 1]
            if repo_url.startswith("file://"):
                repo_path = repo_url[7:]  # Remover file://
            else:
                # Para URLs reales, necesitaríamos clonar el repo
                repo_path = repo_url
            args.extend(["--repo", repo_path])
            i += 2
        elif arg == "--week":
            args.extend(["--week", sys.argv[i + 1]])
            i += 2
        elif arg == "--format":
            args.extend(["--format", sys.argv[i + 1]])
            i += 2
        elif arg == "--student-path":
            args.extend(["--repo", sys.argv[i + 1]])
            i += 2
        elif arg == "--out-md":
            args.extend(["--output", sys.argv[i + 1], "--format", "markdown"])
            i += 2
        elif arg == "--out-json":
            # Crear un archivo temporal para JSON con scoring
            json_file = sys.argv[i + 1]
            args.extend(["--output", json_file.replace('.json', '_full.json'), "--format", "json"])
            i += 2
        else:
            i += 1
    
    # Agregar semana por defecto si no se especifica
    if "--week" not in args and "-w" not in args:
        args = ["--week", "1"] + args
    
    # Ejecutar el script principal
    cmd = [sys.executable, str(main_script)] + args
    result = subprocess.run(cmd, capture_output=False)
    
    # Si se pidió un archivo JSON específico, crear el formato esperado por GitHub Actions
    if "--out-json" in sys.argv:
        json_index = sys.argv.index("--out-json") + 1
        if json_index < len(sys.argv):
            output_file = sys.argv[json_index]
            create_github_actions_json(output_file, result.returncode == 0)
    
    sys.exit(result.returncode)

def create_github_actions_json(output_file: str, passed: bool):
    """Crea un archivo JSON con el formato esperado por GitHub Actions"""
    import json
    
    # Formato simple requerido por el workflow
    data = {
        "passed": passed,
        "timestamp": "2025-08-13T00:00:00Z"
    }
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not create {output_file}: {e}")

if __name__ == "__main__":
    main()
