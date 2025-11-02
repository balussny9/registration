# backend/app/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from pathlib import Path
from .settings import settings

def _resolve_sqlite_url(url: str) -> str:
    """
    Turn a relative sqlite path like 'sqlite:///./data/ssp.db'
    into an absolute path anchored at the backend/app folder.
    Also ensures the parent folder exists.
    """
    if not url.startswith("sqlite:///"):
        return url

    path = url.replace("sqlite:///", "", 1)
    # If already absolute (starts with /), leave it
    if path.startswith("/"):
        db_path = Path(path)
    else:
        # Anchor relative path to this file's folder (backend/app)
        base = Path(__file__).resolve().parent
        db_path = (base / path).resolve()

    db_path.parent.mkdir(parents=True, exist_ok=True)
    # Final absolute URL. Note: db_path starts with '/', so this becomes 'sqlite:////...'
    return f"sqlite:///{db_path}"

DATABASE_URL = _resolve_sqlite_url(settings.DATABASE_URL)

# Needed for SQLite when used across threads
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
