from pydantic import BaseModel
from fastapi import APIRouter
from fastapi import UploadFile, File
from app.services.storage import save_file
from fastapi import HTTPException
import os

# Pydantic model — defines the shape and types of data we expect
# Pydantic automatically rejects requests that don't match these types
class UploadRequest(BaseModel):
    filename: str
    size: int
    description: str


# APIRouter lets us define routes in a separate file from main.py
# Think of it as a section of the traffic director that handles upload-related routes
router = APIRouter()

# Set of allowed file extensions — using a set for fast lookup
ALLOWED_EXTENSIONS = {".pdf", ".txt", ".png", ".jpg"}

# Registers this function as the handler for POST requests to /upload
# status_code=201 tells FastAPI to return 201 Created on success
@router.post("/upload", status_code=201)
async def upload_file(file: UploadFile):
    # UploadFile is FastAPI's container for incoming files
    # .read() reads through file in form of bytes
    # await makes program wait to finish reading the file before continuing
    contents = await file.read()

    # --- Validation guards (bouncer checks) ---
    # Always validate before touching disk

    # Guard 1: reject empty files
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="File is Empty")

    # Guard 2: reject files over 10MB
    # 10 * 1024 * 1024 = 10,485,760 bytes = 10MB
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File Too Large")

    # Guard 3: reject disallowed file types
    # splitext splits "report.pdf" into ("report", ".pdf") — we take index [1] for the extension
    # .lower() normalises ".PDF" to ".pdf" so capitalisation doesn't matter
    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="File Type is Not Allowed")

    # All checks passed — safe to write to disk now
    path = save_file(file.filename, contents)

    # Returns a 201 response with details about the saved file
    return {
        "Filename": file.filename,
        "Size": len(contents),
        "Saved_to": path
    }


   