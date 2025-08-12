"""
Verificaciones de modelos Pydantic específicas para Week 2
"""
import ast
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional


def check_models(repo_path: str) -> Dict[str, Any]:
    """
    Verifica la implementación de modelos Pydantic para Week 2
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Dict con resultados de verificación de modelos
    """
    repo_root = Path(repo_path)
    
    # Archivos donde pueden estar los modelos
    model_files = ["main.py", "models.py", "schemas.py"]
    
    results = {
        "pydantic_imported": False,
        "basemodel_used": False,
        "models_found": [],
        "model_fields": {},
        "field_types": {},
        "validation_used": False,
        "models_score": 0,
        "recommendations": []
    }
    
    all_code = ""
    models_in_files = {}
    
    # Analizar cada archivo
    for file_name in model_files:
        file_path = repo_root / file_name
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                    all_code += code + "\n"
                    
                file_analysis = _analyze_file_for_models(code, file_name)
                models_in_files[file_name] = file_analysis
                
            except Exception as e:
                models_in_files[file_name] = {"error": str(e)}
    
    # Análisis global
    if all_code:
        results.update(_analyze_pydantic_usage(all_code))
        results["models_in_files"] = models_in_files
        results["models_score"] = _calculate_models_score(results)
        results["recommendations"] = _generate_model_recommendations(results)
    
    return results


def _analyze_file_for_models(code: str, file_name: str) -> Dict[str, Any]:
    """
    Analiza un archivo específico en busca de modelos Pydantic
    """
    analysis = {
        "has_pydantic_import": False,
        "has_basemodel": False,
        "models": [],
        "syntax_valid": True
    }
    
    try:
        # Verificar imports
        analysis["has_pydantic_import"] = any(
            pattern in code for pattern in [
                "from pydantic import",
                "import pydantic",
                "from pydantic.main import",
                "from pydantic import BaseModel"
            ]
        )
        
        analysis["has_basemodel"] = "BaseModel" in code
        
        # Intentar parsear el AST para análisis más profundo
        try:
            tree = ast.parse(code)
            models = _extract_models_from_ast(tree)
            analysis["models"] = models
        except SyntaxError:
            analysis["syntax_valid"] = False
            # Fallback: búsqueda por patrones de texto
            analysis["models"] = _extract_models_by_pattern(code)
            
    except Exception as e:
        analysis["error"] = str(e)
    
    return analysis


def _extract_models_from_ast(tree: ast.AST) -> List[Dict[str, Any]]:
    """
    Extrae información de modelos usando AST
    """
    models = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            # Verificar si hereda de BaseModel
            inherits_basemodel = False
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "BaseModel":
                    inherits_basemodel = True
                elif isinstance(base, ast.Attribute) and base.attr == "BaseModel":
                    inherits_basemodel = True
            
            if inherits_basemodel:
                model_info = {
                    "name": node.name,
                    "fields": [],
                    "has_validation": False,
                    "field_types": {}
                }
                
                # Analizar campos del modelo
                for item in node.body:
                    if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        field_name = item.target.id
                        field_type = _get_type_annotation(item.annotation)
                        
                        model_info["fields"].append(field_name)
                        model_info["field_types"][field_name] = field_type
                        
                        # Verificar si tiene validación (Field, validator, etc.)
                        if hasattr(item, 'value') and item.value:
                            if isinstance(item.value, ast.Call):
                                if isinstance(item.value.func, ast.Name) and item.value.func.id == "Field":
                                    model_info["has_validation"] = True
                
                models.append(model_info)
    
    return models


def _extract_models_by_pattern(code: str) -> List[Dict[str, Any]]:
    """
    Extrae modelos usando patrones de texto (fallback)
    """
    models = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('class ') and 'BaseModel' in stripped:
            class_name = stripped.split('class ')[1].split('(')[0].strip()
            
            model_info = {
                "name": class_name,
                "fields": [],
                "has_validation": False,
                "field_types": {},
                "extracted_by": "pattern_matching"
            }
            
            # Buscar campos en las siguientes líneas
            j = i + 1
            while j < len(lines) and (lines[j].startswith('    ') or lines[j].strip() == ''):
                field_line = lines[j].strip()
                if ':' in field_line and not field_line.startswith('#'):
                    field_name = field_line.split(':')[0].strip()
                    field_type = field_line.split(':')[1].split('=')[0].strip() if '=' in field_line else field_line.split(':')[1].strip()
                    
                    model_info["fields"].append(field_name)
                    model_info["field_types"][field_name] = field_type
                    
                    if "Field(" in field_line:
                        model_info["has_validation"] = True
                j += 1
            
            models.append(model_info)
    
    return models


