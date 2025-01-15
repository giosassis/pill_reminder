from app.repositories.medication_repository import MedicationRepository
from app.utils.generate_medication_id import generate_medication_id
from app.schemas.medication_schemas import MedicationCreate, ScheduleCreate
from sqlalchemy.orm import Session
from app.utils import medication_exceptions
from app.models import MedicationSchedule
import re


class MedicationService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = MedicationRepository(db)

    @staticmethod
    def is_valid_time_format(time: str) -> bool:
        return bool(re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", time))

    @staticmethod
    def validate_category(category: str) -> bool:
        valid_categories = ["psiquiatria", "diabetes", "generico"]
        if category not in valid_categories:
            raise ValueError(f"Invalid category: {category}")

    @staticmethod
    def validate_dosage(dosage: str) -> bool:
        if not re.match(r"^\d+(mg|g|mcg|ml)$", dosage):
            raise ValueError(f"Invalid dosage format: {dosage}")
        return True

    @staticmethod
    def validate_name_length(name: str) -> bool:
        if len(name) < 3 or len(name) > 100:
            raise ValueError(
                f"Medication name must be between 3 and 100 characters: {name}")
        return True

    def get_schedules_by_medication(self, medication_id: str):
        return self.db.query(MedicationSchedule).filter(MedicationSchedule.medication_id == medication_id).all()

    def get_medication_by_name(self, medication_name: str):
        return self.repository.get_medication_by_name(medication_name)

    def get_all_medications(self):
        return self.repository.get_all_medications()

    def get_medication_by_id(self, medication_id: str):
        return self.repository.get_medication_by_id(medication_id)

    def create_medication(self, medication_data: MedicationCreate):
        existing_medication = self.repository.get_medication_by_name(
            medication_data.name)
        if existing_medication:
            raise medication_exceptions.MedicationAlreadyExistsError()

        self.validate_name_length(medication_data.name)
        self.validate_dosage(medication_data.dosage)
        self.validate_category(medication_data.category)

        custom_id = generate_medication_id(medication_data.category)

        created_medication = self.repository.create_medication(
            medication_data, custom_id)

        self.create_schedules_for_medication(
            created_medication.id, medication_data.schedules)

        return created_medication

    def create_schedules_for_medication(self, medication_id: str, schedules: list[ScheduleCreate]):
        self.repository.create_schedules_for_medication(
            medication_id, schedules)

    def update_medication(self, medication_id: str, medication_data: MedicationCreate):
        existing_medication = self.repository.get_medication_by_id(
            medication_id)
        if not existing_medication:
            raise medication_exceptions.MedicationNotFoundError()

        self.validate_name_length(medication_data.name)
        self.validate_dosage(medication_data.dosage)
        self.validate_category(medication_data.category)

        updated_medication = self.repository.update_medication(
            medication_id, medication_data)

        self.repository.update_schedules_for_medication(
            medication_id, medication_data.schedules)

        return updated_medication

    def update_schedules_for_medication(self, medication_id: str, schedules: list[ScheduleCreate]):
        self.repository.update_schedules_for_medication(
            medication_id, schedules)

    def delete_medication(self, medication_id: str):
        existing_medication = self.repository.get_medication_by_id(
            medication_id)
        if not existing_medication:
            raise medication_exceptions.MedicationNotFoundError()

        self.repository.delete_schedules_by_medication(medication_id)
        self.repository.delete_medication(medication_id)
