# 🏗️ Arquitectura para Evaluación de 11 Semanas

## 📋 Estrategia Recomendada: Arquitectura Modular

### 🎯 **Principios de Diseño**

1. **DRY (Don't Repeat Yourself)**: Componentes comunes reutilizables
2. **Separación de responsabilidades**: Cada semana es independiente
3. **Configuración sobre código**: Criterios en archivos de config
4. **Escalabilidad**: Fácil agregar nuevas semanas

### 🏗️ **Estructura Propuesta**

```
fastapi-curriculum-evaluator/
├── 📁 core/                           # Lógica común reutilizable
│   ├── base_evaluator.py              # Clase base para todos los evaluadores
│   ├── common_checks.py               # Checks reutilizables (estructura, deps, etc)
│   ├── scoring_engine.py              # Motor de puntuación configurable
│   ├── report_generator.py            # Generador de reportes
│   ├── github_integration.py          # Integración con GitHub API
│   └── utils/
│       ├── file_utils.py
│       ├── test_runner.py
│       └── docker_utils.py
├── 📁 weeks/                          # Evaluadores específicos por semana
│   ├── week01_hello_world/
│   │   ├── evaluator.py               # Lógica específica de la semana
│   │   ├── criteria.yaml              # Criterios y puntajes
│   │   ├── checks/                    # Verificaciones específicas
│   │   │   ├── endpoints.py
│   │   │   └── documentation.py
│   │   └── templates/
│   │       ├── feedback.md
│   │       └── issue_template.yml
│   ├── week02_crud_basic/
│   │   ├── evaluator.py
│   │   ├── criteria.yaml
│   │   ├── checks/
│   │   │   ├── crud_operations.py
│   │   │   ├── data_validation.py
│   │   │   └── error_handling.py
│   │   └── templates/
│   ├── week03_database/
│   │   ├── evaluator.py
│   │   ├── criteria.yaml
│   │   ├── checks/
│   │   │   ├── sqlalchemy_setup.py
│   │   │   ├── models.py
│   │   │   └── migrations.py
│   │   └── templates/
│   ├── week04_auth/
│   │   └── ... (JWT, passwords, roles)
│   ├── week05_middleware/
│   │   └── ... (CORS, logging, rate limiting)
│   ├── week06_testing/
│   │   └── ... (pytest, coverage, mocking)
│   ├── week07_deployment/
│   │   └── ... (Docker, Docker Compose)
│   ├── week08_monitoring/
│   │   └── ... (Logging, metrics, health checks)
│   ├── week09_optimization/
│   │   └── ... (Performance, caching, async)
│   ├── week10_advanced/
│   │   └── ... (WebSockets, background tasks)
│   └── week11_final_project/
│       └── ... (Proyecto integrador completo)
├── 📁 .github/
│   ├── workflows/
│   │   ├── evaluate-week1.yml         # Workflow por semana
│   │   ├── evaluate-week2.yml
│   │   └── ... (uno por semana)
│   └── ISSUE_TEMPLATE/
│       ├── week01.yml                 # Template por semana
│       ├── week02.yml
│       └── ...
├── 📁 cli/                            # CLI para testing local
│   ├── main.py
│   └── commands/
├── 📁 docs/                           # Documentación
│   ├── week_breakdown.md
│   ├── instructor_guide.md
│   └── student_guide.md
├── requirements.txt
├── docker-compose.yml                 # Para testing local
└── README.md
```

### 🔧 **Componentes Clave**

#### **1. BaseEvaluator (core/base_evaluator.py)**

```python
from abc import ABC, abstractmethod
from typing import Dict, Any
import yaml

class BaseEvaluator(ABC):
    def __init__(self, week_number: int, student_repo_path: str):
        self.week = week_number
        self.repo_path = student_repo_path
        self.criteria = self.load_criteria()

    def load_criteria(self) -> Dict:
        """Carga criterios desde archivo YAML"""
        with open(f"weeks/week{self.week:02d}/criteria.yaml") as f:
            return yaml.safe_load(f)

    @abstractmethod
    def run_specific_checks(self) -> Dict[str, Any]:
        """Implementado por cada semana"""
        pass

    def evaluate(self) -> Dict[str, Any]:
        """Pipeline común de evaluación"""
        results = {}

        # Checks comunes (estructura, deps básicas)
        results.update(self.run_common_checks())

        # Checks específicos de la semana
        results.update(self.run_specific_checks())

        # Scoring
        score = self.calculate_score(results)

        # Reporte
        report = self.generate_report(results, score)

        return {
            "results": results,
            "score": score,
            "report": report,
            "passed": score["total"] >= self.criteria["passing_threshold"]
        }
```

#### **2. Configuración por Semana (weeks/week01/criteria.yaml)**

```yaml
week_info:
  number: 1
  title: 'Hello World API'
  description: 'Fundamentos de FastAPI'
  passing_threshold: 70

categories:
  setup:
    weight: 25
    checks:
      - name: 'requirements_txt'
        points: 5
        description: 'Archivo requirements.txt presente'
      - name: 'fastapi_dependency'
        points: 8
        description: 'FastAPI incluido en requirements'
      - name: 'uvicorn_dependency'
        points: 4
        description: 'Uvicorn incluido en requirements'
      - name: 'main_py_exists'
        points: 4
        description: 'Archivo main.py presente'
      - name: 'readme_exists'
        points: 4
        description: 'README.md presente'

  functionality:
    weight: 40
    checks:
      - name: 'app_import'
        points: 15
        description: 'Aplicación FastAPI importable'
      - name: 'root_endpoint'
        points: 15
        description: 'Endpoint GET / funcional'
      - name: 'parametric_endpoint'
        points: 10
        description: 'Endpoint con parámetros'

  documentation:
    weight: 20
    checks:
      - name: 'docs_accessible'
        points: 12
        description: '/docs accesible'
      - name: 'json_responses'
        points: 8
        description: 'Respuestas en formato JSON'

  deliverables:
    weight: 15
    checks:
      - name: 'project_structure'
        points: 15
        description: 'Estructura de proyecto adecuada'
```

#### **3. Evaluador Específico (weeks/week01/evaluator.py)**

```python
from core.base_evaluator import BaseEvaluator
from .checks.endpoints import check_endpoints
from .checks.documentation import check_documentation

class Week01Evaluator(BaseEvaluator):
    def run_specific_checks(self) -> Dict[str, Any]:
        results = {}

        # Checks específicos de Hello World
        results["endpoints"] = check_endpoints(self.repo_path)
        results["documentation"] = check_documentation(self.repo_path)

        return results
```

### 🚀 **Flujo de Trabajo por Semana**

#### **GitHub Actions (workflows/evaluate-week1.yml)**

```yaml
name: Evaluate Week 1
on:
  issues:
    types: [opened, edited]
  workflow_dispatch:

jobs:
  evaluate:
    if: contains(join(github.event.issue.labels.*.name, ','), 'week1')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Extract and clone student repo
        run: |
          # Extrae URL del issue
          python cli/main.py extract-repo --issue-body "${{ github.event.issue.body }}"

      - name: Run Week 1 Evaluation
        run: |
          python cli/main.py evaluate --week 1 --repo ./student_repo

      - name: Post feedback
        uses: peter-evans/create-or-update-comment@v4
        with:
          issue-number: ${{ github.event.issue.number }}
          body-file: evaluation_report.md
```

### 📊 **Ventajas de esta Arquitectura**

1. **🔄 Reutilización**: Componentes comunes evitan duplicación
2. **🎯 Especialización**: Cada semana puede tener lógica única
3. **📈 Escalabilidad**: Fácil agregar semanas 12, 13, etc.
4. **🛠️ Mantenimiento**: Updates independientes por semana
5. **👥 Paralelización**: Equipos pueden trabajar simultáneamente
6. **🧪 Testing**: Cada semana se puede testear independientemente
7. **📋 Configuración**: Criterios modificables sin tocar código

### 🎯 **Progresión de Complejidad por Semanas**

```
Week 1-2:  Hello World + CRUD básico
Week 3-4:  Base de datos + modelos
Week 5-6:  Autenticación + autorización
Week 7-8:  Testing + deployment
Week 9-10: Optimización + features avanzadas
Week 11:   Proyecto integrador completo
```

### 🚀 **Implementación Sugerida**

1. **Fase 1**: Migrar Week 1 actual a la nueva arquitectura
2. **Fase 2**: Crear core components reutilizables
3. **Fase 3**: Implementar Weeks 2-3 usando el nuevo framework
4. **Fase 4**: Paralelizar desarrollo de Weeks 4-11
5. **Fase 5**: Testing integral y documentación

¿Te parece bien esta estrategia? ¿Quieres que empecemos implementando algún componente específico?
