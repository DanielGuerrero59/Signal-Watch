from pydantic import BaseModel
from fastapi import APIRouter 
from fastapi import UploadFile, File 
from app.services.storage import save_file 
from fastapi import HTTPException
import os 

class UploadRequest(BaseModel): 
    filename: str 
    size: int 
    description: str


router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".png", ".jpg"} 

@router.post("/upload", status_code = 201) #https status code 201 to create something 
async def upload_file(file: UploadFile):
    # .read() reads through file in form of bytes 
    #await makes program wait to read the file before continuing 
    contents = await file.read() 
    if(len(contents) ==0):
        raise HTTPException(status_code =400, detail = "File is Empty")
    
    if (len(contents) > 10*1024*1024): #10MB 
        raise HTTPException(status_code = 413, detail = "File Too Large") 
    extension = os.path.splitext(file.filename)[1].lower() 
    if(extension not in ALLOWED_EXTENSIONS): 
        raise HTTPException(status_code = 415, detail = "File Type is Not Allowed") 

    path = save_file(file.filename, contents) 
    
    
    return { 
        "Filename": file.filename, 
        "Size" : len(contents), 
        "Saved_to" : path

    }



