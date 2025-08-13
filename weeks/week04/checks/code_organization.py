"""
Check para verificar organización profesional del código
"""
import os
from pathlib import Path
from typing import Dict, Any, List


def check_code_organization(repo_path: str) -> Dict[str, Any]:
    """
    Verifica la organización profesional del código en carpetas separadas
    """
    results = {
        "has_models_folder": False,
        "has_schemas_folder": False,
        "has_services_folder": False,
        "has_routers_folder": False,
        "models_separated": False,
        "schemas_separated": False,
        "main_organized": False,
        "score": 0,
        "details": [],
        "errors": []
    }
    
    try:
        repo_path = Path(repo_path)
        
        # Verificar carpeta models/
        models_dir = repo_path / "models"
        if models_dir.exists() and models_dir.is_dir():
            results["has_models_folder"] = True
            results["details"].append("✅ Carpeta models/ encontrada")
            results["score"] += 2
            
            # Verificar archivos en models/
            model_files = list(models_dir.glob("*.py"))
            if len(model_files) > 0:
                results["models_separated"] = True
                results["details"].append(f"✅ {len(model_files)} archivo(s) de modelos organizados")
                results["score"] += 2
            else:
                results["errors"].append("❌ Carpeta models/ existe pero está vacía")
        else:
            results["errors"].append("❌ Carpeta models/ no encontrada")
        
        # Verificar carpeta schemas/
        schemas_dir = repo_path / "schemas"
        if schemas_dir.exists() and schemas_dir.is_dir():
            results["has_schemas_folder"] = True
            results["details"].append("✅ Carpeta schemas/ encontrada")
            results["score"] += 2
            
            # Verificar archivos en schemas/
            schema_files = list(schemas_dir.glob("*.py"))
            if len(schema_files) > 0:
                results["schemas_separated"] = True
                results["details"].append(f"✅ {len(schema_files)} archivo(s) de schemas organizados")
                results["score"] += 2
            else:
                results["errors"].append("❌ Carpeta schemas/ existe pero está vacía")
        else:
            results["errors"].append("❌ Carpeta schemas/ no encontrada")
        
        # Verificar carpeta services/ o routers/
        services_dir = repo_path / "services"
        routers_dir = repo_path / "routers"
        api_dir = repo_path / "api"
        
        if services_dir.exists() and services_dir.is_dir():
            results["has_services_folder"] = True
            results["details"].append("✅ Carpeta services/ encontrada")
            results["score"] += 1
        elif routers_dir.exists() and routers_dir.is_dir():
            results["has_routers_folder"] = True
            results["details"].append("✅ Carpeta routers/ encontrada")
            results["score"] += 1
        elif api_dir.exists() and api_dir.is_dir():
            results["details"].append("✅ Carpeta api/ encontrada")
            results["score"] += 1
        
        # Verificar organización del main.py
        main_file = repo_path / "main.py"
        if main_file.exists():
            try:
                content = main_file.read_text(encoding='utf-8')
                
                # Verificar que no esté todo en main.py (heurística)
                lines = content.split('\n')
                non_empty_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
                
                if len(non_empty_lines) < 50:  # main.py conciso
                    results["main_organized"] = True
                    results["details"].append("✅ main.py está bien organizado (conciso)")
                    results["score"] += 1
                else:
                    results["errors"].append("⚠️ main.py parece contener demasiado código")
                
                # Verificar imports de carpetas organizadas
                if "from models" in content or "from .models" in content:
                    results["details"].append("✅ Imports de models/ detectados")
                
                if "from schemas" in content or "from .schemas" in content:
                    results["details"].append("✅ Imports de schemas/ detectados")
                
            except Exception as e:
                results["errors"].append(f"❌ Error leyendo main.py: {str(e)}")
        else:
            results["errors"].append("❌ Archivo main.py no encontrado")
        
        # Verificar estructura general
        expected_folders = ["models", "schemas"]
        found_folders = []
        
        for folder in expected_folders:
            folder_path = repo_path / folder
            if folder_path.exists() and folder_path.is_dir():
                found_folders.append(folder)
        
        if len(found_folders) >= 2:
            results["details"].append("✅ Estructura de carpetas profesional implementada")
        else:
            results["errors"].append("❌ Falta organización en carpetas (models/, schemas/)")
        
        # Máximo 8 puntos para este check
        results["score"] = min(results["score"], 8)
        
    except Exception as e:
        results["errors"].append(f"❌ Error verificando organización: {str(e)}")
    
    return results


def get_code_organization_score(repo_path: str) -> float:
    """Obtiene el score de organización de código (0-8 puntos)"""
    result = check_code_organization(repo_path)
    return result["score"]


def get_code_organization_feedback(repo_path: str) -> List[str]:
    """Obtiene feedback específico para organización de código"""
    result = check_code_organization(repo_path)
    feedback = []
    
    if result["errors"]:
        for error in result["errors"]:
            feedback.append(error)
    
    if not result["has_models_folder"]:
        feedback.append("• Crear carpeta models/ y mover modelos SQLAlchemy ahí")
    
    if not result["has_schemas_folder"]:
        feedback.append("• Crear carpeta schemas/ y mover schemas Pydantic ahí")
    
    if not result["models_separated"]:
        feedback.append("• Separar modelos en archivos individuales dentro de models/")
    
    if not result["schemas_separated"]:
        feedback.append("• Separar schemas en archivos individuales dentro de schemas/")
    
    if not (result["has_services_folder"] or result["has_routers_folder"]):
        feedback.append("• Considerar crear carpeta services/ o routers/ para lógica de negocio")
    
    return feedback
