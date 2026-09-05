# Part D: AI-Generated Alternative Version (Microsoft Copilot)

# List to store all appointments
appointments = []


def book_appointment(patient_name, practitioner_name, appointment_time):
    """Store an appointment in the appointments list."""

    appointment = {
        "patient": patient_name,
        "practitioner": practitioner_name,
        "time": appointment_time
    }

    appointments.append(appointment)
    print("Appointment booked successfully!")


# Example usage
book_appointment("Alice Smith", "Dr. John Doe", "2024-07-20 10:00 AM")
book_appointment("Bob Johnson", "Dr. Jane Roe", "2024-07-20 11:30 AM")

# Display all appointments
for appointment in appointments:
    print(appointment)