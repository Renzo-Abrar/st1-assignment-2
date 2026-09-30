"""
SmartCare v0.5 - System Entry Point
File: main.py
"""

from persistence.sqlite_appointment_repository import SQLiteAppointmentRepository
from presentation.cli import CLI
from services.appointment_service import AppointmentService


def main() -> None:
    # 1. Instantiate Persistence Layer
    repository = SQLiteAppointmentRepository()

    # 2. Inject Repository into Service Layer
    service = AppointmentService(repository=repository)

    # 3. Inject Service into Presentation Layer
    cli = CLI(service=service)

    # 4. Launch Application Interface
    print("Bootstrapping SmartCare v0.5 Layered Architecture...")
    cli.run()


if __name__ == "__main__":
    main()