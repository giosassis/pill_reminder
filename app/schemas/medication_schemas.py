from pydantic import BaseModel, Field, validator
from typing import List
from datetime import datetime, time
from typing import List

class ScheduleCreate(BaseModel):
    schedule_time: time

class MedicationResponse(BaseModel):
    id: str
    name: str
    dosage: str
    schedules: List[ScheduleCreate]  
    category: str

class MedicationCreate(BaseModel):
    name: str
    dosage: str
    schedules: List[ScheduleCreate]
    category: str

    class Config:
        orm_mode = True