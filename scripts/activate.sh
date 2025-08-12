#!/bin/bash
# Script para activar el entorno virtual del proyecto FastAPI Evaluator

# Verificar si el entorno virtual existe
if [ ! -d "venv" ]; then
    echo "❌ Entorno virtual no encontrado. Ejecuta: python3 -m venv venv"
    exit 1
fi

# Activar el entorno virtual
source venv/bin/activate

echo "✅ Entorno virtual 'fastapi-evaluator' activado"
echo "🐍 Python version: $(python --version)"
echo "📦 Pip version: $(pip --version)"
echo ""
echo "💡 Para desactivar el entorno virtual, ejecuta: deactivate"
echo "🚀 Para ejecutar el evaluador, usa: python evaluate.py --help"
