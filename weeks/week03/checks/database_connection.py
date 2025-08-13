"""
Verificaciones de database connection específicas para Week 3
"""
import ast
import re
from pathlib import Path
from typing import Dict, Any, List


def check_database_connection(repo_path: str) -> Dict[str, Any]:
    """
    Verifica database connection para Week 3
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de database connection
    """
    repo_root = Path(repo_path)
    results = {
        "passed": False,
        "score": 0,
        "feedback": [],
        "details": {
            "connection_setup": False,
            "session_management": False,
            "engine_configuration": False,
            "database_url": False
        }
    }
    
    # Buscar archivos Python relevantes
    python_files = list(repo_root.glob("**/*.py"))
    
    # Patrones para detectar configuración de base de datos
    connection_patterns = [
        r"create_engine\s*\(",
        r"engine\s*=",
        r"DATABASE_URL",
        r"SQLALCHEMY_DATABASE_URL",
        r"sqlite://",
        r"postgresql://",
        r"mysql://"
    ]
    
    session_patterns = [
        r"sessionmaker\s*\(",
        r"Session\s*\(",
        r"get_db\s*\(",
        r"SessionLocal",
        r"@contextmanager"
    ]
    
    engine_patterns = [
        r"create_engine\s*\(",
        r"pool_size\s*=",
        r"max_overflow\s*=",
        r"pool_pre_ping\s*="
    ]
    
    try:
        for py_file in python_files:
            if py_file.name.startswith('.') or '__pycache__' in str(py_file):
                continue
                
            try:
                content = py_file.read_text(encoding='utf-8')
                
                # Verificar configuración de conexión
                for pattern in connection_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["details"]["connection_setup"] = True
                        break
                
                # Verificar manejo de sesiones
                for pattern in session_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["details"]["session_management"] = True
                        break
                
                # Verificar configuración de engine
                for pattern in engine_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["details"]["engine_configuration"] = True
                        break
                
                # Verificar URL de base de datos
                if re.search(r"(sqlite://|postgresql://|mysql://)", content, re.IGNORECASE):
                    results["details"]["database_url"] = True
                
            except Exception as e:
                continue
    
    except Exception as e:
        results["feedback"].append(f"Error al analizar archivos: {str(e)}")
        return results
    
    # Evaluar resultados
    score = 0
    
    if results["details"]["connection_setup"]:
        score += 3
    else:
        results["feedback"].append("• Configura la conexión a la base de datos usando create_engine()")
    
    if results["details"]["session_management"]:
        score += 3
    else:
        results["feedback"].append("• Implementa manejo de sesiones con sessionmaker() o Session()")
    
    if results["details"]["engine_configuration"]:
        score += 2
    else:
        results["feedback"].append("• Configura el engine de SQLAlchemy apropiadamente")
    
    if results["details"]["database_url"]:
        score += 2
    else:
        results["feedback"].append("• Define una URL de base de datos válida (sqlite://, postgresql://, etc.)")
    
    results["score"] = score
    results["passed"] = score >= 6  # Pasa si tiene al menos conexión básica y sesiones
    
    if results["passed"]:
        results["feedback"].insert(0, "✓ Configuración de base de datos implementada correctamente")
    
    return results


def get_database_connection_recommendations(repo_path: str) -> List[str]:
    """
    Genera recomendaciones específicas para database connection
    """
    return [
        "Usa create_engine() para crear la conexión a la base de datos",
        "Implementa sessionmaker() para manejo de sesiones",
        "Define una DATABASE_URL o SQLALCHEMY_DATABASE_URL",
        "Considera usar dependency injection para get_db()",
        "Configura pool_size y pool_pre_ping para producción"
    ]
