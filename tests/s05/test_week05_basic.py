"""
Tests básicos para Week 5 - Testing y Documentación
"""
import pytest
import tempfile
import shutil
from pathlib import Path
import sys

# Agregar el directorio padre al path para importar el evaluador
sys.path.append(str(Path(__file__).parent.parent.parent))

from weeks.week05.evaluator import Week05Evaluator


@pytest.fixture
def temp_repo():
    """Crear un repositorio temporal para tests"""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def basic_week05_repo(temp_repo):
    """Crear un repositorio básico de Week 5"""
    # Crear estructura básica
    (temp_repo / "main.py").write_text("""
from fastapi import FastAPI

app = FastAPI(
    title="Test API",
    description="API for testing",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
""")
    
    (temp_repo / "requirements.txt").write_text("""
fastapi>=0.68.0
uvicorn[standard]>=0.15.0
pytest>=6.0.0
httpx>=0.24.0
pytest-asyncio>=0.15.0
sqlalchemy>=1.4.0
pydantic>=1.8.0
""")
    
    # Crear directorio de tests básico
    tests_dir = temp_repo / "tests"
    tests_dir.mkdir()
    
    (tests_dir / "__init__.py").write_text("")
    
    (tests_dir / "conftest.py").write_text("""
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_db():
    # Configuración de base de datos de testing
    return "sqlite:///:memory:"
""")
    
    (tests_dir / "test_api.py").write_text("""
import pytest
from fastapi.testclient import TestClient

def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_read_item(client):
    response = client.get("/items/123")
    assert response.status_code == 200
    assert response.json() == {"item_id": 123}

def test_invalid_item(client):
    response = client.get("/items/invalid")
    assert response.status_code == 422
""")
    
    (temp_repo / "README.md").write_text("""
# Test API

## Installation

```bash
pip install -r requirements.txt
```

## Running the application

```bash
uvicorn main:app --reload
```

## Testing

```bash
pytest
```

## Deployment

This application can be deployed using Docker or directly with uvicorn.

## Environment Variables

- DATABASE_URL: Database connection string
""")
    
    return temp_repo


class TestWeek05Basic:
    """Tests básicos para evaluador de Week 5"""
    
    def test_evaluator_creation(self, basic_week05_repo):
        """Test creación del evaluador"""
        evaluator = Week05Evaluator(str(basic_week05_repo))
        assert evaluator.week_number == 5
        assert evaluator.repo_path == basic_week05_repo
    
    def test_basic_structure_check(self, basic_week05_repo):
        """Test verificación de estructura básica"""
        evaluator = Week05Evaluator(str(basic_week05_repo))
        results = evaluator.run_specific_checks()
        
        # Verificar que se ejecutan todos los checks principales
        assert "pytest_configuration" in results
        assert "test_dependencies" in results
        assert "test_structure" in results
        assert "test_database_config" in results
        assert "model_tests" in results
        assert "endpoint_tests" in results
    
    def test_pytest_configuration_check(self, basic_week05_repo):
        """Test verificación de configuración de pytest"""
        evaluator = Week05Evaluator(str(basic_week05_repo))
        results = evaluator.run_specific_checks()
        
        pytest_config = results["pytest_configuration"]
        assert "tests_directory_exists" in pytest_config
        assert pytest_config["tests_directory_exists"] is True
    
    def test_test_dependencies_check(self, basic_week05_repo):
        """Test verificación de dependencias de testing"""
        evaluator = Week05Evaluator(str(basic_week05_repo))
        results = evaluator.run_specific_checks()
        
        test_deps = results["test_dependencies"]
        assert "dependencies_found" in test_deps
        deps = test_deps["dependencies_found"]
        assert deps.get("pytest") is True
        assert deps.get("httpx") is True
    
    def test_endpoint_tests_check(self, basic_week05_repo):
        """Test verificación de tests de endpoints"""
        evaluator = Week05Evaluator(str(basic_week05_repo))
        results = evaluator.run_specific_checks()
        
        endpoint_tests = results["endpoint_tests"]
        assert "endpoint_test_functions" in endpoint_tests
        assert endpoint_tests["endpoint_test_functions"] > 0
        assert "GET" in endpoint_tests.get("http_methods_tested", [])
    
    def test_deployment_readme_check(self, basic_week05_repo):
        """Test verificación de documentación de deployment"""
        evaluator = Week05Evaluator(str(basic_week05_repo))
        results = evaluator.run_specific_checks()
        
        deployment_readme = results["deployment_readme"]
        assert "deployment_readme" in deployment_readme
        assert "deployment_sections" in deployment_readme
        
        sections = deployment_readme["deployment_sections"]
        assert "Installation" in sections
        assert "Run instructions" in sections


def test_week05_placeholder():
    """Test básico de funcionamiento"""
    assert True
