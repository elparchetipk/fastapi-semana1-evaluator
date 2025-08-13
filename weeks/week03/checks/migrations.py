"""
Verificaciones de migrations específicas para Week 3
"""
import re
from pathlib import Path
from typing import Dict, Any, List


def check_migrations(repo_path: str) -> Dict[str, Any]:
    """
    Verifica migrations para Week 3
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de migrations
    """
    repo_root = Path(repo_path)
    results = {
        "passed": False,
        "score": 0,
        "feedback": [],
        "details": {
            "create_tables": False,
            "alembic_present": False,
            "migration_files": False,
            "database_initialization": False,
            "migration_patterns": []
        }
    }
    
    # Buscar archivos Python relevantes
    python_files = list(repo_root.glob("**/*.py"))
    
    # Verificar si existe alembic
    alembic_dir = repo_root / "alembic"
    alembic_ini = repo_root / "alembic.ini"
    
    if alembic_dir.exists() or alembic_ini.exists():
        results["details"]["alembic_present"] = True
    
    # Buscar archivos de migración
    migration_files = list(repo_root.glob("**/versions/*.py")) or list(repo_root.glob("**/migrations/*.py"))
    if migration_files:
        results["details"]["migration_files"] = True
    
    # Patrones para detectar creación de tablas
    create_table_patterns = [
        r"Base\.metadata\.create_all\s*\(",
        r"\.create_all\s*\(",
        r"engine\.execute\s*\(",
        r"CREATE TABLE",
        r"create_table\s*\(",
        r"op\.create_table\s*\("
    ]
    
    # Patrones de inicialización de BD
    init_patterns = [
        r"Base\.metadata\.create_all",
        r"metadata\.create_all",
        r"init_db\s*\(",
        r"create_database\s*\(",
        r"setup_database\s*\("
    ]
    
    try:
        for py_file in python_files:
            if py_file.name.startswith('.') or '__pycache__' in str(py_file):
                continue
                
            try:
                content = py_file.read_text(encoding='utf-8')
                
                # Verificar creación de tablas
                for pattern in create_table_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["details"]["create_tables"] = True
                        results["details"]["migration_patterns"].append(f"Table creation found in {py_file.name}")
                        break
                
                # Verificar inicialización de BD
                for pattern in init_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["details"]["database_initialization"] = True
                        results["details"]["migration_patterns"].append(f"DB initialization found in {py_file.name}")
                        break
                        
            except Exception as e:
                continue
    
    except Exception as e:
        results["feedback"].append(f"Error al analizar archivos: {str(e)}")
        return results
    
    # Evaluar resultados (este es un criterio opcional en Week 3)
    score = 0
    
    if results["details"]["alembic_present"]:
        score += 2
        results["feedback"].append("✓ Alembic configurado para migraciones")
    
    if results["details"]["migration_files"]:
        score += 2
        results["feedback"].append("✓ Archivos de migración encontrados")
    
    if results["details"]["create_tables"]:
        score += 1
        results["feedback"].append("✓ Creación de tablas implementada")
    
    if results["details"]["database_initialization"]:
        score += 1
        results["feedback"].append("✓ Inicialización de base de datos implementada")
    else:
        results["feedback"].append("• Considera implementar Base.metadata.create_all() para inicializar la BD")
    
    # Para migraciones, es suficiente con tener inicialización básica
    if not results["details"]["create_tables"] and not results["details"]["alembic_present"]:
        results["feedback"].append("• Implementa creación de tablas o configura Alembic para migraciones")
    
    results["score"] = score
    results["passed"] = score >= 1  # Pasa con cualquier tipo de inicialización
    
    return results


def get_migrations_recommendations(repo_path: str) -> List[str]:
    """
    Genera recomendaciones específicas para migrations
    """
    return [
        "Usa Base.metadata.create_all() para crear tablas automáticamente",
        "Considera configurar Alembic para migraciones más robustas",
        "Implementa una función init_db() para inicialización",
        "Crea scripts de inicialización de base de datos",
        "Documenta el proceso de setup de la base de datos en README"
    ]
