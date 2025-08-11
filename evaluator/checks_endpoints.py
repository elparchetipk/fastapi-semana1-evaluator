def probe_endpoints(app_import_result):
    from typing import Any
    if not (app_import_result.get("import_ok") and app_import_result.get("has_app")):
        return {"ok": False, "root": None, "docs": None, "hello_param": None}

    # Importa referencia real
    import importlib
    mod = importlib.import_module("student_main")
    app = getattr(mod, "app", None)
    if app is None:
        return {"ok": False, "root": None, "docs": None, "hello_param": None}

    # TestClient sin levantar uvicorn
    from fastapi.testclient import TestClient
    client = TestClient(app)

    res_root = client.get("/")
    res_docs = client.get("/docs")
    # Heurística: ¿hay endpoint con path param? p.ej. /hello/{name}
    candidates = [("/hello/test", client.get("/hello/test"))]
    hello_ok = None
    for path, r in candidates:
        hello_ok = r.status_code == 200

    ok = (res_root.status_code == 200) and (res_docs.status_code in (200, 307, 308))
    return {
        "ok": ok,
        "root": {"status": res_root.status_code, "json_like": _looks_json(res_root)},
        "docs": {"status": res_docs.status_code},
        "hello_param": hello_ok
    }

def _looks_json(resp):
    try:
        resp.json()
        return True
    except Exception:
        return False
