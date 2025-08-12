import sys
import tempfile
from pathlib import Path
# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from weeks.week02.checks.models import check_models

MODEL_CODE = '''from pydantic import BaseModel, Field\n\nclass Item(BaseModel):\n    id: int\n    name: str = Field(..., min_length=1)\n    price: float\n\nclass User(BaseModel):\n    username: str\n    email: str\n'''

def test_models_detection_and_score():
    with tempfile.TemporaryDirectory() as td:
        p = Path(td)
        (p / 'models.py').write_text(MODEL_CODE)
        res = check_models(str(p))
        assert res['basemodel_used']
        assert 'Item' in res['models_found']
        assert 'User' in res['models_found']
        assert res['models_score'] > 40
