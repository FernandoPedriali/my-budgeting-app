"""Database configuration and session management."""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from .config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # Verifica conexão antes de usar
    pool_size=10,  # Número de conexões no pool
    max_overflow=20,  # Conexões extras além do pool_size
    echo=settings.DEBUG,  # Log SQL queries em desenvolvimento
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency para obter sessão do banco de dados.

    Yields:
        Session: Sessão do SQLAlchemy

    Example:
        ```python
        @router.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
        ```
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
