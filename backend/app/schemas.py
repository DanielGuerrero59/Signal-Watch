from pydantic import BaseModel 
from datetime import datetime 



class UploadResponse(BaseModel): 
    id: int 
    filename: str 
    size: int 
    file_type: str 
    uploaded_at: datetime




    class Config: 
        from_attributes = True


        