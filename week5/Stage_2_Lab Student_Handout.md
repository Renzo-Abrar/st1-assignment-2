# Stage 2 Lab - SmartCare Requirements Engineering

## Part A - Client Brief Analysis (AI OFF)

* **Current State:** SmartCare uses manual paper records and spreadsheets.
* **Key Issues Identified:**
  * Duplicate bookings
  * Difficulty locating patient records
  * Inconsistent appointment status tracking
  * Limited historical record retention
* **Client Goal:** Build a small, maintainable patient, practitioner, and appointment tracking system.

## Part B - Stakeholders and Scope (AI OFF)

### Stakeholder Map

| Stakeholder | Need                                                          | Potential Conflict                                                                                     |
|---|---------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| **Receptionist** | Quick patient lookup with appointment scheduling | Prefers simple, fast interface over multi step verification                                            
| **Practitioner (Doctor/Nurse)** | Accurate patient history and clear daily appointment schedules | Needs detailed patient history without clutter from cancelled appointments.                            |
| **Clinic Manager / Management** | Reliable  tracking and historical appointments | Wants full record retention/audit trails which may clutter operational views if unfiltered.            |
| **Patient** | Efficient booking process and clear status updates | Desires convenience (e.g., self-service/reminders) which may fall outside immediate core system scope. |

### Scope Definition

* **In Scope:**
  * Patient profile management (creation, unique ID assignment, record lookup).
  * Practitioner profile management and schedule visibility.
  * Appointment scheduling, status updating, and cancellation tracking.
  * Retaining cancelled appointments within historical records.

* **Out of Scope:**
  * Patient self-service portal or direct online booking.
  * Automated SMS/Email notifications.
  * Billing, invoicing, or payment processing.
  * Clinical decision support or AI treatment recommendations.

## Part C - Functional Requirements (AI OFF)

* **FR-01:** The system shall allow staff to create a new patient profile with a unique patient ID.
* **FR-02:** The system shall allow staff to search for patient records by patient ID or full name.
* **FR-03:** The system shall allow staff to register new practitioner profiles with assigned specialties.
* **FR-04:** The system shall display daily appointment schedules for selected practitioners.
* **FR-05:** The system shall allow staff to schedule an appointment linking a valid patient, practitioner, date, and time slot.
* **FR-06:** The system shall prevent duplicate appointment bookings for the same practitioner at the same time slot.
* **FR-07:** The system shall allow staff to update an appointment's status to "Completed".
* **FR-08:** The system shall allow staff to mark an appointment as "Cancelled".
* **FR-09:** The system shall retain cancelled appointments in historical records while marking their status as "Cancelled".
* **FR-10:** The system shall display complete historical appointment records for a specified patient.

## Part D - Non-Functional Requirements (AI OFF)

* **NFR-01 (Data Integrity):** The system shall maintain consistent status flags across all appointment records and prevent orphan records.
* **NFR-02 (Maintainability / Testability):** Core business logic (booking validation, conflict checks) shall be decoupled from storage and independently unit-testable.
* **NFR-03 (Performance):** The system shall return patient search results in under 2 seconds for datasets up to 10,000 records under normal load.
* **NFR-04 (Usability):** The interface shall allow staff to complete an appointment booking in 4 steps or fewer.
* **NFR-05 (Reliability & Audit):** Cancelled appointments shall be permanently stored for audit purposes and cannot be hard-deleted through standard operational workflows.

## Part E - User Stories and Acceptance Criteria (AI OFF)

### User Stories

* **US-01:** As a receptionist, I want to search for patients by ID or name, so that I can quickly access their records during check-in.
* **US-02:** As a receptionist, I want the system to block double-bookings for practitioners, so that I avoid scheduling conflicts.
* **US-03:** As a practitioner, I want to view my daily schedule, so that I can manage my time and prepare for consultations.
* **US-04:** As a receptionist, I want to cancel an appointment when requested, so that the time slot becomes available while preserving record history.
* **US-05:** As a clinic manager, I want to retain all historical and cancelled appointment records, so that the clinic maintains complete audit trails.

### Acceptance Criteria (Given-When-Then Format)

