# FastAPI Course Evaluator

Sistema de evaluación automática para curso de FastAPI con análisis estático seguro y feedback estructurado.

## ✨ Características

- **Evaluación automática** de repositorios de estudiantes
- **Análisis estático** sin ejecutar código del estudiante
- **Feedback estructurado** por semana y criterios
- **Integración con GitHub** via issues y workflows
- **Re-evaluación automática** por comentarios o edición de issues
- **Soporte multi-semana** (Weeks 1-11)

## 🚀 Uso Rápido

```bash
# Evaluar repositorio local
python evaluator/run.py --week 1 --repo /path/to/student/repo

# Evaluar desde GitHub URL
python evaluator/run.py --week 2 --repo https://github.com/student/repo

# Re-evaluar issues masivamente
python scripts/reevaluate_issues.py --repo owner/repo
```

## 📚 Semanas Disponibles

| Semana | Tema                     | Estado |
| ------ | ------------------------ | ------ |
| 1      | FastAPI Básico           | ✅     |
| 2      | Bases de Datos           | ✅     |
| 3      | Autenticación JWT        | ✅     |
| 4      | Bases de Datos Avanzadas | ✅     |
| 5      | Testing y Documentación  | 🚧     |
| 6-11   | Por definir              | ⏳     |

## 🔧 Instalación

```bash
git clone https://github.com/your-org/fastapi-course-evaluator.git
cd fastapi-course-evaluator
pip install -r requirements.txt
```

## 📖 Documentación

- **[Índice Completo](docs/README.md)** - Navegación por toda la documentación
- **[Guía de Arquitectura](docs/ARCHITECTURE.md)** - Estructura del sistema
- **[Guía para Estudiantes](docs/GUIA_ESTUDIANTES.md)** - Cómo usar el evaluador
- **[Guía de Re-evaluación](docs/REEVALUACION_GUIA.md)** - Para instructores
- **[Ejemplos de Evaluación](docs/ejemplos/)** - Casos de uso

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Implementa los cambios
4. Agrega tests si es necesario
5. Submit un pull request

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.
