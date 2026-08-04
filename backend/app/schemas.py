from pydantic import BaseModel 
from datetime import datetime 




class UploadResponse(BaseModel): 
    id: int 
    filename: str 
    size: int 
    file_type: str 
    uploaded_at: datetime
    summary: str | None
    transcript: str | None = None




    class Config: 
        # SQLAlchemy uses dot notaiton, this makes it use dot notation and not brackets
        from_attributes = True


        