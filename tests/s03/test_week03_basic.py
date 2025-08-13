"""
Tests básicos para Week 03 - Base de Datos con SQLAlchemy
"""
import sys
import tempfile
import shutil
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from weeks.week03.evaluator import Week03Evaluator
import pytest


def test_week03_evaluator_creation():
    """Test que el evaluador de Week 03 se puede crear correctamente"""
    with tempfile.TemporaryDirectory() as temp_dir:
        evaluator = Week03Evaluator(temp_dir)
        assert evaluator.week_number == 3
        assert evaluator.repo_path == Path(temp_dir).resolve()


def test_week03_missing_files():
    """Test evaluación con archivos faltantes"""
    with tempfile.TemporaryDirectory() as temp_dir:
        evaluator = Week03Evaluator(temp_dir)
        results = evaluator.evaluate()
        
        # Debe fallar por archivos faltantes
        assert results["final_score"] < 50
        assert "results" in results
        
        # Verificar que detecta archivos faltantes
        eval_results = results["results"]
        file_structure = eval_results.get("file_structure", {})
        assert not file_structure.get("main.py", True)
        assert not file_structure.get("requirements.txt", True)
        assert not file_structure.get("README.md", True)


def test_week03_basic_structure():
    """Test evaluación con estructura básica correcta"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Crear archivos básicos
        (temp_path / "main.py").write_text("""
from fastapi import FastAPI
from sqlalchemy import create_engine

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
""")
        
        (temp_path / "requirements.txt").write_text("""
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
""")
        
        (temp_path / "README.md").write_text("""
# FastAPI Week 3 - Database with SQLAlchemy

This project demonstrates integration of FastAPI with SQLAlchemy database.

## Features
- FastAPI application
- SQLAlchemy ORM integration
- Database models
- CRUD operations
""")
        
        evaluator = Week03Evaluator(str(temp_path))
        results = evaluator.evaluate()
        
        # Debe pasar las verificaciones básicas
        assert "results" in results
        assert "final_score" in results
        
        # Verificar estructura de archivos en results
        eval_results = results["results"]
        file_structure = eval_results.get("file_structure", {})
        assert file_structure.get("main.py", False)
        assert file_structure.get("requirements.txt", False)
        assert file_structure.get("README.md", False)
        
        # Verificar dependencias básicas
        dependencies = eval_results.get("dependencies", {})
        assert dependencies.get("fastapi", False)
        assert dependencies.get("uvicorn", False)
        assert dependencies.get("sqlalchemy", False)


def test_week03_sqlalchemy_dependencies():
    """Test verificación de dependencias específicas de SQLAlchemy"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Crear requirements.txt con dependencias de SQLAlchemy
        (temp_path / "requirements.txt").write_text("""
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.7
""")
        
        (temp_path / "main.py").write_text("# Basic FastAPI app")
        (temp_path / "README.md").write_text("# Week 3 Project")
        
        evaluator = Week03Evaluator(str(temp_path))
        results = evaluator.evaluate()
        
        # Verificar que detecta dependencias SQLAlchemy
        eval_results = results["results"]
        sqlalchemy_deps = eval_results.get("sqlalchemy_dependencies", {})
        
        assert "details" in sqlalchemy_deps
        details = sqlalchemy_deps["details"]
        assert details.get("sqlalchemy_present", False)
        # No debe esperar driver en esta prueba específica


def test_week03_database_connection_detection():
    """Test detección de configuración de conexión a base de datos"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Crear archivos con configuración de base de datos
        (temp_path / "main.py").write_text("""
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""")
        
        (temp_path / "requirements.txt").write_text("fastapi\nsqlalchemy\nuvicorn")
        (temp_path / "README.md").write_text("# Week 3 Project")
        
        evaluator = Week03Evaluator(str(temp_path))
        results = evaluator.evaluate()
        
        # Verificar detección de conexión de BD
        eval_results = results["results"]
        db_connection = eval_results.get("database_connection", {})
        
        assert db_connection.get("passed", False) or db_connection.get("score", 0) > 0


def test_week03_feedback_generation():
    """Test generación de feedback específico para Week 3"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Crear solo main.py sin dependencias
        (temp_path / "main.py").write_text("print('hello')")
        
        evaluator = Week03Evaluator(str(temp_path))
        results = evaluator.evaluate()
        
        # Debe generar feedback específico
        assert "report" in results
        report_text = results["report"]
        
        # Verificar que incluye feedback de Week 3
        assert isinstance(report_text, str)
        report_lower = report_text.lower()
        assert any(word in report_lower for word in ["requirements.txt", "sqlalchemy", "readme", "database"])


if __name__ == "__main__":
    pytest.main([__file__])
