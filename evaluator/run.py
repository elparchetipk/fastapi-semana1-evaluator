import argparse, json, os, re, signal, sys, importlib.util, contextlib, time
from pathlib import Path
from .checks_structure import check_structure
from .checks_requirements import check_requirements
from .checks_app_import import try_import_app
from .checks_endpoints import probe_endpoints
from .checks_readme import check_readme
from .scoring import score_all
from .report_md import render_report

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--student-path", required=True)
    parser.add_argument("--out-md", default="report.md")
    parser.add_argument("--out-json", default="score.json")
    args = parser.parse_args()

    student = Path(args.student_path).resolve()
    os.chdir(student)

    results = {}
    results["structure"]   = check_structure(student)
    results["reqs"]        = check_requirements(student)
    app_import = try_import_app(student)
    results["app_import"]  = app_import
    results["endpoints"]   = probe_endpoints(app_import)
    results["readme"]      = check_readme(student)

    # Puntajes y feedback
    scoring = score_all(results)  # dict con breakdown y total
    report  = render_report(args.student_path, results, scoring)

    # Salidas
    with open(Path(args.out_md), "w", encoding="utf-8") as f:
        f.write(report)
    with open(Path(args.out_json), "w", encoding="utf-8") as f:
        json.dump({
            "total": scoring["total"],
            "passed": scoring["total"] >= 70,
            "breakdown": scoring["breakdown"]
        }, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
