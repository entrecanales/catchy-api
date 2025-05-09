from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from core.config import CONNECTION_STRING

engine = create_engine(CONNECTION_STRING)  # loads the connection string
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
