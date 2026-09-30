"""
SmartCare v0.5 - Repository Abstraction
File: repositories/appointment_repository.py
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from domain.appointment import Appointment


class AppointmentRepository(ABC):
    """
    Abstract interface contract defining data access operations for Appointments.
    Services depend on this abstraction rather than concrete storage mechanisms.
    """

    @abstractmethod
    def save(self, appointment: Appointment) -> None:
        """Saves a new appointment or updates an existing entity."""
        pass

    @abstractmethod
    def find_by_id(self, appointment_id: str) -> Optional[Appointment]:
        """Finds an appointment entity by its unique ID string."""
        pass

    @abstractmethod
    def list_all(self) -> List[Appointment]:
        """Retrieves all stored appointment entities."""
        pass