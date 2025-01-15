from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.models.Base import Base
from app.utils.generate_schedule_id import generate_schedule_id

class MedicationSchedule(Base):
    __tablename__ = "medication_schedules"
    id = Column(String, primary_key=True, index=True, default=generate_schedule_id())
    medication_id = Column(String, ForeignKey('medications.id'))
    schedule_time = Column(String)

    medication = relationship("Medication", back_populates="schedules")