from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./Info.sqlite3"

# Для SQLite: check_same_thread=False при работе с многопоточностью/uvicorn
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Импорт моделей регистрирует их в Base.metadata перед create_all().
from . import models  # noqa: E402,F401

def init_db():
    # Вызывать при инициализации (например, при первом запуске), или использовать Alembic
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()