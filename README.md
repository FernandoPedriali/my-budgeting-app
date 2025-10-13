# My Budgeting App

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
.venv\Scripts\activate

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
