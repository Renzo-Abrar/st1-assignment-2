"""
SmartCare v0.5 - Persistence Implementation
File: persistence/sqlite_appointment_repository.py
"""

from typing import Dict, List, Optional
from domain.appointment import Appointment
from repositories.appointment_repository import AppointmentRepository


class SQLiteAppointmentRepository(AppointmentRepository):
    """
    Concrete repository implementation implementing the AppointmentRepository contract.
    Simulates persistence storage while maintaining clean layer separation.
    """

    def __init__(self) -> None:
        self._db: Dict[str, Appointment] = {}

    def save(self, appointment: Appointment) -> None:
        """Saves or updates an appointment in memory / persistent store."""
        self._db[appointment.appointment_id] = appointment

    def find_by_id(self, appointment_id: str) -> Optional[Appointment]:
        """Retrieves an appointment by its ID."""
        return self._db.get(appointment_id)

    def list_all(self) -> List[Appointment]:
        """Returns all appointments stored in repository."""
        return list(self._db.values())