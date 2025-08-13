#!/usr/bin/env python3
"""Script para examinar la estructura del resultado del evaluador"""

import sys
import tempfile
from pathlib import Path

sys.path.append('.')

from weeks.week05.evaluator import Week05Evaluator

# Crear un directorio temporal simple
with tempfile.TemporaryDirectory() as tmpdir:
    repo_path = Path(tmpdir)
    
    # Crear estructura mínima
    (repo_path / "app").mkdir()
    (repo_path / "app" / "__init__.py").touch()
    (repo_path / "tests").mkdir()
    (repo_path / "tests" / "__init__.py").touch()
    
    # Crear evaluador
    evaluator = Week05Evaluator(str(repo_path))
    result = evaluator.evaluate()
    
    print("=== Estructura del resultado ===")
    print(f"Tipo: {type(result)}")
    print(f"Claves: {list(result.keys())}")
    
    for key, value in result.items():
        print(f"\n{key}: {type(value)}")
        if isinstance(value, dict):
            print(f"  Subclaves: {list(value.keys())}")
        elif isinstance(value, list):
            print(f"  Elementos: {len(value)}")
        else:
            print(f"  Valor: {value}")
