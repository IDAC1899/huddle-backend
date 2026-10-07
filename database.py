from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config.environment import DATABASE_URL

# Connect FastAPI with SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    # hosted databases close idle connections, so check each one before using it
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()