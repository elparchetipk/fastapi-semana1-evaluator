"""
Verificaciones de tests de funciones utilitarias para Week 5
"""
import sys
from pathlib import Path
from typing import Dict, Any, List
import ast
import re


def check_utility_function_tests(repo_path: str) -> Dict[str, Any]:
    """
    Verifica los tests de funciones utilitarias
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de tests de funciones utilitarias
    """
    repo_root = Path(repo_path)
    tests_dir = repo_root / 'tests'
    
    if not tests_dir.exists():
        return {
            "tests_directory_exists": False,
            "utility_test_files": [],
            "utility_test_functions": 0,
            "score": 0,
            "max_score": 7,
            "recommendations": ["Crear directorio 'tests/' y agregar tests de funciones utilitarias"]
        }
    
    # Buscar archivos de test de utilidades
    utility_test_files = []
    utility_test_patterns = [
        'test*util*.py',
        'test*helper*.py',
        'test*tool*.py',
        '*util*test*.py',
        '*helper*test*.py'
    ]
    
    for pattern in utility_test_patterns:
        utility_test_files.extend(list(tests_dir.glob(pattern)))
        utility_test_files.extend(list(tests_dir.rglob(pattern)))
    
    # Remover duplicados
    utility_test_files = list(set(utility_test_files))
    
    test_analysis = {
        "auth_utils_tests": 0,
        "data_utils_tests": 0,
        "validation_utils_tests": 0,
        "formatting_utils_tests": 0,
        "security_utils_tests": 0
    }
    
    total_utility_test_functions = 0
    
    # Buscar módulos de utilidades en el proyecto
    utility_modules = []
    for py_file in repo_root.rglob('*.py'):
        if any(term in py_file.name.lower() for term in ['util', 'helper', 'tool', 'auth', 'security']):
            if 'test' not in py_file.name.lower():
                utility_modules.append(py_file)
    
    # Analizar contenido de archivos de test
    for test_file in utility_test_files:
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)
                
                # Contar funciones de test
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                        total_utility_test_functions += 1
                        
                        # Categorizar tests por contenido
                        func_content = ast.get_source_segment(content, node) or ""
                        func_content_lower = func_content.lower()
                        
                        # Tests de utilidades de autenticación
                        if any(term in func_content_lower for term in ['auth', 'login', 'token', 'password', 'hash']):
                            test_analysis["auth_utils_tests"] += 1
                        
                        # Tests de utilidades de datos
                        if any(term in func_content_lower for term in ['data', 'format', 'convert', 'parse', 'transform']):
                            test_analysis["data_utils_tests"] += 1
                            
                        # Tests de validación
                        if any(term in func_content_lower for term in ['valid', 'check', 'verify', 'sanitize']):
                            test_analysis["validation_utils_tests"] += 1
                            
                        # Tests de formateo
                        if any(term in func_content_lower for term in ['format', 'clean', 'normalize']):
                            test_analysis["formatting_utils_tests"] += 1
                            
                        # Tests de seguridad
                        if any(term in func_content_lower for term in ['security', 'encrypt', 'decrypt', 'safe']):
                            test_analysis["security_utils_tests"] += 1
                            
        except Exception as e:
            continue
    
    # También buscar en archivos de test generales
    general_test_files = list(tests_dir.glob('test*.py'))
    for test_file in general_test_files:
        if test_file not in utility_test_files:
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Buscar funciones de test de utilidades
                    utility_keywords = ['util', 'helper', 'auth', 'hash', 'validate', 'format']
                    for keyword in utility_keywords:
                        if re.search(rf'def test.*{keyword}', content.lower()):
                            tree = ast.parse(content)
                            for node in ast.walk(tree):
                                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                                    if keyword in node.name.lower():
                                        total_utility_test_functions += 1
                                        if keyword in ['auth', 'hash']:
                                            test_analysis["auth_utils_tests"] += 1
                                        elif keyword in ['validate']:
                                            test_analysis["validation_utils_tests"] += 1
                                        elif keyword in ['format']:
                                            test_analysis["formatting_utils_tests"] += 1
                            break
            except Exception as e:
                continue
    
    # Calcular puntuación
    score = 0
    
    # Puntos por tener tests de utilidades
    if total_utility_test_functions > 0:
        score += 2
    
    # Puntos por cantidad de tests
    if total_utility_test_functions >= 5:
        score += 3
    elif total_utility_test_functions >= 3:
        score += 2
    elif total_utility_test_functions >= 1:
        score += 1
    
    # Puntos por variedad de tipos de tests
    test_types_count = sum(1 for count in test_analysis.values() if count > 0)
    if test_types_count >= 3:
        score += 2
    elif test_types_count >= 2:
        score += 1
    
    recommendations = []
    if total_utility_test_functions == 0:
        recommendations.append("Crear tests para funciones utilitarias")
    
    if test_analysis["auth_utils_tests"] == 0 and any('auth' in str(f).lower() for f in utility_modules):
        recommendations.append("Agregar tests para funciones de autenticación")
        
    if test_analysis["validation_utils_tests"] == 0:
        recommendations.append("Agregar tests para funciones de validación")
        
    if len(utility_modules) > 0 and total_utility_test_functions == 0:
        recommendations.append("Se detectaron módulos utilitarios sin tests")
    
    return {
        "tests_directory_exists": True,
        "utility_test_files": [str(f.relative_to(repo_root)) for f in utility_test_files],
        "utility_modules_found": [str(f.relative_to(repo_root)) for f in utility_modules],
        "utility_test_functions": total_utility_test_functions,
        "test_analysis": test_analysis,
        "score": min(score, 7),
        "max_score": 7,
        "recommendations": recommendations
    }


def get_utility_function_tests_recommendations(repo_path: str) -> List[str]:
    """
    Genera recomendaciones específicas para tests de funciones utilitarias
    """
    return [
        "Crear tests/test_utils.py para tests de utilidades",
        "Testear funciones de autenticación y hashing",
        "Testear funciones de validación de datos",
        "Testear funciones de formateo y transformación",
        "Usar casos edge y de error en los tests"
    ]
