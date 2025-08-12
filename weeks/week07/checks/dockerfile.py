"""
Verificaciones de dockerfile específicas para Week 7
"""
import sys
from pathlib import Path
from typing import Dict, Any, List


def check_dockerfile(repo_path: str) -> Dict[str, Any]:
    """
    Verifica dockerfile para Week 7
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de dockerfile
    """
    repo_root = Path(repo_path)
    
    # TODO: Implementar verificaciones específicas para dockerfile
    
    return {
        "dockerfile_implemented": False,
        "dockerfile_score": 0,
        "recommendations": [
            "Implementar dockerfile"
        ],
        "error": "Check not implemented yet"
    }


def get_dockerfile_recommendations(repo_path: str) -> List[str]:
    """
    Genera recomendaciones específicas para dockerfile
    """
    return [
        f"Implementar dockerfile según los requisitos de Week 7"
    ]
