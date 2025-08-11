from pathlib import Path
import re

def check_requirements(root: Path):
    req = root / "requirements.txt"
    if not req.exists():
        return {"ok": False, "fastapi": False, "uvicorn": False}
    text = req.read_text(encoding="utf-8", errors="ignore").lower()
    def has(pkg): 
        return any(line.strip().startswith(pkg) for line in text.splitlines())
    return {"ok": True, "fastapi": has("fastapi"), "uvicorn": has("uvicorn")}
