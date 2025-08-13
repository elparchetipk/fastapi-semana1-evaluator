"""
Tests end-to-end para Week 03 - Base de Datos con SQLAlchemy
"""
import sys
import tempfile
import shutil
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from weeks.week03.evaluator import Week03Evaluator


def test_week03_perfect_repository():
    """Test evaluación con repositorio perfecto de Week 3"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Crear main.py completo con SQLAlchemy
        (temp_path / "main.py").write_text("""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel
from typing import List, Optional

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    title: str
    content: str
    author_id: int

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    
    class Config:
        orm_mode = True

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Week 3 - Database Integration")

# User CRUD endpoints
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}

# Post CRUD endpoints
@app.post("/posts/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts/", response_model=List[PostResponse])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts

@app.get("/posts/{post_id}", response_model=PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}

@app.get("/")
def read_root():
    return {"message": "FastAPI Week 3 - Database Integration"}
""")
        
        # Crear requirements.txt completo
        (temp_path / "requirements.txt").write_text("""
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
""")
        
        # Crear README.md detallado
        (temp_path / "README.md").write_text("""
# FastAPI Week 3 - Database Integration

This project demonstrates integration of FastAPI with SQLAlchemy for database operations.

## Features

- **FastAPI Application**: Modern, fast web framework for building APIs
- **SQLAlchemy ORM**: Object-Relational Mapping for database operations
- **Database Models**: User and Post models with relationships
- **CRUD Operations**: Complete Create, Read, Update, Delete operations
- **Data Relationships**: Foreign keys and relationships between tables
- **Data Validation**: Pydantic models for request/response validation
- **Dependency Injection**: Database session management with FastAPI dependencies

## Models

### User Model
- id: Primary key
- name: User's name (required)
- email: User's email (unique, required)
- posts: Relationship to user's posts

### Post Model
- id: Primary key
- title: Post title (required)
- content: Post content
- author_id: Foreign key to User
- author: Relationship to post author

## Endpoints

### Users
- POST /users/ - Create new user
- GET /users/ - List all users
- GET /users/{user_id} - Get specific user
- PUT /users/{user_id} - Update user
- DELETE /users/{user_id} - Delete user

### Posts
- POST /posts/ - Create new post
- GET /posts/ - List all posts
- GET /posts/{post_id} - Get specific post
- DELETE /posts/{post_id} - Delete post

## Database

Uses SQLite database with SQLAlchemy ORM. Tables are created automatically on startup.

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000
API documentation at http://localhost:8000/docs

## Architecture

- **Database Layer**: SQLAlchemy models and session management
- **API Layer**: FastAPI endpoints with dependency injection
- **Validation Layer**: Pydantic models for data validation
- **Relationship Management**: Proper foreign keys and relationships
""")
        
        evaluator = Week03Evaluator(str(temp_path))
        results = evaluator.evaluate()
        
        # Debe tener score muy alto para aprobar (≥75)
        assert results["final_score"] >= 90
        
        # Verificaciones de estructura básica
        file_structure = results["results"]["file_structure"]
        assert file_structure["main.py"]
        assert file_structure["requirements.txt"]
        assert file_structure["README.md"]
        
        # Verificaciones de dependencias
        dependencies = results["results"]["dependencies"]
        assert dependencies["fastapi"]
        assert dependencies["sqlalchemy"]
        assert dependencies["uvicorn"]
        
        # Verificaciones específicas de Week 3
        models_definition = results["results"]["models_definition"]
        
        # Dependencias SQLAlchemy
        sqlalchemy_deps = results["results"]["sqlalchemy_dependencies"]
        assert sqlalchemy_deps["passed"]
        assert sqlalchemy_deps["score"] >= 7
        
        # Conexión de base de datos
        db_connection = results["results"]["database_connection"]
        assert db_connection["passed"]
        assert db_connection["score"] >= 6
        
        # Modelos SQLAlchemy
        models = models_definition
        assert models["passed"]
        assert models["score"] >= 6
        
        # Operaciones CRUD
        crud_operations = ["create_with_db", "read_with_db", "update_with_db", "delete_with_db"]
        for crud_op in crud_operations:
            crud_result = results["results"][crud_op]
            assert crud_result["score"] > 0  # Al menos algo detectado
        
        # Feedback debe ser principalmente positivo en el reporte
        report = results["report"]
        assert len(report) > 200  # Debe tener contenido substancial


def test_week03_good_repository():
    """Test evaluación con repositorio bueno pero no perfecto"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Crear main.py con funcionalidad básica pero completa (sin relaciones complejas)
        (temp_path / "main.py").write_text("""
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    return {"message": "User created", "id": user.id}

@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "name": user.name, "email": user.email}

@app.put("/users/{user_id}")
def update_user(user_id: int, name: str, email: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.name = name
    db_user.email = email
    db.commit()
    return {"message": "User updated"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}

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
# FastAPI Week 3

Basic FastAPI application with SQLAlchemy database integration.

## Features
- FastAPI app
- SQLAlchemy models
- Basic CRUD operations
""")
        
        evaluator = Week03Evaluator(str(temp_path))
        results = evaluator.evaluate()
        
        # Debe tener score alto para aprobar (≥75) pero puede ser perfecto
        assert results["final_score"] >= 75
        
        # Debe pasar verificaciones básicas
        assert results["results"]["file_structure"]["main.py"]
        assert results["results"]["dependencies"]["sqlalchemy"]
        
        # Debe detectar algunas funcionalidades
        assert results["results"]["database_connection"]["score"] > 0
        assert results["results"]["models_definition"]["score"] > 0


def test_week03_cli_integration():
    """Test integración con CLI de evaluación"""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Crear repositorio básico
        (temp_path / "main.py").write_text("""
from fastapi import FastAPI
from sqlalchemy import create_engine

app = FastAPI()
engine = create_engine("sqlite:///test.db")

@app.get("/")
def read_root():
    return {"message": "Hello World"}
""")
        
        (temp_path / "requirements.txt").write_text("fastapi\nsqlalchemy\nuvicorn")
        (temp_path / "README.md").write_text("# Week 3 Project")
        
        # Test que se puede importar y usar desde CLI
        from weeks.week03.evaluator import run_week03_evaluation
        
        results = run_week03_evaluation(str(temp_path))
        
        assert "final_score" in results
        assert "report" in results
        assert isinstance(results["final_score"], (int, float))
        assert isinstance(results["report"], str)
