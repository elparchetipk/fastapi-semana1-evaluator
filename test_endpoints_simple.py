#!/usr/bin/env python3
"""
Test simple para diagnosticar problemas con endpoints.py
"""
import sys
from pathlib import Path

# Agregar paths
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

print("Testing endpoints module...")

try:
    # Test directo
    from weeks.week01.checks import endpoints
    print("✓ endpoints module imported")
    
    # Verificar funciones
    if hasattr(endpoints, 'check_endpoints'):
        print("✓ check_endpoints found")
        
        # Test con directorio temporal
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Crear archivos básicos
            tmp_path = Path(tmp_dir)
            (tmp_path / "main.py").write_text('from fastapi import FastAPI\napp = FastAPI()\n')
            (tmp_path / "requirements.txt").write_text('fastapi\nuvicorn\n')
            
            print(f"Testing with temp repo: {tmp_dir}")
            result = endpoints.check_endpoints(str(tmp_path))
            print(f"Result: {result}")
    else:
        print("✗ check_endpoints not found")
        print(f"Available: {dir(endpoints)}")
        
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
