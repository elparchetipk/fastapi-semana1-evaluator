import sys
import tempfile
from pathlib import Path
# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from weeks.week02.evaluator import Week02Evaluator

SAMPLE_MAIN = '''from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)

DB = []

@app.post('/items')
def create_item(item: Item):
    if any(x.id == item.id for x in DB):
        raise HTTPException(status_code=400, detail='Item exists')
    DB.append(item)
    return item

@app.get('/items')
def list_items():
    return DB

@app.get('/items/{item_id}')
def get_item(item_id: int):
    for x in DB:
        if x.id == item_id:
            return x
    raise HTTPException(status_code=404, detail='Not Found')

@app.put('/items/{item_id}')
def update_item(item_id: int, item: Item):
    for idx, x in enumerate(DB):
        if x.id == item_id:
            DB[idx] = item
            return item
    raise HTTPException(status_code=404, detail='Not Found')

@app.delete('/items/{item_id}')
def delete_item(item_id: int):
    for idx, x in enumerate(DB):
        if x.id == item_id:
            del DB[idx]
            return {'ok': True}
    raise HTTPException(status_code=404, detail='Not Found')
'''

REQS = 'fastapi\nuvicorn\npydantic\n'
README = '# Week2 CRUD\nInstalacion\n\nuvicorn main:app --reload\n'

def test_week02_full_crud_passes():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td)
        (p / 'main.py').write_text(SAMPLE_MAIN)
        (p / 'requirements.txt').write_text(REQS)
        (p / 'README.md').write_text(README)
        ev = Week02Evaluator(str(p))
        res = ev.evaluate()
        assert res['final_score'] >= 70
        crud = res['results'].get('crud_operations', {})
        assert crud.get('create_operation')
        assert crud.get('read_operation')
        assert crud.get('read_all_operation')
        assert crud.get('update_operation')
        assert crud.get('delete_operation')
