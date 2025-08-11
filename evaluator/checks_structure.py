from pathlib import Path

def check_structure(root: Path):
    files = {
        "main_py": (root / "main.py").exists(),
        "requirements_txt": (root / "requirements.txt").exists(),
        "readme_md": (root / "README.md").exists(),
    }
    return {"ok": all(files.values()), "files": files}
