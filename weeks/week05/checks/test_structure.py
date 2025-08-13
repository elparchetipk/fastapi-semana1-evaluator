"""
Verificaciones de estructura de tests para Week 5
"""
import sys
from pathlib import Path
from typing import Dict, Any, List
import ast


def check_test_structure(repo_path: str) -> Dict[str, Any]:
    """
    Verifica la estructura organizada de tests
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de estructura de tests
    """
    repo_root = Path(repo_path)
    tests_dir = repo_root / 'tests'
    
    if not tests_dir.exists():
        return {
            "tests_directory_exists": False,
            "test_files": [],
            "structure_score": 0,
            "score": 0,
            "max_score": 8,
            "recommendations": ["Crear directorio 'tests/' para organizar tests"]
        }
    
    # Buscar archivos de test
    test_files = []
    test_files.extend(list(tests_dir.glob('test_*.py')))
    test_files.extend(list(tests_dir.glob('*_test.py')))
    test_files.extend(list(tests_dir.rglob('test_*.py')))
    test_files.extend(list(tests_dir.rglob('*_test.py')))
    
    # Remover duplicados
    test_files = list(set(test_files))
    
    structure_analysis = {
        "conftest_exists": (tests_dir / 'conftest.py').exists(),
        "init_exists": (tests_dir / '__init__.py').exists(),
        "subdirectories": [],
        "test_categories": set()
    }
    
    # Analizar subdirectorios
    for item in tests_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            structure_analysis["subdirectories"].append(item.name)
    
    # Analizar categorías de tests basadas en nombres
    test_function_count = 0
    for test_file in test_files:
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)
                
                # Contar funciones de test
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                        test_function_count += 1
                        
                        # Categorizar tests por nombre
                        if 'unit' in test_file.name or 'model' in node.name or 'util' in node.name:
                            structure_analysis["test_categories"].add('unit')
                        elif 'integration' in test_file.name or 'api' in node.name or 'endpoint' in node.name:
                            structure_analysis["test_categories"].add('integration')
                        elif 'db' in node.name or 'database' in node.name:
                            structure_analysis["test_categories"].add('database')
                            
        except Exception as e:
            continue
    
    # Calcular puntuación basada en estructura
    score = 0
    
    # Puntos por archivos de test existentes
    if test_files:
        score += 3
    
    # Puntos por conftest.py
    if structure_analysis["conftest_exists"]:
        score += 2
    
    # Puntos por organización en subdirectorios o categorías claras
    if structure_analysis["subdirectories"] or len(structure_analysis["test_categories"]) >= 2:
        score += 2
    
    # Puntos por cantidad de tests
    if test_function_count >= 5:
        score += 1
    
    recommendations = []
    if not test_files:
        recommendations.append("Crear archivos de test (test_*.py)")
    if not structure_analysis["conftest_exists"]:
        recommendations.append("Crear tests/conftest.py para configuración compartida")
    if len(structure_analysis["test_categories"]) < 2:
        recommendations.append("Organizar tests en categorías (unit, integration, etc.)")
    if test_function_count < 5:
        recommendations.append("Implementar más funciones de test")
    
    return {
        "tests_directory_exists": True,
        "test_files": [str(f.relative_to(repo_root)) for f in test_files],
        "test_function_count": test_function_count,
        "structure_analysis": {
            **structure_analysis,
            "test_categories": list(structure_analysis["test_categories"])
        },
        "score": min(score, 8),
        "max_score": 8,
        "recommendations": recommendations
    }


def get_test_structure_recommendations(repo_path: str) -> List[str]:
    """
    Genera recomendaciones específicas para estructura de tests
    """
    return [
        "Organizar tests en el directorio 'tests/'",
        "Crear tests/conftest.py para fixtures compartidas",
        "Separar tests unitarios de tests de integración",
        "Usar nomenclatura clara: test_*.py o *_test.py",
        "Organizar en subdirectorios por módulo o funcionalidad"
    ]
