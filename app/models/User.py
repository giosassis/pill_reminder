from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.Base import Base 
from app.models.UserMedication import UserMedication

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    nickname = Column(String, index=True)
    email = Column(String, unique=True, nullable=False)
    
    medications = relationship("Medication", secondary="user_medications", back_populates="users")