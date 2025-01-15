from sqlalchemy import Column, String, ForeignKey
from app.models.Base import Base 

class UserMedication(Base):
    __tablename__ = "user_medications"
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    medication_id = Column(String, ForeignKey("medications.id"), primary_key=True)
    