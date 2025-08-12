import sys
import tempfile
from pathlib import Path
# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from weeks.week01.evaluator import Week01Evaluator

SAMPLE_MAIN = """from fastapi import FastAPI
app = FastAPI()
@app.get('/')
def root():
    return {'message': 'Hello World'}
@app.get('/hello/{name}')
def hello(name: str):
    return {'message': f'Hello {name}'}
"""
REQS = """fastapi\nuvicorn\n"""
README = """# Week1\nInstalacion\nuvicorn main:app --reload\n"""

def test_week01_full():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td)
        (p / 'main.py').write_text(SAMPLE_MAIN)
        (p / 'requirements.txt').write_text(REQS)
        (p / 'README.md').write_text(README)
        ev = Week01Evaluator(str(p))
        res = ev.evaluate()
        assert res['final_score'] >= 70
