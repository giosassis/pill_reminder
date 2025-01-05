from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models, database
from app.models.medication_models import Medication
from app.services import generate_id
from app.database import get_db_connection
from app.schemas import MedicationCreate, Medication  

router = APIRouter()

@router.post("/medications/", response_model=Medication)
def create_medication(medication: MedicationCreate, db: Session = Depends(get_db_connection)):
    custom_id = generate_id.generate_id(medication.category)  
    db_medication = models.Medication(id=custom_id, **medication.dict())
    db.add(db_medication)
    db.commit()
    db.refresh(db_medication)
    return db_medication

@router.get("/medications/")
def get_medications(db: Session = Depends(database.get_db_connection)):
    medications = db.query(models.Medication).all()
    return medications
