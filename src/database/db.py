from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.config import get_settings
from src.database.base import Base

settings = get_settings()

def _build_engine():
    return create_engine(
        settings.database_url,
        echo=settings.sql_echo,
        pool_pre_ping=True
    )

engine = _build_engine()

SessionLocal = sessionmaker(bind=engine,autoflush=True)

def get_db():
    db = SessionLocal()

    try:
        yield db
    except:
        db.rollback()
        raise
    finally:
        db.close()

def create_tables():
    from src.models import departments,employees,leave_requests,leave_types,user
    Base.metadata.create_all(bind=engine)