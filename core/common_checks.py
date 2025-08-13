"""
Checks comunes que pueden ser reutilizados por todos los evaluadores semanales.
Estos checks proporcionan funcionalidad base que es común a múltiples semanas.
"""
import sys
import subprocess
import importlib.util
from pathlib import Path
from typing import Dict, Any, List, Optional, Union


class CommonChecks:
    """
    Clase que encapsula checks comunes reutilizables entre semanas.
    """
    
    def __init__(self, repo_path: Union[str, Path]):
        """
        Inicializa los checks comunes.
        
        Args:
            repo_path: Ruta al repositorio del estudiante
        """
        self.repo_path = Path(repo_path).resolve()
    
    # === FILE STRUCTURE CHECKS ===
    
    def check_file_exists(self, file_path: str) -> bool:
        """Verifica si un archivo existe en el repositorio"""
        return (self.repo_path / file_path).exists()
    
    def check_required_files(self, required_files: List[str]) -> Dict[str, bool]:
        """
        Verifica múltiples archivos requeridos.
        
        Args:
            required_files: Lista de rutas de archivos requeridos
            
        Returns:
            Dict con el estado de cada archivo
        """
        return {
            file_path: self.check_file_exists(file_path)
            for file_path in required_files
        }
    
    def check_directory_structure(self, expected_dirs: List[str]) -> Dict[str, bool]:
        """
        Verifica que existan directorios esperados.
        
        Args:
            expected_dirs: Lista de directorios esperados
            
        Returns:
            Dict con el estado de cada directorio
        """
        return {
            dir_path: (self.repo_path / dir_path).is_dir()
            for dir_path in expected_dirs
        }
    
    # === DEPENDENCY CHECKS ===
    
    def check_requirements_file(self) -> Dict[str, Any]:
        """
        Analiza el archivo requirements.txt.
        
        Returns:
            Dict con información sobre las dependencias
        """
        req_file = self.repo_path / "requirements.txt"
        
        if not req_file.exists():
            return {
                "exists": False,
                "packages": [],
                "valid_format": False
            }
        
        try:
            content = req_file.read_text(encoding="utf-8", errors="ignore")
            lines = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
            
            packages = []
            for line in lines:
                # Parse package name (ignore version specifiers)
                pkg_name = line.split("==")[0].split(">=")[0].split("<=")[0].split("~=")[0].split("!=")[0]
                packages.append(pkg_name.strip())
            
            return {
                "exists": True,
                "packages": packages,
                "valid_format": True,
                "content": content
            }
            
        except Exception as e:
            return {
                "exists": True,
                "packages": [],
                "valid_format": False,
                "error": str(e)
            }
    
    def check_package_in_requirements(self, package_name: str) -> bool:
        """
        Verifica si un paquete específico está en requirements.txt.
        Soporta extras como uvicorn[standard].
        
        Args:
            package_name: Nombre del paquete a buscar
            
        Returns:
            True si el paquete está presente
        """
        req_info = self.check_requirements_file()
        if not req_info["exists"]:
            return False
        
        package_name_lower = package_name.lower()
        
        # Buscar coincidencia exacta o como parte de un paquete con extras
        for pkg in req_info["packages"]:
            pkg_lower = pkg.lower()
            # Coincidencia exacta
            if pkg_lower == package_name_lower:
                return True
            # Coincidencia con extras (ej: uvicorn[standard] contiene uvicorn)
            if '[' in pkg_lower and pkg_lower.split('[')[0] == package_name_lower:
                return True
        
        return False
    
    def check_multiple_packages(self, packages: List[str]) -> Dict[str, bool]:
        """
        Verifica múltiples paquetes en requirements.txt.
        
        Args:
            packages: Lista de nombres de paquetes
            
        Returns:
            Dict con el estado de cada paquete
        """
        return {
            package: self.check_package_in_requirements(package)
            for package in packages
        }
    
    def check_any_package(self, packages: List[str]) -> Dict[str, bool]:
        """
        Verifica si al menos uno de varios paquetes está presente en requirements.txt.
        Útil para verificar drivers de BD o paquetes alternativos.
        
        Args:
            packages: Lista de nombres de paquetes alternativos
            
        Returns:
            Dict con el estado de cada paquete
        """
        return {
            package: self.check_package_in_requirements(package)
            for package in packages
        }
    
    # === PYTHON CODE CHECKS ===
    
    def check_python_syntax(self, file_path: str) -> Dict[str, Any]:
        """
        Verifica la sintaxis de un archivo Python.
        
        Args:
            file_path: Ruta relativa al archivo Python
            
        Returns:
            Dict con información sobre la sintaxis
        """
        full_path = self.repo_path / file_path
        
        if not full_path.exists():
            return {
                "file_exists": False,
                "syntax_valid": False,
                "error": f"File not found: {file_path}"
            }
        
        try:
            content = full_path.read_text(encoding="utf-8", errors="ignore")
            compile(content, str(full_path), 'exec')
            
            return {
                "file_exists": True,
                "syntax_valid": True,
                "line_count": len(content.splitlines()),
                "character_count": len(content)
            }
            
        except SyntaxError as e:
            return {
                "file_exists": True,
                "syntax_valid": False,
                "error": f"Syntax error: {e}",
                "line_number": e.lineno,
                "column": e.offset
            }
        except Exception as e:
            return {
                "file_exists": True,
                "syntax_valid": False,
                "error": f"Error reading file: {e}"
            }
    
    def check_imports_in_file(self, file_path: str, expected_imports: List[str]) -> Dict[str, bool]:
        """
        Verifica que imports específicos estén presentes en un archivo.
        
        Args:
            file_path: Ruta al archivo Python
            expected_imports: Lista de imports esperados
            
        Returns:
            Dict con el estado de cada import
        """
        full_path = self.repo_path / file_path
        
        if not full_path.exists():
            return {import_name: False for import_name in expected_imports}
        
        try:
            content = full_path.read_text(encoding="utf-8", errors="ignore")
            content_lower = content.lower()
            
            results = {}
            for import_name in expected_imports:
                # Buscar diferentes patrones de import
                patterns = [
                    f"import {import_name}",
                    f"from {import_name} import",
                    f"from {import_name.split('.')[0]} import"
                ]
                
                found = any(pattern.lower() in content_lower for pattern in patterns)
                results[import_name] = found
            
            return results
            
        except Exception:
            return {import_name: False for import_name in expected_imports}
    
    def check_class_or_function_exists(self, file_path: str, name: str) -> bool:
        """
        Verifica si una clase o función específica existe en un archivo.
        
        Args:
            file_path: Ruta al archivo Python
            name: Nombre de la clase o función
            
        Returns:
            True si existe
        """
        full_path = self.repo_path / file_path
        
        if not full_path.exists():
            return False
        
        try:
            content = full_path.read_text(encoding="utf-8", errors="ignore")
            
            # Buscar definiciones de clase o función
            patterns = [
                f"class {name}",
                f"def {name}(",
                f"async def {name}("
            ]
            
            return any(pattern in content for pattern in patterns)
            
        except Exception:
            return False
    
    # === APP IMPORT CHECKS ===
    
    def check_fastapi_app_exists(self, main_file: str = "main.py") -> Dict[str, Any]:
        """
        Verifica que exista una aplicación FastAPI en el archivo principal.
        
        Args:
            main_file: Nombre del archivo principal
            
        Returns:
            Dict con información sobre la app FastAPI
        """
        full_path = self.repo_path / main_file
        
        if not full_path.exists():
            return {
                "file_exists": False,
                "has_fastapi_import": False,
                "has_app_instance": False,
                "app_variable_name": None
            }
        
        try:
            content = full_path.read_text(encoding="utf-8", errors="ignore")
            
            # Verificar import de FastAPI
            has_fastapi_import = any(
                pattern in content.lower() for pattern in [
                    "from fastapi import",
                    "import fastapi"
                ]
            )
            
            # Buscar instancia de app
            app_patterns = [
                "app = FastAPI()",
                "app=FastAPI()",
                "app = fastapi.FastAPI()",
                "app=fastapi.FastAPI()"
            ]
            
            has_app_instance = any(pattern in content for pattern in app_patterns)
            
            # Intentar encontrar el nombre de la variable app
            app_variable_name = None
            if "= FastAPI()" in content:
                for line in content.split('\n'):
                    if "= FastAPI()" in line:
                        app_variable_name = line.split('=')[0].strip()
                        break
            
            return {
                "file_exists": True,
                "has_fastapi_import": has_fastapi_import,
                "has_app_instance": has_app_instance,
                "app_variable_name": app_variable_name or "app",
                "content_analysis": self._analyze_main_content(content)
            }
            
        except Exception as e:
            return {
                "file_exists": True,
                "has_fastapi_import": False,
                "has_app_instance": False,
                "app_variable_name": None,
                "error": str(e)
            }
    
    def _analyze_main_content(self, content: str) -> Dict[str, Any]:
        """Analiza el contenido del archivo main.py"""
        lines = content.split('\n')
        
        return {
            "total_lines": len(lines),
            "non_empty_lines": len([line for line in lines if line.strip()]),
            "has_endpoints": "@app." in content,
            "has_get_decorator": "@app.get" in content,
            "has_post_decorator": "@app.post" in content,
            "has_root_endpoint": "@app.get(\"/\")" in content or "@app.get('/')" in content,
            "estimated_complexity": "simple" if len(lines) < 30 else "medium" if len(lines) < 100 else "complex"
        }
    
    # === README CHECKS ===
    
    def check_readme_content(self, readme_file: str = "README.md") -> Dict[str, Any]:
        """
        Analiza el contenido del README.
        
        Args:
            readme_file: Nombre del archivo README
            
        Returns:
            Dict con análisis del README
        """
        full_path = self.repo_path / readme_file
        
        if not full_path.exists():
            return {
                "exists": False,
                "has_title": False,
                "has_installation": False,
                "has_usage": False,
                "has_examples": False,
                "estimated_completeness": 0
            }
        
        try:
            content = full_path.read_text(encoding="utf-8", errors="ignore")
            content_lower = content.lower()
            
            # Análisis de contenido
            has_title = content.startswith("#") or "fastapi" in content_lower
            has_installation = any(term in content_lower for term in [
                "pip install", "requirements.txt", "instalación", "installation"
            ])
            has_usage = any(term in content_lower for term in [
                "uvicorn", "python main.py", "how to run", "uso", "usage"
            ])
            has_examples = any(term in content_lower for term in [
                "curl", "example", "ejemplo", "http://", "localhost"
            ])
            
            # Puntuación de completitud (0-100)
            completeness_score = 0
            if has_title: completeness_score += 25
            if has_installation: completeness_score += 25
            if has_usage: completeness_score += 25
            if has_examples: completeness_score += 25
            
            return {
                "exists": True,
                "has_title": has_title,
                "has_installation": has_installation,
                "has_usage": has_usage,
                "has_examples": has_examples,
                "estimated_completeness": completeness_score,
                "character_count": len(content),
                "line_count": len(content.split('\n')),
                "word_count": len(content.split())
            }
            
        except Exception as e:
            return {
                "exists": True,
                "has_title": False,
                "has_installation": False,
                "has_usage": False,
                "has_examples": False,
                "estimated_completeness": 0,
                "error": str(e)
            }
    
    # === DOCKER CHECKS ===
    
    def check_docker_setup(self) -> Dict[str, Any]:
        """
        Verifica la configuración de Docker.
        
        Returns:
            Dict con información sobre Docker setup
        """
        dockerfile_exists = self.check_file_exists("Dockerfile")
        dockercompose_exists = self.check_file_exists("docker-compose.yml") or self.check_file_exists("docker-compose.yaml")
        dockerignore_exists = self.check_file_exists(".dockerignore")
        
        docker_analysis = {}
        
        if dockerfile_exists:
            docker_analysis.update(self._analyze_dockerfile())
        
        if dockercompose_exists:
            docker_analysis.update(self._analyze_docker_compose())
        
        return {
            "dockerfile_exists": dockerfile_exists,
            "docker_compose_exists": dockercompose_exists,
            "dockerignore_exists": dockerignore_exists,
            "analysis": docker_analysis
        }
    
    def _analyze_dockerfile(self) -> Dict[str, Any]:
        """Analiza el contenido del Dockerfile"""
        dockerfile_path = self.repo_path / "Dockerfile"
        
        try:
            content = dockerfile_path.read_text(encoding="utf-8", errors="ignore")
            content_lower = content.lower()
            
            return {
                "has_python_base": "from python" in content_lower,
                "has_workdir": "workdir" in content_lower,
                "has_copy_requirements": "copy requirements.txt" in content_lower,
                "has_pip_install": "pip install" in content_lower,
                "has_expose": "expose" in content_lower,
                "has_cmd": "cmd" in content_lower or "entrypoint" in content_lower,
                "estimated_quality": "good" if all([
                    "from python" in content_lower,
                    "workdir" in content_lower,
                    "copy" in content_lower,
                    "pip install" in content_lower
                ]) else "needs_improvement"
            }
            
        except Exception:
            return {"analysis_error": True}
    
    def _analyze_docker_compose(self) -> Dict[str, Any]:
        """Analiza el archivo docker-compose.yml"""
        compose_files = ["docker-compose.yml", "docker-compose.yaml"]
        
        for compose_file in compose_files:
            compose_path = self.repo_path / compose_file
            if compose_path.exists():
                try:
                    content = compose_path.read_text(encoding="utf-8", errors="ignore")
                    content_lower = content.lower()
                    
                    return {
                        "has_services": "services:" in content_lower,
                        "has_ports": "ports:" in content_lower,
                        "has_volumes": "volumes:" in content_lower,
                        "has_environment": "environment:" in content_lower,
                        "estimated_complexity": "simple" if content.count("services:") == 1 else "multi_service"
                    }
                    
                except Exception:
                    return {"analysis_error": True}
        
        return {}
    
    # === UTILITY METHODS ===
    
    def run_command(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """
        Ejecuta un comando en el directorio del repositorio.
        
        Args:
            command: Comando a ejecutar
            timeout: Timeout en segundos
            
        Returns:
            Dict con resultado del comando
        """
        try:
            result = subprocess.run(
                command.split(),
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": result.returncode == 0,
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds"
            }
        except Exception as e:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(e)
            }


# Factory function para facilitar el uso
def create_common_checks(repo_path: Union[str, Path]) -> CommonChecks:
    """
    Factory function para crear una instancia de CommonChecks.
    
    Args:
        repo_path: Ruta al repositorio del estudiante
        
    Returns:
        Instancia configurada de CommonChecks
    """
    return CommonChecks(repo_path)
