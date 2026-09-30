"""
SmartCare v0.5 - Service Layer
File: services/appointment_service.py

Coordinates application workflows for appointment management while preserving
domain behavior and delegating data persistence to the repository contract.
"""

from datetime import datetime
from typing import List, Optional

from domain.appointment import Appointment, AppointmentStatus
from domain.patient import Patient
from domain.practitioner import Practitioner
from repositories.appointment_repository import AppointmentRepository


class AppointmentService:
    """
    Application service coordinating use cases for appointments.
    """

    def __init__(self, repository: AppointmentRepository) -> None:
        """
        Initialize the service with a repository abstraction.

        :param repository: Contract instance for appointment persistence.
        """
        self._repository = repository

    def book_appointment(
        self,
        appointment_id: str,
        patient: Patient,
        practitioner: Practitioner,
        date_time: datetime
    ) -> Appointment:
        """
        Coordinates the booking of a new appointment.
        """
        appointment = Appointment(
            appointment_id=appointment_id,
            patient=patient,
            practitioner=practitioner,
            date_time=date_time,
            status=AppointmentStatus.SCHEDULED
        )

        if not appointment.validate():
            raise ValueError("Invalid appointment data or referenced domain entities.")

        self._repository.save(appointment)
        return appointment

    def cancel_appointment(self, appointment_id: str) -> bool:
        """
        Coordinates cancelling an existing appointment.
        """
        appointment = self._repository.find_by_id(appointment_id)
        if not appointment:
            raise ValueError(f"Appointment with ID '{appointment_id}' not found.")

        # Delegate status transition rule to the domain model
        appointment.cancel()

        self._repository.save(appointment)
        return True

    def get_appointment(self, appointment_id: str) -> Optional[Appointment]:
        """Retrieves an appointment by its identifier."""
        return self._repository.find_by_id(appointment_id)

    def list_all_appointments(self) -> List[Appointment]:
        """Retrieves all appointments."""
        return self._repository.list_all()