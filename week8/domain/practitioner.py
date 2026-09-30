"""
SmartCare v0.4 - Practitioner Domain Model
Stage 4 Lab Deliverable - Part C (AI OFF)
"""


class Practitioner:
    """
    Represents a healthcare practitioner in the SmartCare system.
    Encapsulates practitioner identity, specialty, and state validation.
    """

    def __init__(self, practitioner_id: str, name: str, specialty: str) -> None:
        """
        Initialize a new Practitioner instance.

        :param practitioner_id: Unique string identifier for the practitioner
        :param name: Full name of the practitioner
        :param specialty: Medical specialty or discipline
        """
        self._practitioner_id: str = practitioner_id.strip() if practitioner_id else ""
        self._name: str = name.strip() if name else ""
        self._specialty: str = specialty.strip() if specialty else ""

    @property
    def practitioner_id(self) -> str:
        """Get the practitioner ID."""
        return self._practitioner_id

    @property
    def name(self) -> str:
        """Get the practitioner name."""
        return self._name

    @property
    def specialty(self) -> str:
        """Get the practitioner specialty."""
        return self._specialty

    @specialty.setter
    def specialty(self, value: str) -> None:
        """Update specialty details with basic string cleaning."""
        self._specialty = value.strip() if value else ""

    def validate(self) -> bool:
        """
        Validates core invariants for a practitioner.
        Returns True if practitioner_id, name, and specialty are non-empty strings.
        """
        if not self._practitioner_id or not self._name or not self._specialty:
            return False
        return True

    def __repr__(self) -> str:
        return f"Practitioner(practitioner_id='{self._practitioner_id}', name='{self._name}', specialty='{self._specialty}')"



#Local Verification
if __name__ == "__main__":
    # Test valid practitioner
    doc = Practitioner("DR001", "Dr. Sarah Connor", "General Practice")
    print(f"Valid Practitioner: {doc}")
    print(f"Is valid? {doc.validate()}")  # Expected: True

    # Test invalid practitioner (missing specialty)
    invalid_doc = Practitioner("DR002", "Dr. John Doe", "")
    print(f"Invalid Practitioner Is Valid? {invalid_doc.validate()}")  # Expected: False