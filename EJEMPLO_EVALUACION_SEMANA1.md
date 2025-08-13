# 📋 Ejemplo de Evaluación Automática - Semana 1

## ¿Qué esperan los estudiantes cuando suben su proyecto?

### 📍 **IMPORTANTE: Dónde aparece la respuesta**

La evaluación automática **NO aparece en tu repositorio personal**. La respuesta aparece como un **comentario en el issue que creaste en este repositorio evaluador**.

---

## 🔄 Flujo completo del proceso:

### 1. **El estudiante crea un issue aquí**

- En: `https://github.com/epti-dev/fastapi-semana1-evaluator`
- Con el template: "📋 Entrega Semana 1 - FastAPI Básico"
- Incluye la URL de SU repositorio personal

### 2. **GitHub Actions se ejecuta automáticamente**

- Tiempo estimado: 2-3 minutos
- El estudiante puede ver el progreso en la pestaña "Actions"

### 3. **La respuesta aparece como comentario**

- **Ubicación**: En el mismo issue que creó el estudiante
- **Formato**: Comentario automatizado con feedback completo

---

## 📝 Ejemplo de respuesta exitosa:

```markdown
✅ **APROBADO** — Puntaje: **85/100**

## Week 1: Hello World API

### 📊 Desglose por categorías

| Categoría     | Puntaje | Estado |
| ------------- | ------- | ------ |
| Setup         | 25/25   | ✅     |
| Functionality | 35/40   | ⚠️     |
| Documentation | 15/20   | ⚠️     |
| Deliverables  | 10/10   | ✅     |
| Understanding | 0/5     | ❌     |

### 🎯 Umbral de aprobación: 75%

### 📋 Feedback específico:

✅ **Lo que está bien:**

1. Sintaxis correcta en main.py
2. Archivo main.py presente y accesible
3. Archivo requirements.txt presente
4. FastAPI correctamente instalado y configurado
5. Uvicorn disponible para ejecutar la aplicación

🔧 **Lo que se debe mejorar:**

1. Agrega un endpoint con parámetros (ej: `/hello/{name}`)
2. Mejora la documentación en README.md con ejemplos
3. Agrega una reflexión sobre FastAPI y APIs REST

✅ **Aspectos de Week 1 implementados correctamente:**
• Estructura de archivos básica completa
• Dependencias FastAPI correctamente especificadas
• Aplicación FastAPI funcional con endpoint básico
• Documentación automática accesible en /docs

---

> 🤖 Evaluación automática generada el 2025-08-13 15:30:22
```

---

## 📝 Ejemplo de respuesta con errores:

```markdown
❌ **REPROBADO** — Puntaje: **45/100**

## Week 1: Hello World API

### 📊 Desglose por categorías

| Categoría     | Puntaje | Estado |
| ------------- | ------- | ------ |
| Setup         | 15/25   | ⚠️     |
| Functionality | 10/40   | ❌     |
| Documentation | 10/20   | ⚠️     |
| Deliverables  | 10/10   | ✅     |
| Understanding | 0/5     | ❌     |

### 🎯 Umbral de aprobación: 75%

### 📋 Feedback específico:

✅ **Lo que está bien:**

1. Archivo main.py presente
2. Archivo requirements.txt presente
3. README.md presente

🔧 **Lo que se debe mejorar:**

1. **CRÍTICO**: Corrige errores de sintaxis en main.py
2. **CRÍTICO**: Agrega `app = FastAPI()` en main.py
3. **CRÍTICO**: Crea endpoint GET / que retorne JSON
4. Agrega uvicorn a requirements.txt
5. Mejora la documentación con comandos de instalación

❌ **Problemas críticos encontrados:**
• Error de sintaxis impide importar la aplicación
• No se encontró instancia de FastAPI
• Endpoint raíz "/" no funciona o no existe
• Falta uvicorn en las dependencias

---

> 🤖 Evaluación automática generada el 2025-08-13 15:30:22
```

---

## 🔄 ¿Qué puede hacer el estudiante después?

### ✅ **Si aprobó (≥75 puntos):**

- ¡Felicitaciones! Puede continuar con la Semana 2
- Revisar sugerencias de mejora para perfeccionar el código
- El issue se marca automáticamente con label `aprobado`

### 🔧 **Si no aprobó (<75 puntos):**

1. **Revisar el feedback detallado** en el comentario
2. **Corregir los problemas** en su repositorio personal
3. **Editar el mismo issue** para re-evaluar
4. **Esperar nueva evaluación** (2-3 minutos)

---

## 🚨 ¿Qué pasa si hay errores técnicos?

```markdown
## ❌ Error en la Evaluación

No se pudo completar la evaluación automática. Posibles causas:

- 🔒 **Repositorio privado**: Asegúrate de que tu repositorio sea público
- 🔗 **URL incorrecta**: Verifica que la URL del repositorio esté correcta
- 📁 **Estructura incorrecta**: Revisa que tengas los archivos requeridos
- 🐛 **Error técnico**: Contacta a tu instructor para asistencia

### 📞 Siguiente paso:

1. Verifica que tu repositorio sea **público**
2. Asegúrate de que la URL esté correcta
3. Revisa la estructura de archivos requerida
4. Edita este issue para re-evaluar
```

---

## 📞 **Resumen para estudiantes:**

1. **Creas issue AQUÍ** (en el repositorio evaluador)
2. **Incluyes URL de TU repositorio** personal
3. **Esperas 2-3 minutos**
4. **Recibes comentario AQUÍ** (en el mismo issue)
5. **Si necesitas re-evaluar**: Editas el mismo issue

**📍 La evaluación SIEMPRE aparece como comentario en el issue del repositorio evaluador, NO en tu repositorio personal.**
