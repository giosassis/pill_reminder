from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os

DATABASE_URL = os.getenv('DATABASE_URL') 

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db_connection():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1")).fetchone()
        yield db 
    except SQLAlchemyError as e:
        print(f"Erro na conexão: {str(e)}")
    finally:
        db.close()