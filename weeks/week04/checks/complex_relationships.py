"""
Check para verificar relaciones complejas entre modelos SQLAlchemy
"""
import re
from pathlib import Path
from typing import Dict, Any, List


def check_complex_relationships(repo_path: str) -> Dict[str, Any]:
    """
    Verifica relaciones complejas entre modelos SQLAlchemy
    """
    results = {
        "has_relationships": False,
        "has_foreign_keys": False,
        "has_many_to_many": False,
        "has_one_to_many": False,
        "has_back_populates": False,
        "models_organized": False,
        "score": 0,
        "details": [],
        "errors": [],
        "relationship_count": 0,
        "foreign_key_count": 0
    }
    
    try:
        repo_path = Path(repo_path)
        
        # Buscar archivos Python que podrían contener modelos
        python_files = []
        
        # Buscar en models/ si existe
        models_dir = repo_path / "models"
        if models_dir.exists():
            results["models_organized"] = True
            results["details"].append("✅ Modelos organizados en carpeta models/")
            results["score"] += 2
            python_files.extend(models_dir.glob("*.py"))
        
        # También buscar en archivos principales
        for pattern in ["main.py", "models.py", "database.py", "app.py"]:
            file_path = repo_path / pattern
            if file_path.exists():
                python_files.append(file_path)
        
        # Buscar recursivamente archivos .py
        for py_file in repo_path.rglob("*.py"):
            if "venv" not in str(py_file) and "__pycache__" not in str(py_file):
                python_files.append(py_file)
        
        # Remover duplicados
        python_files = list(set(python_files))
        
        # Analizar archivos
        relationship_patterns = [
            r'relationship\s*\(',
            r'\.relationship\s*\(',
            r'from\s+sqlalchemy\.orm\s+import.*relationship'
        ]
        
        foreign_key_patterns = [
            r'ForeignKey\s*\(',
            r'\.ForeignKey\s*\(',
            r'foreign_key\s*=',
            r'Column\s*\([^)]*ForeignKey'
        ]
        
        many_to_many_patterns = [
            r'secondary\s*=',
            r'Table\s*\(',
            r'association_table',
            r'many.*many'
        ]
        
        back_populates_patterns = [
            r'back_populates\s*=',
            r'backref\s*='
        ]
        
        for py_file in python_files:
            try:
                content = py_file.read_text(encoding='utf-8')
                
                # Verificar relationships
                for pattern in relationship_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        results["has_relationships"] = True
                        results["relationship_count"] += len(matches)
                
                # Verificar foreign keys
                for pattern in foreign_key_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    if matches:
                        results["has_foreign_keys"] = True
                        results["foreign_key_count"] += len(matches)
                
                # Verificar many-to-many
                for pattern in many_to_many_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["has_many_to_many"] = True
                        break
                
                # Verificar back_populates
                for pattern in back_populates_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["has_back_populates"] = True
                        break
                
                # Detectar one-to-many (heurística)
                if re.search(r'relationship.*list|relationship.*List|\[\s*["\'].*["\']\s*\]', content, re.IGNORECASE):
                    results["has_one_to_many"] = True
                
            except Exception as e:
                results["errors"].append(f"❌ Error leyendo {py_file.name}: {str(e)}")
        
        # Calcular score basado en hallazgos
        if results["has_relationships"]:
            results["details"].append(f"✅ {results['relationship_count']} relación(es) encontrada(s)")
            results["score"] += 3
        else:
            results["errors"].append("❌ No se encontraron definiciones de relationships")
        
        if results["has_foreign_keys"]:
            results["details"].append(f"✅ {results['foreign_key_count']} foreign key(s) encontrada(s)")
            results["score"] += 2
        else:
            results["errors"].append("❌ No se encontraron foreign keys")
        
        if results["has_many_to_many"]:
            results["details"].append("✅ Relaciones many-to-many implementadas")
            results["score"] += 3
        else:
            results["errors"].append("❌ No se encontraron relaciones many-to-many")
        
        if results["has_one_to_many"]:
            results["details"].append("✅ Relaciones one-to-many implementadas")
            results["score"] += 2
        else:
            results["errors"].append("❌ No se encontraron relaciones one-to-many")
        
        if results["has_back_populates"]:
            results["details"].append("✅ back_populates o backref configurado")
            results["score"] += 1
        
        # Máximo 10 puntos para este check
        results["score"] = min(results["score"], 10)
        
    except Exception as e:
        results["errors"].append(f"❌ Error verificando relaciones: {str(e)}")
    
    return results


def get_relationships_score(repo_path: str) -> float:
    """Obtiene el score de relaciones complejas (0-10 puntos)"""
    result = check_complex_relationships(repo_path)
    return result["score"]


def get_relationships_feedback(repo_path: str) -> List[str]:
    """Obtiene feedback específico para relaciones"""
    result = check_complex_relationships(repo_path)
    feedback = []
    
    if result["errors"]:
        for error in result["errors"]:
            feedback.append(error)
    
    if not result["has_relationships"]:
        feedback.append("• Implementar relaciones entre modelos usando relationship()")
    
    if not result["has_foreign_keys"]:
        feedback.append("• Agregar ForeignKey en columnas para relaciones")
    
    if not result["has_many_to_many"]:
        feedback.append("• Implementar al menos una relación many-to-many con tabla association")
    
    if not result["has_one_to_many"]:
        feedback.append("• Implementar relaciones one-to-many entre modelos")
    
    if not result["models_organized"]:
        feedback.append("• Organizar modelos en carpeta models/ separada")
    
    return feedback
