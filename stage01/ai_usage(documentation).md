Part A - Problem Understanding: (AI OFF)

# Stage 1 Lab: AI Usage & Problem Analysis

## Part A - Problem Understanding (AI OFF)
* **What data must be stored?** Patient name, practitioner name, and appointment time slot.
* **What functions might be useful?** Functions for booking new appointments and displaying existing ones.
* **What could go wrong?** Double-booking practitioners, submitting blank fields, or losing data when the script exits.
* **What requirements are unclear?** Time slot durations, collision handling rules, and whether file persistence is required.

## Part B - Human Prototype Analysis (5 Limitations)
1. **No User Interactivity:** Data is hardcoded, requiring source code edits to add bookings instead of interactive prompts.
2. **No Collision Detection:** Does not check if a practitioner is already booked at the exact same time slot.
3. **No Data Persistence:** Appointments are stored in-memory in a Python list and reset every time the script stops.
4. **Weak Validation:** Only checks for empty patient name strings, ignoring invalid times or `None` values.
5. **No Modification:** Once appended, appointments cannot be edited, canceled, or removed.

## Part C - AI Tutor Interaction (Microsoft Copilot)
**Prompt Sent:**

Act as a Python tutor... (I used Task 1 Enhanced function)

**Key Observations from Copilot Response:**
* **Explanation:** Confirmed that the global list `appointments` stores dictionary objects, and identified how `book_appointment()` uses conditional validation with `raise ValueError`.
* **3 Limitations Identified:**
  1. Only patient name is validated (practitioner name and time can still be empty).
  2. Appointment time is stored as an unvalidated plain text string.
  3. No conflict/collision checking (double-booking the same practitioner is allowed).
* **Suggested Improvements:**
  1. Validate all inputs (including whitespace check).
  2. Use Python's `datetime` module for time handling/sorting.
  3. Add scheduling conflict checks before appending.

## Part F - Input Verification Testing

| Test Input Scenario | AI Version Behavior (`smartcare_ai.py`) |
| --- | --- |
| **Normal Input** (`"Alice Smith"`, `"Dr. John Doe"`, `"10:00 AM"`) | Successfully adds to list and prints raw dictionary. |
| **Blank Patient Name** (`""`) | Accepts empty string `""` without any warning. |
| **Duplicate Practitioner & Time** | Allows double-booking; appends duplicate entry. |
| **`None` Values** | Accepts `None` for all parameters without error checking. |

## Part G - Controlled Code Improvement
* **Chosen Improvement:** Enhanced input validation in `smartcare_v01.py`.
* **Details:** Updated the booking logic to reject empty strings or whitespace-only inputs for `practitioner_name` and `appointment_time` alongside `patient_name`.