class MedicationNotFoundError(Exception):
    def __init__(self, message="Medication not found"):
        self.message = message
        super().__init__(self.message)

class MedicationAlreadyExistsError(Exception):
    def __init__(self, message="Medication with this name already exists"):
        self.message = message
        super().__init__(self.message)
