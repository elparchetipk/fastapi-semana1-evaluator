"""
Check para verificar configuración y uso de Alembic para migraciones
"""
import os
import re
from pathlib import Path
from typing import Dict, Any


def check_alembic_migrations(repo_path: str) -> Dict[str, Any]:
    """
    Verifica que Alembic esté configurado correctamente para migraciones
    """
    results = {
        "alembic_ini_exists": False,
        "alembic_folder_exists": False,
        "versions_folder_exists": False,
        "has_migration_files": False,
        "env_py_exists": False,
        "alembic_in_requirements": False,
        "score": 0,
        "details": [],
        "errors": []
    }
    
    try:
        repo_path = Path(repo_path)
        
        # Verificar alembic.ini
        alembic_ini = repo_path / "alembic.ini"
        if alembic_ini.exists():
            results["alembic_ini_exists"] = True
            results["details"].append("✅ Archivo alembic.ini encontrado")
            results["score"] += 3
        else:
            results["errors"].append("❌ Archivo alembic.ini no encontrado")
        
        # Verificar carpeta alembic/
        alembic_folder = repo_path / "alembic"
        if alembic_folder.exists() and alembic_folder.is_dir():
            results["alembic_folder_exists"] = True
            results["details"].append("✅ Carpeta alembic/ encontrada")
            results["score"] += 2
            
            # Verificar env.py
            env_py = alembic_folder / "env.py"
            if env_py.exists():
                results["env_py_exists"] = True
                results["details"].append("✅ Archivo env.py encontrado")
                results["score"] += 2
            else:
                results["errors"].append("❌ Archivo alembic/env.py no encontrado")
            
            # Verificar carpeta versions/
            versions_folder = alembic_folder / "versions"
            if versions_folder.exists() and versions_folder.is_dir():
                results["versions_folder_exists"] = True
                results["details"].append("✅ Carpeta alembic/versions/ encontrada")
                results["score"] += 2
                
                # Verificar archivos de migración
                migration_files = list(versions_folder.glob("*.py"))
                if migration_files:
                    results["has_migration_files"] = True
                    results["details"].append(f"✅ {len(migration_files)} archivo(s) de migración encontrado(s)")
                    results["score"] += 3
                else:
                    results["errors"].append("❌ No se encontraron archivos de migración en versions/")
            else:
                results["errors"].append("❌ Carpeta alembic/versions/ no encontrada")
        else:
            results["errors"].append("❌ Carpeta alembic/ no encontrada")
        
        # Verificar requirements.txt
        requirements_file = repo_path / "requirements.txt"
        if requirements_file.exists():
            try:
                content = requirements_file.read_text()
                if re.search(r'alembic', content, re.IGNORECASE):
                    results["alembic_in_requirements"] = True
                    results["details"].append("✅ Alembic encontrado en requirements.txt")
                    results["score"] += 2
                else:
                    results["errors"].append("❌ Alembic no encontrado en requirements.txt")
            except Exception as e:
                results["errors"].append(f"❌ Error leyendo requirements.txt: {str(e)}")
        else:
            results["errors"].append("❌ Archivo requirements.txt no encontrado")
        
        # Máximo 12 puntos para este check
        results["score"] = min(results["score"], 12)
        
    except Exception as e:
        results["errors"].append(f"❌ Error verificando Alembic: {str(e)}")
    
    return results


def get_alembic_score(repo_path: str) -> float:
    """Obtiene el score de Alembic (0-12 puntos)"""
    result = check_alembic_migrations(repo_path)
    return result["score"]


def get_alembic_feedback(repo_path: str) -> list:
    """Obtiene feedback específico para Alembic"""
    result = check_alembic_migrations(repo_path)
    feedback = []
    
    if result["errors"]:
        for error in result["errors"]:
            feedback.append(error)
    
    if not result["alembic_ini_exists"]:
        feedback.append("• Ejecutar 'alembic init alembic' para configurar Alembic")
    
    if not result["alembic_in_requirements"]:
        feedback.append("• Agregar 'alembic' a requirements.txt")
    
    if not result["has_migration_files"]:
        feedback.append("• Crear al menos una migración con 'alembic revision --autogenerate -m \"initial\"'")
    
    return feedback
