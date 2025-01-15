from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app import models, database
from app.schemas.medication_schemas import MedicationCreate, MedicationResponse
from app.services.medications_service import MedicationService
from app.utils import medication_exceptions
from typing import List
import logging


router = APIRouter()


@router.get("/medications/", response_model=List[MedicationResponse])
def get_medications(db: Session = Depends(database.get_db_connection)):
    service = MedicationService(db)
    medications = service.get_all_medications()
    return medications


@router.get("/medications/name/{medication_name}", response_model=MedicationResponse)
def get_medication_my_name(medication_name, db: Session = Depends(database.get_db_connection)):
    service = MedicationService(db)
    medication = service.get_medication_by_name(medication_name)
    if not medication:
        raise HTTPException(status_code=404, detail="Medication not found.")
    return medication


@router.get("/medications/{medication_id}", response_model=MedicationResponse)
def get_medications_by_id(medication_id, db: Session = Depends(database.get_db_connection)):
    medication = db.query(models.Medication).filter(
        models.Medication.id == medication_id).first()
    if medication is None:
        raise HTTPException(status_code=404, detail="Medication not found")
    return medication


@router.post("/medications/", response_model=MedicationCreate)
def create_medication(medication: MedicationCreate, db: Session = Depends(database.get_db_connection)):
    service = MedicationService(db)
    try:
        created_medication = service.create_medication(medication)
        return created_medication
    except medication_exceptions.MedicationAlreadyExistsError:
        raise HTTPException(
            status_code=400, detail="Medication with this name already exists.")
    except Exception as error:
        logging.error(
            f"An error occurred while creating the medication: {error}")
        raise HTTPException(
            status_code=500, detail="An error occurred while creating the medication.")


@router.put("/medications/{medication_id}", response_model=MedicationResponse)
def update_medication(medication_id: str, medication_data: MedicationCreate, db: Session = Depends(database.get_db_connection)):
    service = MedicationService(db)
    try:
        updated_medication = service.update_medication(
            medication_id, medication_data)
        return updated_medication
    except medication_exceptions.MedicationNotFoundError:
        raise HTTPException(status_code=404, detail="Medication not found.")
    except Exception as error:
        logging.error(
            f"An error occurred while updating the medication: {error}")
        raise HTTPException(
            status_code=500, detail="An error occurred while updating the medication.")


@router.delete("/medications/{medication_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_medication(medication_id: str, db: Session = Depends(database.get_db_connection)):
    service = MedicationService(db)
    try:
        service.delete_medication(medication_id)
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"detail": "Medication deleted successfully."})
    except medication_exceptions.MedicationNotFoundError:
        raise HTTPException(status_code=404, detail="Medication not found.")
    except Exception as error:
        logging.error(
            f"An error occurred while deleting the medication: {error}")
        raise HTTPException(
            status_code=500, detail="An error occurred while deleting the medication.")
