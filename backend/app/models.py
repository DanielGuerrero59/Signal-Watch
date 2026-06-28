from sqlalchemy import Column, Integer, String, DateTime 
from datetime import datetime 
from app.database import Base 


class Upload(Base): 
    __tablename__ = "uploads" 


    id = Column(Integer, primary_key =True, index = True) 
    filename = Column(String, nullable= False)
    size = Column(Integer, nullable = False)
    file_type = Column(String, nullable = False)
    path = Column(String, nullable = False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

