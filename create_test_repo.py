#!/usr/bin/env python3
"""Script para crear un repositorio de prueba para Week 5"""

import tempfile
from pathlib import Path
import sys

sys.path.append('.')

from tests.s05.test_week05_integration import create_mock_week05_repo

# Crear repo de prueba en /tmp
repo_path = Path("/tmp/test_week05_repo")
create_mock_week05_repo(repo_path)

print(f"✅ Repositorio de prueba creado en: {repo_path}")
print("Estructura creada:")
for item in repo_path.rglob("*"):
    if item.is_file():
        print(f"  📄 {item.relative_to(repo_path)}")
    elif item.is_dir():
        print(f"  📁 {item.relative_to(repo_path)}/")
