"""
Verificaciones de dependencias de testing para Week 5
"""
import sys
from pathlib import Path
from typing import Dict, Any, List


def check_test_dependencies(repo_path: str) -> Dict[str, Any]:
    """
    Verifica las dependencias necesarias para testing
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de dependencias de testing
    """
    repo_root = Path(repo_path)
    requirements_file = repo_root / 'requirements.txt'
    
    if not requirements_file.exists():
        return {
            "dependencies_found": {},
            "missing_dependencies": ["requirements.txt not found"],
            "score": 0,
            "max_score": 7,
            "recommendations": ["Crear archivo requirements.txt"]
        }
    
    # Dependencias requeridas y opcionales
    required_deps = {
        'pytest': False,
        'httpx': False
    }
    
    optional_deps = {
        'pytest-asyncio': False,
        'pytest-cov': False,
        'faker': False,
        'factory-boy': False
    }
    
    try:
        with open(requirements_file, 'r') as f:
            content = f.read().lower()
            
            # Verificar dependencias requeridas
            for dep in required_deps:
                if dep in content:
                    required_deps[dep] = True
            
            # Verificar dependencias opcionales
            for dep in optional_deps:
                if dep in content:
                    optional_deps[dep] = True
                    
    except Exception as e:
        return {
            "dependencies_found": {},
            "missing_dependencies": [f"Error reading requirements.txt: {e}"],
            "score": 0,
            "max_score": 7,
            "recommendations": ["Revisar formato de requirements.txt"]
        }
    
    # Calcular puntuación
    score = 0
    for dep, found in required_deps.items():
        if found:
            score += 3 if dep == 'pytest' else 2
    
    # Bonus por dependencias opcionales
    bonus = sum(1 for found in optional_deps.values() if found)
    score += min(bonus, 2)
    
    missing_deps = [dep for dep, found in required_deps.items() if not found]
    
    recommendations = []
    if missing_deps:
        recommendations.extend([f"Agregar {dep} a requirements.txt" for dep in missing_deps])
    
    if not optional_deps['pytest-asyncio']:
        recommendations.append("Considerar agregar pytest-asyncio para tests async")
    
    if not optional_deps['pytest-cov']:
        recommendations.append("Considerar agregar pytest-cov para coverage")
    
    return {
        "dependencies_found": {**required_deps, **optional_deps},
        "missing_dependencies": missing_deps,
        "score": min(score, 7),
        "max_score": 7,
        "recommendations": recommendations
    }


def get_test_dependencies_recommendations(repo_path: str) -> List[str]:
    """
    Genera recomendaciones específicas para dependencias de testing
    """
    return [
        "Instalar pytest como framework de testing principal",
        "Instalar httpx para testing de APIs HTTP",
        "Considerar pytest-asyncio para tests asíncronos",
        "Considerar pytest-cov para medición de coverage",
        "Considerar faker o factory-boy para datos de prueba"
    ]
