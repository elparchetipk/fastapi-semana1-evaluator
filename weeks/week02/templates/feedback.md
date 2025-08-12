# 📋 Feedback de Evaluación - Semana 2: CRUD Básico con FastAPI

**Estudiante**: {{student_name}}  
**Fecha de Evaluación**: {{evaluation_date}}  
**Score Final**: {{final_score|round(1)}}/100 ({{status}})

---

## 📊 Resumen de Resultados

### ✅ Aspectos Completados

{{#completed_aspects}}

- ✅ {{.}}
  {{/completed_aspects}}

### ⚠️ Aspectos por Mejorar

{{#improvement_aspects}}

- ⚠️ {{.}}
  {{/improvement_aspects}}

### ❌ Aspectos Faltantes

{{#missing_aspects}}

- ❌ {{.}}
  {{/missing_aspects}}

---

## 🔍 Análisis Detallado

### 📁 Estructura del Proyecto ({{structure_score}}/100)

{{#structure_feedback}}

- {{.}}
  {{/structure_feedback}}

### 🏗️ Modelos Pydantic ({{models_score}}/100)

{{#models_feedback}}

- {{.}}
  {{/models_feedback}}

### 🔧 Operaciones CRUD ({{crud_score}}/100)

{{#crud_feedback}}

- {{.}}
  {{/crud_feedback}}

### 🌐 Endpoints y API ({{endpoints_score}}/100)

{{#endpoints_feedback}}

- {{.}}
  {{/endpoints_feedback}}

### ✅ Validación de Datos ({{validation_score}}/100)

{{#validation_feedback}}

- {{.}}
  {{/validation_feedback}}

### 📝 Calidad de Código ({{quality_score}}/100)

{{#quality_feedback}}

- {{.}}
  {{/quality_feedback}}

---

## 🎯 Recomendaciones Específicas

### 🚀 Prioridad Alta

{{#high_priority}}

1. **{{title}}**: {{description}}
   ```{{language}}
   {{code_example}}
   ```
   {{/high_priority}}

### 📈 Mejoras Sugeridas

{{#medium_priority}}

- **{{title}}**: {{description}}
  {{/medium_priority}}

### 💡 Optimizaciones Opcionales

{{#low_priority}}

- {{.}}
  {{/low_priority}}

---

## 📚 Recursos de Apoyo

### 📖 Documentación

- [FastAPI CRUD Operations](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Pydantic Models](https://pydantic-docs.helpmanual.io/usage/models/)
- [HTTP Status Codes](https://fastapi.tiangolo.com/tutorial/response-status-code/)

### 💻 Ejemplos de Código

#### Modelo Pydantic Básico

```python
from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
```

#### Endpoints CRUD Básicos

```python
from fastapi import FastAPI, HTTPException
from typing import List

app = FastAPI()

# Base de datos en memoria
items_db = {}
next_id = 1

@app.post("/items/", response_model=Item)
def create_item(item: ItemCreate):
    global next_id
    new_item = Item(id=next_id, **item.dict())
    items_db[next_id] = new_item
    next_id += 1
    return new_item

@app.get("/items/", response_model=List[Item])
def read_items():
    return list(items_db.values())

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item_update: ItemUpdate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    stored_item = items_db[item_id]
    update_data = item_update.dict(exclude_unset=True)
    updated_item = stored_item.copy(update=update_data)
    items_db[item_id] = updated_item
    return updated_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": "Item deleted successfully"}
```

---

## 🎯 Objetivos para la Próxima Semana

{{#next_week_objectives}}

- [ ] {{.}}
      {{/next_week_objectives}}

---

## 📞 Soporte

Si tienes dudas sobre este feedback:

1. Revisa la documentación oficial de FastAPI
2. Consulta los ejemplos de código proporcionados
3. Participa en las sesiones de Q&A
4. Contacta a tu instructor

**¡Sigue adelante! 🚀 Cada línea de código te acerca más a ser un desarrollador experto en FastAPI.**
