"""
SmartCare v0.5 - Presentation Layer
File: presentation/cli.py
"""

from services.appointment_service import AppointmentService


class CLI:
    """
    Command Line Interface for SmartCare.
    Handles terminal menus, user input, and delegates actions to AppointmentService.
    """

    def __init__(self, service: AppointmentService) -> None:
        self._service = service

    def display_menu(self) -> None:
        print("\n==========================================")
        print("  SmartCare Clinic Appointment System v0.5 ")
        print("==========================================")
        print("1. View All Appointments")
        print("2. Cancel Appointment")
        print("3. Exit")

    def run(self) -> None:
        """Main interaction loop for handling user choices."""
        while True:
            self.display_menu()
            choice = input("\nSelect an option (1-3): ").strip()

            if choice == "1":
                appointments = self._service.list_all_appointments()
                if not appointments:
                    print("\n[!] No appointments found in system.")
                else:
                    print("\n--- Current Appointments ---")
                    for appt in appointments:
                        print(f"ID: {appt.appointment_id} | Patient: {appt.patient.name} | Status: {appt.status.name}")

            elif choice == "2":
                appt_id = input("Enter Appointment ID to cancel: ").strip()
                try:
                    self._service.cancel_appointment(appt_id)
                    print(f"\n[✓] Appointment '{appt_id}' cancelled successfully.")
                except Exception as err:
                    print(f"\n[X] Error: {err}")

            elif choice == "3":
                print("\nExiting SmartCare System. Goodbye!")
                break

            else:
                print("\n[X] Invalid option. Please select 1, 2, or 3.")