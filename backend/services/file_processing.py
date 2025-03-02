# backend/services/file_processing.py

# This file contains the file processing functions to read and save data to the database.
# The functions read different file types (JSON, YAML, CSV, XML) and save the data to the database.
import json
import yaml
import pandas as pd
import xmltodict
from backend.db.session import SessionLocal  # Import SessionLocal from session.py
from backend.models.people import Person  # Import Person model
from sqlalchemy.orm import Session

# Function to read JSON file
def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Function to read YAML file
def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to read CSV file
def read_csv(file_path):
    return pd.read_csv(file_path)

# Function to read XML file
def read_xml(file_path):
    with open(file_path, 'r') as file:
        return xmltodict.parse(file.read())

# Unified file reading function to handle different file types
def read_file(file_path, file_type):
    if file_type == 'json':
        return read_json(file_path)
    elif file_type == 'yaml':
        return read_yaml(file_path)
    elif file_type == 'csv':
        return read_csv(file_path)
    elif file_type == 'xml':
        return read_xml(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

# Save people data to the database, checking for duplicates and adding new people
def save_people_to_db(people_data):
    db: Session = SessionLocal()  # Get the database session
    try:
        for person in people_data:
            # Check if person already exists by email or ID
            existing_person = db.query(Person).filter(Person.email == person["email"]).first()
            if existing_person:
                # update the existing person
                existing_person.first_name = person["first_name"]
                existing_person.last_name = person["last_name"]
                existing_person.telephone = person["telephone"]
                existing_person.devices = person["devices"]
                existing_person.location = person["location"]
            else:
                # add a new entry
                new_person = Person(
                    id=int(person["id"]),  # Ensure the ID is an integer
                    first_name=person["first_name"],
                    last_name=person["last_name"],
                    telephone=person["telephone"],
                    email=person["email"],
                    devices=person["devices"],
                    location=person["location"]
                )
                db.add(new_person)
        db.commit()  # Commit the transaction
    except Exception as e:
        db.rollback()  # Rollback in case of an error
        raise e
    finally:
        db.close()  # Close the session
