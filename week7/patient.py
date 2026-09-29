"""
SmartCare v0.4 - Patient Domain Model
Stage 4 Lab Deliverable - Part B (AI OFF)
"""

from typing import Optional


class Patient:
    """
    Represents a patient in the SmartCare system.
    Encapsulates patient identity and basic state validation.
    """

    def __init__(self, patient_id: str, name: str, contact_info: str) -> None:
        """
        Initialize a new Patient instance.

        :param patient_id: Unique string identifier for the patient
        :param name: Full name of the patient
        :param contact_info: Phone number, email, or contact details
        """
        self._patient_id: str = patient_id.strip() if patient_id else ""
        self._name: str = name.strip() if name else ""
        self._contact_info: str = contact_info.strip() if contact_info else ""

    @property
    def patient_id(self) -> str:
        """Get the patient ID."""
        return self._patient_id

    @property
    def name(self) -> str:
        """Get the patient name."""
        return self._name

    @property
    def contact_info(self) -> str:
        """Get the patient contact info."""
        return self._contact_info

    @contact_info.setter
    def contact_info(self, value: str) -> None:
        """Update contact info with basic string cleaning."""
        self._contact_info = value.strip() if value else ""

    def validate(self) -> bool:
        """
        Validates core invariants for a patient.
        Returns True if patient_id and name are non-empty strings.
        """
        if not self._patient_id or not self._name:
            return False
        return True

    def __repr__(self) -> str:
        return f"Patient(patient_id='{self._patient_id}', name='{self._name}')"




#Local Verification

if __name__ == "__main__":
    # Test valid patient
    valid_patient = Patient("P001", "Alice Smith", "alice@example.com")
    print(f"Valid Patient: {valid_patient}")
    print(f"Is valid? {valid_patient.validate()}")  # Expected: True

    # Test invalid patient (missing name)
    invalid_patient = Patient("P002", "", "bob@example.com")
    print(f"Invalid Patient Is Valid? {invalid_patient.validate()}")  # Expected: False