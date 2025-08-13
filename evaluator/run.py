#!/usr/bin/env python3
"""
Script de compatibilidad para GitHub Actions
Redirige al evaluate.py principal con los argumentos correctos
"""
import sys
import subprocess
import tempfile
import shutil
import os
from pathlib import Path
from urllib.parse import urlparse

def clone_repository(repo_url: str) -> str:
    """
    Clona un repositorio de GitHub y retorna la ruta local
    
    Args:
        repo_url: URL del repositorio (puede incluir subcarpeta)
        
    Returns:
        Ruta local al repositorio clonado
    """
    # Crear directorio temporal
    temp_dir = tempfile.mkdtemp(prefix="eval_repo_")
    
    try:
        # Extraer la URL base del repositorio y la subcarpeta
        if "/tree/" in repo_url:
            # URL con subcarpeta: https://github.com/user/repo/tree/branch/subfolder
            parts = repo_url.split("/tree/")
            base_repo_url = parts[0]
            tree_path = parts[1]
            
            # Extraer branch y subfolder
            tree_parts = tree_path.split("/", 1)
            branch = tree_parts[0]
            subfolder = tree_parts[1] if len(tree_parts) > 1 else ""
        else:
            # URL simple: https://github.com/user/repo
            base_repo_url = repo_url
            branch = "main"
            subfolder = ""
        
        print(f"🔄 Clonando repositorio: {base_repo_url}")
        if subfolder:
            print(f"📁 Subcarpeta: {subfolder}")
        
        # Clonar el repositorio
        clone_cmd = [
            "git", "clone", 
            "--depth", "1",  # Clone shallow para mayor velocidad
            "--branch", branch,
            base_repo_url, 
            temp_dir
        ]
        
        result = subprocess.run(clone_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            # Si falla con la branch especificada, intentar con main/master
            for default_branch in ["main", "master"]:
                if default_branch != branch:
                    print(f"🔄 Intentando con branch {default_branch}...")
                    clone_cmd[5] = default_branch  # Reemplazar el branch
                    result = subprocess.run(clone_cmd, capture_output=True, text=True)
                    if result.returncode == 0:
                        break
            
            if result.returncode != 0:
                raise Exception(f"Error clonando repositorio: {result.stderr}")
        
        # Si hay subcarpeta, apuntar a ella
        if subfolder:
            subfolder_path = Path(temp_dir) / subfolder
            if not subfolder_path.exists():
                raise Exception(f"Subcarpeta no encontrada: {subfolder}")
            return str(subfolder_path)
        
        return temp_dir
        
    except Exception as e:
        # Limpiar directorio temporal si hay error
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise e

def main():
    """Redirige al evaluate.py principal"""
    # Ruta al script principal
    main_script = Path(__file__).parent.parent / "evaluate.py"
    
    # Argumentos por defecto para Semana 1 si no se especifican
    args = []
    cloned_repo_path = None
    
    # Procesar argumentos del estilo GitHub Actions
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == "--repo-url":
            # Manejar URL del repositorio
            repo_url = sys.argv[i + 1]
            if repo_url.startswith("file://"):
                repo_path = repo_url[7:]  # Remover file://
            else:
                # Clonar repositorio remoto
                try:
                    repo_path = clone_repository(repo_url)
                    cloned_repo_path = repo_path  # Guardar para limpieza posterior
                    print(f"✅ Repositorio clonado en: {repo_path}")
                except Exception as e:
                    print(f"❌ Error clonando repositorio: {e}")
                    sys.exit(1)
            
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
    
    try:
        # Ejecutar el script principal
        cmd = [sys.executable, str(main_script)] + args
        result = subprocess.run(cmd, capture_output=False)
        
        # Si se pidió un archivo JSON específico, crear el formato esperado por GitHub Actions
        if "--out-json" in sys.argv:
            json_index = sys.argv.index("--out-json") + 1
            if json_index < len(sys.argv):
                output_file = sys.argv[json_index]
                create_github_actions_json(output_file, result.returncode == 0)
        
        exit_code = result.returncode
        
    finally:
        # Limpiar repositorio clonado si existe
        if cloned_repo_path and os.path.exists(cloned_repo_path):
            # Si es una subcarpeta, limpiar el directorio padre
            cleanup_path = cloned_repo_path
            if "/tmp/" in cloned_repo_path:
                # Buscar el directorio temporal raíz
                parts = cloned_repo_path.split("/")
                for i, part in enumerate(parts):
                    if part.startswith("eval_repo_"):
                        cleanup_path = "/".join(parts[:i+1])
                        break
            
            print(f"🧹 Limpiando repositorio temporal: {cleanup_path}")
            shutil.rmtree(cleanup_path, ignore_errors=True)
    
    sys.exit(exit_code)

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
