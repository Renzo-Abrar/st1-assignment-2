# --- Part B: Task 1 (Basic Version) ---
print("Welcome to SmartCare: Community Clinic Appointment Booking System!")

# First Appointment
patient1_name = 'Alice Smith'
practitioner1_name = 'Dr. John Doe'
appointment1_time = '2024-07-20 10:00 AM'
print(f"Patient: {patient1_name} | Practitioner: {practitioner1_name} | Time: {appointment1_time}")

# Second Appointment
patient2_name = 'Bob Johnson'
practitioner2_name = 'Dr. Jane Roe'
appointment2_time = '2024-07-20 11:30 AM'
print(f"Patient: {patient2_name} | Practitioner: {practitioner2_name} | Time: {appointment2_time}")

print("\n--------------------------------------------------\n")

# --- Part B: Task 1 Enhanced (List & Function Version) ---
appointments = []

def book_appointment(patient_name, practitioner_name, appointment_time):
    if not patient_name:
        raise ValueError("Patient name cannot be empty")
    appointment = {
        "patient": patient_name,
        "practitioner": practitioner_name,
        "time": appointment_time
    }
    appointments.append(appointment)

def display_appointments():
    if not appointments:
        print("No appointments recorded.")
        return
    for appointment in appointments:
        print(f"Patient: {appointment['patient']} | Practitioner: {appointment['practitioner']} | Time: {appointment['time']}")

print("Welcome to SmartCare: The Clinical Appointment Booking System!")
book_appointment('Alice Smith', 'Dr. John Doe', '2024-07-20 10:00 AM')
book_appointment('Bob Johnson', 'Dr. Jane Roe', '2024-07-20 11:30 AM')
display_appointments()

# ==================================================
# --- Part G: Controlled Code Improvement ---
# ==================================================
# Controlled Improvement: Added input validation for practitioner name
# and appointment time to ensure complete appointment records.

appointments_improved = []


def book_appointment_improved(patient_name, practitioner_name, appointment_time):
    if not patient_name or not patient_name.strip():
        raise ValueError("Patient name cannot be empty.")
    if not practitioner_name or not practitioner_name.strip():
        raise ValueError("Practitioner name cannot be empty.")
    if not appointment_time or not appointment_time.strip():
        raise ValueError("Appointment time cannot be empty.")

    appointment = {
        "patient": patient_name.strip(),
        "practitioner": practitioner_name.strip(),
        "time": appointment_time.strip()
    }
    appointments_improved.append(appointment)
    print("Improved booking added successfully!")


# Testing the improved function
print("\n--- Part G Improved Function Execution ---")
try:
    book_appointment_improved("Alice Smith", "Dr. John Doe", "2024-07-20 10:00 AM")
    # Uncommenting the line below will trigger input validation:
    # book_appointment_improved("Bob Johnson", "", "2024-07-20 11:30 AM")
except ValueError as e:
    print(f"Validation Error Caught: {e}")