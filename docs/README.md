# 📖 Documentación FastAPI Course Evaluator

Bienvenido a la documentación completa del sistema de evaluación automática para el curso de FastAPI.

## 📋 Índice de Documentación

### 🏗️ Arquitectura y Desarrollo

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitectura detallada del sistema
- **[ARCHITECTURE_ROOT.md](ARCHITECTURE_ROOT.md)** - Arquitectura a nivel de proyecto
- **[MIGRATION_SUMMARY.md](MIGRATION_SUMMARY.md)** - Resumen de migraciones realizadas
- **[PROYECTO_COMPLETADO.md](PROYECTO_COMPLETADO.md)** - Estado del proyecto

### 👥 Guías de Usuario

- **[GUIA_ESTUDIANTES.md](GUIA_ESTUDIANTES.md)** - Guía completa para estudiantes
- **[REEVALUACION_GUIA.md](REEVALUACION_GUIA.md)** - Guía de re-evaluación para instructores

### 📊 Evaluación y Resultados

- **[RESUMEN_EVALUACION.md](RESUMEN_EVALUACION.md)** - Resumen del sistema de evaluación
- **[ejemplos/](ejemplos/)** - Ejemplos de evaluaciones

### 📁 Estructura por Semanas

Cada semana tiene su propia documentación en `/weeks/weekXX/`:

- `README.md` - Objetivos y requisitos de la semana
- `criteria.yaml` - Criterios de evaluación detallados
- `RUBRICA_EVALUACION.md` - Rúbrica de evaluación

## 🚀 Enlaces Rápidos

### Para Estudiantes

1. **[Cómo funciona la evaluación](GUIA_ESTUDIANTES.md#como-funciona-la-evaluacion)**
2. **[Formato de entrega](GUIA_ESTUDIANTES.md#formato-de-entrega)**
3. **[Ejemplos de evaluación](ejemplos/)**

### Para Instructores

1. **[Sistema de re-evaluación](REEVALUACION_GUIA.md)**
2. **[Arquitectura del evaluador](ARCHITECTURE.md)**
3. **[Configuración de GitHub](REEVALUACION_GUIA.md#configuracion-github)**

### Para Desarrolladores

1. **[Estructura del código](ARCHITECTURE.md#estructura-de-codigo)**
2. **[Agregar nueva semana](ARCHITECTURE.md#agregar-nueva-semana)**
3. **[Ejecutar tests](../README.md#testing)**

## 🔧 Configuración Rápida

```bash
# Clonar repositorio
git clone <repository>
cd fastapi-course-evaluator

# Instalar dependencias
pip install -r requirements.txt

# Evaluar un repositorio
python evaluator/run.py --week 1 --repo /path/to/repo
```

## ❓ Soporte

Para dudas o problemas:

1. Revisar la documentación correspondiente
2. Buscar en [Issues](../../../issues) existentes
3. Crear un nuevo [Issue](../../../issues/new) si es necesario

---

**Última actualización:** Agosto 2025  
**Versión:** 1.0.0
