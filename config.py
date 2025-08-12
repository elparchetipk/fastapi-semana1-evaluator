"""
Configuración global del sistema de evaluación FastAPI
"""
from pathlib import Path
from typing import Dict, Any, List

# Directorios del sistema
ROOT_DIR = Path(__file__).parent
CORE_DIR = ROOT_DIR / "core"
WEEKS_DIR = ROOT_DIR / "weeks"
EVALUATOR_DIR = ROOT_DIR / "evaluator"

# Configuración de semanas
AVAILABLE_WEEKS = list(range(1, 12))  # Semanas 1-11

# Configuración de scoring por defecto
DEFAULT_SCORING_WEIGHTS = {
    "structure": 25,      # Estructura del proyecto
    "functionality": 40,  # Funcionalidad (endpoints, etc.)
    "documentation": 20,  # README, docstrings, etc.
    "code_quality": 15    # Sintaxis, imports, etc.
}

# Umbral de aprobación por defecto
DEFAULT_PASSING_SCORE = 70

# Configuración de feedback
MAX_FEEDBACK_ITEMS = 10
FEEDBACK_PRIORITIES = ["critical", "important", "suggestion", "info"]

# Configuración de reportes
REPORT_FORMATS = ["markdown", "json", "summary", "html"]

# Templates por defecto
DEFAULT_TEMPLATES = {
    "feedback_header": "## 📋 Feedback de Evaluación - Semana {week}",
    "score_section": "**Score Final:** {score}/100 ({status})",
    "suggestions_header": "### 🔍 Sugerencias de Mejora"
}

# Configuración de checks comunes
COMMON_FILES = {
    "python_main": ["main.py", "app.py", "src/main.py"],
    "requirements": ["requirements.txt", "pyproject.toml", "Pipfile"],
    "readme": ["README.md", "readme.md", "README.rst"],
    "gitignore": [".gitignore"],
    "dockerfiles": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml"]
}

# Dependencias por semana (configuración básica)
WEEK_DEPENDENCIES = {
    1: ["fastapi", "uvicorn"],
    2: ["fastapi", "uvicorn", "pydantic"],
    3: ["fastapi", "uvicorn", "pydantic", "python-multipart"],
    4: ["fastapi", "uvicorn", "pydantic", "sqlalchemy"],
    5: ["fastapi", "uvicorn", "pydantic", "sqlalchemy", "alembic"],
    # ... más semanas se configuran según necesidad
}

# Endpoints esperados por semana
WEEK_ENDPOINTS = {
    1: ["/", "/hello/{name}", "/docs"],
    2: ["/", "/items", "/items/{item_id}", "/docs"],
    3: ["/", "/upload", "/form", "/docs"],
    # ... más semanas
}

# Configuración de timeout para pruebas
TEST_TIMEOUTS = {
    "import_timeout": 30,      # Timeout para importar la app
    "endpoint_timeout": 10,    # Timeout para probar endpoints
    "startup_timeout": 15      # Timeout para startup de la app
}

def get_week_config(week_number: int) -> Dict[str, Any]:
    """
    Obtiene la configuración específica para una semana
    
    Args:
        week_number: Número de semana (1-11)
        
    Returns:
        Configuración de la semana
    """
    if week_number not in AVAILABLE_WEEKS:
        raise ValueError(f"Semana {week_number} no válida. Debe estar entre 1 y 11.")
    
    return {
        "week": week_number,
        "dependencies": WEEK_DEPENDENCIES.get(week_number, WEEK_DEPENDENCIES[1]),
        "endpoints": WEEK_ENDPOINTS.get(week_number, WEEK_ENDPOINTS[1]),
        "scoring_weights": DEFAULT_SCORING_WEIGHTS.copy(),
        "passing_score": DEFAULT_PASSING_SCORE,
        "week_dir": WEEKS_DIR / f"week{week_number:02d}"
    }

def get_all_weeks_config() -> Dict[int, Dict[str, Any]]:
    """
    Obtiene la configuración de todas las semanas disponibles
    
    Returns:
        Dict con configuración de cada semana
    """
    return {week: get_week_config(week) for week in AVAILABLE_WEEKS}

# Configuración de logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard"
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "evaluator.log",
            "formatter": "detailed"
        }
    },
    "loggers": {
        "fastapi_evaluator": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False
        }
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}
