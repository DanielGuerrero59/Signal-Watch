from pydantic import BaseModel
from fastapi import APIRouter 
from fastapi import UploadFile, File 
from app.services.storage import save_file 

class UploadRequest(BaseModel): 
    filename: str 
    size: int 
    description: str


router = APIRouter()

@router.post("/upload", status_code = 201) #https status code 201 to create something 
async def upload_file(file: UploadFile):
    # .read() reads through file in form of bytes 
    #await makes program wait to read the file before continuing 
    contents = await file.read() 
    path = save_file(file.filename, contents) 
    return { 
        "Filename": file.filename, 
        "Size" : len(contents), 
        "Saved_to" : path

    }



