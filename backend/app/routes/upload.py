from fastapi import APIRouter, UploadFile, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.services.storage import save_file
from app.database import get_db
from app.models import Upload
from app.schemas import UploadResponse  
import os
from app.services.dispatch import run_ai_pipeline


# APIRouter lets us define routes in a separate file from main.py
# Think of it as a section of the traffic director that handles upload-related routes
router = APIRouter()

# Set of allowed file extensions — using a set for fast lookup
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".png", ".jpg", ".jpeg", ".mp3", ".wav", ".m4a", ".csv"}
    
# Registers this function as the handler for POST requests to /upload
# status_code=201 tells FastAPI to return 201 Created on success
@router.post("/upload", status_code=201)
#Depends(get_db) opens a fresh connection to the database, hands functionality to db, and closes on its own. 
async def upload_file(file: UploadFile, background_tasks: BackgroundTasks , db: Session = Depends(get_db)):
    # UploadFile is FastAPI's container for incoming files
    

    
    # Guard: reject disallowed file types
    # splitext splits "report.pdf" into ("report", ".pdf") — we take index [1] for the extension
    # .lower() normalises ".PDF" to ".pdf" so capitalisation doesn't matter
    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="File Type is Not Allowed")

    # All checks passed — safe to write to disk now
    path, size = await save_file(file, file.filename, 10 * 1024 * 1024)




    #Write metadata row to DB 
    upload_row = Upload(filename = file.filename, size = size, file_type = extension, path=path)
    db.add(upload_row) 
    db.commit() 
    db.refresh(upload_row) 


    background_tasks.add_task(run_ai_pipeline, upload_row.id, path, extension)

    # Returns a 201 response with details about the saved file
    return {
        "id":  upload_row.id,
        "Filename": file.filename,
        "Size": size,
        "Saved_to": path
    }

#No exception needed here, empty list if nothing 
# Query with upload for PostGres, client gets response model of UploadResponse 
@router.get("/uploads", response_model=list[UploadResponse])
def list_uploads(file_type: str | None = None, db: Session = Depends(get_db)):
    #creates query object
    query = db.query(Upload)

    if file_type is not None: 
        #filters query object
        query = query.filter(Upload.file_type == file_type)

    #translated and sent to Postgres
    uploads = query.all()
    return uploads
   


# needs exception so client gets more info other than null on their end 
@router.get("/uploads/{upload_id}", response_model=UploadResponse)
def get_upload(upload_id: int, db: Session = Depends(get_db)):
    upload = db.query(Upload).filter(Upload.id == upload_id).first()
    if upload is None:
        raise HTTPException(status_code=404, detail="Upload not found")
    return upload