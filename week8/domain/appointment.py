"""
SmartCare v0.4 - Appointment Domain Model & Status Enum
Stage 4 Lab Deliverable - Part G (Refactored Implementation)
"""

from datetime import datetime
from enum import Enum, auto
from domain.patient import Patient
from domain.practitioner import Practitioner


class AppointmentStatus(Enum):
    """Enumeration of valid appointment lifecycle states."""
    SCHEDULED = auto()
    CANCELLED = auto()
    COMPLETED = auto()


class InvalidStatusTransitionError(Exception):
    """Raised when an illegal appointment status transition is attempted."""
    pass


class Appointment:
    """
    Represents a medical appointment linking a Patient and a Practitioner.
    Manages schedule state and protects status invariants.
    """

    def __init__(
        self,
        appointment_id: str,
        patient: Patient,
        practitioner: Practitioner,
        date_time: datetime,
        status: AppointmentStatus = AppointmentStatus.SCHEDULED
    ) -> None:
        self._appointment_id: str = appointment_id.strip() if appointment_id else ""
        self._patient: Patient = patient
        self._practitioner: Practitioner = practitioner
        self._date_time: datetime = date_time
        self._status: AppointmentStatus = status

    @property
    def appointment_id(self) -> str:
        return self._appointment_id

    @property
    def patient(self) -> Patient:
        return self._patient

    @property
    def practitioner(self) -> Practitioner:
        return self._practitioner

    @property
    def date_time(self) -> datetime:
        return self._date_time

    @property
    def status(self) -> AppointmentStatus:
        return self._status

    def _ensure_scheduled(self, action_name: str) -> None:
        """Helper to ensure transition operations originate from SCHEDULED status."""
        if self._status != AppointmentStatus.SCHEDULED:
            raise InvalidStatusTransitionError(
                f"Cannot {action_name} appointment from current status {self._status.name}."
            )

    def schedule(self) -> bool:
        """Validates that appointment is in SCHEDULED state."""
        self._ensure_scheduled("schedule")
        return True

    def cancel(self) -> bool:
        """Cancels appointment and retains object in memory for audit logging."""
        self._ensure_scheduled("cancel")
        self._status = AppointmentStatus.CANCELLED
        return True

    def complete(self) -> bool:
        """Marks the appointment as completed."""
        self._ensure_scheduled("complete")
        self._status = AppointmentStatus.COMPLETED
        return True

    def validate(self) -> bool:
        """Validates core appointment invariants and referenced domain objects."""
        if not self._appointment_id or not self._patient or not self._practitioner or not self._date_time:
            return False
        return self._patient.validate() and self._practitioner.validate()

    def __repr__(self) -> str:
        return (
            f"Appointment(id='{self._appointment_id}', "
            f"patient='{self._patient.name}', "
            f"practitioner='{self._practitioner.name}', "
            f"status={self._status.name})"
        )


if __name__ == "__main__":
    # Quick manual check post-refactor
    patient = Patient("P001", "Alice Smith", "alice@example.com")
    practitioner = Practitioner("DR001", "Dr. Sarah Connor", "General Practice")
    appt = Appointment("A001", patient, practitioner, datetime(2026, 10, 15, 10, 0))
    print(f"Refactored Appointment Created: {appt}")
    appt.cancel()
    print(f"After Cancel: {appt}")