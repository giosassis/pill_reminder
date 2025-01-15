from sqlalchemy.orm import Session, joinedload
from app.models.Medication import Medication as MedicationModel
from app.models.MedicationSchedule import MedicationSchedule
from app.utils.generate_schedule_id import generate_schedule_id
import json
from typing import List


class MedicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_medications(self):
        return self.db.query(MedicationModel).options(joinedload(MedicationModel.schedules)).all()

    def get_medication_by_id(self, medication_id: str):
        return self.db.query(MedicationModel).filter(MedicationModel.id == medication_id).first()

    def get_medication_by_name(self, name: str):
        return self.db.query(MedicationModel).filter(MedicationModel.name == name).first()

    def get_medication_by_time(db: Session, times: list):
        schedules = db.query(MedicationSchedule).filter(
            MedicationSchedule.schedules.in_(times)).all()

        result = []
        for schedule in schedules:
            medication = db.query(MedicationModel).filter(
                MedicationModel.id == schedule.medication_id).first()
            if medication:
                result.append({
                    'id': medication.id,
                    'name': medication.name,
                    'dosage': medication.dosage,
                    'category': medication.category,
                    'schedule_time': schedule.schedule_time
                })

        return json.dumps(result)

    def create_medication(self, medication_data: MedicationModel, custom_id: str):
        try:
            new_medication = MedicationModel(
                id=custom_id, **medication_data.dict(exclude={'schedules'}))
            self.db.add(new_medication)
            self.db.commit()
            self.db.refresh(new_medication)

            return new_medication
        except Exception as e:
            self.db.rollback()
            raise e

    def create_schedules_for_medication(self, medication_id: str, schedules: list):
        for schedule in schedules:
            custom_schedule_id = generate_schedule_id()
            print(f"Generated Schedule ID: {custom_schedule_id}")

            new_schedule = MedicationSchedule(
                id=custom_schedule_id,
                medication_id=medication_id,
                schedule_time=schedule.schedule_time
            )
            self.db.add(new_schedule)
            print(f"Inserting schedule: {new_schedule}")
        self.db.commit()
        return "Schedules created successfully"

    def update_medication(self, medication_id: str, medication_data: MedicationModel):
        medication = self.get_medication_by_id(medication_id)
        if not medication:
            raise ValueError("Medication not found.")

        medication.name = medication_data.name
        medication.dosage = medication_data.dosage
        medication.category = medication_data.category

        self.db.commit()
        self.db.refresh(medication)
        return medication

    def update_schedules_for_medication(self, medication_id: str, schedules: List[MedicationSchedule]):
        self.db.query(MedicationSchedule).filter(
            MedicationSchedule.medication_id == medication_id).delete()
        self.create_schedules_for_medication(medication_id, schedules)

    def delete_medication(self, medication_id: str):
        medication = self.get_medication_by_id(medication_id)
        if not medication:
            raise ValueError("Medication not found.")

        self.db.delete(medication)
        self.db.commit()

    def delete_schedules_by_medication(self, medication_id: str):
        self.db.query(MedicationSchedule).filter(
            MedicationSchedule.medication_id == medication_id).delete()
        self.db.commit()
