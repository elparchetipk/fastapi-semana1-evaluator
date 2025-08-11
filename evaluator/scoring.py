def score_all(r):
    breakdown = {}

    # 1) Setup (25)
    setup = 0
    if r["structure"]["files"]["requirements_txt"]: setup += 5
    if r["reqs"]["ok"] and r["reqs"]["fastapi"]:    setup += 8
    if r["reqs"]["uvicorn"]:                        setup += 4
    if r["structure"]["files"]["readme_md"]:        setup += 4
    if r["structure"]["files"]["main_py"]:          setup += 4
    breakdown["setup"] = min(setup, 25)

    # 2) Hello World API (25)
    hello = 0
    if r["app_import"]["import_ok"] and r["app_import"]["has_app"]: hello += 10
    if r["endpoints"]["root"] and r["endpoints"]["root"]["status"] == 200: hello += 10
    if r["endpoints"]["hello_param"]: hello += 5
    breakdown["hello_world"] = min(hello, 25)

    # 3) Testing & Docs (25)
    testdocs = 0
    if r["endpoints"]["docs"] and r["endpoints"]["docs"]["status"] in (200,307,308): testdocs += 12
    if r["endpoints"]["root"] and r["endpoints"]["root"]["json_like"]:               testdocs += 8
    # margen para manejo de errores/reportes básicos (heurística: si import falla, 0)
    if r["app_import"]["import_ok"]:                                                 testdocs += 5
    breakdown["testing_docs"] = min(testdocs, 25)

    # 4) Entregables (15)
    entregables = 0
    if r["structure"]["files"]["readme_md"]:        entregables += 4
    if r["structure"]["files"]["requirements_txt"]: entregables += 4
    if r["structure"]["files"]["main_py"]:          entregables += 4
    # +3 por organización básica (heurística: si import y /docs ok)
    if r["app_import"]["import_ok"] and (r["endpoints"]["docs"] and r["endpoints"]["docs"]["status"] in (200,307,308)):
        entregables += 3
    breakdown["deliverables"] = min(entregables, 15)

    # 5) Comprensión (10)
    comp = 0
    if r["readme"]["exists"] and r["readme"]["has_reflection"]: comp += 6
    if r["readme"]["exists"] and r["readme"]["has_commands"]:   comp += 4
    breakdown["understanding"] = min(comp, 10)

    total = sum(breakdown.values())
    return {"breakdown": breakdown, "total": total}
