#!/usr/bin/env python3
"""
Script para crear un repositorio de prueba y probar la funcionalidad completa de Week01
"""
import tempfile
import os
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

def test_week01_full_evaluation():
    """Test completo de evaluación con repositorio de ejemplo"""
    print("=== Test Evaluación Completa Week01 ===")
    
    from weeks.week01.evaluator import Week01Evaluator
    
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir)
        print(f"Creando repositorio de prueba en: {repo_path}")
        
        # Crear repositorio de ejemplo
        create_sample_repo(repo_path)
        print("✓ Repositorio de ejemplo creado")
        
        # Listar archivos creados
        print("Archivos creados:")
        for file in repo_path.iterdir():
            print(f"  - {file.name}")
        
        try:
            # Crear evaluador
            evaluator = Week01Evaluator(str(repo_path))
            print("✓ Evaluador creado exitosamente")
            
            # Ejecutar evaluación completa
            print("\n--- Ejecutando evaluación completa ---")
            results = evaluator.evaluate()
            print("✓ Evaluación completa terminada")
            
            # Mostrar resultados
            print(f"\nScore final: {results.get('score', 'N/A')}")
            print(f"Passed: {results.get('passed', 'N/A')}")
            
            # Mostrar resultados detallados
            print("\n--- Resultados detallados ---")
            checks = results.get('checks', {})
            for check_name, check_result in checks.items():
                print(f"\n{check_name}:")
                if isinstance(check_result, dict):
                    for key, value in check_result.items():
                        if key != 'details':  # Evitar demasiado detalle
                            print(f"  {key}: {value}")
                else:
                    print(f"  Resultado: {check_result}")
            
            # Mostrar feedback
            if 'feedback' in results:
                print("\n--- Feedback ---")
                for feedback_item in results['feedback']:
                    print(f"  {feedback_item}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error en evaluación completa: {e}")
            import traceback
            traceback.print_exc()
            return False

def test_week01_individual_checks():
    """Test de checks individuales"""
    print("\n=== Test Checks Individuales ===")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir)
        create_sample_repo(repo_path)
        
        # Test check_endpoints
        try:
            from weeks.week01.checks.endpoints import check_endpoints
            result = check_endpoints(str(repo_path))
            print(f"✓ check_endpoints: {result}")
        except Exception as e:
            print(f"✗ Error en check_endpoints: {e}")
        
        # Test check_documentation
        try:
            from weeks.week01.checks.documentation import check_documentation
            result = check_documentation(str(repo_path))
            print(f"✓ check_documentation: {result}")
        except Exception as e:
            print(f"✗ Error en check_documentation: {e}")
        
        # Test check_project_structure
        try:
            from weeks.week01.checks.structure import check_project_structure
            result = check_project_structure(str(repo_path))
            print(f"✓ check_project_structure: {result}")
        except Exception as e:
            print(f"✗ Error en check_project_structure: {e}")

if __name__ == "__main__":
    print("Iniciando test completo de Week01Evaluator...")
    
    test_week01_individual_checks()
    success = test_week01_full_evaluation()
    
    if success:
        print("\n🎉 Test completo de Week01 exitoso")
    else:
        print("\n❌ Se encontraron errores en el test completo")
