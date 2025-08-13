"""
Verificaciones de configuración de pytest para Week 5
"""
import sys
from pathlib import Path
from typing import Dict, Any, List
import configparser
import toml


def check_pytest_configuration(repo_path: str) -> Dict[str, Any]:
    """
    Verifica la configuración correcta de pytest
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de configuración pytest
    """
    repo_root = Path(repo_path)
    issues = []
    config_found = False
    config_details = {}
    
    # Buscar archivos de configuración de pytest
    config_files = [
        'pytest.ini',
        'pyproject.toml',
        'setup.cfg',
        'tox.ini'
    ]
    
    for config_file in config_files:
        config_path = repo_root / config_file
        if config_path.exists():
            config_found = True
            try:
                if config_file == 'pyproject.toml':
                    with open(config_path) as f:
                        config = toml.load(f)
                        if 'tool' in config and 'pytest' in config['tool']:
                            config_details['pyproject.toml'] = config['tool']['pytest']
                else:
                    config = configparser.ConfigParser()
                    config.read(config_path)
                    if 'tool:pytest' in config:
                        config_details[config_file] = dict(config['tool:pytest'])
                    elif 'pytest' in config:
                        config_details[config_file] = dict(config['pytest'])
            except Exception as e:
                issues.append(f"Error leyendo {config_file}: {e}")
    
    # Verificar directorio de tests
    tests_dir = repo_root / 'tests'
    tests_exist = tests_dir.exists() and tests_dir.is_dir()
    
    if not tests_exist:
        issues.append("No se encontró el directorio 'tests/'")
    else:
        # Verificar estructura básica de tests
        test_files = list(tests_dir.glob('test_*.py')) + list(tests_dir.glob('*_test.py'))
        if not test_files:
            issues.append("No se encontraron archivos de test en el directorio 'tests/'")
    
    # Verificar conftest.py
    conftest_path = tests_dir / 'conftest.py' if tests_exist else None
    conftest_exists = conftest_path and conftest_path.exists()
    
    # Evaluación
    score = 0
    if config_found:
        score += 4
    if tests_exist:
        score += 2
    if conftest_exists:
        score += 2
    
    recommendations = []
    if not config_found:
        recommendations.append("Crear archivo de configuración pytest (pytest.ini o pyproject.toml)")
    if not tests_exist:
        recommendations.append("Crear directorio 'tests/' para organizar tests")
    if not conftest_exists:
        recommendations.append("Crear tests/conftest.py para configuración compartida de tests")
    
    return {
        "config_found": config_found,
        "config_details": config_details,
        "tests_directory_exists": tests_exist,
        "conftest_exists": conftest_exists,
        "score": min(score, 8),
        "max_score": 8,
        "issues": issues,
        "recommendations": recommendations
    }


def get_pytest_configuration_recommendations(repo_path: str) -> List[str]:
    """
    Genera recomendaciones específicas para configuración de pytest
    """
    return [
        "Crear pytest.ini o configurar [tool.pytest] en pyproject.toml",
        "Configurar testpaths = ['tests']",
        "Configurar addopts para opciones de testing",
        "Crear tests/conftest.py para fixtures compartidas"
    ]
