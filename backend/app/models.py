from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime 
from app.database import Base 

#One form of Base being used, other models can have different structure.
class Upload(Base): 
    __tablename__ = "uploads" 


    id = Column(Integer, primary_key =True, index = True) 
    filename = Column(String, nullable= False)
    size = Column(Integer, nullable = False)
    file_type = Column(String, nullable = False)
    path = Column(String, nullable = False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    summary = Column(Text, nullable=True)

