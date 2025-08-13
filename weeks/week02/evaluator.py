"""
Evaluador específico para Semana 2 - CRUD Básico con FastAPI (versión segura análisis estático)
"""
import sys
from pathlib import Path
from typing import Dict, Any, List

# Agregar el directorio padre al path para importar core
sys.path.append(str(Path(__file__).parent.parent.parent))

from core import BaseEvaluator

# Import checks using absolute imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from checks.crud_operations import check_crud_operations
from checks.models import check_models
from checks.endpoints import check_endpoints


class Week02Evaluator(BaseEvaluator):
    """Evaluador para Semana 2 empleando únicamente análisis estático."""

    def __init__(self, student_repo_path: str):
        super().__init__(week_number=2, student_repo_path=student_repo_path)

    def _run_common_checks(self) -> Dict[str, Any]:  # type: ignore[override]
        repo = self.repo_path
        results: Dict[str, Any] = {}
        structure = {
            "files": {
                "main_py": (repo / "main.py").exists(),
                "requirements_txt": (repo / "requirements.txt").exists(),
                "readme_md": (repo / "README.md").exists(),
            }
        }
        structure["ok"] = all(structure["files"].values()) if structure["files"] else False
        reqs_present: Dict[str, bool] = {}
        if (repo / "requirements.txt").exists():
            try:
                txt = (repo / "requirements.txt").read_text(encoding="utf-8", errors="ignore").lower()
                for pkg in ["fastapi", "uvicorn", "pydantic"]:
                    reqs_present[pkg] = pkg in txt
            except Exception:
                pass
        results["structure"] = structure
        results["requirements"] = reqs_present
        if (repo / "README.md").exists():
            readme = (repo / "README.md").read_text(encoding="utf-8", errors="ignore")
            results["readme"] = {
                "length": len(readme.split()),
                "has_install": any(k in readme.lower() for k in ["install", "requirements", "pip"]),
                "has_run": any(k in readme.lower() for k in ["uvicorn", "run", "start"])
            }
        return results

    def run_specific_checks(self) -> Dict[str, Any]:  # type: ignore[override]
        results: Dict[str, Any] = {}
        results["models"] = check_models(str(self.repo_path))
        results["crud_operations"] = check_crud_operations(str(self.repo_path))
        results["endpoints"] = check_endpoints(str(self.repo_path))
        results["data_validation"] = self._check_data_validation(results)
        results["error_handling"] = self._check_error_handling(results)
        return results

    def _check_data_validation(self, all_results: Dict[str, Any]) -> Dict[str, Any]:
        models_res = all_results.get("models", {})
        endpoints_res = all_results.get("endpoints", {}).get("validation_in_endpoints", {})
        score = 0
        if models_res.get("basemodel_used"):
            score += 50
        if models_res.get("validation_used"):
            score += 20
        if endpoints_res.get("has_response_validation"):
            score += 15
        if endpoints_res.get("has_request_validation"):
            score += 15
        return {
            "pydantic_used": models_res.get("basemodel_used", False),
            "validation_patterns": {
                "model_validation": models_res.get("validation_used", False),
                "request_validation": endpoints_res.get("has_request_validation", False),
                "response_validation": endpoints_res.get("has_response_validation", False)
            },
            "validation_score": score
        }

    def _check_error_handling(self, all_results: Dict[str, Any]) -> Dict[str, Any]:
        endpoints_res = all_results.get("endpoints", {}).get("validation_in_endpoints", {})
        indicators = {
            "has_http_exceptions": endpoints_res.get("has_error_handling", False),
            "handles_not_found": bool(endpoints_res.get("has_error_handling")),
            "handles_validation_errors": endpoints_res.get("has_error_handling", False),
            "custom_error_responses": endpoints_res.get("has_error_handling", False)
        }
        score = (sum(indicators.values()) / len(indicators) * 100) if indicators else 0
        indicators["error_handling_score"] = score
        return indicators

    def get_week_specific_feedback(self, results: Dict[str, Any]) -> List[str]:  # type: ignore[override]
        """
        Genera feedback específico para Week 2 - CRUD Básico con FastAPI
        Incluye tanto aspectos positivos como mejoras necesarias
        """
        feedback = []
        successful_aspects = []
        
        # Analizar operaciones CRUD
        crud = results.get("crud_operations", {})
        crud_operations = [
            ("create_operation", "CREATE", "endpoint POST para crear recursos"),
            ("read_all_operation", "READ ALL", "endpoint GET para listar todos los recursos"),
            ("read_operation", "READ ONE", "endpoint GET para obtener un recurso específico"),
            ("update_operation", "UPDATE", "endpoint PUT/PATCH para actualizar recursos"),
            ("delete_operation", "DELETE", "endpoint DELETE para eliminar recursos")
        ]
        
        successful_crud = []
        missing_crud = []
        for operation, label, description in crud_operations:
            if crud.get(operation, False):
                successful_crud.append(f"Operación {label}")
            else:
                missing_crud.append(f"Implementar {description}")
        
        if successful_crud:
            successful_aspects.append(f"Operaciones CRUD implementadas: {', '.join(successful_crud)}")
        
        if missing_crud:
            feedback.extend(missing_crud)
        
        # Analizar modelos Pydantic
        models_res = results.get("models", {})
        if models_res.get("basemodel_used", False):
            successful_aspects.append("Modelos Pydantic (BaseModel) definidos correctamente")
        else:
            feedback.append("Definir modelos Pydantic usando BaseModel para validación de datos")
        
        if models_res.get("validation_used", False):
            successful_aspects.append("Validaciones de campo implementadas en modelos")
        else:
            feedback.append("Agregar validaciones usando Field() u otras restricciones en los modelos")
        
        # Analizar validación de endpoints
        endpoints_res = results.get("endpoints", {})
        if endpoints_res.get("docs_accessible", False):
            successful_aspects.append("Documentación automática FastAPI (/docs) accesible")
        else:
            feedback.append("Asegurar que la aplicación FastAPI esté correctamente configurada para habilitar /docs")
        
        val = endpoints_res.get("validation_in_endpoints", {})
        if val.get("has_request_validation", False):
            successful_aspects.append("Validación de request data implementada")
        
        if val.get("has_response_validation", False):
            successful_aspects.append("Modelos de respuesta definidos")
        
        if val.get("has_error_handling", False):
            successful_aspects.append("Manejo de errores con HTTPException implementado")
        else:
            feedback.append("Implementar manejo de errores con HTTPException y códigos de estado apropiados")
        
        # Analizar validación de datos
        data_validation = results.get("data_validation", {})
        if data_validation.get("score", 0) > 0:
            successful_aspects.append("Sistema de validación de datos funcionando")
        
        # Combinar aspectos exitosos y mejoras
        combined_feedback = []
        
        if successful_aspects:
            combined_feedback.append("✅ **Aspectos de Week 2 implementados correctamente:**")
            for aspect in successful_aspects:
                combined_feedback.append(f"• {aspect}")
            combined_feedback.append("")  # Línea en blanco
        
        if feedback:
            combined_feedback.append("🔧 **Mejoras específicas de Week 2:**")
            for improvement in feedback:
                combined_feedback.append(f"• {improvement}")
        
        return combined_feedback

    def _get_check_result(self, check_name: str) -> bool:  # type: ignore[override]
        r = self.results
        mapping = {
            "requirements_complete": lambda: all(r.get("requirements", {}).get(pkg, False) for pkg in ["fastapi", "uvicorn", "pydantic"]),
            "project_structure": lambda: r.get("structure", {}).get("files", {}).get("main_py", False),
            "main_py_organized": lambda: r.get("structure", {}).get("files", {}).get("main_py", False),
            "create_endpoint": lambda: r.get("crud_operations", {}).get("create_operation", False),
            "read_all_endpoint": lambda: r.get("crud_operations", {}).get("read_all_operation", False),
            "read_one_endpoint": lambda: r.get("crud_operations", {}).get("read_operation", False),
            "update_endpoint": lambda: r.get("crud_operations", {}).get("update_operation", False),
            "delete_endpoint": lambda: r.get("crud_operations", {}).get("delete_operation", False),
            "pydantic_models": lambda: r.get("models", {}).get("basemodel_used", False),
            "request_validation": lambda: r.get("endpoints", {}).get("validation_in_endpoints", {}).get("has_request_validation", False),
            "response_models": lambda: r.get("endpoints", {}).get("validation_in_endpoints", {}).get("has_response_validation", False),
            "http_exceptions": lambda: r.get("endpoints", {}).get("validation_in_endpoints", {}).get("has_error_handling", False),
            "status_codes": lambda: r.get("endpoints", {}).get("validation_in_endpoints", {}).get("has_error_handling", False),
        }
        if check_name in mapping:
            try:
                return bool(mapping[check_name]())
            except Exception:
                return False
        return super()._get_check_result(check_name)

    def get_week02_summary(self) -> Dict[str, Any]:
        if not self.results:
            return {"error": "No evaluation results"}
        crud = self.results.get("crud_operations", {})
        models_r = self.results.get("models", {})
        endpoints_r = self.results.get("endpoints", {})
        return {
            "crud_complete": all(crud.get(k) for k in ["create_operation", "read_operation", "read_all_operation", "update_operation", "delete_operation"]),
            "models_ok": models_r.get("basemodel_used", False),
            "validation": endpoints_r.get("validation_in_endpoints", {}),
            "ready_for_week3": all([
                models_r.get("basemodel_used", False),
                crud.get("create_operation", False),
                crud.get("read_operation", False),
                crud.get("update_operation", False)
            ])
        }
