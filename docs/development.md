# Guia de Desenvolvimento

## Setup do Ambiente

### 1. Ambiente Virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
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
