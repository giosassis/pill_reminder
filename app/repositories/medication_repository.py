from sqlalchemy.orm import Session
from app.models.medication_models import Medication as MedicationModel
from app.utils.generate_medication_id import generate_medication_id
class MedicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_medications(self):
        return self.db.query(MedicationModel).all()

    def get_medication_by_id(self, medication_id: str):
        return self.db.query(MedicationModel).filter(MedicationModel.id == medication_id).first()

    def get_medication_by_name(self, name: str):
        return self.db.query(MedicationModel).filter(MedicationModel.name == name).first()

    def create_medication(self, medication_data: MedicationModel, custom_id: str):
        try:
            new_medication = MedicationModel(id=custom_id, **medication_data.dict())
            self.db.add(new_medication)
            self.db.commit()
            self.db.refresh(new_medication) 
            return new_medication
        except Exception as e:
            self.db.rollback() 
            raise e
        
    def update_medication(self, medication_id: str, updates: dict):
        medication = self.get_medication_by_id(medication_id)
        if not medication:
            raise ValueError("Medication not found")
        
        for key, value in updates.items():
            setattr(medication, key, value)
        
        self.db.commit()
        self.db.refresh(medication)
        return medication
    
    def delete_medication(self, medication_id: str):
        medication = self.get_medication_by_id(medication_id)
        if not medication:
            raise ValueError("Medication not found")
        
        self.db.delete(medication)
        self.db.commit()
