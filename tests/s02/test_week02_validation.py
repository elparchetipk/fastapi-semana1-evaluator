#!/usr/bin/env python3
"""
Test simple para validar Week02 evaluator
"""
import tempfile
import sys
from pathlib import Path

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def test_week02_evaluation():
    """Test básico de evaluación Week02"""
    from weeks.week02.evaluator import Week02Evaluator
    
    # Código mínimo CRUD
    main_code = '''from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    price: float

items = []

@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return item

@app.get("/items")
def read_items():
    return items

@app.get("/items/{item_id}")
def read_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404)

@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: Item):
    for i, item in enumerate(items):
        if item.id == item_id:
            items[i] = updated_item
            return updated_item
    raise HTTPException(status_code=404)

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for i, item in enumerate(items):
        if item.id == item_id:
            del items[i]
            return {"message": "deleted"}
    raise HTTPException(status_code=404)
'''
    
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_path = Path(temp_dir)
        
        # Crear archivos
        (repo_path / "main.py").write_text(main_code)
        (repo_path / "requirements.txt").write_text("fastapi\nuvicorn\npydantic\n")
        (repo_path / "README.md").write_text("# Week 2 CRUD\nBasic CRUD implementation\n")
        
        # Crear evaluador y ejecutar
        evaluator = Week02Evaluator(str(repo_path))
        results = evaluator.evaluate()
        
        print(f"Score: {results['final_score']}")
        print(f"Passed: {results.get('passed', False)}")
        
        # Verificar operaciones CRUD
        crud = results['results'].get('crud_operations', {})
        print(f"CRUD Operations:")
        print(f"  Create: {crud.get('create_operation', False)}")
        print(f"  Read: {crud.get('read_operation', False)}")
        print(f"  Read All: {crud.get('read_all_operation', False)}")
        print(f"  Update: {crud.get('update_operation', False)}")
        print(f"  Delete: {crud.get('delete_operation', False)}")
        
        return results['final_score'] >= 70

if __name__ == "__main__":
    success = test_week02_evaluation()
    print(f"\nTest {'PASSED' if success else 'FAILED'}")
