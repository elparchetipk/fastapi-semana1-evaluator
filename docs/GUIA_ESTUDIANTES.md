# 📋 Guía para Estudiantes: ¿Qué Esperar de la Evaluación Automática?

## 🎯 ¿Cómo funciona el proceso de evaluación?

### 1. **Subir tu proyecto a GitHub** 🌐

- Tu repositorio **DEBE ser público**
- **IMPORTANTE**: El nombre del repositorio debe seguir el formato específico:

```text
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

```text
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

### Si tu proyecto fue **PENDIENTE** o dio **ERROR**

1. **Arregla los problemas** mencionados en el feedback
2. **Sube los cambios** a tu repositorio de GitHub
3. **Edita tu issue original** (no crear uno nuevo)
4. **Cambia cualquier texto** en el issue (ej: agregar "v2" al título)
5. **Guarda los cambios** - el sistema re-evaluará automáticamente

### ⚡ **Re-evaluación automática**

- Cada vez que edites el issue, se ejecuta una nueva evaluación
- **No hay límite** de intentos
- **No necesitas crear issues nuevos**

---

## 🎯 Criterios de Aprobación para Semana 1

### **Puntaje mínimo**: 75/100

### **Elementos obligatorios**

- ✅ `main.py` con aplicación FastAPI funcional
- ✅ `requirements.txt` con fastapi y uvicorn
- ✅ `README.md` con instrucciones básicas
- ✅ Endpoint `GET /` que responde JSON
- ✅ `/docs` accesible (documentación automática)

### **Estructura mínima esperada**

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

  ```text
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

### ✅ **Antes de subir tu issue**

1. **Prueba localmente**: `uvicorn main:app --reload`
2. **Verifica `/docs`**: Ve a <http://localhost:8000/docs>
3. **Repositorio público**: Verifica en GitHub que no tenga el candado 🔒
4. **URL correcta**: Copia la URL exacta desde la barra del navegador

### ✅ **Estructura recomendada**

```text
mi-proyecto-fastapi/
├── main.py              # Aplicación principal
├── requirements.txt     # Dependencias
├── README.md           # Documentación
└── .gitignore          # Opcional pero recomendado
```

### ✅ **README.md básico**

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

```text
ficha-apellido-nombre-fastapi-semanaX
```

**Donde:**

- `ficha` = Tu número de ficha/curso (ej: 3147246)
- `apellido` = Tu apellido en minúsculas
- `nombre` = Tu nombre en minúsculas
- `semanaX` = El número de la semana (semana1, semana2, etc.)

### **✅ Ejemplos CORRECTOS:**

```text
3147246-rodriguez-juan-fastapi-semana1
2766065-perez-maria-fastapi-semana2
1234567-garcia-carlos-fastapi-semana3
4567890-martinez-ana-fastapi-semana4
```

### **❌ Ejemplos INCORRECTOS:**

```text
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

## 🧪 Week 5: Testing y Documentación Avanzada

### **🎯 Objetivo de la Semana 5**

Implementar un **sistema completo de testing** y **documentación profesional** para tu API FastAPI, preparándola para deployment en producción. Esta semana te convertirás en un desarrollador que sabe garantizar la calidad del código.

### **📋 Checklist de Requisitos para Week 5**

#### **🔧 Testing Setup (35 puntos)**

- ✅ **Configuración de Pytest** (8 pts)

  - `pytest.ini` o configuración en `pyproject.toml`
  - Configuración de paths, marcadores y opciones
  - Ejemplo: `testpaths = ["tests"]`, `python_files = ["test_*.py"]`

- ✅ **Dependencias de Testing** (7 pts)

  - `pytest`, `httpx`, `pytest-asyncio` en requirements.txt
  - Dependencias para testing de BD (ej: `pytest-cov`, `faker`)
  - Versiones compatibles especificadas

- ✅ **Estructura de Tests** (8 pts)

  - Directorio `tests/` organizado por tipos
  - `conftest.py` con fixtures compartidas
  - Organización por categorías (unit, integration, e2e)

- ✅ **Configuración de BD de Test** (12 pts)
  - Base de datos separada para testing (SQLite recomendado)
  - Setup y teardown automático de BD en tests
  - Fixtures para datos de prueba limpios

