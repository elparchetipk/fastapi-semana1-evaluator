#!/usr/bin/env python3
"""
Script de prueba para diagnosticar problemas en Week01Evaluator
"""
import tempfile
import os
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

def test_week01_basic():
    """Test básico del evaluador Week01"""
    print("=== Test Básico Week01 ===")
    
    try:
        from weeks.week01.evaluator import Week01Evaluator
        print("✓ Importación de Week01Evaluator exitosa")
    except Exception as e:
        print(f"✗ Error importando Week01Evaluator: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Crear directorio temporal
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Usando directorio temporal: {temp_dir}")
        
        try:
            evaluator = Week01Evaluator(temp_dir)
            print("✓ Creación de evaluador exitosa")
            print(f"  - Week number: {evaluator.week_number}")
            print(f"  - Repo path: {evaluator.repo_path}")
        except Exception as e:
            print(f"✗ Error creando evaluador: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Test de checks específicos
        try:
            print("\n--- Ejecutando run_specific_checks ---")
            results = evaluator.run_specific_checks()
            print("✓ run_specific_checks completado")
            print(f"Resultados obtenidos: {list(results.keys())}")
            
            for key, value in results.items():
                print(f"\n{key}:")
                if isinstance(value, dict):
                    if 'error' in value:
                        print(f"  ✗ Error: {value['error']}")
                    if 'passed' in value:
                        print(f"  Passed: {value['passed']}")
                    if 'score' in value:
                        print(f"  Score: {value['score']}")
                else:
                    print(f"  Valor: {value}")
                    
        except Exception as e:
            print(f"✗ Error en run_specific_checks: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

def test_week01_imports():
    """Test de importaciones específicas"""
    print("\n=== Test de Importaciones ===")
    
    # Test de imports desde checks
    try:
        from weeks.week01.checks.endpoints import check_endpoints
        print("✓ check_endpoints importado")
    except Exception as e:
        print(f"✗ Error importando check_endpoints: {e}")
    
    try:
        from weeks.week01.checks.documentation import check_documentation  
        print("✓ check_documentation importado")
    except Exception as e:
        print(f"✗ Error importando check_documentation: {e}")
    
    try:
        from weeks.week01.checks.structure import check_project_structure
        print("✓ check_project_structure importado")
    except Exception as e:
        print(f"✗ Error importando check_project_structure: {e}")

def test_core_imports():
    """Test de importaciones del core"""
    print("\n=== Test Core Imports ===")
    
    try:
        from core import BaseEvaluator
        print("✓ BaseEvaluator importado")
    except Exception as e:
        print(f"✗ Error importando BaseEvaluator: {e}")
    
    try:
        from core import CommonChecks
        print("✓ CommonChecks importado")
    except Exception as e:
        print(f"✗ Error importando CommonChecks: {e}")

if __name__ == "__main__":
    print("Iniciando diagnóstico de Week01Evaluator...")
    
    test_core_imports()
    test_week01_imports()
    
    success = test_week01_basic()
    
    if success:
        print("\n🎉 Todos los tests básicos pasaron")
    else:
        print("\n❌ Se encontraron errores en los tests")
