#!/usr/bin/env python3
"""
Script de prueba para verificar el sistema de evaluación
"""
import sys
import tempfile
import shutil
from pathlib import Path
from textwrap import dedent

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent))

def create_test_repo() -> Path:
    """
    Crea un repositorio de prueba para Week 1
    """
    # Crear directorio temporal
    test_dir = Path(tempfile.mkdtemp(prefix="fastapi_week01_test_"))
    
    # Crear main.py básico
    main_py = test_dir / "main.py"
    main_py.write_text(dedent("""
        from fastapi import FastAPI
        
        app = FastAPI()
        
        @app.get("/")
        def read_root():
            return {"message": "Hello World"}
        
        @app.get("/hello/{name}")
        def hello_name(name: str):
            return {"message": f"Hello {name}"}
        
        if __name__ == "__main__":
            import uvicorn
            uvicorn.run(app, host="0.0.0.0", port=8000)
    """).strip())
    
    # Crear requirements.txt
    requirements = test_dir / "requirements.txt"
    requirements.write_text(dedent("""
        fastapi>=0.68.0
        uvicorn[standard]>=0.15.0
    """).strip())
    
    # Crear README.md
    readme = test_dir / "README.md"
    readme.write_text(dedent("""
        # FastAPI Week 1 - Hello World
        
        Una API simple usando FastAPI.
        
        ## Instalación
        
        ```bash
        pip install -r requirements.txt
        ```
        
        ## Ejecución
        
        ```bash
        uvicorn main:app --reload
        ```
        
        ## Endpoints
        
        - `GET /` - Retorna Hello World
        - `GET /hello/{name}` - Saluda con el nombre proporcionado
        - `GET /docs` - Documentación automática
    """).strip())
    
    print(f"✅ Repositorio de prueba creado en: {test_dir}")
    return test_dir


def run_test_evaluation():
    """
    Ejecuta una evaluación de prueba
    """
    print("🧪 Iniciando prueba del sistema de evaluación...")
    
    # Crear repositorio de prueba
    test_repo = create_test_repo()
    
    try:
        # Importar y ejecutar el evaluador
        from weeks.week01.evaluator import Week01Evaluator
        
        print("📋 Ejecutando evaluación de Week 1...")
        evaluator = Week01Evaluator(str(test_repo))
        results = evaluator.evaluate()
        
        # Mostrar resultados
        print("\n📊 RESULTADOS DE LA PRUEBA:")
        print("=" * 50)
        
        final_score = results.get('final_score', 0)
        print(f"Score Final: {final_score:.1f}/100")
        print(f"Estado: {'✅ APROBADO' if final_score >= 70 else '❌ REPROBADO'}")
        
        # Mostrar checks principales
        checks = results.get('checks', {})
        print(f"\nChecks ejecutados: {len(checks)}")
        for check_name, check_result in checks.items():
            status = "✅" if check_result.get('passed', False) else "❌"
            print(f"  {status} {check_name}: {check_result.get('score', 0)}/100")
        
        # Mostrar feedback
        feedback = results.get('feedback', [])
        if feedback:
            print(f"\nFeedback ({len(feedback)} elementos):")
            for item in feedback[:5]:  # Mostrar solo los primeros 5
                print(f"  • {item}")
            if len(feedback) > 5:
                print(f"  ... y {len(feedback) - 5} más")
        
        print("\n🎉 ¡Prueba completada exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la prueba: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Limpiar repositorio de prueba
        try:
            shutil.rmtree(test_repo)
            print(f"🧹 Repositorio de prueba eliminado: {test_repo}")
        except Exception as e:
            print(f"⚠️  Error eliminando repositorio de prueba: {e}")


def test_cli():
    """
    Prueba el CLI principal
    """
    print("\n🧪 Probando CLI principal...")
    
    # Crear repositorio de prueba
    test_repo = create_test_repo()
    
    try:
        # Ejecutar el CLI
        import subprocess
        result = subprocess.run([
            sys.executable, "evaluate.py",
            "--week", "1",
            "--repo", str(test_repo),
            "--format", "summary"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        print(f"Exit code: {result.returncode}")
        print(f"Stdout:\n{result.stdout}")
        
        if result.stderr:
            print(f"Stderr:\n{result.stderr}")
        
        if result.returncode == 0:
            print("✅ CLI funcionando correctamente")
            return True
        else:
            print("❌ CLI falló")
            return False
            
    except Exception as e:
        print(f"❌ Error probando CLI: {e}")
        return False
        
    finally:
        # Limpiar
        try:
            shutil.rmtree(test_repo)
        except:
            pass


def main():
    """
    Ejecuta todas las pruebas
    """
    print("🔧 SISTEMA DE PRUEBAS - FastAPI Evaluator")
    print("=" * 60)
    
    success_count = 0
    total_tests = 2
    
    # Prueba 1: Evaluación directa
    print("\n1️⃣ PRUEBA: Evaluación directa")
    if run_test_evaluation():
        success_count += 1
    
    # Prueba 2: CLI
    print("\n2️⃣ PRUEBA: CLI principal")
    if test_cli():
        success_count += 1
    
    # Resumen final
    print(f"\n🏁 RESUMEN FINAL:")
    print(f"Pruebas exitosas: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("🎉 ¡Todas las pruebas pasaron! El sistema está listo.")
        sys.exit(0)
    else:
        print("❌ Algunas pruebas fallaron. Revisa los errores arriba.")
        sys.exit(1)


if __name__ == "__main__":
    main()
