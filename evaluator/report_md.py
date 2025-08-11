def render_report(student_path, results, scoring):
    b = scoring["breakdown"]; total = scoring["total"]
    status = "✅ **APROBADO**" if total >= 70 else "🕐 **PENDIENTE**"
    lines = []
    lines.append(f"{status} — Puntaje: **{total}/100**\n")
    lines.append("### Desglose por criterio")
    lines.append("| Criterio | Puntaje |")
    lines.append("|---|---:|")
    lines.append(f"| Setup | {b['setup']} |")
    lines.append(f"| Hello World API | {b['hello_world']} |")
    lines.append(f"| Testing & Docs | {b['testing_docs']} |")
    lines.append(f"| Entregables | {b['deliverables']} |")
    lines.append(f"| Comprensión | {b['understanding']} |")
    lines.append("\n### Feedback accionable")
    fb = []

    if not results["structure"]["files"]["main_py"]:
        fb.append("• Falta `main.py` en la raíz del repo.")
    if not results["reqs"]["fastapi"]:
        fb.append("• `requirements.txt` no incluye `fastapi`.")
    if not results["reqs"]["uvicorn"]:
        fb.append("• `requirements.txt` no incluye `uvicorn`.")
    if not (results["app_import"]["import_ok"] and results["app_import"]["has_app"]):
        fb.append("• No se pudo importar `app` desde `main.py` (revisa `app = FastAPI()` y errores de sintaxis).")
    if not (results["endpoints"]["root"] and results["endpoints"]["root"]["status"] == 200):
        fb.append("• `GET /` no responde 200. Agrega `@app.get('/')` con JSON simple.")
    if not (results["endpoints"]["docs"] and results["endpoints"]["docs"]["status"] in (200,307,308)):
        fb.append("• `/docs` no es accesible. Verifica que `app` exista y no tengas middlewares bloqueando docs.")
    if not results["readme"]["has_commands"]:
        fb.append("• Agrega comandos mínimos en README (instalación y ejecución).")
    if not results["readme"]["has_screenshot"]:
        fb.append("• Agrega un screenshot de `/docs` funcionando al README.")
    if not results["readme"]["has_reflection"]:
        fb.append("• Agrega una reflexión corta (2–3 oraciones) sobre FastAPI y API REST.")

    if not fb:
        fb.append("¡Buen trabajo! Cumples los criterios fundamentales de la semana 1.")
    lines += fb

    lines.append("\n> Re-ejecuta corrigiendo y vuelve a **Editar** este issue para obtener nueva evaluación.")
    return "\n".join(lines)
