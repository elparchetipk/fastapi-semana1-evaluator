import sys, importlib.util, signal, contextlib
from pathlib import Path

class Timeout(Exception): pass
def _handler(signum, frame): raise Timeout()

def try_import_app(root: Path):
    main_py = root / "main.py"
    if not main_py.exists():
        return {"import_ok": False, "has_app": False, "error": "main.py no encontrado"}

    # Aíslate del sys.modules lo justo
    spec = importlib.util.spec_from_file_location("student_main", str(main_py))
    if spec is None:
        return {"import_ok": False, "has_app": False, "error": "No se pudo crear spec para main.py"}
    
    mod = importlib.util.module_from_spec(spec)

    signal.signal(signal.SIGALRM, _handler)
    signal.alarm(3)  # 3s hard timeout en import
    try:
        if spec.loader is None:
            return {"import_ok": False, "has_app": False, "error": "No se pudo obtener loader para main.py"}
        spec.loader.exec_module(mod)  # puede ejecutar código del estudiante
        app = getattr(mod, "app", None)
        return {"import_ok": True, "has_app": app is not None, "app_ref": "student_main.app" if app else None}
    except Timeout:
        return {"import_ok": False, "has_app": False, "error": "timeout importando main.py"}
    except Exception as e:
        return {"import_ok": False, "has_app": False, "error": f"{type(e).__name__}: {e}"}
    finally:
        signal.alarm(0)
