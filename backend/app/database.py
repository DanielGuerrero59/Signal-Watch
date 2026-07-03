import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base 


load_dotenv() 


#Read key value pair holding our connection string 
DATABASE_URL = os.getenv("DATABASE_URL") 


#Create engine that bridges to Postgres
engine  = create_engine(DATABASE_URL) 

# makes sessions that use connections waiting around in the engine, autocommit off makes committing only occur when explicitely told so. 
SessionLocal = sessionmaker(autocommit= False, autoflush = False, bind = engine)

# declarative_base makes a fresh empty class that can be used inside of Base
Base = declarative_base() 