#### Scenario 1: Successful Patient Search (US-01)
* **GIVEN** a registered patient exists in the system with ID `P1001`,
* **WHEN** the receptionist searches for `P1001`,
* **THEN** the system displays the patient's full details within 2 seconds.

#### Scenario 2: Double-Booking Prevention (US-02)
* **GIVEN** Practitioner `Dr. Smith` has an appointment scheduled at `10:00 AM`,
* **WHEN** the receptionist attempts to book another patient with `Dr. Smith` at `10:00 AM`,
* **THEN** the system  then rejects the booking and displays a schedule conflict error.

#### Scenario 3: Negative Path - Invalid Cancellation (US-04)
* **GIVEN** an appointment with status `Completed`,
* **WHEN** staff attempt to mark the appointment as `Cancelled`,
* **THEN** the system rejects the status change and displays an invalid operation error.

## Part F - AI Requirements Review (Microsoft Copilot Audit)

### Summary of Audit Findings
* **Ambiguities Identified:** 
  * Patient ID format/generation rules (FR-01) and full-name search rules (FR-02).
  * Scope of "complete historical appointment records" (FR-10) and definition of time slot duration (FR-05, FR-06).
* **Inconsistencies Identified:** 
  * Missing initial state in the appointment lifecycle (e.g., "Scheduled" state prior to "Completed" or "Cancelled").
  * Disconnect between US-04 (which explicitly states cancelling frees the time slot) and FR-08/FR-09 (which only specify status update and retention).
* **Testability Concerns:** 
  * NFR-01 (Data Integrity) and NFR-04 (Usability) lack precise quantitative criteria for what constitutes a "step" or "consistent flags".

---

## Part G - AI Requirements Audit & Action Plan

| AI Suggestion / Finding                                                                              | Classification | Evidence / Reason                                                                                      | Action Plan / Resolution                                                                                                                                              |
|------------------------------------------------------------------------------------------------------|----------------|--------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Clarify Appointment Status Model** (Define initial 'Scheduled' state and valid state transitions). | Accepted       | Direct evidence from FR-07, FR-08, and Acceptance Criteria (Completed cannot transition to Cancelled). | **Update Spec:** Explicitly define the lifecycle: `Scheduled` -> `Completed` OR `Scheduled` -> `Cancelled`. Block all invalid transitions.                            |
| **Explicitly state slot availability upon cancellation** (Link FR-08 to US-04).                      | Accepted       | Direct evidence in US-04 ("time slot becomes available while preserving record history").              | **Update Spec:** Update FR-08 to state: "The system shall mark cancelled appointments as 'Cancelled' and immediately free the associated time slot for new bookings." |
| **Add facial recognition login for staff**                                                           | Out of Scope   | Exceeds scope the boundaries of a basic record tracking system.                                        | **Reject:** Maintain strict out-of-scope boundaries.                                                                                                                  |
| **Add SMS / Email patient notification gateway**                                                     | Out of Scope   | No evidence in client brief, system is internal-only.                                                  | **Reject:** Focus solely on internal staff workflows.                                                                                                                 |
| **Define Patient Search matching logic** (Case-insensitive, partial matching vs exact).              | Accepted       | Supported by FR-02 ambiguity analysis, prevents developer interpretation drift.                        | **Update Spec:** Specify that FR-02 requires case-insensitive, partial-string matching for patient name searches.                                                     |

## Part H - Reflection & Exit Question

During the requirements audit, Microsoft Copilot shows structural gaps that I missed. Most notable was how it identidfied that our appointment status model was incomplete, while we defined "Completed" and "Cancalled" states, we did lack the initial "Scheduled" status and formal transition rules. Copilot also caught an inconsitency between User Story 04 and FR-08, and it poitned out that the functional requirements failed to state that cancelling an appointment would release the time slot for any future bookings.

When prompted for system enhancements, AI often overreaches by inventing out of scope features like automated SMS reminders, online payments and biometrics. These features would lack any supporting evidence in the client brief and would exceed the scop for the management app.

After the review, FR-08 was updated to show that marking an appointment as "Cancelled" frees the time slot while preserving record history.

Requirements needs evidence because unbacked recommendations cause scope creep, high development costs, and failing systems that would not help the clients core needs. Thats why having human validation against client evidence remains important.

