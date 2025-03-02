
from fastapi import FastAPI
from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from backend.api.file_api import router as file_api_router

app = FastAPI()
app.include_router(file_api_router)

# Updated Database URL with your username and database
DATABASE_URL = "postgresql://rachistoteles:rachistoteles@localhost/venmitodb"

# Async Database Setup with 'databases'
database = Database(DATABASE_URL)

# SQLAlchemy Setup
engine = create_engine(DATABASE_URL)
metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Your models here (example: a User model)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

# Initialize Database Connection
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI with PostgreSQL!"}
