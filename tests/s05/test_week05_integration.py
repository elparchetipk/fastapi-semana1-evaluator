import pytest
import tempfile
import os
from pathlib import Path
import sys

# Agregar el directorio principal al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from w    def test_empty_repository_evaluation(self):
        """Test con repositorio vacío para verificar que maneja casos edge"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            
            # Solo crear directorio vacío
            evaluator = Week05Evaluator(str(repo_path))
            result = evaluator.evaluate()k05.evaluator import Week05Evaluator


def create_mock_week05_repo(base_dir: Path):
    """Crear un repositorio mock para Week 5 con estructura básica"""
    
    # Crear estructura básica de FastAPI
    (base_dir / "app").mkdir()
    (base_dir / "app" / "__init__.py").touch()
    
    # main.py con configuración básica
    main_content = '''from fastapi import FastAPI

app = FastAPI(
    title="API de Reservas",
    description="Sistema de reservas para restaurante",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "API funcionando"}

@app.get("/reservas/")
def get_reservas():
    return {"reservas": []}
'''
    (base_dir / "app" / "main.py").write_text(main_content)
    
    # models.py con modelos de SQLAlchemy
    models_content = '''from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Reserva(Base):
    __tablename__ = "reservas"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    fecha = Column(DateTime, nullable=False)
    personas = Column(Integer, nullable=False)
'''
    (base_dir / "app" / "models.py").write_text(models_content)
    
    # Crear directorio tests con estructura básica
    (base_dir / "tests").mkdir()
    (base_dir / "tests" / "__init__.py").touch()
    
    # conftest.py para configuración de tests
    conftest_content = '''import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)
'''
    (base_dir / "tests" / "conftest.py").write_text(conftest_content)
    
    # test_main.py con tests básicos
    test_main_content = '''import pytest
from fastapi.testclient import TestClient
from app.main import app

def test_read_root():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API funcionando"}

def test_get_reservas():
    client = TestClient(app)
    response = client.get("/reservas/")
    assert response.status_code == 200
    assert "reservas" in response.json()
'''
    (base_dir / "tests" / "test_main.py").write_text(test_main_content)
    
    # test_models.py con tests de modelos
    test_models_content = '''import pytest
from app.models import Reserva

def test_reserva_creation():
    reserva = Reserva(
        nombre="Juan Pérez",
        personas=4
    )
    assert reserva.nombre == "Juan Pérez"
    assert reserva.personas == 4
'''
    (base_dir / "tests" / "test_models.py").write_text(test_models_content)
    
    # pytest.ini con configuración
    pytest_ini_content = '''[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
'''
    (base_dir / "pytest.ini").write_text(pytest_ini_content)
    
    # requirements.txt con dependencias de testing
    requirements_content = '''fastapi>=0.68.0
uvicorn>=0.15.0
sqlalchemy>=1.4.0
pytest>=6.0.0
pytest-asyncio>=0.21.0
httpx>=0.24.0
'''
    (base_dir / "requirements.txt").write_text(requirements_content)
    
    # README.md con documentación de deployment
    readme_content = '''# API de Reservas

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn app.main:app --reload
```

## Tests

```bash
pytest
```

## Deployment

### Docker

```bash
docker build -t reservas-api .
docker run -p 8000:8000 reservas-api
```

### Variables de entorno

- `DATABASE_URL`: URL de la base de datos
- `SECRET_KEY`: Clave secreta para JWT
'''
    (base_dir / "README.md").write_text(readme_content)
    
    return base_dir


class TestWeek05Integration:
    """Tests de integración para Week 5"""
    
    def test_complete_repository_evaluation(self):
        """Test completo con un repositorio mock que debería obtener buena puntuación"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            create_mock_week05_repo(repo_path)
            
            # Crear evaluador y ejecutar
            evaluator = Week05Evaluator(str(repo_path))
            result = evaluator.evaluate()
            
            # Verificaciones básicas
            assert result is not None
            assert 'evaluation' in result
            assert 'total_score' in result['evaluation']
            assert 'max_score' in result['evaluation']
            
            # Debería tener una puntuación razonable (al menos 50%)
            total_score = result['evaluation']['total_score']
            max_score = result['evaluation']['max_score']
            percentage = (total_score / max_score) * 100 if max_score > 0 else 0
            
            print(f"Puntuación obtenida: {total_score}/{max_score} ({percentage:.1f}%)")
            assert percentage >= 50, f"Puntuación muy baja: {percentage:.1f}%"
            
            # Verificar que los checks principales funcionan
            checks = result['evaluation']['checks']
            assert 'pytest_configuration' in checks
            assert 'test_dependencies' in checks
            assert 'test_structure' in checks
            
    def test_empty_repository_evaluation(self):
        """Test con repositorio vacío para verificar que maneja casos edge"""
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_path = Path(tmpdir)
            
            # Solo crear directorio vacío
            evaluator = Week05Evaluator(str(repo_path))
            result = evaluator.evaluate(str(repo_path))
            
            # Debería funcionar pero con puntuación baja
            assert result is not None
            assert 'evaluation' in result
            
            total_score = result['evaluation']['total_score']
            max_score = result['evaluation']['max_score']
            percentage = (total_score / max_score) * 100 if max_score > 0 else 0
            
            print(f"Puntuación repositorio vacío: {total_score}/{max_score} ({percentage:.1f}%)")
            assert percentage < 20, f"Puntuación demasiado alta para repo vacío: {percentage:.1f}%"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
