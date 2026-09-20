from enum import Enum


class AppointmentStatus(Enum):
    """Simple enumeration for tracking appointment lifecycle states."""
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class Patient:
    """Class representing a patient in the SmartCare system."""

    def __init__(self, patient_id: str, name: str, contact_info: str):
        self.patient_id = patient_id
        self.name = name
        self.contact_info = contact_info

    def validate(self) -> bool:
        """Check if essential patient data is present."""
        if self.patient_id != "" and self.name != "":
            return True
        return False


class Practitioner:
    """Class representing a healthcare practitioner."""

    def __init__(self, practitioner_id: str, name: str, specialty: str):
        self.practitioner_id = practitioner_id
        self.name = name
        self.specialty = specialty

    def validate(self) -> bool:
        """Check if essential practitioner data is present."""
        if self.practitioner_id != "" and self.name != "":
            return True
        return False


class Appointment:
    """Class linking a patient and practitioner at a specific date/time."""

    def __init__(self, appointment_id: str, patient: Patient, practitioner: Practitioner, date_time: str):
        self.appointment_id = appointment_id
        self.patient = patient
        self.practitioner = practitioner
        self.date_time = date_time
        self.status = AppointmentStatus.SCHEDULED

    def schedule(self) -> bool:
        """Schedules the appointment if both patient and practitioner are valid."""
        if self.patient.validate() and self.practitioner.validate():
            self.status = AppointmentStatus.SCHEDULED
            return True
        return False

    def cancel(self) -> bool:
        """Cancels appointment if it has not been completed yet."""
        if self.status == AppointmentStatus.COMPLETED:
            return False
        self.status = AppointmentStatus.CANCELLED
        return True