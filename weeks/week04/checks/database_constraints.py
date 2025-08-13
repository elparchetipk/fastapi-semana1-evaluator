"""
Check para verificar constraints, índices y validaciones de base de datos
"""
import re
from pathlib import Path
from typing import Dict, Any, List


def check_database_constraints(repo_path: str) -> Dict[str, Any]:
    """
    Verifica constraints, índices y validaciones en la base de datos
    """
    results = {
        "has_constraints": False,
        "has_indexes": False,
        "has_unique_constraints": False,
        "has_check_constraints": False,
        "has_validations": False,
        "score": 0,
        "details": [],
        "errors": [],
        "constraint_count": 0,
        "index_count": 0
    }
    
    try:
        repo_path = Path(repo_path)
        
        # Buscar archivos Python
        python_files = []
        for py_file in repo_path.rglob("*.py"):
            if "venv" not in str(py_file) and "__pycache__" not in str(py_file):
                python_files.append(py_file)
        
        # Patrones para detectar constraints
        constraint_patterns = [
            r'CheckConstraint\s*\(',
            r'UniqueConstraint\s*\(',
            r'ForeignKeyConstraint\s*\(',
            r'PrimaryKeyConstraint\s*\('
        ]
        
        # Patrones para detectar índices
        index_patterns = [
            r'Index\s*\(',
            r'index\s*=\s*True',
            r'unique\s*=\s*True',
            r'__table_args__.*Index'
        ]
        
        # Patrones para validaciones
        validation_patterns = [
            r'validates\s*\(',
            r'@validates',
            r'validator\s*\(',
            r'@validator',
            r'validate_'
        ]
        
        # Patrones para unique constraints
        unique_patterns = [
            r'unique\s*=\s*True',
            r'UniqueConstraint',
            r'unique_together'
        ]
        
        # Patrones para check constraints
        check_patterns = [
            r'CheckConstraint',
            r'check\s*=',
            r'CheckConstraint\s*\([^)]*text'
        ]
        
        for py_file in python_files:
            try:
                content = py_file.read_text(encoding='utf-8')
                
                # Verificar constraints generales
                for pattern in constraint_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        results["has_constraints"] = True
                        results["constraint_count"] += len(matches)
                
                # Verificar índices
                for pattern in index_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        results["has_indexes"] = True
                        results["index_count"] += len(matches)
                
                # Verificar unique constraints
                for pattern in unique_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["has_unique_constraints"] = True
                        break
                
                # Verificar check constraints
                for pattern in check_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["has_check_constraints"] = True
                        break
                
                # Verificar validaciones
                for pattern in validation_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["has_validations"] = True
                        break
                
            except Exception as e:
                results["errors"].append(f"❌ Error leyendo {py_file.name}: {str(e)}")
        
        # Calcular score basado en hallazgos
        if results["has_constraints"] or results["constraint_count"] > 0:
            results["details"].append(f"✅ {results['constraint_count']} constraint(s) encontrado(s)")
            results["score"] += 2
        else:
            results["errors"].append("❌ No se encontraron constraints de base de datos")
        
        if results["has_indexes"] or results["index_count"] > 0:
            results["details"].append(f"✅ {results['index_count']} índice(s) encontrado(s)")
            results["score"] += 2
        else:
            results["errors"].append("❌ No se encontraron índices de base de datos")
        
        if results["has_unique_constraints"]:
            results["details"].append("✅ Constraints UNIQUE implementados")
            results["score"] += 2
        else:
            results["errors"].append("❌ No se encontraron constraints UNIQUE")
        
        if results["has_check_constraints"]:
            results["details"].append("✅ Check constraints implementados")
            results["score"] += 1
        
        if results["has_validations"]:
            results["details"].append("✅ Validaciones de modelo implementadas")
            results["score"] += 1
        else:
            results["errors"].append("❌ No se encontraron validaciones de modelo")
        
        # Máximo 8 puntos para este check
        results["score"] = min(results["score"], 8)
        
    except Exception as e:
        results["errors"].append(f"❌ Error verificando constraints: {str(e)}")
    
    return results


def get_database_constraints_score(repo_path: str) -> float:
    """Obtiene el score de constraints y validaciones (0-8 puntos)"""
    result = check_database_constraints(repo_path)
    return result["score"]


def get_database_constraints_feedback(repo_path: str) -> List[str]:
    """Obtiene feedback específico para constraints"""
    result = check_database_constraints(repo_path)
    feedback = []
    
    if result["errors"]:
        for error in result["errors"]:
            feedback.append(error)
    
    if not result["has_constraints"] and result["constraint_count"] == 0:
        feedback.append("• Implementar constraints de base de datos (UniqueConstraint, CheckConstraint)")
    
    if not result["has_indexes"] and result["index_count"] == 0:
        feedback.append("• Agregar índices en campos relevantes (index=True, Index())")
    
    if not result["has_unique_constraints"]:
        feedback.append("• Implementar constraints UNIQUE para campos únicos")
    
    if not result["has_validations"]:
        feedback.append("• Agregar validaciones de modelo (@validates, @validator)")
    
    if not result["has_check_constraints"]:
        feedback.append("• Considerar implementar check constraints para validaciones complejas")
    
    return feedback
