from pydantic import BaseModel
from fastapi import APIRouter 

class UploadRequest(BaseModel): 
    filename: str 
    size: int 
    description: str


router = APIRouter()

@router.post("/upload", status_code = 201) #https status code 201 to create something 
def upload_file(request: UploadRequest):
    return { 
        "received" : request.filename, 
        "size" : request.size, 
        "description" : request.description
    }



