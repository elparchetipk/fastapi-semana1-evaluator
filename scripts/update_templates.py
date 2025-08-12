#!/usr/bin/env python3
"""
Script para actualizar todos los templates de feedback para mostrar scores redondeados
"""
import re
from pathlib import Path

def update_feedback_templates():
    """Actualiza todos los templates de feedback"""
    weeks_dir = Path(__file__).parent / "weeks"
    
    for week_dir in weeks_dir.iterdir():
        if not week_dir.is_dir() or not week_dir.name.startswith("week"):
            continue
            
        feedback_file = week_dir / "templates" / "feedback.md"
        if feedback_file.exists():
            content = feedback_file.read_text()
            
            # Actualizar para mostrar score redondeado
            content = re.sub(
                r'\*\*Score Final\*\*: \{\{final_score\}\}/100',
                r'**Score Final**: {{final_score|round(1)}}/100',
                content
            )
            
            feedback_file.write_text(content)
            print(f"✅ Actualizado: {feedback_file}")

def update_issue_templates():
    """Actualiza todos los templates de issues"""
    weeks_dir = Path(__file__).parent / "weeks"
    
    for week_dir in weeks_dir.iterdir():
        if not week_dir.is_dir() or not week_dir.name.startswith("week"):
            continue
            
        issue_file = week_dir / "templates" / "issue_template.yml"
        if issue_file.exists():
            content = issue_file.read_text()
            
            # Actualizar para mostrar score redondeado  
            content = re.sub(
                r'\*\*Score Final\*\*: \$\{\{ final_score \}\}/100',
                r'**Score Final**: ${{ final_score | round(1) }}/100',
                content
            )
            
            issue_file.write_text(content)
            print(f"✅ Actualizado: {issue_file}")

def main():
    print("🔧 Actualizando templates para mostrar scores redondeados...")
    update_feedback_templates()
    update_issue_templates()
    print("✅ ¡Todos los templates actualizados!")

if __name__ == "__main__":
    main()
