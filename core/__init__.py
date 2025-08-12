"""
Core framework para el sistema de evaluación automática FastAPI.
Proporciona componentes reutilizables para evaluadores semanales.
"""

from .base_evaluator import BaseEvaluator
from .common_checks import CommonChecks, create_common_checks
from .scoring_engine import ScoringEngine, create_scoring_engine
from .report_generator import ReportGenerator, create_report_generator

__version__ = "1.0.0"
__all__ = [
    "BaseEvaluator",
    "CommonChecks", 
    "create_common_checks",
    "ScoringEngine",
    "create_scoring_engine", 
    "ReportGenerator",
    "create_report_generator"
]

# Constantes del framework
DEFAULT_TIMEOUT = 300
DEFAULT_PASSING_THRESHOLD = 70
SUPPORTED_WEEKS = list(range(1, 12))  # Weeks 1-11

# Configuración por defecto
DEFAULT_CONFIG = {
    "timeout_seconds": DEFAULT_TIMEOUT,
    "passing_threshold": DEFAULT_PASSING_THRESHOLD,
    "max_retries": 3,
    "enable_caching": True,
    "strict_mode": False
}

def get_framework_info():
    """Retorna información sobre el framework"""
    return {
        "version": __version__,
        "supported_weeks": SUPPORTED_WEEKS,
        "components": __all__,
        "default_config": DEFAULT_CONFIG
    }
