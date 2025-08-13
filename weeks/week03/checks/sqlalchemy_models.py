"""
Verificaciones de sqlalchemy models específicas para Week 3
"""
import ast
import re
from pathlib import Path
from typing import Dict, Any, List


def check_sqlalchemy_models(repo_path: str) -> Dict[str, Any]:
    """
    Verifica sqlalchemy models para Week 3
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de sqlalchemy models
    """
    repo_root = Path(repo_path)
    results = {
        "passed": False,
        "score": 0,
        "feedback": [],
        "details": {
            "models_defined": False,
            "base_model": False,
            "columns_defined": False,
            "relationships": False,
            "constraints": False,
            "table_names": [],
            "model_classes": []
        }
    }
    
    # Buscar archivos Python relevantes
    python_files = list(repo_root.glob("**/*.py"))
    
    # Patrones para detectar modelos SQLAlchemy
    base_patterns = [
        r"declarative_base\s*\(",
        r"from\s+sqlalchemy\.ext\.declarative\s+import\s+declarative_base",
        r"from\s+sqlalchemy\.orm\s+import\s+declarative_base",
        r"Base\s*=\s*declarative_base"
    ]
    
    column_patterns = [
        r"Column\s*\(",
        r"from\s+sqlalchemy\s+import.*Column",
        r"Integer\s*\(",
        r"String\s*\(",
        r"ForeignKey\s*\(",
        r"relationship\s*\("
    ]
    
    constraint_patterns = [
        r"nullable\s*=\s*False",
        r"unique\s*=\s*True",
        r"primary_key\s*=\s*True",
        r"index\s*=\s*True",
        r"CheckConstraint",
        r"UniqueConstraint"
    ]
    
    try:
        for py_file in python_files:
            if py_file.name.startswith('.') or '__pycache__' in str(py_file):
                continue
                
            try:
                content = py_file.read_text(encoding='utf-8')
                
                # Verificar Base declarativo
                for pattern in base_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["details"]["base_model"] = True
                        break
                
                # Verificar definición de columnas
                for pattern in column_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["details"]["columns_defined"] = True
                        break
                
                # Verificar restricciones
                for pattern in constraint_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["details"]["constraints"] = True
                        break
                
                # Verificar relaciones
                if re.search(r"relationship\s*\(", content, re.IGNORECASE):
                    results["details"]["relationships"] = True
                
                # Buscar clases que heredan de Base
                try:
                    tree = ast.parse(content)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            # Verificar si hereda de Base o tiene __tablename__
                            has_tablename = any(
                                isinstance(child, ast.Assign) and
                                any(target.id == "__tablename__" for target in child.targets if isinstance(target, ast.Name))
                                for child in node.body
                            )
                            
                            if has_tablename or any(
                                isinstance(base, ast.Name) and base.id == "Base"
                                for base in node.bases
                            ):
                                results["details"]["model_classes"].append(node.name)
                                results["details"]["models_defined"] = True
                                
                                # Buscar __tablename__
                                for child in node.body:
                                    if (isinstance(child, ast.Assign) and 
                                        any(target.id == "__tablename__" for target in child.targets if isinstance(target, ast.Name))):
                                        if isinstance(child.value, ast.Constant):
                                            results["details"]["table_names"].append(child.value.value)
                
                except SyntaxError:
                    continue
                    
            except Exception as e:
                continue
    
    except Exception as e:
        results["feedback"].append(f"Error al analizar archivos: {str(e)}")
        return results
    
    # Evaluar resultados
    score = 0
    
    if results["details"]["base_model"]:
        score += 2
    else:
        results["feedback"].append("• Define Base = declarative_base() para los modelos")
    
    if results["details"]["models_defined"]:
        score += 3
    else:
        results["feedback"].append("• Define al menos una clase modelo que herede de Base")
    
    if results["details"]["columns_defined"]:
        score += 2
    else:
        results["feedback"].append("• Define columnas usando Column() en los modelos")
    
    if results["details"]["relationships"]:
        score += 2
    else:
        results["feedback"].append("• Implementa relaciones entre modelos usando relationship()")
    
    if results["details"]["constraints"]:
        score += 1
    else:
        results["feedback"].append("• Agrega restricciones como nullable=False, unique=True, etc.")
    
    results["score"] = score
    results["passed"] = score >= 6  # Pasa si tiene base + modelos + columnas
    
    if results["passed"]:
        results["feedback"].insert(0, f"✓ Modelos SQLAlchemy definidos: {', '.join(results['details']['model_classes'])}")
    
    return results


def get_sqlalchemy_models_recommendations(repo_path: str) -> List[str]:
    """
    Genera recomendaciones específicas para sqlalchemy models
    """
    return [
        "Define Base = declarative_base() como base para los modelos",
        "Crea clases modelo que hereden de Base",
        "Define __tablename__ en cada modelo",
        "Usa Column() para definir columnas con tipos apropiados",
        "Implementa relaciones con relationship() y ForeignKey()",
        "Agrega restricciones como nullable, unique, primary_key",
        "Considera usar constraints como CheckConstraint para validaciones"
    ]
