from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.people import People
from db.session import get_db  # This is the session management function

router = APIRouter()

# Fetch a person by ID
@router.get("/people/{person_id}")
async def read_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(People).filter(People.id == person_id).first()
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

# Create a new person
@router.post("/people/")
async def create_person(first_name: str, last_name: str, telephone: str, email: str, 
                        devices: list, location: dict, db: Session = Depends(get_db)):
    person = People(first_name=first_name, last_name=last_name, telephone=telephone, 
                    email=email, devices=devices, location=location)
    db.add(person)
    db.commit()
    db.refresh(person)
    return person
