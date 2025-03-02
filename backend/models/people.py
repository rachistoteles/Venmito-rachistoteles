# backend/models/people.py

# This file contains the SQLAlchemy model for the Person table in the database.

from sqlalchemy import Column, Integer, String

class Person:
    __tablename__ = 'people'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    telephone = Column(String)
    devices = Column(String)
    location = Column(String)