#### **🔬 Unit Testing (25 puntos)**

- ✅ **Tests de Modelos** (8 pts)

  - Validación de modelos SQLAlchemy
  - Tests de modelos Pydantic (validaciones, defaults)
  - Tests de constraints y relaciones

- ✅ **Tests de Funciones Utilitarias** (7 pts)

  - Tests para funciones auxiliares
  - Tests de validación de datos
  - Tests con mocks cuando sea necesario

- ✅ **Tests de Lógica de Negocio** (10 pts)
  - Tests para reglas de negocio específicas
  - Tests de cálculos y procesamiento
  - Tests de flujos complejos

#### **🌐 Integration Testing (25 puntos)**

- ✅ **Tests de Endpoints** (10 pts)
  - Tests con `TestClient` de FastAPI
  - Validación de status codes y responses
  - Tests de diferentes HTTP methods
- ✅ **Tests de Integración BD** (8 pts)
  - Tests de operaciones CRUD completas
  - Tests de transacciones
  - Tests con datos reales
- ✅ **Tests de Manejo de Errores** (7 pts)
  - Tests de casos de error esperados
  - Tests de validación de entrada
  - Tests de responses de error

#### **📚 Documentation (15 puntos)**

- ✅ **Personalización OpenAPI** (5 pts)
  - Título, descripción y versión personalizados
  - Tags y metadata de endpoints
  - Configuración de responses
- ✅ **Ejemplos de API** (5 pts)
  - Ejemplos en requests y responses
  - Documentación de parámetros
  - Casos de uso claros
- ✅ **README de Deployment** (5 pts)
  - Instrucciones de instalación
  - Variables de entorno documentadas
  - Comandos para deployment

### **📁 Estructura Mínima Esperada**

```text
ficha-apellido-nombre-fastapi-semana5/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app con metadata personalizada
│   ├── models.py            # Modelos SQLAlchemy
│   ├── schemas.py           # Schemas Pydantic
│   ├── database.py          # Configuración de BD
│   └── utils.py             # Funciones utilitarias
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures compartidas
│   ├── test_models.py       # Tests unitarios de modelos
│   ├── test_endpoints.py    # Tests de integración de API
│   ├── test_utils.py        # Tests de funciones utilitarias
│   └── test_database.py     # Tests de integración de BD
├── pytest.ini              # Configuración de pytest
├── requirements.txt         # Incluyendo deps de testing
└── README.md               # Con info de deployment
```

### **⚙️ Ejemplo de Configuración**

#### **pytest.ini**

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
asyncio_mode = auto
```

#### **conftest.py - Configuración Completa de Testing**

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base

# Base de datos de test (SQLite en memoria para velocidad)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture
def db():
    """Fixture para base de datos de testing con setup/teardown automático"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    """Fixture para cliente HTTP con BD de test"""
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def sample_reserva_data():
    """Datos de prueba para reservas"""
    return {
        "nombre": "Juan Pérez",
        "email": "juan@email.com",
        "fecha": "2024-12-25T19:00:00",
        "personas": 4,
        "telefono": "+1234567890"
    }

@pytest.fixture
def created_reserva(client, sample_reserva_data):
    """Fixture que crea una reserva para testing"""
    response = client.post("/reservas/", json=sample_reserva_data)
    return response.json()
```

        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
def override_get_db():
try:
yield db
finally:
db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

````

#### **FastAPI con Metadata Personalizada (main.py)**

```python
from fastapi import FastAPI

app = FastAPI(
    title="Mi API de Reservas",
    description="Sistema completo de reservas para restaurante con testing avanzado",
    version="2.0.0",
    contact={
        "name": "Tu Nombre",
        "email": "tu.email@ejemplo.com",
    },
    license_info={
        "name": "MIT",
    },
)

@app.get("/", tags=["Health"], summary="Health Check")
def health_check():
    """Endpoint para verificar que la API está funcionando."""
    return {"status": "healthy", "version": "2.0.0"}

@app.get("/reservas/", tags=["Reservas"], summary="Listar Reservas")
def get_reservas():
    """
    Obtiene todas las reservas disponibles.

    Returns:
        Lista de reservas con sus detalles completos.
    """
    return {"reservas": []}
````

#### **Requirements.txt con Testing**

```txt
# API Core
fastapi>=0.68.0
uvicorn[standard]>=0.15.0
sqlalchemy>=1.4.0

