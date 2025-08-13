#!/bin/bash

# Script para verificar configuración de GitHub Actions

echo "🔍 Verificando configuración de GitHub Actions..."
echo ""

# Verificar si estamos en un repositorio git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ No estamos en un repositorio Git"
    exit 1
fi

echo "✅ Repositorio Git detectado"

# Verificar rama actual
CURRENT_BRANCH=$(git branch --show-current)
echo "📍 Rama actual: $CURRENT_BRANCH"

# Verificar si los workflows existen
if [ -d ".github/workflows" ]; then
    echo "✅ Directorio .github/workflows existe"
    echo "📄 Workflows encontrados:"
    ls -la .github/workflows/
else
    echo "❌ Directorio .github/workflows NO existe"
    exit 1
fi

echo ""

# Verificar si los workflows tienen sintaxis válida YAML
echo "🔍 Verificando sintaxis YAML de workflows..."

for workflow in .github/workflows/*.yml .github/workflows/*.yaml; do
    if [ -f "$workflow" ]; then
        echo "Verificando: $workflow"
        if python -c "import yaml; yaml.safe_load(open('$workflow'))" 2>/dev/null; then
            echo "✅ $workflow - Sintaxis YAML válida"
        else
            echo "❌ $workflow - Error de sintaxis YAML"
        fi
    fi
done

echo ""

# Verificar templates de issues
if [ -d ".github/ISSUE_TEMPLATE" ]; then
    echo "✅ Directorio .github/ISSUE_TEMPLATE existe"
    echo "📄 Templates encontrados:"
    ls -la .github/ISSUE_TEMPLATE/
else
    echo "❌ Directorio .github/ISSUE_TEMPLATE NO existe"
fi

echo ""

# Información sobre remotes
echo "🌐 Información de remotes:"
git remote -v

echo ""
echo "📋 Para habilitar GitHub Actions:"
echo "1. Ve a tu repositorio en GitHub"
echo "2. Haz clic en la pestaña 'Actions'"
echo "3. Si está deshabilitado, haz clic en 'I understand my workflows, go ahead and enable them'"
echo ""
echo "📋 Para probar el workflow:"
echo "1. Crea un issue usando el template de Semana 1"
echo "2. Asegúrate de que tenga los labels 'semana1' y 'submission'"
echo "3. Comenta '/debug' para probar el workflow de debug"
echo "4. Comenta '/evaluar' para probar la evaluación"
