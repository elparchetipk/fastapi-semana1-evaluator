# Semana 10: API Avanzada - WebSockets y Background Tasks

⏰ **DURACIÓN TOTAL: 6 HORAS EXACTAS**  
📚 **NIVEL: Avanzado (construye sobre Semanas 1-9)**

## 🚨 **IMPORTANTE: Expandiendo las Capacidades de la API**

Esta semana está diseñada para estudiantes que **ya tienen una API completa containerizada con testing y deployment** (Semanas 1-9). Implementaremos funcionalidades avanzadas de tiempo real y procesamiento en background para crear aplicaciones más robustas y escalables.

- ✅ **Completamente realizable en 6 horas**
- ✅ **Enfoque práctico en funcionalidades modernas**
- ✅ **Preparación para aplicaciones de alto rendimiento**

## 🎯 Objetivos de la Semana (Fundamentales)

Al finalizar esta semana de 6 horas (incluye break de 30 min), los estudiantes:

1. ✅ **Implementarán WebSockets** para comunicación en tiempo real
2. ✅ **Configurarán Background Tasks** para procesamiento asíncrono
3. ✅ **Integrarán Server-Sent Events (SSE)** para actualizaciones en vivo
4. ✅ **Aplicarán caching avanzado** con Redis y técnicas de optimización
5. ✅ **Crearán aplicaciones interactivas** con funcionalidades de tiempo real

### ❌ **Lo que NO se espera dominar esta semana**

- Microservicios complejos con message brokers
- WebSockets clustering y scaling horizontal
- Background processing distribuido con Celery
- Streaming de datos masivos
- Implementación completa de GraphQL subscriptions

## ⏱️ Distribución de Tiempo (6 horas total)

| Bloque | Actividad                    | Tiempo | Descripción                                  |
| ------ | ---------------------------- | ------ | -------------------------------------------- |
| **1**  | WebSockets y Tiempo Real     | 90 min | Implementación de comunicación bidireccional |
| **2**  | Background Tasks y Jobs      | 90 min | Procesamiento asíncrono y tareas programadas |
| **3**  | Server-Sent Events y Caching | 90 min | Eventos en tiempo real y optimización        |
| **4**  | Aplicación Integrada         | 90 min | Chat en tiempo real con notificaciones       |

## 📚 Contenido de la Semana

### **📋 Navegación Ordenada (Seguir este orden)**

1. **[🧭 1-teoria/](./1-teoria/)** - Conceptos de comunicación en tiempo real y async
2. **[💻 2-practica/](./2-practica/)** - Implementación de WebSockets y Background Tasks
3. **[🎯 3-ejercicios/](./3-ejercicios/)** - Ejercicios de aplicaciones en tiempo real
4. **[🚀 4-proyecto/](./4-proyecto/)** - Sistema de chat y notificaciones completo
5. **[📚 5-recursos/](./5-recursos/)** - Referencias y herramientas avanzadas

### **🗂️ Estructura Detallada**

```
semana-10/
├── 📄 README.md                          # Esta guía principal
├── 📄 RUBRICA_EVALUACION.md              # Criterios de evaluación
├── 📁 1-teoria/
│   └── 📄 01-api-avanzada-conceptos.md   # WebSockets, SSE, Background Tasks
├── 📁 2-practica/
│   ├── 📄 35-websockets-tiempo-real.md   # Implementación WebSockets
│   ├── 📄 36-background-tasks.md         # Tareas en background
│   ├── 📄 37-server-sent-events.md      # Events y streaming
│   └── 📄 38-aplicacion-integrada.md    # Chat completo con notificaciones
├── 📁 3-ejercicios/
│   ├── 📄 README.md                      # Guía de ejercicios
│   └── 📄 ejercicios-api-avanzada.md    # Ejercicios prácticos
├── 📁 4-proyecto/
│   ├── 📄 README.md                      # Guía del proyecto
│   └── 📄 especificacion-chat.md        # Sistema de chat en tiempo real
└── 📁 5-recursos/
    ├── 📄 referencias.md                 # Enlaces y documentación
    ├── 📄 websockets-cheatsheet.md      # Comandos y patrones WebSockets
    └── 📄 performance-tips.md           # Optimización y mejores prácticas
```

## 🔧 Prácticas de la Semana

### **📋 Práctica 35: WebSockets y Tiempo Real (90 min)**

- Configuración de WebSockets en FastAPI
- Gestión de conexiones y salas
- Implementación de chat básico
- Manejo de errores y desconexiones

### **📋 Práctica 36: Background Tasks (90 min)**

- Tasks síncronos y asíncronos
- Procesamiento de emails y notificaciones
- Integración con Redis para queues
- Monitoring y logs de tasks

### **📋 Práctica 37: Server-Sent Events (90 min)**

- SSE para actualizaciones en vivo
- Streaming de datos en tiempo real
- Caching inteligente con Redis
- Optimización de performance

### **📋 Práctica 38: Aplicación Integrada (90 min)**

- Chat completo con WebSockets
- Notificaciones con Background Tasks
- Dashboard de actividad con SSE
- Deployment con Docker

## 📅 Cronograma de la Jornada de 6 Horas

| Tiempo      | Actividad                  | Duración | Acumulado |
| ----------- | -------------------------- | -------- | --------- |
| 12:00-13:30 | WebSockets y Tiempo Real   | 90 min   | 90 min    |
| 13:30-14:00 | Background Tasks (parte 1) | 30 min   | 120 min   |
| 14:00-14:30 | **☕ BREAK OBLIGATORIO**   | 30 min   | 150 min   |
| 14:30-15:30 | Background Tasks (parte 2) | 60 min   | 210 min   |
| 15:30-17:00 | Server-Sent Events         | 90 min   | 300 min   |
| 17:00-18:00 | Aplicación Integrada       | 60 min   | 360 min   |

