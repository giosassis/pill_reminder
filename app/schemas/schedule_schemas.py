from pydantic import BaseModel

class ScheduleCreate(BaseModel):
    medication_id: str  
    schedule_time: str 

    class Config:
        orm_mode = True