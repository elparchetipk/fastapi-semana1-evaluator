# 🔄 Guía de Re-evaluación para Instructores

## Métodos para Re-evaluar Issues Existentes

Después de realizar correcciones en el sistema de evaluación, existen varias formas de activar la re-evaluación de issues ya enviados por estudiantes.

### 1. 💬 Re-evaluación por Comentarios (Automática)

Los estudiantes pueden activar una re-evaluación comentando en su issue:

```
/evaluar
```

```
/re-evaluar
```

```
/check
```

**Activación automática**: El workflow se ejecuta inmediatamente cuando detecta estos comandos.

### 2. ✏️ Re-evaluación por Edición (Automática)

Los estudiantes pueden editar su issue original y la evaluación se ejecutará automáticamente al guardar los cambios.

### 3. 🔧 Re-evaluación Masiva Manual (GitHub Actions)

Para re-evaluar múltiples issues de una semana específica:

1. Ve a **Actions** en el repositorio
2. Selecciona **"🔄 Re-evaluación Masiva"**
3. Haz clic en **"Run workflow"**
4. Configura los parámetros:
   - **Semana**: 1-11
   - **Label adicional**: (opcional) Ej: `revisar`, `pendiente`
   - **Modo de prueba**: Activa para ver qué se haría sin ejecutar

### 4. 🐍 Script Local de Re-evaluación

Para control más granular desde la línea de comandos:

```bash
# Instalar dependencias
pip install requests

# Configurar token de GitHub
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# Re-evaluar semana 1 (modo de prueba)
python scripts/reevaluate_issues.py --owner epti --repo bc-channel --week 1 --dry-run

# Re-evaluar semana 1 (real)
python scripts/reevaluate_issues.py --owner epti --repo bc-channel --week 1

# Re-evaluar solo issues con label "revisar"
python scripts/reevaluate_issues.py --owner epti --repo bc-channel --week 1 --labels revisar

# Limitar a 10 issues
python scripts/reevaluate_issues.py --owner epti --repo bc-channel --week 1 --max-issues 10
```

## 📋 Casos de Uso Comunes

### Después de Corregir un Bug

```bash
# 1. Identifica la semana afectada
# 2. Ejecuta en modo de prueba para ver el alcance
python scripts/reevaluate_issues.py --owner epti --repo bc-channel --week 2 --dry-run

# 3. Ejecuta la re-evaluación real
python scripts/reevaluate_issues.py --owner epti --repo bc-channel --week 2
```

### Re-evaluar Solo Issues Pendientes

```bash
python scripts/reevaluate_issues.py --owner epti --repo bc-channel --week 1 --labels pendiente,revisar
```

### Re-evaluación Masiva con GitHub Actions

1. **Actions** → **🔄 Re-evaluación Masiva** → **Run workflow**
2. Selecciona semana y parámetros
3. Ejecuta en modo de prueba primero
4. Ejecuta la re-evaluación real

## 🔍 Monitoreo y Verificación

### Verificar que la Re-evaluación Funcionó

1. Revisa los **Actions** del repositorio para ver ejecuciones recientes
2. Verifica que los issues tengan nuevos comentarios con evaluaciones actualizadas
3. Comprueba que los labels se actualizaron correctamente (`aprobado`/`revisar`)

### Logs y Debugging

- **GitHub Actions**: Ve a la pestaña Actions para logs detallados
- **Script local**: El script proporciona output detallado del progreso
- **Issues**: Cada re-evaluación deja un comentario con timestamp

## ⚠️ Consideraciones Importantes

### Rate Limiting

- **GitHub Actions**: Maneja automáticamente el rate limiting
- **Script local**: Incluye pausas de 1 segundo entre requests
- **Comentarios manuales**: Sin límites prácticos para uso normal

### Permisos Requeridos

- **Token de GitHub**: Necesita permisos de `issues:write`
- **Repository**: Debe tener permisos de escritura en issues

### Mejores Prácticas

1. **Siempre ejecuta en modo de prueba primero** con `--dry-run`
2. **Limita el número de issues** con `--max-issues` para pruebas
3. **Usa labels específicos** para targeting preciso
4. **Monitorea los logs** para detectar problemas
5. **Informa a los estudiantes** sobre las re-evaluaciones masivas

## 🚨 Resolución de Problemas

### Error de Token

```bash
export GITHUB_TOKEN=ghp_xxxxxxxxxxxx
```

### Rate Limiting

- Reduce `--max-issues`
- Aumenta las pausas en el script
- Usa GitHub Actions para procesos masivos

### Issues No Encontrados

- Verifica los labels exactos: `evaluacion`, `semana-X`
- Confirma que los issues estén abiertos (`state: open`)
- Revisa los permisos del token

### Workflow No Se Ejecuta

- Verifica que el issue tenga el label `evaluacion`
- Confirma que el comentario contiene `/evaluar`, `/re-evaluar` o `/check`
- Revisa los logs en la pestaña Actions

---

## 📞 Soporte

Para problemas técnicos:

1. Revisa los logs en **Actions**
2. Verifica la configuración del token
3. Confirma los permisos del repositorio
4. Contacta al equipo técnico con los logs específicos
