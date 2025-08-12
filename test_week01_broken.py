#!/usr/bin/env python3
"""
Test de evaluación con repositorio con errores para Week01
"""
import tempfile
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

def create_broken_repo(repo_path: Path):
    """Crea un repositorio con errores para probar la detección"""
    
    # Crear main.py con errores
    main_content = '''from fastapi import FastAPI

app = FastAPI()

# Falta el endpoint raíz
@app.get("/hello")
def hello():
    return {"message": "Hello"}

# Error de sintaxis en la siguiente línea
def broken_function(
    return "error"
'''
    (repo_path / "main.py").write_text(main_content)
    
    # Crear requirements.txt sin uvicorn
    requirements_content = '''fastapi>=0.68.0
# falta uvicorn
requests
'''
    (repo_path / "requirements.txt").write_text(requirements_content)
    
    # README.md muy básico
    readme_content = '''# Proyecto
Esto es un proyecto.
'''
    (repo_path / "README.md").write_text(readme_content)

def run_broken_repo_test():
    """
    Prueba la evaluación con un repositorio con errores
    """
    from weeks.week01.checks.endpoints import check_endpoints
    from weeks.week01.checks.documentation import check_documentation
    from weeks.week01.checks.structure import check_project_structure
    
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir)
        print(f"📁 Creando repositorio con errores: {repo_path}")
        
        # Crear repositorio con errores
        create_broken_repo(repo_path)
        print("⚠️ Repositorio con errores creado")
        
        # Ejecutar todos los checks
        results = {}
        
        print("\n🔍 Ejecutando checks...")
        
        print("- Verificando endpoints...")
        results["endpoints"] = check_endpoints(str(repo_path))
        
        print("- Verificando documentación...")
        results["documentation"] = check_documentation(str(repo_path))
        
        print("- Verificando estructura...")
        results["project_structure"] = check_project_structure(str(repo_path))
        
        # Mostrar resultados detallados
        print(f"\n📊 RESULTADOS DETALLADOS:")
        
        for check_name, check_result in results.items():
            passed = check_result.get("passed", False)
            score = check_result.get("score", 0)
            status = "✅" if passed else "❌"
            
            print(f"\n{status} {check_name.upper()}: {score:.1f}/100")
            
            if "error" in check_result:
                print(f"   💔 Error: {check_result['error']}")
            
            # Mostrar detalles específicos
            if check_name == "endpoints":
                print(f"   - App importable: {check_result.get('app_importable', False)}")
                print(f"   - Endpoint raíz: {check_result.get('root_working', False)}")
                print(f"   - Endpoint paramétrico: {check_result.get('parametric_endpoint', False)}")
            
            elif check_name == "documentation":
                print(f"   - README existe: {check_result.get('readme_exists', False)}")
                print(f"   - Comandos de setup: {check_result.get('has_setup_commands', False)}")
                print(f"   - Reflexión sobre FastAPI: {check_result.get('has_reflection', False)}")
            
            elif check_name == "project_structure":
                basic_files = check_result.get('basic_files', {})
                requirements = check_result.get('requirements', {})
                print(f"   - Archivos presentes: {basic_files.get('all_present', False)}")
                print(f"   - FastAPI en requirements: {requirements.get('fastapi', False)}")
                print(f"   - Uvicorn en requirements: {requirements.get('uvicorn', False)}")
        
        # Calcular score total
        total_score = sum(r.get("score", 0) for r in results.values()) / len(results)
        passed_overall = total_score >= 70
        
        print(f"\n🎯 RESULTADO FINAL:")
        print(f"Score total: {total_score:.1f}/100")
        print(f"Estado: {'✅ APROBADO' if passed_overall else '❌ REPROBADO'}")
        
        return results

if __name__ == "__main__":
    print("🧪 TEST DE REPOSITORIO CON ERRORES - WEEK 01")
    print("=" * 55)
    
    run_broken_repo_test()
    
    print(f"\n✨ TEST COMPLETADO")
    print("Este test demuestra que el evaluador detecta correctamente los errores.")
