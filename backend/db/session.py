from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import databases

DATABASE_URL = "postgresql://rachistoteles:rachistoteles@localhost/venmitodb"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Database session generator (for dependency injection)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Async database connection with 'databases'
database = databases.Database(DATABASE_URL)