# Testing
pytest>=6.0.0
pytest-asyncio>=0.21.0
httpx>=0.24.0
pytest-cov>=4.0.0

# Optional: Coverage y reporting
coverage>=6.0
```

### **🚀 Comandos Esenciales para Week 5**

#### **Ejecutar Tests**

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con verbose output
pytest -v

# Ejecutar tests específicos
pytest tests/test_models.py -v

# Ejecutar con cobertura
pytest --cov=app --cov-report=html

# Ejecutar solo tests unitarios
pytest tests/unit/ -v

# Ejecutar solo tests de integración
pytest tests/integration/ -v
```

#### **Verificar Documentación**

```bash
# Iniciar la API
uvicorn app.main:app --reload

# Verificar endpoints de documentación:
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
# - OpenAPI JSON: http://localhost:8000/openapi.json
```

#### **Estructura de Tests Recomendada**

```text
tests/
├── conftest.py              # Fixtures globales
├── unit/
│   ├── test_models.py       # Tests de modelos
│   ├── test_schemas.py      # Tests de Pydantic schemas
│   └── test_utils.py        # Tests de funciones utilitarias
├── integration/
│   ├── test_endpoints.py    # Tests de endpoints
│   ├── test_database.py     # Tests de BD
│   └── test_auth.py         # Tests de autenticación
└── e2e/
    └── test_flows.py        # Tests end-to-end
```

### **✅ Verificación Pre-entrega Week 5**

Antes de crear tu issue, ejecuta estos comandos:

```bash
# 1. Verificar que todos los tests pasan
pytest -v

# 2. Verificar cobertura mínima
pytest --cov=app --cov-report=term

# 3. Verificar que la API arranca
uvicorn app.main:app --reload

# 4. Verificar documentación
curl http://localhost:8000/docs

# 5. Verificar estructura de archivos
find . -name "*.py" | grep -E "(test_|conftest)" | head -10
```

**Checklist de pre-entrega:**

- [ ] ✅ Todos los tests pasan sin errores
- [ ] ✅ Cobertura de tests > 70%
- [ ] ✅ API arranca sin errores
- [ ] ✅ Documentación visible en `/docs`
- [ ] ✅ README.md actualizado con comandos de testing
- [ ] ✅ requirements.txt incluye dependencias de testing

---

## 🎓 ¿Qué Sigue Después de Aprobar?

### **Week 1 → Week 2**

1. **¡Felicitaciones!** 🎉 Has completado la Semana 1
2. **Continúa aprendiendo** con la Semana 2: Modelos con Pydantic

### **Week 2 → Week 3**

1. **¡Excelente!** 🚀 Has dominado los modelos Pydantic
2. **Siguiente paso**: Semana 3: Base de Datos con SQLAlchemy

### **Week 3 → Week 4**

1. **¡Increíble!** 💪 Ya manejas bases de datos básicas
2. **Continúa**: Semana 4: Bases de Datos Avanzadas

### **Week 4 → Week 5**

1. **¡Impresionante!** 🔥 Dominas bases de datos avanzadas
2. **Continúa**: Semana 5: Testing y Documentación Avanzada

### **Week 5 → Siguientes Semanas**

1. **¡Profesional!** ⭐ Has implementado testing completo
2. **Próximos pasos**:

   - Semana 6: Autenticación y Seguridad
   - Semana 7: Deploy y DevOps
   - Semana 8: Performance y Optimización
   - Semana 9: Microservicios
   - Semana 10: Monitoreo y Logging
   - Semana 11: Proyecto Final Integrador

### **📚 Recursos Adicionales**

- **Mantén tu repositorio** - puede ser útil para futuras referencias
- **Comparte tu experiencia** con otros estudiantes
- **Continúa practicando** - la práctica hace al maestro

---

> 💡 **Recuerda**: Este evaluador es una herramienta de aprendizaje. Su objetivo es ayudarte a interiorizar los conceptos fundamentales de FastAPI mediante feedback inmediato y criterios claros.

## ¡Éxitos con tu proyecto! 🚀
