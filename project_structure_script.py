#!/usr/bin/env python3
"""
Script para criar a estrutura de pastas do projeto my-budgeting-app
Execução: python create_structure.py
"""

import os
from pathlib import Path


def create_structure():
    """Cria a estrutura completa de pastas e arquivos __init__.py"""
    
    # Estrutura de diretórios
    directories = [
        # Backend
        "backend/alembic/versions",
        "backend/app/models",
        "backend/app/schemas",
        "backend/app/repositories",
        "backend/app/services",
        "backend/app/api/v1",
        "backend/app/core",
        "backend/app/utils",
        "backend/tests/unit",
        "backend/tests/integration",
        
        # Frontend
        "frontend/app/components/base",
        "frontend/app/components/custom",
        "frontend/app/layouts",
        "frontend/app/pages",
        "frontend/app/services",
        "frontend/app/utils",
        "frontend/app/theme",
        "frontend/static/images",
        "frontend/static/icons",
        
        # Docker
        "docker",
        
        # Docs
        "docs/api",
        
        # GitHub
        ".github/workflows",
        
        # VSCode
        ".vscode",
    ]
    
    # Arquivos __init__.py que devem ser criados
    init_files = [
        # Backend
        "backend/app/__init__.py",
        "backend/app/models/__init__.py",
        "backend/app/schemas/__init__.py",
        "backend/app/repositories/__init__.py",
        "backend/app/services/__init__.py",
        "backend/app/api/__init__.py",
        "backend/app/api/v1/__init__.py",
        "backend/app/core/__init__.py",
        "backend/app/utils/__init__.py",
        "backend/tests/__init__.py",
        
        # Frontend
        "frontend/app/__init__.py",
        "frontend/app/components/__init__.py",
        "frontend/app/components/base/__init__.py",
        "frontend/app/components/custom/__init__.py",
        "frontend/app/layouts/__init__.py",
        "frontend/app/pages/__init__.py",
        "frontend/app/services/__init__.py",
        "frontend/app/utils/__init__.py",
        "frontend/app/theme/__init__.py",
    ]
    
    # Arquivos placeholder importantes
    placeholder_files = {
        "backend/app/main.py": '"""FastAPI Application Entry Point"""\n\n# TODO: Implement FastAPI app\n',
        "backend/app/config.py": '"""Application Configuration"""\n\n# TODO: Implement config\n',
        "backend/app/database.py": '"""Database Setup"""\n\n# TODO: Implement SQLAlchemy setup\n',
        "backend/alembic/env.py": '"""Alembic Environment Configuration"""\n\n# TODO: Configure Alembic\n',
        "backend/tests/conftest.py": '"""Pytest Fixtures"""\n\n# TODO: Implement fixtures\n',
        
        "frontend/app/main.py": '"""NiceGUI Application Entry Point"""\n\n# TODO: Implement NiceGUI app\n',
        "frontend/app/config.py": '"""Frontend Configuration"""\n\n# TODO: Implement config\n',
        "frontend/app/theme/styles.css": '/* Custom Styles */\n\n/* TODO: Add custom CSS */\n',
        
        ".env.example": """# Database
DATABASE_URL=postgresql://user:password@localhost:5432/budgeting_app

# API
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=True

# Frontend
FRONTEND_HOST=0.0.0.0
FRONTEND_PORT=8080

# Environment
ENVIRONMENT=development
DEBUG=True
""",
        
        ".gitignore": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment variables
.env
.env.local

# Database
*.db
*.sqlite3

# Docker
*.log

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Alembic
alembic/versions/*.pyc
""",
        
        "README.md": """# My Budgeting App

Sistema de controle financeiro pessoal desenvolvido em Python.

## 🚀 Tecnologias

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: NiceGUI + Quasar
- **Infraestrutura**: Docker + Docker Compose

## 📋 Pré-requisitos

- Python 3.11+
- Docker e Docker Compose
- Git

## 🔧 Instalação

```bash
# Clone o repositório
git clone https://github.com/FernandoPedriali/my-budgeting-app.git
cd my-budgeting-app

# Crie o ambiente virtual
python -m venv .venv

# Ative o ambiente virtual
# Linux/Mac:
source .venv/bin/activate
# Windows:
.venv\\Scripts\\activate

# Instale as dependências
pip install -e .

# Configure as variáveis de ambiente
cp .env.example .env

# Inicie os containers
docker-compose up -d
```

## 🏗️ Estrutura do Projeto

```
my-budgeting-app/
├── backend/          # API FastAPI
├── frontend/         # Interface NiceGUI
├── docker/           # Configurações Docker
└── docs/             # Documentação
```

## 📚 Documentação

- [API Documentation](docs/api/)
- [Design System](docs/design-system.md)
- [Development Guide](docs/development.md)

## 🧪 Testes

```bash
# Executar testes
pytest

# Executar com coverage
pytest --cov=backend/app
```

## 📝 Convenções de Código

- Seguimos PEP 8
- Type hints obrigatórios
- Docstrings em formato Google Style

## 🤝 Contribuindo

1. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
2. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
3. Push para a branch (`git push origin feature/AmazingFeature`)
4. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

## ✨ Autor

Fernando Pedriali
""",
        
        "pyproject.toml": """[project]
name = "my-budgeting-app"
version = "0.1.0"
description = "Sistema de controle financeiro pessoal"
authors = [{name = "Fernando Pedriali"}]
requires-python = ">=3.11"

dependencies = [
    "fastapi>=0.110.0",
    "uvicorn[standard]>=0.27.0",
    "sqlalchemy>=2.0.0",
    "alembic>=1.13.0",
    "psycopg2-binary>=2.9.9",
    "pydantic>=2.6.0",
    "pydantic-settings>=2.1.0",
    "nicegui>=1.4.0",
    "httpx>=0.26.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "black>=24.0.0",
    "ruff>=0.2.0",
    "mypy>=1.8.0",
]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 100
target-version = ['py311']

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["backend/tests"]
asyncio_mode = "auto"
""",
        
        "docker-compose.yml": """version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: budgeting_db
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: budgeting_app
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: .
      dockerfile: docker/backend.Dockerfile
    container_name: budgeting_backend
    command: uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://user:password@postgres:5432/budgeting_app
    volumes:
      - ./backend:/app/backend
    depends_on:
      postgres:
        condition: service_healthy

  frontend:
    build:
      context: .
      dockerfile: docker/frontend.Dockerfile
    container_name: budgeting_frontend
    command: python -m frontend.app.main
    ports:
      - "8080:8080"
    environment:
      API_URL: http://backend:8000
    volumes:
      - ./frontend:/app/frontend
    depends_on:
      - backend

volumes:
  postgres_data:
""",
        
        "alembic.ini": """# A generic, single database configuration.

[alembic]
script_location = backend/alembic
prepend_sys_path = .
version_path_separator = os

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
""",
        
        ".vscode/settings.json": """{
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.ruffEnabled": true,
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.tabSize": 4
  },
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
""",
        
        ".vscode/launch.json": """{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Backend: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "backend.app.main:app",
        "--reload",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
      ],
      "jinja": true,
      "justMyCode": false
    },
    {
      "name": "Frontend: NiceGUI",
      "type": "python",
      "request": "launch",
      "module": "frontend.app.main",
      "justMyCode": false
    },
    {
      "name": "Tests: Pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": [
        "backend/tests",
        "-v"
      ],
      "justMyCode": false
    }
  ]
}
""",
        
        "docker/backend.Dockerfile": """FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Copy application code
COPY backend ./backend

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
""",
        
        "docker/frontend.Dockerfile": """FROM python:3.11-slim

WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Copy application code
COPY frontend ./frontend

CMD ["python", "-m", "frontend.app.main"]
""",
        
        "docs/development.md": """# Guia de Desenvolvimento

## Setup do Ambiente

### 1. Ambiente Virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\\Scripts\\activate     # Windows
```

### 2. Instalar Dependências

```bash
pip install -e ".[dev]"
```

### 3. Configurar Banco de Dados

```bash
# Iniciar PostgreSQL
docker-compose up -d postgres

# Criar migrations
alembic revision --autogenerate -m "Initial migration"

# Aplicar migrations
alembic upgrade head
```

## Executando a Aplicação

### Backend (FastAPI)

```bash
uvicorn backend.app.main:app --reload
```

API disponível em: http://localhost:8000
Docs disponível em: http://localhost:8000/docs

### Frontend (NiceGUI)

```bash
python -m frontend.app.main
```

Interface disponível em: http://localhost:8080

## Testes

```bash
# Todos os testes
pytest

# Com coverage
pytest --cov=backend/app --cov-report=html

# Testes específicos
pytest backend/tests/unit/
pytest backend/tests/integration/
```

## Convenções

### Commits

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Manutenção

### Código

- PEP 8 compliance
- Type hints obrigatórios
- Docstrings em formato Google Style
- Máximo 100 caracteres por linha
""",
    }
    
    print("🚀 Criando estrutura do projeto my-budgeting-app...\n")
    
    # Criar diretórios
    print("📁 Criando diretórios...")
    for directory in directories:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        print(f"   ✓ {directory}")
    
    # Criar arquivos __init__.py
    print("\n📄 Criando arquivos __init__.py...")
    for init_file in init_files:
        path = Path(init_file)
        path.touch(exist_ok=True)
        print(f"   ✓ {init_file}")
    
    # Criar arquivos placeholder
    print("\n📝 Criando arquivos de configuração...")
    for file_path, content in placeholder_files.items():
        path = Path(file_path)
        if not path.exists():
            path.write_text(content, encoding='utf-8')
            print(f"   ✓ {file_path}")
    
    print("\n✨ Estrutura criada com sucesso!")
    print("\n📋 Próximos passos:")
    print("   1. cd my-budgeting-app")
    print("   2. python -m venv .venv")
    print("   3. source .venv/bin/activate  # ou .venv\\Scripts\\activate no Windows")
    print("   4. pip install -e .")
    print("   5. cp .env.example .env")
    print("   6. docker-compose up -d")
    print("\n🎉 Bom desenvolvimento!")


if __name__ == "__main__":
    create_structure()
