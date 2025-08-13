# 📋 Guía para Estudiantes: ¿Qué Esperar de la Evaluación Automática?

## 🎯 ¿Cómo funciona el proceso de evaluación?

### 1. **Subir tu proyecto a GitHub** 🌐

- Tu repositorio **DEBE ser público**
- **IMPORTANTE**: El nombre del repositorio debe seguir el formato específico:

  ```
  ficha-apellido-nombre-fastapi-semanaX
  ```

  **Ejemplos de nombres correctos:**

  - `3147246-rodriguez-juan-fastapi-semana1`
  - `2766065-perez-maria-fastapi-semana2`
  - `1234567-garcia-carlos-fastapi-semana3`

  **❌ Nombres incorrectos:**

  - `mi-proyecto-fastapi` (falta ficha y formato)
  - `juan-fastapi-semana1` (falta ficha)
  - `fastapi-semana1` (falta ficha y nombre)

- Estructura requerida:
  ```
  ficha-apellido-nombre-fastapi-semanaX/
  ├── main.py
  ├── requirements.txt
  └── README.md
  ```

### 2. **Crear un Issue para evaluación** 📝

- Ve a la página de **Issues** de este repositorio
- Haz clic en **"New Issue"**
- Selecciona la plantilla **"📋 Entrega Semana 1 - Hello World API"**
- Completa todos los campos requeridos

### 3. **¿Qué pasa después?** ⏱️

- **Tiempo de respuesta**: 2-3 minutos
- El sistema evalúa automáticamente tu repositorio
- Recibes un comentario detallado en tu issue

---

## 📊 Ejemplos de Respuestas que Recibirás

### ✅ **Ejemplo 1: Proyecto APROBADO (100/100)**

```markdown
✅ **APROBADO** — Puntaje: **100/100**

## Week 1: Hello World API

### 📊 Desglose por categorías

| Categoría     | Puntaje | Estado |
| ------------- | ------- | ------ |
| Setup         | 25/25   | ✅     |
| Functionality | 40/40   | ✅     |
| Documentation | 20/20   | ✅     |
| Deliverables  | 10/10   | ✅     |
| Understanding | 5/5     | ✅     |

### 🎯 Umbral de aprobación: 75%

### 📋 Feedback específico:

✅ **Lo que está bien:**

1. Sintaxis correcta en main.py
2. Archivo main.py presente y accesible
3. Archivo requirements.txt presente
4. Documentación README.md presente
5. FastAPI correctamente instalado y configurado
6. Uvicorn disponible para ejecutar la aplicación

🎉 **¡Excelente trabajo!** No hay mejoras críticas necesarias.

✅ **Aspectos de Week 1 implementados correctamente:**
• Estructura de archivos básica completa (main.py, requirements.txt, README.md)
• Dependencias FastAPI correctamente especificadas en requirements.txt
• FastAPI correctamente importado en main.py
• Instancia de aplicación FastAPI creada correctamente
• Endpoint GET / funcionando y retornando JSON válido
• Documentación automática FastAPI accesible en /docs
• README con comandos de instalación y ejecución
• Código bien estructurado y documentado

---

> 🤖 Evaluación automática generada el 2025-08-13
```

**📝 Etiquetas automáticas añadidas:** `aprobado`

---

### ⚠️ **Ejemplo 2: Proyecto PENDIENTE (45/100)**

```markdown
❌ **PENDIENTE** — Puntaje: **45/100**

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
3. Documentación README.md presente

🔧 **Lo que necesitas mejorar:**
• Agregar FastAPI a requirements.txt
• Importar FastAPI en main.py
• Crear instancia de aplicación FastAPI (app = FastAPI())
• Implementar endpoint GET / que retorne JSON
• Asegurar que uvicorn esté en requirements.txt
• Agregar comandos de instalación en README.md
• Agregar comandos de ejecución en README.md

❌ **Aspectos críticos faltantes:**
• FastAPI no está correctamente importado en main.py
• No se encuentra la instancia de aplicación FastAPI
• Endpoint GET / no implementado o no funcional
• Dependencias incompletas en requirements.txt

---

> 🤖 Evaluación automática generada el 2025-08-13
```

**📝 Etiquetas automáticas añadidas:** `revisar`

---

### 🚫 **Ejemplo 3: Error de Repositorio**

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

## 🔄 ¿Cómo Re-evaluar tu Proyecto?

### Si tu proyecto fue **PENDIENTE** o dio **ERROR**:

1. **Arregla los problemas** mencionados en el feedback
2. **Sube los cambios** a tu repositorio de GitHub
3. **Edita tu issue original** (no crear uno nuevo)
4. **Cambia cualquier texto** en el issue (ej: agregar "v2" al título)
5. **Guarda los cambios** - el sistema re-evaluará automáticamente

### ⚡ **Re-evaluación automática**:

- Cada vez que edites el issue, se ejecuta una nueva evaluación
- **No hay límite** de intentos
- **No necesitas crear issues nuevos**

---

## 🎯 Criterios de Aprobación para Semana 1

### **Puntaje mínimo**: 75/100

### **Elementos obligatorios**:

- ✅ `main.py` con aplicación FastAPI funcional
- ✅ `requirements.txt` con fastapi y uvicorn
- ✅ `README.md` con instrucciones básicas
- ✅ Endpoint `GET /` que responde JSON
- ✅ `/docs` accesible (documentación automática)

### **Estructura mínima esperada**:

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

