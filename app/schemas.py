from pydantic import BaseModel
from typing import List

class MedicationCreate(BaseModel):
    name: str
    dosage: str
    schedule_times: List[str]

class Medication(MedicationCreate):
    id: int

    class Config:
        orm_mode = True
