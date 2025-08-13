"""
Tests para Week 03 con repositorios que tienen errores
"""
import sys
import tempfile
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from weeks.week03.evaluator import Week03Evaluator


def test_week03_syntax_errors():
    """Test evaluación con errores de sintaxis"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Crear main.py con errores de sintaxis
        (temp_path / "main.py").write_text("""
from fastapi import FastAPI
app = FastAPI(

@app.get("/")
def read_root(
    return {"message": "Hello World"
""")
        
        (temp_path / "requirements.txt").write_text("fastapi\nsqlalchemy\nuvicorn")
        (temp_path / "README.md").write_text("# Week 3 Project")
        
        evaluator = Week03Evaluator(str(temp_path))
        results = evaluator.evaluate()
        
        # Debe detectar errores de sintaxis
        syntax_validation = results["results"]["syntax_validation"]
        main_syntax = syntax_validation.get("main.py", {})
        assert not main_syntax.get("syntax_valid", True)


def test_week03_missing_dependencies():
    """Test evaluación con dependencias faltantes"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Crear archivos sin dependencias SQLAlchemy
        (temp_path / "main.py").write_text("""
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
""")
        
        (temp_path / "requirements.txt").write_text("fastapi==0.104.1")  # Solo FastAPI, sin SQLAlchemy
        (temp_path / "README.md").write_text("# Week 3 Project")
        
        evaluator = Week03Evaluator(str(temp_path))
        results = evaluator.evaluate()
        
        # Debe detectar dependencias faltantes
        dependencies = results["results"]["dependencies"]
        assert dependencies.get("fastapi", False)
        assert not dependencies.get("sqlalchemy", True)
        
        # Verificar feedback sobre dependencias faltantes
        report = results["report"]
        assert "sqlalchemy" in report.lower() or "sql" in report.lower()


def test_week03_incomplete_database_setup():
    """Test evaluación con configuración incompleta de base de datos"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Crear archivos con FastAPI pero sin configuración de BD
        (temp_path / "main.py").write_text("""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/items/")
def create_item(item: dict):
    # Sin usar base de datos
    return item
""")
        
        (temp_path / "requirements.txt").write_text("fastapi\nsqlalchemy\nuvicorn")
        (temp_path / "README.md").write_text("# Week 3 Project")
        
        evaluator = Week03Evaluator(str(temp_path))
        results = evaluator.evaluate()
        
        # Debe detectar configuración incompleta
        database_connection = results["results"]["database_connection"]
        db_connection = database_connection
        
        # Score debe ser bajo por falta de configuración real de BD
        assert db_connection.get("score", 10) < 5


def test_week03_no_crud_operations():
    """Test evaluación sin operaciones CRUD reales"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Crear archivos con modelos pero sin CRUD
        (temp_path / "main.py").write_text("""
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
""")
        
        (temp_path / "requirements.txt").write_text("fastapi\nsqlalchemy\nuvicorn")
        (temp_path / "README.md").write_text("# Week 3 Project")
        
        evaluator = Week03Evaluator(str(temp_path))
        results = evaluator.evaluate()
        
        # Debe detectar modelos pero falta CRUD
        models_definition = results["results"]["models_definition"]
        
        models = models_definition
        assert models.get("score", 0) > 0  # Modelos definidos
        
        # CRUD operations deben tener score bajo
        crud_checks = ["create_with_db", "read_with_db", "update_with_db", "delete_with_db"]
        for crud_check in crud_checks:
            crud_result = results["results"].get(crud_check, {})
            assert crud_result.get("score", 10) < 5


def test_week03_no_models():
    """Test evaluación sin modelos SQLAlchemy"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Crear archivos sin modelos SQLAlchemy
        (temp_path / "main.py").write_text("""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/items/")
def create_item(item: dict):
    return {"id": 1, **item}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"id": item_id, "name": "Sample Item"}
""")
        
        (temp_path / "requirements.txt").write_text("fastapi\nsqlalchemy\nuvicorn")
        (temp_path / "README.md").write_text("# Week 3 Project")
        
        evaluator = Week03Evaluator(str(temp_path))
        results = evaluator.evaluate()
        
        # Debe detectar falta de modelos
        models_definition = results["results"]["models_definition"]
        models = models_definition
        
        assert not models.get("passed", True)
        assert models.get("score", 10) < 3


def test_week03_overall_broken_score():
    """Test que repositorios rotos tienen score general bajo"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Crear repositorio con múltiples problemas
        (temp_path / "main.py").write_text("# Archivo casi vacío")
        (temp_path / "requirements.txt").write_text("fastapi")  # Falta SQLAlchemy
        
        evaluator = Week03Evaluator(str(temp_path))
        results = evaluator.evaluate()
        
        # Score general debe ser muy bajo (bien por debajo del umbral de 75)
        assert results["final_score"] < 50
        
        # Debe tener feedback extenso
        assert len(results["report"]) > 100  # El reporte debe tener contenido substancial