```txt
# requirements.txt
fastapi>=0.68.0
uvicorn[standard]>=0.15.0
```

---

## 🔍 ¿Dónde Ver las Respuestas?

### **1. En tu Issue**

- La respuesta aparece como un **comentario** en tu issue
- **Tiempo**: 2-3 minutos después de crear/editar el issue
- **Ubicación**: Sección de comentarios del issue

### **2. Etiquetas Automáticas**

- **`aprobado`**: Proyecto cumple con los requisitos (≥75 puntos)
- **`revisar`**: Proyecto necesita mejoras (<75 puntos)
- **`pendiente`**: Esperando evaluación o con errores técnicos

### **3. Notificaciones de GitHub**

- Recibirás notificación por email (si está habilitado)
- Notificación en la campana 🔔 de GitHub

---

## 🆘 Problemas Comunes y Soluciones

### **❌ "No recibo respuesta después de 5 minutos"**

**Posibles causas:**

- **📛 Nombre de repositorio incorrecto**: Debe seguir el formato `ficha-apellido-nombre-fastapi-semanaX`
  ```
  ✅ Correcto: 3147246-rodriguez-juan-fastapi-semana1
  ❌ Incorrecto: mi-proyecto-fastapi
  ❌ Incorrecto: juan-fastapi-proyecto
  ❌ Incorrecto: fastapi-semana1
  ```
- Tu repositorio es privado → Hazlo público
- URL incorrecta en el issue → Verifica la URL
- Falta la etiqueta `evaluacion` → Contacta al instructor

### **❌ "Dice que mi main.py no existe"**

**Solución:**

- El archivo debe estar en la **raíz** del repositorio
- Nombre exacto: `main.py` (no `Main.py` o `main.PY`)

### **❌ "Dice que FastAPI no está instalado"**

**Solución:**

- Agrega `fastapi>=0.68.0` a `requirements.txt`
- Agrega `uvicorn[standard]>=0.15.0` a `requirements.txt`

### **❌ "No encuentra el endpoint GET /"**

**Solución:**

```python
@app.get("/")  # Exactamente así
def read_root():
    return {"message": "Hello World"}  # Debe retornar un dict/JSON
```

---

## 💡 Tips para el Éxito

### ✅ **Antes de subir tu issue**:

1. **Prueba localmente**: `uvicorn main:app --reload`
2. **Verifica `/docs`**: Ve a http://localhost:8000/docs
3. **Repositorio público**: Verifica en GitHub que no tenga el candado 🔒
4. **URL correcta**: Copia la URL exacta desde la barra del navegador

### ✅ **Estructura recomendada**:

```
mi-proyecto-fastapi/
├── main.py              # Aplicación principal
├── requirements.txt     # Dependencias
├── README.md           # Documentación
└── .gitignore          # Opcional pero recomendado
```

### ✅ **README.md básico**:

```markdown
# Mi Proyecto FastAPI - Semana 1

## Instalación

pip install -r requirements.txt

## Ejecutar

uvicorn main:app --reload

## Documentación

http://localhost:8000/docs
```

---

## 📝 Formato OBLIGATORIO del Nombre del Repositorio

### **🚨 IMPORTANTE: Formato Específico Requerido**

El nombre de tu repositorio **DEBE** seguir este formato exacto:

```
ficha-apellido-nombre-fastapi-semanaX
```

**Donde:**

- `ficha` = Tu número de ficha/curso (ej: 3147246)
- `apellido` = Tu apellido en minúsculas
- `nombre` = Tu nombre en minúsculas
- `semanaX` = El número de la semana (semana1, semana2, etc.)

### **✅ Ejemplos CORRECTOS:**

```
3147246-rodriguez-juan-fastapi-semana1
2766065-perez-maria-fastapi-semana2
1234567-garcia-carlos-fastapi-semana3
4567890-martinez-ana-fastapi-semana4
```

### **❌ Ejemplos INCORRECTOS:**

```
❌ mi-proyecto-fastapi              (no sigue el formato)
❌ juan-fastapi-semana1             (falta ficha)
❌ fastapi-semana1                  (falta ficha y nombre)
❌ 3147246-fastapi-semana1          (falta apellido-nombre)
❌ 3147246-Juan-Rodriguez-semana1   (mayúsculas, falta fastapi)
```

### **⚠️ Consecuencias de nombre incorrecto:**

- El sistema automático **NO PODRÁ** encontrar tu repositorio
- Tu entrega **NO SERÁ EVALUADA**
- Recibirás error: "Repositorio no encontrado"

### **🔧 ¿Cómo cambiar el nombre del repositorio?**

1. Ve a tu repositorio en GitHub
2. Haz clic en **Settings** (Configuración)
3. Baja hasta **Repository name**
4. Cambia al formato correcto
5. Haz clic en **Rename**

---

## 🎓 ¿Qué Sigue Después de Aprobar?

1. **¡Felicitaciones!** 🎉 Has completado la Semana 1
2. **Continúa aprendiendo** con la Semana 2: Modelos con Pydantic
3. **Mantén tu repositorio** - puede ser útil para futuras referencias
4. **Comparte tu experiencia** con otros estudiantes

---

> 💡 **Recuerda**: Este evaluador es una herramienta de aprendizaje. Su objetivo es ayudarte a interiorizar los conceptos fundamentales de FastAPI mediante feedback inmediato y criterios claros.

**¡Éxitos con tu proyecto! 🚀**