def _get_type_annotation(annotation) -> str:
    """
    Extrae la anotación de tipo como string
    """
    if isinstance(annotation, ast.Name):
        return annotation.id
    elif isinstance(annotation, ast.Constant):
        return str(annotation.value)
    elif isinstance(annotation, ast.Attribute):
        return f"{_get_type_annotation(annotation.value)}.{annotation.attr}"
    elif isinstance(annotation, ast.Subscript):
        base = _get_type_annotation(annotation.value)
        slice_val = _get_type_annotation(annotation.slice)
        return f"{base}[{slice_val}]"
    else:
        return "Unknown"


def _analyze_pydantic_usage(code: str) -> Dict[str, Any]:
    """
    Analiza el uso general de Pydantic en todo el código
    """
    analysis = {
        "pydantic_imported": False,
        "basemodel_used": False,
        "models_found": [],
        "model_fields": {},
        "field_types": {},
        "validation_used": False
    }
    
    # Verificar imports de Pydantic
    pydantic_patterns = [
        "from pydantic import BaseModel",
        "from pydantic import",
        "import pydantic",
        "pydantic.BaseModel"
    ]
    
    analysis["pydantic_imported"] = any(pattern in code for pattern in pydantic_patterns)
    analysis["basemodel_used"] = "BaseModel" in code
    
    # Verificar uso de validación
    validation_patterns = [
        "Field(",
        "@validator",
        "@root_validator",
        "ValidationError",
        "constr(",
        "conint(",
        "confloat("
    ]
    
    analysis["validation_used"] = any(pattern in code for pattern in validation_patterns)
    
    # Extraer todos los modelos encontrados
    try:
        tree = ast.parse(code)
        all_models = _extract_models_from_ast(tree)
        analysis["models_found"] = [model["name"] for model in all_models]
        
        # Consolidar campos y tipos
        for model in all_models:
            analysis["model_fields"][model["name"]] = model["fields"]
            analysis["field_types"].update(model["field_types"])
            
    except SyntaxError:
        # Fallback para código con errores de sintaxis
        fallback_models = _extract_models_by_pattern(code)
        analysis["models_found"] = [model["name"] for model in fallback_models]
    
    return analysis


def _calculate_models_score(results: Dict[str, Any]) -> float:
    """
    Calcula el score de implementación de modelos
    """
    score = 0
    
    # Pydantic importado correctamente (20 puntos)
    if results.get("pydantic_imported", False):
        score += 20
    
    # BaseModel usado (20 puntos)
    if results.get("basemodel_used", False):
        score += 20
    
    # Modelos encontrados (40 puntos)
    models_count = len(results.get("models_found", []))
    if models_count >= 2:
        score += 40
    elif models_count == 1:
        score += 25
    
    # Validación utilizada (20 puntos)
    if results.get("validation_used", False):
        score += 20
    
    return score


def _generate_model_recommendations(results: Dict[str, Any]) -> List[str]:
    """
    Genera recomendaciones para mejorar los modelos
    """
    recommendations = []
    
    if not results.get("pydantic_imported", False):
        recommendations.append("Importa Pydantic: 'from pydantic import BaseModel'")
    
    if not results.get("basemodel_used", False):
        recommendations.append("Crea clases que hereden de BaseModel para definir modelos")
    
    models_count = len(results.get("models_found", []))
    if models_count == 0:
        recommendations.append("Define al menos un modelo Pydantic para tus datos")
    elif models_count == 1:
        recommendations.append("Considera crear modelos adicionales (ej: CreateItem, UpdateItem)")
    
    if not results.get("validation_used", False):
        recommendations.append("Usa Field() para agregar validaciones a tus campos")
    
    # Recomendaciones específicas por archivo
    files_analysis = results.get("models_in_files", {})
    if "main.py" in files_analysis and files_analysis["main.py"].get("models"):
        if not any("models.py" in f or "schemas.py" in f for f in files_analysis.keys()):
            recommendations.append("Considera mover los modelos a un archivo separado (models.py o schemas.py)")
    
    return recommendations


def check_specific_model(repo_path: str, model_name: str) -> Dict[str, Any]:
    """
    Verifica un modelo específico
    """
    results = check_models(repo_path)
    
    if model_name in results.get("models_found", []):
        return {
            "model_exists": True,
            "model_name": model_name,
            "fields": results.get("model_fields", {}).get(model_name, []),
            "field_types": {k: v for k, v in results.get("field_types", {}).items() 
                           if k in results.get("model_fields", {}).get(model_name, [])}
        }
    else:
        return {
            "model_exists": False,
            "model_name": model_name,
            "suggestion": f"Crea el modelo {model_name} que herede de BaseModel"
        }


def get_model_recommendations(repo_path: str) -> List[str]:
    """
    Obtiene recomendaciones específicas para modelos
    """
    results = check_models(repo_path)
    return results.get("recommendations", [])
