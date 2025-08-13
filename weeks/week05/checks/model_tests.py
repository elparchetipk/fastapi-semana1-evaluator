"""
Verificaciones de tests de modelos para Week 5
"""
import sys
from pathlib import Path
from typing import Dict, Any, List
import ast
import re


def check_model_tests(repo_path: str) -> Dict[str, Any]:
    """
    Verifica los tests de modelos Pydantic y SQLAlchemy
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de tests de modelos
    """
    repo_root = Path(repo_path)
    tests_dir = repo_root / 'tests'
    
    if not tests_dir.exists():
        return {
            "tests_directory_exists": False,
            "model_test_files": [],
            "model_test_functions": 0,
            "pydantic_tests": 0,
            "sqlalchemy_tests": 0,
            "score": 0,
            "max_score": 8,
            "recommendations": ["Crear directorio 'tests/' y agregar tests de modelos"]
        }
    
    # Buscar archivos de test de modelos
    model_test_files = []
    model_test_patterns = [
        'test*model*.py',
        'test*schema*.py', 
        '*model*test*.py',
        '*schema*test*.py'
    ]
    
    for pattern in model_test_patterns:
        model_test_files.extend(list(tests_dir.glob(pattern)))
        model_test_files.extend(list(tests_dir.rglob(pattern)))
    
    # Remover duplicados
    model_test_files = list(set(model_test_files))
    
    test_analysis = {
        "pydantic_tests": 0,
        "sqlalchemy_tests": 0,
        "validation_tests": 0,
        "serialization_tests": 0,
        "relationship_tests": 0
    }
    
    total_model_test_functions = 0
    
    # Analizar contenido de archivos de test
    for test_file in model_test_files:
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)
                
                # Contar funciones de test
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                        total_model_test_functions += 1
                        
                        # Categorizar tests por contenido
                        func_content = ast.get_source_segment(content, node) or ""
                        func_content_lower = func_content.lower()
                        
                        # Tests de Pydantic
                        if any(term in func_content_lower for term in ['pydantic', 'basemodel', 'validation', 'validator']):
                            test_analysis["pydantic_tests"] += 1
                        
                        # Tests de SQLAlchemy  
                        if any(term in func_content_lower for term in ['sqlalchemy', 'session', 'query', 'model', 'table']):
                            test_analysis["sqlalchemy_tests"] += 1
                            
                        # Tests de validación
                        if any(term in func_content_lower for term in ['valid', 'invalid', 'error', 'exception']):
                            test_analysis["validation_tests"] += 1
                            
                        # Tests de serialización
                        if any(term in func_content_lower for term in ['json', 'dict', 'serialize', 'parse']):
                            test_analysis["serialization_tests"] += 1
                            
                        # Tests de relaciones
                        if any(term in func_content_lower for term in ['relationship', 'foreign', 'join']):
                            test_analysis["relationship_tests"] += 1
                            
        except Exception as e:
            continue
    
    # También buscar en archivos de test generales
    general_test_files = list(tests_dir.glob('test*.py'))
    for test_file in general_test_files:
        if test_file not in model_test_files:
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Buscar funciones de test de modelos en archivos generales
                    if re.search(r'def test.*model', content.lower()) or re.search(r'def test.*schema', content.lower()):
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                                func_content = ast.get_source_segment(content, node) or ""
                                if any(term in func_content.lower() for term in ['model', 'schema', 'pydantic', 'sqlalchemy']):
                                    total_model_test_functions += 1
                                    if 'pydantic' in func_content.lower():
                                        test_analysis["pydantic_tests"] += 1
                                    if 'sqlalchemy' in func_content.lower():
                                        test_analysis["sqlalchemy_tests"] += 1
            except Exception as e:
                continue
    
    # Calcular puntuación
    score = 0
    
    # Puntos por tener archivos de test de modelos
    if model_test_files or total_model_test_functions > 0:
        score += 2
    
    # Puntos por cantidad de tests
    if total_model_test_functions >= 3:
        score += 2
    elif total_model_test_functions >= 1:
        score += 1
    
    # Puntos por tests de Pydantic
    if test_analysis["pydantic_tests"] >= 2:
        score += 2
    elif test_analysis["pydantic_tests"] >= 1:
        score += 1
    
    # Puntos por tests de SQLAlchemy
    if test_analysis["sqlalchemy_tests"] >= 2:
        score += 2
    elif test_analysis["sqlalchemy_tests"] >= 1:
        score += 1
    
    # Bonus por variedad de tests
    test_types = sum(1 for count in test_analysis.values() if count > 0)
    if test_types >= 3:
        score += 1
    
    recommendations = []
    if total_model_test_functions == 0:
        recommendations.append("Crear tests para modelos Pydantic y SQLAlchemy")
    
    if test_analysis["pydantic_tests"] == 0:
        recommendations.append("Agregar tests de validación para modelos Pydantic")
        
    if test_analysis["sqlalchemy_tests"] == 0:
        recommendations.append("Agregar tests para modelos SQLAlchemy")
        
    if test_analysis["validation_tests"] == 0:
        recommendations.append("Agregar tests de validación de datos")
    
    return {
        "tests_directory_exists": True,
        "model_test_files": [str(f.relative_to(repo_root)) for f in model_test_files],
        "model_test_functions": total_model_test_functions,
        "test_analysis": test_analysis,
        "score": min(score, 8),
        "max_score": 8,
        "recommendations": recommendations
    }


def get_model_tests_recommendations(repo_path: str) -> List[str]:
    """
    Genera recomendaciones específicas para tests de modelos
    """
    return [
        "Crear tests/test_models.py para tests de modelos",
        "Testear validación de datos en modelos Pydantic",
        "Testear creación y consulta de modelos SQLAlchemy",
        "Testear serialización y deserialización",
        "Testear casos de error y validación"
    ]
