"""
Verificaciones de tests de lógica de negocio para Week 5
"""
import sys
from pathlib import Path
from typing import Dict, Any, List
import ast
import re


def check_business_logic_tests(repo_path: str) -> Dict[str, Any]:
    """
    Verifica los tests de lógica de negocio
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de tests de lógica de negocio
    """
    repo_root = Path(repo_path)
    tests_dir = repo_root / 'tests'
    
    if not tests_dir.exists():
        return {
            "tests_directory_exists": False,
            "business_test_files": [],
            "business_test_functions": 0,
            "score": 0,
            "max_score": 10,
            "recommendations": ["Crear directorio 'tests/' y agregar tests de lógica de negocio"]
        }
    
    # Buscar archivos de test de lógica de negocio
    business_test_files = []
    business_test_patterns = [
        'test*service*.py',
        'test*business*.py',
        'test*logic*.py',
        'test*crud*.py',
        '*service*test*.py',
        '*business*test*.py',
        '*logic*test*.py',
        '*crud*test*.py'
    ]
    
    for pattern in business_test_patterns:
        business_test_files.extend(list(tests_dir.glob(pattern)))
        business_test_files.extend(list(tests_dir.rglob(pattern)))
    
    # Remover duplicados
    business_test_files = list(set(business_test_files))
    
    test_analysis = {
        "crud_operations_tests": 0,
        "business_rules_tests": 0,
        "service_layer_tests": 0,
        "workflow_tests": 0,
        "complex_logic_tests": 0
    }
    
    total_business_test_functions = 0
    
    # Buscar módulos de lógica de negocio en el proyecto
    business_modules = []
    business_keywords = ['service', 'business', 'logic', 'crud', 'repository', 'manager']
    
    for py_file in repo_root.rglob('*.py'):
        if any(term in py_file.name.lower() for term in business_keywords):
            if 'test' not in py_file.name.lower() and py_file.name != 'main.py':
                business_modules.append(py_file)
    
    # Analizar contenido de archivos de test
    for test_file in business_test_files:
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)
                
                # Contar funciones de test
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                        total_business_test_functions += 1
                        
                        # Categorizar tests por contenido
                        func_content = ast.get_source_segment(content, node) or ""
                        func_content_lower = func_content.lower()
                        
                        # Tests de operaciones CRUD
                        if any(term in func_content_lower for term in ['create', 'read', 'update', 'delete', 'crud', 'get_by']):
                            test_analysis["crud_operations_tests"] += 1
                        
                        # Tests de reglas de negocio
                        if any(term in func_content_lower for term in ['rule', 'policy', 'constraint', 'business', 'logic']):
                            test_analysis["business_rules_tests"] += 1
                            
                        # Tests de capa de servicio
                        if any(term in func_content_lower for term in ['service', 'manager', 'handler']):
                            test_analysis["service_layer_tests"] += 1
                            
                        # Tests de workflows
                        if any(term in func_content_lower for term in ['workflow', 'process', 'pipeline', 'flow']):
                            test_analysis["workflow_tests"] += 1
                            
                        # Tests de lógica compleja
                        if any(term in func_content_lower for term in ['complex', 'algorithm', 'calculation', 'compute']):
                            test_analysis["complex_logic_tests"] += 1
                            
        except Exception as e:
            continue
    
    # También buscar en archivos de test generales por funciones de negocio
    general_test_files = list(tests_dir.glob('test*.py'))
    for test_file in general_test_files:
        if test_file not in business_test_files:
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Buscar funciones que indiquen tests de lógica de negocio
                    business_patterns = [
                        r'def test.*create.*',
                        r'def test.*update.*',
                        r'def test.*delete.*',
                        r'def test.*service.*',
                        r'def test.*business.*',
                        r'def test.*logic.*',
                        r'def test.*process.*'
                    ]
                    
                    for pattern in business_patterns:
                        if re.search(pattern, content.lower()):
                            tree = ast.parse(content)
                            for node in ast.walk(tree):
                                if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                                    func_name_lower = node.name.lower()
                                    if any(term in func_name_lower for term in ['create', 'update', 'delete', 'service', 'business']):
                                        total_business_test_functions += 1
                                        
                                        if any(term in func_name_lower for term in ['create', 'update', 'delete']):
                                            test_analysis["crud_operations_tests"] += 1
                                        elif 'service' in func_name_lower:
                                            test_analysis["service_layer_tests"] += 1
                                        elif 'business' in func_name_lower:
                                            test_analysis["business_rules_tests"] += 1
                            break
            except Exception as e:
                continue
    
    # Calcular puntuación
    score = 0
    
    # Puntos por tener tests de lógica de negocio
    if total_business_test_functions > 0:
        score += 2
    
    # Puntos por cantidad de tests
    if total_business_test_functions >= 8:
        score += 4
    elif total_business_test_functions >= 5:
        score += 3
    elif total_business_test_functions >= 3:
        score += 2
    elif total_business_test_functions >= 1:
        score += 1
    
    # Puntos por tests CRUD
    if test_analysis["crud_operations_tests"] >= 4:
        score += 2
    elif test_analysis["crud_operations_tests"] >= 2:
        score += 1
    
    # Puntos por variedad de tipos de tests
    test_types_count = sum(1 for count in test_analysis.values() if count > 0)
    if test_types_count >= 3:
        score += 2
    elif test_types_count >= 2:
        score += 1
    
    recommendations = []
    if total_business_test_functions == 0:
        recommendations.append("Crear tests para lógica de negocio")
    
    if test_analysis["crud_operations_tests"] == 0:
        recommendations.append("Agregar tests para operaciones CRUD")
        
    if test_analysis["service_layer_tests"] == 0 and any('service' in str(f).lower() for f in business_modules):
        recommendations.append("Agregar tests para capa de servicios")
        
    if test_analysis["business_rules_tests"] == 0:
        recommendations.append("Agregar tests para reglas de negocio específicas")
    
    if len(business_modules) > 0 and total_business_test_functions == 0:
        recommendations.append("Se detectaron módulos de lógica de negocio sin tests")
    
    return {
        "tests_directory_exists": True,
        "business_test_files": [str(f.relative_to(repo_root)) for f in business_test_files],
        "business_modules_found": [str(f.relative_to(repo_root)) for f in business_modules],
        "business_test_functions": total_business_test_functions,
        "test_analysis": test_analysis,
        "score": min(score, 10),
        "max_score": 10,
        "recommendations": recommendations
    }


def get_business_logic_tests_recommendations(repo_path: str) -> List[str]:
    """
    Genera recomendaciones específicas para tests de lógica de negocio
    """
    return [
        "Crear tests/test_services.py para tests de servicios",
        "Testear todas las operaciones CRUD",
        "Testear reglas de negocio específicas",
        "Testear flujos de trabajo complejos",
        "Testear casos edge de la lógica de negocio"
    ]
