#!/usr/bin/env python3
"""Script para examinar en detalle los resultados de cada check"""

import sys
import tempfile
from pathlib import Path
import json

sys.path.append('.')

from weeks.week05.evaluator import Week05Evaluator

print("=== Análisis detallado de Week 5 ===")

# Test 1: Repositorio vacío
print("\n--- Test 1: Repositorio vacío ---")
with tempfile.TemporaryDirectory() as tmpdir:
    repo_path = Path(tmpdir)
    
    evaluator = Week05Evaluator(str(repo_path))
    result = evaluator.evaluate()
    
    print(f"Final score: {result['final_score']}")
    print(f"Passed: {result['passed']}")
    
    print("\nResults by check:")
    for check_name, check_result in result['results'].items():
        print(f"  {check_name}:")
        if isinstance(check_result, dict):
            score = check_result.get('score', 'N/A')
            max_score = check_result.get('max_score', 'N/A')
            print(f"    Score: {score}/{max_score}")
            if 'error' in check_result:
                print(f"    Error: {check_result['error']}")
        else:
            print(f"    Result: {check_result}")

# Test 2: Repositorio con estructura básica
print("\n--- Test 2: Repositorio con estructura básica ---")
with tempfile.TemporaryDirectory() as tmpdir:
    repo_path = Path(tmpdir)
    
    # Crear estructura mínima
    (repo_path / "app").mkdir()
    (repo_path / "app" / "__init__.py").touch()
    (repo_path / "tests").mkdir()
    (repo_path / "tests" / "__init__.py").touch()
    (repo_path / "requirements.txt").write_text("fastapi\npytest\n")
    
    evaluator = Week05Evaluator(str(repo_path))
    result = evaluator.evaluate()
    
    print(f"Final score: {result['final_score']}")
    print(f"Passed: {result['passed']}")
    
    print("\nResults by check:")
    for check_name, check_result in result['results'].items():
        print(f"  {check_name}:")
        if isinstance(check_result, dict):
            score = check_result.get('score', 'N/A')
            max_score = check_result.get('max_score', 'N/A')
            print(f"    Score: {score}/{max_score}")
            if 'error' in check_result:
                print(f"    Error: {check_result['error']}")
        else:
            print(f"    Result: {check_result}")

# Test 3: Verificar la lógica de scoring
print("\n--- Test 3: Scoring details ---")
with tempfile.TemporaryDirectory() as tmpdir:
    repo_path = Path(tmpdir)
    
    evaluator = Week05Evaluator(str(repo_path))
    result = evaluator.evaluate()
    
    print(f"Scoring breakdown:")
    print(json.dumps(result['scoring'], indent=2))
