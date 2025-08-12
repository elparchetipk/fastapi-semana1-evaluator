import sys
import tempfile
from pathlib import Path
# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from weeks.week01.checks.endpoints import check_endpoints

def test_week01_broken_repo_detects_missing_root():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td)
        (p / 'main.py').write_text('from fastapi import FastAPI\napp=FastAPI()')
        (p / 'requirements.txt').write_text('fastapi')
        res = check_endpoints(str(p))
        assert not res.get('root_working')
