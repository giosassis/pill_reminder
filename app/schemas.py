from pydantic import BaseModel
from typing import List

class MedicationCreate(BaseModel):
    name: str
    dosage: str
    schedule_times: List[str]  
    category: str
    id: str = None  

class Medication(MedicationCreate):
    id: str

    class Config:
        orm_mode = True