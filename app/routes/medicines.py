from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app import models, database
from app.models.medication_models import Medication
from app.utils.generate_medication_id import generate_medication_id
from app.database import get_db_connection
from app.schemas import MedicationCreate, Medication  

router = APIRouter()
@router.get("/medications/")
def get_medications(db: Session = Depends(database.get_db_connection)):
    medications = db.query(models.Medication).all()
    return medications

@router.get("/medications/{medication_id}")
def get_medications_by_id(medication_id, db: Session = Depends(database.get_db_connection)):
    medication = db.query(models.Medication).filter(models.Medication.id == medication_id).first()
    if medication is None:
        raise HTTPException(status_code=404, detail="Medication not found")
    return medication

@router.post("/medications/", response_model=Medication)
def create_medication(medication: MedicationCreate, db: Session = Depends(get_db_connection)):
    existing_medication = db.query(models.Medication).filter(models.Medication.name == medication.name).first()
    if existing_medication:
        raise HTTPException(status_code=400, detail="Medication with this name already exists")
    
    custom_id = generate_medication_id.generate_medication_id(medication.category)  
    db_medication = models.Medication(id=custom_id, **medication.dict())
    
    db.add(db_medication)
    db.commit()
    db.refresh(db_medication)
    return db_medication

@router.put("/medications/{medication_id}", response_model=Medication)
def update_medication(medication_id: str, medication_update: MedicationCreate, db: Session = Depends(get_db_connection)):
    medication = db.query(models.Medication).filter(models.Medication.id == medication_id).first()
    if medication is None:
        raise HTTPException(status_code=404, detail="Medication not found")
    medication.name = medication_update.name
    medication.category = medication_update.category
    medication.dosage = medication_update.dosage
    medication.schedule_times = medication_update.schedule_times
    db.commit()
    db.refresh(medication)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"detail": "Medication successfully updated"})

@router.delete("/medications/{medication_id}", response_model=Medication)
def delete_medication(medication_id: str, db: Session = Depends(get_db_connection)):
    medication_to_delete = db.query(models.Medication).filter(models.Medication.id == medication_id).first()
    if medication_to_delete is None:
        raise HTTPException(status_code=404, detail="Medication not found")
    db.delete(medication_to_delete)
    db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"detail": "Medication successfully deleted"})
