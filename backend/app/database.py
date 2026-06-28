import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base 


load_dotenv() 


#Read key value pair holding our connection string 
DATABASE_URL = os.getenv("DATABASE_URL") 


#Create engine that bridges to Postgres
engine  = create_engine(DATABASE_URL) 

# makes sessions that use connections waiting around in the engine 
SessionLocal = sessionmaker(autocommit= False, autoflush = False, bind = engine)

Base = declarative_base() 


