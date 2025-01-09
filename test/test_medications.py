import pytest
from app.services.medications_service import MedicationService
from app.schemas import MedicationCreate
from unittest.mock import MagicMock
from app.utils.medication_exceptions import MedicationAlreadyExistsError, MedicationNotFoundError
@pytest.fixture
def medication_repo_mock():
    return MagicMock()

@pytest.fixture
def medication_service(medication_repo_mock):
    return MedicationService(medication_repo_mock)

def test_create_medication_success():
    repo_mock = MagicMock()
    service = MedicationService(db=None)
    service.repository = repo_mock

    medication_data = MedicationCreate(
        name="Med1",
        dosage="10mg",
        category="psiquiatria",
        schedule_times=["08:00", "14:30"]
    )

    repo_mock.get_medication_by_name.return_value = None 
    repo_mock.create_medication.return_value = medication_data

    created_medication = service.create_medication(medication_data)

    assert created_medication.name == "Med1"
    assert created_medication.dosage == "10mg"
    assert created_medication.category == "psiquiatria"
    assert created_medication.schedule_times == ["08:00", "14:30"]
    repo_mock.create_medication.assert_called_once()  

def test_create_medication_already_exists():
    repo_mock = MagicMock()
    service = MedicationService(db=None)
    service.repository = repo_mock

    medication_data = MedicationCreate(
        name="Med1",
        dosage="10mg",
        category="psiquiatria",
        schedule_times=["08:00", "14:30"]
    )

    repo_mock.get_medication_by_name.return_value = medication_data 

    with pytest.raises(MedicationAlreadyExistsError):
        service.create_medication(medication_data)













