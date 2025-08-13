---
name: '📋 Entrega Semana 5 - Testing y Documentación Avanzada'
about: 'Evalúa tu proyecto de la Semana 5: Testing completo y documentación profesional'
title: '[SEMANA 5] [TU-NOMBRE] - Testing y Documentación Avanzada'
labels: ['semana-5', 'evaluacion', 'pendiente']
assignees: []
---

## 📋 Información del Estudiante

**Nombre completo:** [Tu nombre completo]  
**Cohort/Grupo:** [Tu cohort o grupo]  
**Fecha de entrega:** [DD/MM/YYYY]

## 🔗 Repositorio a Evaluar

**URL del repositorio:** [https://github.com/tu-usuario/tu-repo-semana5]

> ⚠️ **IMPORTANTE**: Tu repositorio debe ser **público** para que el evaluador pueda acceder.

## ✅ Checklist Pre-entrega

Antes de enviar, verifica que tu repositorio contenga:

### 🧪 Testing Setup

- [ ] `pytest.ini` o configuración en `pyproject.toml`
- [ ] Directorio `tests/` organizado
- [ ] `conftest.py` con fixtures compartidas
- [ ] `requirements.txt` con dependencias de testing

### 🔬 Tests Unitarios

- [ ] Tests para modelos SQLAlchemy
- [ ] Tests para modelos Pydantic/validaciones
- [ ] Tests para funciones utilitarias
- [ ] Tests con mocks cuando sea necesario

### 🌐 Tests de Integración

- [ ] Tests de endpoints con `TestClient`
- [ ] Tests de base de datos (con DB de test)
- [ ] Tests de flujos completos
- [ ] Tests de manejo de errores

### 📚 Documentación Avanzada

- [ ] OpenAPI personalizada (title, description, version)
- [ ] Ejemplos en los endpoints
- [ ] Documentación de respuestas de error
- [ ] Tags y metadata de endpoints

### 🚀 Deployment y README

- [ ] `README.md` con instrucciones de instalación
- [ ] Información de variables de entorno
- [ ] Instrucciones de deployment
- [ ] Comandos para ejecutar tests

## 🎯 Criterios de Evaluación

Tu proyecto será evaluado en las siguientes áreas:

### Testing Setup (35 puntos)

- **Configuración de Pytest** (8 pts): pytest.ini o pyproject.toml configurados
- **Dependencias de Testing** (7 pts): pytest, httpx, pytest-asyncio instalados
- **Estructura de Tests** (8 pts): organización clara en directorios
- **Configuración de BD de Test** (12 pts): setup para testing con BD

### Unit Testing (25 puntos)

- **Tests de Modelos** (8 pts): validación de modelos SQLAlchemy
- **Tests de Funciones Utilitarias** (7 pts): funciones auxiliares testadas
- **Tests de Lógica de Negocio** (10 pts): reglas de negocio validadas

### Integration Testing (25 puntos)

- **Tests de Endpoints** (10 pts): endpoints testados con TestClient
- **Tests de Integración BD** (8 pts): operaciones de BD en contexto real
- **Tests de Manejo de Errores** (7 pts): casos de error manejados

### Documentation (15 puntos)

- **Personalización OpenAPI** (5 pts): metadata y configuración custom
- **Ejemplos de API** (5 pts): ejemplos en endpoints y responses
- **README de Deployment** (5 pts): documentación de instalación y deploy

## Total: 100 puntos | Umbral de aprobación: 75%

## 📝 Notas del Estudiante

**Enfoque de Testing:**
[Describe tu estrategia de testing: tipos de tests, uso de mocks, organización, etc.]

**Características de Documentación:**
[Lista las mejoras que implementaste en la documentación]

**Desafíos encontrados:**
[¿Qué fue lo más difícil? ¿Qué aprendiste?]

**Notas adicionales:**
[Cualquier información adicional que quieras compartir]

---

## 🤖 Para el Evaluador Automático

Este issue será procesado automáticamente. El bot:

1. Clonará tu repositorio
2. Ejecutará todos los checks de evaluación
3. Generará un reporte detallado
4. Asignará la puntuación final

**Umbral de aprobación:** 75/100 puntos

---

## 📚 Recursos de Apoyo

- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Pytest Documentation](https://docs.pytest.org/)
- [SQLAlchemy Testing](https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites)
- [OpenAPI Specification](https://swagger.io/specification/)

---

**Fecha de envío:** [Se completa automáticamente]
**Estado:** 🟡 Pendiente de evaluación