**Total**: Exactamente 6 horas (360 minutos)

## 🎯 Ejercicios Prácticos

1. **🔌 WebSocket Chat**: Sistema de mensajería en tiempo real
2. **📧 Email Processor**: Background tasks para notificaciones
3. **📊 Dashboard Live**: Actualizaciones en tiempo real con SSE
4. **🔔 Notification System**: Sistema completo de notificaciones
5. **🎮 Game Engine**: Motor simple de juego multijugador
6. **💬 Proyecto Integrador**: Sistema de chat empresarial completo

## 🚀 Proyecto de la Semana

### **Sistema de Chat Empresarial en Tiempo Real**

Desarrollarás un sistema completo de comunicación que incluye:

- **💬 Chat en tiempo real** con WebSockets
- **📧 Notificaciones por email** con Background Tasks
- **📊 Dashboard de actividad** con Server-Sent Events
- **🔒 Autenticación integrada** (usando semanas anteriores)
- **🐳 Containerización completa** (usando semana 9)
- **🧪 Testing de WebSockets** (usando semana 8)

## 📊 Criterios de Evaluación

### **Funcionalidades Core (60%)**

- WebSockets funcionando correctamente
- Background Tasks procesando trabajos
- Server-Sent Events actualizando en tiempo real
- Integración con sistema de autenticación existente

### **Calidad Técnica (25%)**

- Manejo apropiado de conexiones
- Error handling y recovery
- Performance y optimización
- Clean code y documentación

### **Integración (15%)**

- Uso de conocimientos de semanas anteriores
- Containerización apropiada
- Testing de componentes asíncronos
- Deployment funcional

## 🏆 Criterios de Éxito

### **✅ Mínimo Viable (Aprobado - 70%)**

- WebSocket básico funcionando
- Al menos un Background Task implementado
- SSE básico con actualizaciones simples
- Integración con autenticación existente

### **🎯 Implementación Completa (Bueno - 85%)**

- Sistema de chat completo
- Múltiples tipos de Background Tasks
- Dashboard en tiempo real funcional
- Manejo de errores robusto

### **🌟 Implementación Avanzada (Excelente - 95%)**

- Chat con salas y funcionalidades avanzadas
- Sistema de notificaciones complejo
- Optimizaciones de performance aplicadas
- Monitoring y métricas implementadas

## 🚀 Quick Start

### **1. Preparación del Entorno**

```bash
# 1. Navegar a semana 10
cd semana-10

# 2. Verificar instalaciones previas
docker --version
redis-server --version

# 3. Activar entorno virtual (si usas uno)
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# 4. Instalar dependencias adicionales
pip install websockets python-socketio
```

### **2. Verificar Base de Semanas Anteriores**

```bash
# Verificar que tienes una API funcionando de semanas anteriores
curl http://localhost:8000/health
curl http://localhost:8000/docs

# Verificar autenticación (de semana 7)
curl -X POST http://localhost:8000/auth/login

# Verificar container (de semana 9)
docker-compose ps
```

### **3. Empezar con Teoría**

```bash
# Leer conceptos fundamentales
# 📖 1-teoria/01-api-avanzada-conceptos.md
```

### **4. Continuar con Primera Práctica**

```bash
# Implementar WebSockets básico
# 💻 2-practica/35-websockets-tiempo-real.md
```

## 🔗 Conexión con Semanas Anteriores

### **🏗️ Construye sobre:**

- **Semana 1-3**: Base de FastAPI y APIs REST
- **Semana 4-6**: Modelos de datos y CRUD completo
- **Semana 7**: Sistema de autenticación y autorización
- **Semana 8**: Testing y calidad de código
- **Semana 9**: Containerización y deployment

### **🚀 Prepara para:**

- **Semana 11**: Proyecto final integrador con todas las tecnologías

## 💡 Tips de la Semana

- **⚡ Performance**: WebSockets pueden ser resource-intensive, monitorea conexiones
- **🔒 Security**: Autentica conexiones WebSocket usando tokens de semanas anteriores
- **🧪 Testing**: Los tests asíncronos requieren técnicas especiales
- **📊 Monitoring**: Implementa métricas para Background Tasks y conexiones
- **🐳 Docker**: Considera networking especial para WebSockets en containers

---

## 📋 Antes de Empezar

### ✅ **Checklist de Prerrequisitos**

- [ ] ✅ **API REST completa** funcionando (Semanas 1-6)
- [ ] ✅ **Sistema de autenticación** implementado (Semana 7)
- [ ] ✅ **Tests automatizados** pasando (Semana 8)
- [ ] ✅ **Aplicación containerizada** (Semana 9)
- [ ] ✅ **Redis** instalado y funcionando
- [ ] ✅ **Docker** y Docker Compose operativos
- [ ] ✅ **Postman** o cliente WebSocket para testing

### 🚨 **Si algo no funciona**

1. **Revisar semanas anteriores** - Esta semana asume que todo lo previo funciona
2. **Verificar dependencias** - Redis, Docker, y librerías async
3. **Consultar recursos** - Referencias y troubleshooting en `5-recursos/`

---

**🎯 ¡Bienvenidos a la Semana 10! Llevemos nuestras APIs al siguiente nivel con funcionalidades en tiempo real.**

---

_Semana 10 - API Avanzada - Bootcamp FastAPI_  
_Duración: 6 horas exactas_
