# This file contains the API endpoints for file processing
#
# The API endpoints are:
# - GET /process-file/{file_name}/{file_type}
# - POST /upload-file/{file_type}
#
# The GET endpoint reads a file from the data folder and processes it based on the file type (json, yaml, csv, xml).
# The POST endpoint uploads a file to the temp folder for processing.
#
# The file processing functions are imported from backend/services/file_processing.py.


import os
from fastapi import APIRouter, HTTPException, File, UploadFile
from typing import Any
from backend.services.file_processing import save_people_to_db, read_file
from pathlib import Path

router = APIRouter()

@router.get("/process-file/{file_name}/{file_type}")
async def process_file(file_name: str, file_type: str) -> Any:
    
    absolute_file_path = Path(r"C:\Users\racha\OneDrive\Documents\XtillionProject\Venmito-rachistoteles\data") 
    file_path = absolute_file_path / file_name  

    if not file_path.exists():  
        raise HTTPException(status_code=404, detail=f"File {file_name} not found")

    try:
        data = read_file(file_path, file_type)
        return {"status": "success", "data": data}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.post("/upload-file/{file_type}")
async def upload_file(file_type: str, file: UploadFile = File(...)):
    
    temp_folder = Path(r"C:\Users\racha\OneDrive\Documents\XtillionProject\Venmito-rachistoteles\temp")
    
  
    temp_folder.mkdir(parents=True, exist_ok=True)


    file_path = temp_folder / file.filename  

    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        return {"status": "success", "file_path": str(file_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    # finally:
    #     # Clean up the uploaded file
    #     os.remove(file_path)