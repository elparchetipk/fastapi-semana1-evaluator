# Week01 basic tests
import sys
from pathlib import Path
# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from weeks.week01.evaluator import Week01Evaluator

def test_import_week01():
    assert Week01Evaluator is not None


def test_week01_minimal_repo_passes():
    # Reusa lógica mínima de week01 para asegurar que evaluate() produce score
    import tempfile
    from pathlib import Path
    from weeks.week01.checks.endpoints import check_endpoints
    with tempfile.TemporaryDirectory() as td:
        p = Path(td)
        (p / 'main.py').write_text('from fastapi import FastAPI\napp=FastAPI()\n@app.get(\"/\")\ndef root():\n return {"message":"hi"}')
        (p / 'requirements.txt').write_text('fastapi\nuvicorn\n')
        (p / 'README.md').write_text('# Readme\n')
        ev = Week01Evaluator(str(p))
        res = ev.evaluate()
        assert 'final_score' in res
        # sanity: endpoints check worked
        ep = check_endpoints(str(p))
        assert ep.get('root_working', False)
