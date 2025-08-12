import sys
import tempfile
from pathlib import Path
# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from weeks.week02.evaluator import Week02Evaluator

def test_week02_detects_missing_operations_and_models():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td)
        # main.py with only GET list
        (p / 'main.py').write_text('from fastapi import FastAPI\napp = FastAPI()\n@app.get(\"/items\")\ndef list_items():\n    return []')
        (p / 'requirements.txt').write_text('fastapi\nuvicorn\n')
        (p / 'README.md').write_text('# Week2\n')
        ev = Week02Evaluator(str(p))
        res = ev.evaluate()
        crud = res['results'].get('crud_operations', {})
        assert crud.get('read_all_operation')
        assert not crud.get('create_operation')
        assert not crud.get('read_operation')
        assert res['final_score'] < 70
