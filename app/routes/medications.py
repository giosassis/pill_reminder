from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import MedicationCreate
from app.services.medications_service import MedicationService
from app.database import get_db_connection
from app.utils.medication_exceptions import MedicationNotFoundError, MedicationAlreadyExistsError
from typing import List

router = APIRouter()

def get_service(db: Session = Depends(get_db_connection)) -> MedicationService:
    return MedicationService(db)

@router.get("/medications/", response_model=List[MedicationCreate])
def get_all_medications(service: MedicationService = Depends(get_service)):
    return service.get_all_medications()

@router.get("/medications/ids/")
def get_medication_ids(service: MedicationService = Depends(get_service)):
    return service.get_medication_ids()

@router.post("/medications/", response_model=MedicationCreate)
def create_medication(
    medication_data: MedicationCreate, 
    service: MedicationService = Depends(get_service)
):
    try:
        return service.create_medication(medication_data)
    except MedicationAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Medication with this name already exists")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e.message))

@router.put("/medications/{medication_id}", response_model=MedicationCreate)
def update_medication(
    medication_id: str, 
    medication_update: MedicationCreate,
    service: MedicationService = Depends(get_service)
):
    medication_update.id = medication_id
    try:
        return service.update_medication(medication_update)
    except MedicationNotFoundError:
        raise HTTPException(status_code=404, detail="Medication not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/medications/{medication_id}")
def delete_medication(
    medication_id: str, 
    service: MedicationService = Depends(get_service)
):
    try:
        return service.delete_medication(medication_id)
    except MedicationNotFoundError:
        raise HTTPException(status_code=404, detail="Medication not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
