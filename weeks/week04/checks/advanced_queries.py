"""
Check para verificar queries avanzadas con SQLAlchemy
"""
import re
from pathlib import Path
from typing import Dict, Any, List


def check_advanced_queries(repo_path: str) -> Dict[str, Any]:
    """
    Verifica el uso de queries avanzadas con SQLAlchemy
    """
    results = {
        "has_joins": False,
        "has_filters": False,
        "has_aggregations": False,
        "has_subqueries": False,
        "has_pagination": False,
        "has_ordering": False,
        "score": 0,
        "details": [],
        "errors": [],
        "query_count": 0
    }
    
    try:
        repo_path = Path(repo_path)
        
        # Buscar archivos Python
        python_files = []
        for py_file in repo_path.rglob("*.py"):
            if "venv" not in str(py_file) and "__pycache__" not in str(py_file):
                python_files.append(py_file)
        
        # Patrones para detectar queries avanzadas
        join_patterns = [
            r'\.join\s*\(',
            r'\.outerjoin\s*\(',
            r'\.left_join\s*\(',
            r'joinedload',
            r'selectinload'
        ]
        
        filter_patterns = [
            r'\.filter\s*\(',
            r'\.filter_by\s*\(',
            r'\.where\s*\(',
            r'and_\s*\(',
            r'or_\s*\('
        ]
        
        aggregation_patterns = [
            r'func\.count',
            r'func\.sum',
            r'func\.avg',
            r'func\.max',
            r'func\.min',
            r'group_by',
            r'having'
        ]
        
        subquery_patterns = [
            r'\.subquery\s*\(',
            r'exists\s*\(',
            r'any_\s*\(',
            r'\.scalar_subquery'
        ]
        
        pagination_patterns = [
            r'\.limit\s*\(',
            r'\.offset\s*\(',
            r'paginate',
            r'skip.*take',
            r'limit.*offset'
        ]
        
        ordering_patterns = [
            r'\.order_by\s*\(',
            r'desc\s*\(',
            r'asc\s*\(',
            r'\.sort'
        ]
        
        for py_file in python_files:
            try:
                content = py_file.read_text(encoding='utf-8')
                
                # Contar queries básicas
                query_indicators = [
                    r'session\.query',
                    r'db\.query',
                    r'select\s*\(',
                    r'\.all\s*\(',
                    r'\.first\s*\(',
                    r'\.one\s*\('
                ]
                
                for pattern in query_indicators:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    results["query_count"] += len(matches)
                
                # Verificar joins
                for pattern in join_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["has_joins"] = True
                        break
                
                # Verificar filtros
                for pattern in filter_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["has_filters"] = True
                        break
                
                # Verificar agregaciones
                for pattern in aggregation_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["has_aggregations"] = True
                        break
                
                # Verificar subqueries
                for pattern in subquery_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["has_subqueries"] = True
                        break
                
                # Verificar paginación
                for pattern in pagination_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["has_pagination"] = True
                        break
                
                # Verificar ordenamiento
                for pattern in ordering_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        results["has_ordering"] = True
                        break
                
            except Exception as e:
                results["errors"].append(f"❌ Error leyendo {py_file.name}: {str(e)}")
        
        # Calcular score basado en hallazgos
        if results["query_count"] > 0:
            results["details"].append(f"✅ {results['query_count']} operación(es) de query encontrada(s)")
            results["score"] += 1
        
        if results["has_joins"]:
            results["details"].append("✅ Queries con JOIN implementadas")
            results["score"] += 3
        else:
            results["errors"].append("❌ No se encontraron queries con JOIN")
        
        if results["has_filters"]:
            results["details"].append("✅ Filtros avanzados implementados")
            results["score"] += 2
        else:
            results["errors"].append("❌ No se encontraron filtros avanzados")
        
        if results["has_aggregations"]:
            results["details"].append("✅ Funciones de agregación utilizadas")
            results["score"] += 2
        
        if results["has_subqueries"]:
            results["details"].append("✅ Subqueries implementadas")
            results["score"] += 2
        
        if results["has_pagination"]:
            results["details"].append("✅ Paginación implementada")
            results["score"] += 1
        
        if results["has_ordering"]:
            results["details"].append("✅ Ordenamiento de resultados implementado")
            results["score"] += 1
        
        # Máximo 10 puntos para este check
        results["score"] = min(results["score"], 10)
        
    except Exception as e:
        results["errors"].append(f"❌ Error verificando queries avanzadas: {str(e)}")
    
    return results


def get_advanced_queries_score(repo_path: str) -> float:
    """Obtiene el score de queries avanzadas (0-10 puntos)"""
    result = check_advanced_queries(repo_path)
    return result["score"]


def get_advanced_queries_feedback(repo_path: str) -> List[str]:
    """Obtiene feedback específico para queries avanzadas"""
    result = check_advanced_queries(repo_path)
    feedback = []
    
    if result["errors"]:
        for error in result["errors"]:
            feedback.append(error)
    
    if not result["has_joins"]:
        feedback.append("• Implementar queries con JOIN entre tablas relacionadas")
    
    if not result["has_filters"]:
        feedback.append("• Usar filtros avanzados (.filter(), .where(), and_(), or_())")
    
    if not result["has_aggregations"]:
        feedback.append("• Implementar funciones de agregación (count, sum, avg, etc.)")
    
    if not result["has_pagination"]:
        feedback.append("• Agregar paginación con limit() y offset()")
    
    if result["query_count"] == 0:
        feedback.append("• Implementar operaciones de consulta a la base de datos")
    
    return feedback
