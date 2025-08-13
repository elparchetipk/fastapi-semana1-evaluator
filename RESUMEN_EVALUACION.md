# 🚀 Resumen Rápido: Evaluación Automática Semana 1

## ✅ ¿Qué deben hacer tus estudiantes?

### 1. **Preparar el repositorio** (GitHub público)

```
mi-proyecto-fastapi/
├── main.py
├── requirements.txt
└── README.md
```

### 2. **Crear Issue**

- Ir a **Issues** → **New Issue**
- Usar plantilla **"📋 Entrega Semana 1"**
- Pegar URL de su repositorio público

### 3. **Esperar respuesta automática** ⏱️

- **Tiempo**: 2-3 minutos
- **Dónde**: Como comentario EN EL MISMO ISSUE que crearon (en este repositorio evaluador)
- **Formato**: Feedback detallado con puntaje

---

## 📊 ¿Qué respuestas recibirán?

### ✅ **APROBADO (≥75 puntos)**

```markdown
✅ **APROBADO** — Puntaje: **85/100**

### 📊 Desglose por categorías

| Categoría     | Puntaje | Estado |
| ------------- | ------- | ------ |
| Setup         | 25/25   | ✅     |
| Functionality | 35/40   | ✅     |
| Documentation | 15/20   | ⚠️     |
| Deliverables  | 10/10   | ✅     |

### 📋 Feedback específico:

✅ **Lo que está bien:**
• FastAPI correctamente configurado
• Endpoints funcionando correctamente
• Estructura de archivos completa

🔧 **Lo que se puede mejorar:**
• Agregar más detalles al README.md
• Incluir ejemplos de uso en la documentación
```

### ❌ **PENDIENTE (<75 puntos)**

```markdown
❌ **PENDIENTE** — Puntaje: **45/100**

🔧 **Lo que necesitas mejorar:**
• Agregar FastAPI a requirements.txt
• Implementar endpoint GET / que retorne JSON
• Crear instancia de aplicación FastAPI (app = FastAPI())
• Asegurar que uvicorn esté en requirements.txt
```

### 🚫 **ERROR (Repositorio inaccesible)**

```markdown
## ❌ Error en la Evaluación

- 🔒 **Repositorio privado**: Hazlo público
- 🔗 **URL incorrecta**: Verifica la URL
- 📁 **Archivos faltantes**: main.py, requirements.txt, README.md
```

---

## 🔄 Re-evaluación

**Para proyectos PENDIENTES:**

1. Corregir problemas mencionados
2. Subir cambios a GitHub
3. **Editar el mismo issue** (no crear nuevo)
4. Evaluación automática en 2-3 minutos

---

## 🎯 Criterios de Aprobación

| Aspecto           | Puntos | Requisito                                  |
| ----------------- | ------ | ------------------------------------------ |
| **Setup**         | 25     | `main.py`, `requirements.txt`, `README.md` |
| **Functionality** | 40     | FastAPI app + GET / endpoint               |
| **Documentation** | 20     | README con instrucciones + /docs accesible |
| **Deliverables**  | 10     | Estructura organizada                      |
| **Understanding** | 5      | Implementación básica correcta             |

**Total**: 100 puntos | **Mínimo**: 75 para aprobar

---

## 💡 Tips para Estudiantes

### ✅ **main.py mínimo**:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

### ✅ **requirements.txt**:

```
fastapi>=0.68.0
uvicorn[standard]>=0.15.0
```

### ✅ **Verificar antes de subir**:

- `uvicorn main:app --reload` funciona
- http://localhost:8000/docs accesible
- Repositorio es público (sin 🔒)

---

**📋 Documentación completa:** Ver `GUIA_ESTUDIANTES.md`
