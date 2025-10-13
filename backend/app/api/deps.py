"""API dependencies."""

from typing import Generator

from sqlalchemy.orm import Session

from backend.app.database import SessionLocal


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
