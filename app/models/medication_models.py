from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from app.models.base import Base 

class Medication(Base):
    __tablename__ = "medications"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    dosage = Column(String)
    schedule_times = Column(ARRAY(String))
    category = Column(String)