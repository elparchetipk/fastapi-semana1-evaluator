#!/usr/bin/env python3
"""
Test final de evaluación simplificada para Week01
"""
import tempfile
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

def create_sample_repo(repo_path: Path):
    """Crea un repositorio de ejemplo para Week 1"""
    
    # Crear main.py
    main_content = '''from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
def read_item(name: str):
    return {"message": f"Hello {name}"}
'''
    (repo_path / "main.py").write_text(main_content)
    
    # Crear requirements.txt
    requirements_content = '''fastapi>=0.68.0
uvicorn[standard]>=0.15.0
'''
    (repo_path / "requirements.txt").write_text(requirements_content)
    
    # Crear README.md
    readme_content = '''# Week 1 - Hello World API

Este proyecto implementa una API básica usando FastAPI.

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn main:app --reload
```

## Endpoints

- GET `/` - Retorna un saludo básico
- GET `/hello/{name}` - Retorna un saludo personalizado
- GET `/docs` - Documentación automática

## Reflexión sobre FastAPI

FastAPI es un framework moderno para crear APIs web con Python. 
Proporciona documentación automática y validación de tipos.
'''
    (repo_path / "README.md").write_text(readme_content)

def run_week01_evaluation_simple(repo_path: str):
    """
    Ejecuta una evaluación simplificada de Week 1
    """
    from weeks.week01.checks.endpoints import check_endpoints
    from weeks.week01.checks.documentation import check_documentation
    from weeks.week01.checks.structure import check_project_structure
    
    # Ejecutar todos los checks
    results = {}
    
    print("Ejecutando checks de endpoints...")
    results["endpoints"] = check_endpoints(repo_path)
    
    print("Ejecutando checks de documentación...")
    results["documentation"] = check_documentation(repo_path)
    
    print("Ejecutando checks de estructura...")
    results["project_structure"] = check_project_structure(repo_path)
    
    # Calcular score simplificado
    total_score = 0
    total_checks = 0
    
    for check_name, check_result in results.items():
        if isinstance(check_result, dict) and "score" in check_result:
            score = check_result["score"]
            total_score += score
            total_checks += 1
            print(f"  {check_name}: {score:.1f}/100")
    
    final_score = total_score / total_checks if total_checks > 0 else 0
    passed = final_score >= 70
    
    print(f"\n🎯 EVALUACIÓN SEMANA 1")
    print(f"Score final: {final_score:.1f}/100")
    print(f"Estado: {'✅ APROBADO' if passed else '❌ REPROBADO'}")
    print(f"Umbral de aprobación: 70%")
    
    # Mostrar detalles por check
    print(f"\n📊 DETALLES POR CHECK:")
    for check_name, check_result in results.items():
        passed_check = check_result.get("passed", False)
        score = check_result.get("score", 0)
        status = "✅" if passed_check else "❌"
        print(f"  {status} {check_name}: {score:.1f}/100")
        
        # Mostrar errores si los hay
        if "error" in check_result:
            print(f"    ⚠️  Error: {check_result['error']}")
    
    return {
        "final_score": final_score,
        "passed": passed,
        "results": results,
        "summary": f"Evaluación Week 1 - Score: {final_score:.1f}/100 - {'APROBADO' if passed else 'REPROBADO'}"
    }

if __name__ == "__main__":
    print("🚀 EVALUADOR WEEK 01 - VERSIÓN SIMPLIFICADA")
    print("=" * 50)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir)
        print(f"📁 Creando repositorio de prueba: {repo_path}")
        
        # Crear repositorio de ejemplo
        create_sample_repo(repo_path)
        print("✅ Repositorio de ejemplo creado exitosamente")
        
        # Listar archivos creados
        print("\n📄 Archivos en el repositorio:")
        for file in repo_path.iterdir():
            print(f"  - {file.name}")
        
        print(f"\n🔍 INICIANDO EVALUACIÓN...")
        print("-" * 30)
        
        # Ejecutar evaluación
        evaluation_result = run_week01_evaluation_simple(str(repo_path))
        
        print(f"\n✨ EVALUACIÓN COMPLETADA")
        print(f"📋 Resumen: {evaluation_result['summary']}")
