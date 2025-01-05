from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os
import logging

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL was not specified in configfile.")

echo = True if os.getenv("ENVIRONMENT") == "development" else False
engine = create_engine(DATABASE_URL, echo=echo)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db_connection():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1")).fetchone()
        yield db 
    except SQLAlchemyError as e:
        logging.error(f"There was an error when trying to connect to database: {str(e)}")
        raise Exception("Error to connect to database") 
    finally:
        db.close()