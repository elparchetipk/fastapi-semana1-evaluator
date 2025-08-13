#!/usr/bin/env python3

import sys
from pathlib import Path

# Test script para debuggear week05 evaluator

# Agregar paths
sys.path.append('.')
sys.path.append('weeks/week05/checks')
weeks_path = Path('weeks/week05/checks')
sys.path.append(str(weeks_path))

print("Python paths:")
for p in sys.path[-5:]:
    print(f"  {p}")

print("\nChecks directory exists:", weeks_path.exists())
print("Checks directory contents:")
for f in weeks_path.iterdir():
    print(f"  {f.name}")

print("\nTrying direct import of pytest_config...")
try:
    import pytest_config
    print("✓ pytest_config imported successfully")
    print("Functions available:", [x for x in dir(pytest_config) if not x.startswith('_')])
    
    if hasattr(pytest_config, 'check_pytest_configuration'):
        print("✓ check_pytest_configuration function found")
        # Test con un directorio temporal
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            result = pytest_config.check_pytest_configuration(tmpdir)
            print("✓ Function executed successfully")
            print("Result:", result)
    else:
        print("✗ check_pytest_configuration function not found")
        
except ImportError as e:
    print(f"✗ Import failed: {e}")
except Exception as e:
    print(f"✗ Execution failed: {e}")

print("\nTrying Week05Evaluator...")
try:
    from weeks.week05.evaluator import Week05Evaluator
    print("✓ Week05Evaluator imported successfully")
    
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        evaluator = Week05Evaluator(tmpdir)
        print("✓ Evaluator created successfully")
        
        results = evaluator.run_specific_checks()
        print("✓ run_specific_checks executed")
        print("Results keys:", list(results.keys()))
        
        if 'pytest_configuration' in results:
            print("pytest_configuration result:", results['pytest_configuration'])
        
except Exception as e:
    print(f"✗ Week05Evaluator failed: {e}")
    import traceback
    traceback.print_exc()
