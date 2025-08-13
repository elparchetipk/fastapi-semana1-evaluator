"""
Verificaciones de crud operations específicas para Week 3
"""
import ast
import re
from pathlib import Path
from typing import Dict, Any, List


def check_crud_operations(repo_path: str) -> Dict[str, Any]:
    """
    Verifica crud operations para Week 3
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de crud operations
    """
    repo_root = Path(repo_path)
    results = {
        "passed": False,
        "score": 0,
        "feedback": [],
        "details": {
            "create_operations": False,
            "read_operations": False,
            "update_operations": False,
            "delete_operations": False,
            "database_queries": False,
            "endpoints_found": [],
            "crud_patterns": []
        }
    }
    
    # Buscar archivos Python relevantes
    python_files = list(repo_root.glob("**/*.py"))
    
    # Patrones para detectar operaciones CRUD
    create_patterns = [
        r"@app\.post\s*\(",
        r"@router\.post\s*\(",
        r"\.add\s*\(",
        r"session\.add\s*\(",
        r"db\.add\s*\(",
        r"commit\s*\(\)",
        r"session\.commit\s*\(\)"
    ]
    
    read_patterns = [
        r"@app\.get\s*\(",
        r"@router\.get\s*\(",
        r"\.query\s*\(",
        r"session\.query\s*\(",
        r"db\.query\s*\(",
        r"\.filter\s*\(",
        r"\.first\s*\(\)",
        r"\.all\s*\(\)"
    ]
    
    update_patterns = [
        r"@app\.put\s*\(",
        r"@router\.put\s*\(",
        r"@app\.patch\s*\(",
        r"@router\.patch\s*\(",
        r"\.update\s*\(",
        r"session\.merge\s*\(",
        r"db\.merge\s*\("
    ]
    
    delete_patterns = [
        r"@app\.delete\s*\(",
        r"@router\.delete\s*\(",
        r"\.delete\s*\(",
        r"session\.delete\s*\(",
        r"db\.delete\s*\("
    ]
    
    db_query_patterns = [
        r"session\.",
        r"db\.",
        r"\.query\(",
        r"\.filter\(",
        r"\.join\(",
        r"select\s*\(",
        r"insert\s*\(",
        r"update\s*\(",
        r"delete\s*\("
    ]
    
    try:
        for py_file in python_files:
            if py_file.name.startswith('.') or '__pycache__' in str(py_file):
                continue
                
            try:
                content = py_file.read_text(encoding='utf-8')
                
                # Verificar operaciones CREATE
                for pattern in create_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["details"]["create_operations"] = True
                        results["details"]["crud_patterns"].append(f"CREATE pattern found in {py_file.name}")
                        break
                
                # Verificar operaciones READ
                for pattern in read_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["details"]["read_operations"] = True
                        results["details"]["crud_patterns"].append(f"READ pattern found in {py_file.name}")
                        break
                
                # Verificar operaciones UPDATE
                for pattern in update_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["details"]["update_operations"] = True
                        results["details"]["crud_patterns"].append(f"UPDATE pattern found in {py_file.name}")
                        break
                
                # Verificar operaciones DELETE
                for pattern in delete_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["details"]["delete_operations"] = True
                        results["details"]["crud_patterns"].append(f"DELETE pattern found in {py_file.name}")
                        break
                
                # Verificar consultas de base de datos
                for pattern in db_query_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["details"]["database_queries"] = True
                        break
                
                # Buscar endpoints FastAPI
                endpoints = re.findall(r"@(app|router)\.(get|post|put|patch|delete)\s*\(\s*[\"']([^\"']+)[\"']", content, re.IGNORECASE)
                for match in endpoints:
                    method, _, path = match
                    results["details"]["endpoints_found"].append(f"{method.upper()} {path}")
                    
            except Exception as e:
                continue
    
    except Exception as e:
        results["feedback"].append(f"Error al analizar archivos: {str(e)}")
        return results
    
    # Evaluar resultados
    score = 0
    
    if results["details"]["create_operations"]:
        score += 2.5
    else:
        results["feedback"].append("• Implementa operaciones CREATE (POST) con persistencia en BD")
    
    if results["details"]["read_operations"]:
        score += 2.5
    else:
        results["feedback"].append("• Implementa operaciones READ (GET) consultando la BD")
    
    if results["details"]["update_operations"]:
        score += 2.5
    else:
        results["feedback"].append("• Implementa operaciones UPDATE (PUT/PATCH) actualizando la BD")
    
    if results["details"]["delete_operations"]:
        score += 2.5
    else:
        results["feedback"].append("• Implementa operaciones DELETE eliminando de la BD")
    
    results["score"] = score
    results["passed"] = score >= 7  # Pasa si tiene al menos 3 de las 4 operaciones
    
    if results["passed"]:
        operations_count = sum([
            results["details"]["create_operations"],
            results["details"]["read_operations"],
            results["details"]["update_operations"],
            results["details"]["delete_operations"]
        ])
        results["feedback"].insert(0, f"✓ Operaciones CRUD implementadas: {operations_count}/4")
    
    return results


def get_crud_operations_recommendations(repo_path: str) -> List[str]:
    """
    Genera recomendaciones específicas para crud operations
    """
    return [
        "Implementa endpoints POST para crear registros en la BD",
        "Implementa endpoints GET para consultar datos de la BD",
        "Implementa endpoints PUT/PATCH para actualizar registros",
        "Implementa endpoints DELETE para eliminar registros",
        "Usa session.add() y session.commit() para persistir datos",
        "Usa session.query() para consultar datos",
        "Maneja errores de base de datos apropiadamente",
        "Considera usar dependency injection para get_db()"
    ]
