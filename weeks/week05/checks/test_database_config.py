"""
Verificaciones de configuración de base de datos de testing para Week 5
"""
import sys
from pathlib import Path
from typing import Dict, Any, List
import ast
import re


def check_test_database_config(repo_path: str) -> Dict[str, Any]:
    """
    Verifica la configuración de base de datos separada para testing
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de configuración de BD de testing
    """
    repo_root = Path(repo_path)
    issues = []
    config_found = False
    test_db_evidence = []
    
    # Archivos donde buscar configuración de testing DB
    config_files = [
        'config.py',
        'database.py',
        'settings.py',
        'conftest.py',
        'tests/conftest.py'
    ]
    
    db_config_patterns = [
        r'test.*database',
        r'database.*test',
        r'sqlite.*memory',
        r':memory:',
        r'test\.db',
        r'testing.*url',
        r'TEST_DATABASE',
        r'create_all\(\)',
        r'drop_all\(\)'
    ]
    
    for config_file in config_files:
        config_path = repo_root / config_file
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Buscar patrones de configuración de testing DB
                    for pattern in db_config_patterns:
                        matches = re.findall(pattern, content, re.IGNORECASE)
                        if matches:
                            test_db_evidence.append({
                                'file': config_file,
                                'pattern': pattern,
                                'matches': matches
                            })
                            config_found = True
                    
                    # Análisis AST para configuraciones más complejas
                    try:
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                # Buscar funciones relacionadas con setup/teardown de DB
                                if any(keyword in node.name.lower() for keyword in 
                                      ['setup', 'teardown', 'fixture', 'test_db', 'test_session']):
                                    test_db_evidence.append({
                                        'file': config_file,
                                        'type': 'function',
                                        'name': node.name
                                    })
                                    config_found = True
                                    
                            elif isinstance(node, ast.Assign):
                                # Buscar asignaciones de variables de testing
                                for target in node.targets:
                                    if isinstance(target, ast.Name):
                                        if any(keyword in target.id.lower() for keyword in 
                                              ['test_db', 'test_database', 'testing_db']):
                                            test_db_evidence.append({
                                                'file': config_file,
                                                'type': 'variable',
                                                'name': target.id
                                            })
                                            config_found = True
                    except:
                        pass
                        
            except Exception as e:
                issues.append(f"Error analizando {config_file}: {e}")
    
    # Verificar archivos de requirements para SQLite
    requirements_file = repo_root / 'requirements.txt'
    sqlite_in_requirements = False
    if requirements_file.exists():
        try:
            with open(requirements_file, 'r') as f:
                content = f.read().lower()
                if 'sqlite' in content or 'aiosqlite' in content:
                    sqlite_in_requirements = True
                    test_db_evidence.append({
                        'file': 'requirements.txt',
                        'type': 'dependency',
                        'evidence': 'SQLite dependency found'
                    })
        except:
            pass
    
    # Buscar en tests específicamente
    tests_dir = repo_root / 'tests'
    if tests_dir.exists():
        test_files = list(tests_dir.glob('**/*.py'))
        for test_file in test_files:
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if any(pattern in content.lower() for pattern in 
                          ['test_client', 'testclient', 'override_get_db', 'test_session']):
                        test_db_evidence.append({
                            'file': str(test_file.relative_to(repo_root)),
                            'type': 'test_setup',
                            'evidence': 'Test client or DB override found'
                        })
                        config_found = True
            except:
                continue
    
    # Calcular puntuación
    score = 0
    if config_found:
        score += 6
    if sqlite_in_requirements:
        score += 2
    if any('conftest.py' in str(evidence.get('file', '')) for evidence in test_db_evidence):
        score += 2
    if len(test_db_evidence) >= 3:
        score += 2
    
    recommendations = []
    if not config_found:
        recommendations.append("Configurar base de datos separada para testing")
        recommendations.append("Usar SQLite en memoria para tests rápidos")
    if not sqlite_in_requirements:
        recommendations.append("Considerar usar SQLite para testing")
    if not any('conftest.py' in str(evidence.get('file', '')) for evidence in test_db_evidence):
        recommendations.append("Configurar fixtures de DB en tests/conftest.py")
    
    return {
        "test_db_config_found": config_found,
        "sqlite_in_requirements": sqlite_in_requirements,
        "evidence": test_db_evidence,
        "score": min(score, 12),
        "max_score": 12,
        "issues": issues,
        "recommendations": recommendations
    }


def get_test_database_config_recommendations(repo_path: str) -> List[str]:
    """
    Genera recomendaciones específicas para configuración de DB de testing
    """
    return [
        "Configurar base de datos separada para testing (ej: SQLite en memoria)",
        "Crear fixtures de DB en tests/conftest.py",
        "Implementar setup/teardown de tablas para cada test",
        "Usar dependency override para reemplazar DB principal en tests",
        "Considerar usar pytest-asyncio para tests async de DB"
    ]
