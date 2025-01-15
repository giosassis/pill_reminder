from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.Base import Base
from app.models.User import User
from app.models.UserMedication import UserMedication
from app.models.MedicationSchedule import MedicationSchedule

class Medication(Base):
    __tablename__ = "medications"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    dosage = Column(String)
    category = Column(String)
    
    schedules = relationship("MedicationSchedule", back_populates="medication")
    users = relationship("User", secondary="user_medications", back_populates="medications")