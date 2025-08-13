"""
Verificaciones de tests de endpoints para Week 5
"""
import sys
from pathlib import Path
from typing import Dict, Any, List
import ast
import re


def check_endpoint_tests(repo_path: str) -> Dict[str, Any]:
    """
    Verifica los tests de todos los endpoints principales
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de tests de endpoints
    """
    repo_root = Path(repo_path)
    tests_dir = repo_root / 'tests'
    
    if not tests_dir.exists():
        return {
            "tests_directory_exists": False,
            "endpoint_test_files": [],
            "endpoint_test_functions": 0,
            "score": 0,
            "max_score": 10,
            "recommendations": ["Crear directorio 'tests/' y agregar tests de endpoints"]
        }
    
    # Buscar archivos de test de endpoints/API
    endpoint_test_files = []
    endpoint_test_patterns = [
        'test*api*.py',
        'test*endpoint*.py',
        'test*route*.py',
        '*api*test*.py',
        '*endpoint*test*.py',
        '*route*test*.py'
    ]
    
    for pattern in endpoint_test_patterns:
        endpoint_test_files.extend(list(tests_dir.glob(pattern)))
        endpoint_test_files.extend(list(tests_dir.rglob(pattern)))
    
    # Remover duplicados
    endpoint_test_files = list(set(endpoint_test_files))
    
    test_analysis = {
        "get_endpoint_tests": 0,
        "post_endpoint_tests": 0,
        "put_endpoint_tests": 0,
        "delete_endpoint_tests": 0,
        "client_usage": 0,
        "status_code_tests": 0,
        "response_data_tests": 0
    }
    
    total_endpoint_test_functions = 0
    http_methods_tested = set()
    
    # Analizar contenido de archivos de test
    for test_file in endpoint_test_files:
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)
                
                # Verificar uso de TestClient
                if 'testclient' in content.lower() or 'client' in content.lower():
                    test_analysis["client_usage"] += 1
                
                # Contar funciones de test
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                        total_endpoint_test_functions += 1
                        
                        # Categorizar tests por contenido
                        func_content = ast.get_source_segment(content, node) or ""
                        func_content_lower = func_content.lower()
                        
                        # Tests de métodos HTTP
                        if 'client.get' in func_content_lower or '.get(' in func_content_lower:
                            test_analysis["get_endpoint_tests"] += 1
                            http_methods_tested.add('GET')
                        
                        if 'client.post' in func_content_lower or '.post(' in func_content_lower:
                            test_analysis["post_endpoint_tests"] += 1
                            http_methods_tested.add('POST')
                            
                        if 'client.put' in func_content_lower or '.put(' in func_content_lower:
                            test_analysis["put_endpoint_tests"] += 1
                            http_methods_tested.add('PUT')
                            
                        if 'client.delete' in func_content_lower or '.delete(' in func_content_lower:
                            test_analysis["delete_endpoint_tests"] += 1
                            http_methods_tested.add('DELETE')
                        
                        # Tests de códigos de estado
                        if any(term in func_content_lower for term in ['status_code', '.status', '200', '201', '404', '422']):
                            test_analysis["status_code_tests"] += 1
                            
                        # Tests de datos de respuesta
                        if any(term in func_content_lower for term in ['.json()', 'response.data', 'assert', 'json']):
                            test_analysis["response_data_tests"] += 1
                            
        except Exception as e:
            continue
    
    # También buscar en archivos de test generales
    general_test_files = list(tests_dir.glob('test*.py'))
    for test_file in general_test_files:
        if test_file not in endpoint_test_files:
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Buscar indicios de tests de API
                    if any(term in content.lower() for term in ['client.get', 'client.post', 'testclient', '/api/']):
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_'):
                                func_content = ast.get_source_segment(content, node) or ""
                                func_content_lower = func_content.lower()
                                
                                if any(term in func_content_lower for term in ['client.', 'response', 'status']):
                                    total_endpoint_test_functions += 1
                                    
                                    # Detectar métodos HTTP
                                    if 'get' in func_content_lower:
                                        test_analysis["get_endpoint_tests"] += 1
                                        http_methods_tested.add('GET')
                                    if 'post' in func_content_lower:
                                        test_analysis["post_endpoint_tests"] += 1
                                        http_methods_tested.add('POST')
            except Exception as e:
                continue
    
    # Buscar definición de endpoints en el proyecto principal
    main_files = [repo_root / 'main.py', repo_root / 'app.py']
    routers_dir = repo_root / 'routers'
    
    endpoints_defined = set()
    
    for main_file in main_files:
        if main_file.exists():
            try:
                with open(main_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Buscar decoradores de FastAPI
                    http_decorators = re.findall(r'@app\.(get|post|put|delete|patch)', content.lower())
                    endpoints_defined.update(method.upper() for method in http_decorators)
                    
            except Exception as e:
                continue
    
    # Buscar en archivos de routers
    if routers_dir.exists():
        for router_file in routers_dir.glob('*.py'):
            try:
                with open(router_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    http_decorators = re.findall(r'@router\.(get|post|put|delete|patch)', content.lower())
                    endpoints_defined.update(method.upper() for method in http_decorators)
                    
            except Exception as e:
                continue
    
    # Calcular puntuación
    score = 0
    
    # Puntos por tener tests de endpoints
    if total_endpoint_test_functions > 0:
        score += 2
    
    # Puntos por cantidad de tests
    if total_endpoint_test_functions >= 6:
        score += 3
    elif total_endpoint_test_functions >= 4:
        score += 2
    elif total_endpoint_test_functions >= 2:
        score += 1
    
    # Puntos por cobertura de métodos HTTP
    methods_tested_count = len(http_methods_tested)
    if methods_tested_count >= 4:
        score += 3
    elif methods_tested_count >= 3:
        score += 2
    elif methods_tested_count >= 2:
        score += 1
    
    # Puntos por uso de TestClient
    if test_analysis["client_usage"] > 0:
        score += 1
    
    # Puntos por tests de códigos de estado
    if test_analysis["status_code_tests"] >= 3:
        score += 1
    
    recommendations = []
    if total_endpoint_test_functions == 0:
        recommendations.append("Crear tests para endpoints de la API")
    
    if test_analysis["client_usage"] == 0:
        recommendations.append("Usar TestClient de FastAPI para tests de API")
        
    missing_methods = endpoints_defined - http_methods_tested
    if missing_methods:
        recommendations.append(f"Agregar tests para métodos: {', '.join(missing_methods)}")
        
    if test_analysis["status_code_tests"] == 0:
        recommendations.append("Verificar códigos de estado HTTP en los tests")
        
    if test_analysis["response_data_tests"] == 0:
        recommendations.append("Verificar datos de respuesta en los tests")
    
    return {
        "tests_directory_exists": True,
        "endpoint_test_files": [str(f.relative_to(repo_root)) for f in endpoint_test_files],
        "endpoint_test_functions": total_endpoint_test_functions,
        "http_methods_tested": list(http_methods_tested),
        "endpoints_defined": list(endpoints_defined),
        "test_analysis": test_analysis,
        "score": min(score, 10),
        "max_score": 10,
        "recommendations": recommendations
    }


def get_endpoint_tests_recommendations(repo_path: str) -> List[str]:
    """
    Genera recomendaciones específicas para tests de endpoints
    """
    return [
        "Crear tests/test_api.py para tests de endpoints",
        "Usar TestClient de FastAPI para simular requests",
        "Testear todos los métodos HTTP (GET, POST, PUT, DELETE)",
        "Verificar códigos de estado HTTP",
        "Verificar estructura de respuestas JSON"
    ]
