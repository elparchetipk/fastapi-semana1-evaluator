from pathlib import Path
import re

def check_readme(root: Path):
    readme = root / "README.md"
    if not readme.exists():
        return {"exists": False, "has_commands": False, "has_screenshot": False, "has_reflection": False}
    text = readme.read_text(encoding="utf-8", errors="ignore")
    has_commands   = bool(re.search(r"(uvicorn|python\\s+main\\.py|pip\\s+install)", text, re.I))
    has_screenshot = ("![" in text) or ("<img" in text.lower())
    # reflexión: 2-3 oraciones: heurística simple por puntos y palabras clave
    has_reflection = (text.lower().count("fastapi") + text.lower().count("api")) >= 2 and text.count(".") >= 2
    return {
        "exists": True,
        "has_commands": has_commands,
        "has_screenshot": has_screenshot,
        "has_reflection": has_reflection
    }
