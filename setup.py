"""
Setup para el sistema de evaluación automática de FastAPI
"""
from setuptools import setup, find_packages
from pathlib import Path

# Leer el README para la descripción larga
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Leer requirements básicos
requirements = [
    "fastapi>=0.68.0",
    "uvicorn[standard]>=0.15.0",
    "pydantic>=1.8.0",
    "requests>=2.25.0",
    "PyYAML>=5.4.0",
    "jinja2>=3.0.0",
    "markdown>=3.3.0",
    "click>=8.0.0"
]

# Requirements de desarrollo
dev_requirements = [
    "pytest>=6.0.0",
    "pytest-asyncio>=0.15.0",
    "black>=21.0.0",
    "isort>=5.9.0",
    "flake8>=3.9.0",
    "mypy>=0.910"
]

setup(
    name="fastapi-evaluator",
    version="1.0.0",
    description="Sistema de evaluación automática para bootcamp de FastAPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="EPTI Dev Team",
    author_email="dev@epti.com",
    url="https://github.com/epti-dev/fastapi-evaluator",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "": ["*.yaml", "*.yml", "*.md", "*.txt", "*.json"],
        "weeks": ["**/*"],
        "core": ["**/*"],
        "evaluator": ["**/*"]
    },
    install_requires=requirements,
    extras_require={
        "dev": dev_requirements,
        "test": ["pytest>=6.0.0", "pytest-asyncio>=0.15.0"],
        "docs": ["mkdocs>=1.2.0", "mkdocs-material>=7.0.0"]
    },
    entry_points={
        "console_scripts": [
            "fastapi-evaluate=evaluate:main",
            "fastapi-test=test_system:main"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Education",
        "Topic :: Software Development :: Testing",
        "Framework :: FastAPI"
    ],
    python_requires=">=3.8",
    keywords="fastapi, evaluation, bootcamp, automated-testing, education",
    project_urls={
        "Bug Reports": "https://github.com/epti-dev/fastapi-evaluator/issues",
        "Source": "https://github.com/epti-dev/fastapi-evaluator",
        "Documentation": "https://github.com/epti-dev/fastapi-evaluator/wiki"
    }
)
