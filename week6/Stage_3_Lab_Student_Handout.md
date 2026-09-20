# Stage 3 Lab Activities: SmartCare Domain Modelling

## A - Requirements Review

### Highlighting Nouns, Verbs, and Business Rules (SmartCare v0.2)

* **Nouns (Candidate Concepts / State):**
  * `Patient`: patient ID, name, contact details.
  * `Practitioner`: practitioner ID, name, specialty.
  * `Appointment`: appointment ID, date, time, status.
  * `Schedule`: time slot, availability.
* **Verbs (Behaviours / Operations):**
  * `create` / `register`: adding new patient or practitioner records.
  * `schedule`: booking an appointment between a patient and a practitioner.
  * `cancel`: updating an appointment status to cancelled.
  * `validate`: checking completeness and correctness of entity data.
  * `check_conflict`: detecting overlapping practitioner bookings.
* **Business Rules:**
  * A practitioner cannot be double-booked for the same time slot (FR-05).
  * An appointment status must transition legally (e.g., cannot cancel a completed appointment) (FR-06).
  * Cancelled appointments must be retained for historical audit trails rather than deleted (FR-06).



## B - Candidate Classes

| Candidate Concept | Supporting Requirement ID | Identified State (Attributes)                                      | Identified Behaviour (Operations)            |
|:------------------|:--------------------------|:-------------------------------------------------------------------|:---------------------------------------------|
| **Patient**       | FR-01                     | `patient_id`, `name`, `contact_info`                               | `validate()`                                 |
| **Practitioner**  | FR-02                     | `practitioner_id`, `name`, `specialty`                             | `validate()`                                 |
| **Appointment**   | FR-04, FR-05, FR-06       | `appointment_id`, `patient`, `practitioner`, `date_time`, `status` | `schedule()`, `cancel()`, `check_conflict()` |
| **Clinic**        | N/A (Architecture)        | `clinic_name`                                                      | N/A                                          |
| **Database**      | N/A (Infrastructure)      | N/A                                                                | N/A                                          |



## C - CRC Cards

### Class: Patient
* **Responsibilities:**
  * Maintain core patient details (`patient_id`, `name`, `contact_info`).
  * Validate that required patient state is complete.
* **Collaborators:**
  * `Appointment`

### Class: Practitioner
* **Responsibilities:**
  * Maintain practitioner details (`practitioner_id`, `name`, `specialty`).
  * Validate practitioner profile data.
* **Collaborators:**
  * `Appointment`

### Class: Appointment
* **Responsibilities:**
  * Maintain association between exactly one `Patient` and one `Practitioner`.
  * Track appointment time and state (`Scheduled`, `Completed`, `Cancelled`).
  * Enforce valid lifecycle transitions (e.g., cancel appointment).
* **Collaborators:**
  * `Patient`
  * `Practitioner`



## E - AI Design Review

### Copilot Design Recommendations & Review

GitHub Copilot was requested to analyze the confirmed SmartCare v0.3 requirements (FR-01 to FR-06) and suggest candidate classes, relationships, and supporting classes.

#### Suggested Core Domain Classes

| Class            | Supporting Requirement ID | Copilot Justification                                                                     |
|:-----------------|:--------------------------|:------------------------------------------------------------------------------------------|
| **Patient**      | FR-01                     | Patient records must be created and maintained.                                           |
| **Practitioner** | FR-02                     | Practitioner records must be created and maintained.                                      |
| **Appointment**  | FR-04, FR-05, FR-06       | Appointment booking, conflict checking, status management, and cancellation are required. |

#### Excluded / Unrecommended Classes

| Candidate Class | Reason for Exclusion                                                                                                   |
|:----------------|:-----------------------------------------------------------------------------------------------------------------------|
| **Clinic**      | Identified as an architectural concept; no functional requirement explicitly supports it.                              |
| **Database**    | Infrastructure implementation detail, not a domain concept.                                                            |
| **Schedule**    | Availability and conflict checking are handled via `Appointment` and `Practitioner`; no persistent entity is required. |

#### Suggested Relationships

1. **Patient ↔ Appointment:** Association with Multiplicity `1` to `0..*` (FR-04). One patient can have zero or many appointments; each appointment belongs to exactly one patient.
2. **Practitioner ↔ Appointment:** Association with Multiplicity `1` to `0..*` (FR-04, FR-05). One practitioner can have zero or many appointments; each appointment involves exactly one practitioner.
3. **Patient ↔ Practitioner:** Indirect association mediated entirely through `Appointment`.

## F - Compare and Decide

### Evaluation of Copilot Proposals vs. Confirmed Requirements

Based on the human domain model and Copilot's suggested ideas, the evaluate and record the design choices:

| AI Suggestion                                 | Decision     | Justification / Evidence                                                                                                                                                                                                                                                             | Model Change                                                                                                            |
|:----------------------------------------------|:-------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------|
| **`AppointmentStatus` (Enum)**                | **Accepted** | **Supported by FR-04 & FR-06:** Appointments explicitly track lifecycle states (`Scheduled`, `Completed`, `Cancelled`). Using an enumeration prevents invalid string assignments and enforces valid state transitions.                                                               | Added `AppointmentStatus` enumeration to the domain model and linked it to `Appointment`.                               |
| **`SchedulingEngine` (Service)**              | **Modified** | **Partial support via FR-05:** Conflict detection (preventing practitioner double-booking) is a critical business rule, but a full standalone engine/service class is unnecessary in v0.3. Conflict validation can be performed directly within domain entities or parameter checks. | Kept conflict check logic co-located with `Appointment` state validation rather than creating a separate service class. |
| **`AppointmentManager` / `ClinicController`** | **Rejected** | **No requirement support:** Neither the client brief or functional requirements request application-layer managers or controllers for Stage 3. Introducing manager classes risks creating "God Classes" that strip domain entities of their proper responsibilities.                 | Rejected. Domain entities retain responsibility for their own state and lifecycle.                                      |

## (Part G is Attached)

## H - Consistency Check

To ensure structural and behavioural alignment across requirements, model design, and code implementation, the following verification checks were performed:

* **Class Name Alignment:** Class names in `domain_models.py` (`Patient`, `Practitioner`, `Appointment`, `AppointmentStatus`) match the UML class diagram and CRC cards exactly.
* **Attribute Consistency:** All domain attributes (`patient_id`, `name`, `contact_info`, `practitioner_id`, `specialty`, `appointment_id`, `date_time`, `status`) reflect the state variables defined in requirements FR-01, FR-02, and FR-04.
* **Method & Responsibility Allocation:** Methods (`validate()`, `schedule()`, `cancel()`) align with the responsibilities assigned to each entity in the CRC cards.
* **Relationship Integrity:** Associations are maintained via object references (e.g., `Appointment` holds references to `Patient` and `Practitioner` instances) rather than unvalidated flat strings.
* **Scope Control:** No unsupported manager, engine, database, or controller classes were added during coding, ensuring the implementation stays strictly within the confirmed Stage 3 domain boundaries.

---

## Reflection

### 1. What modelling decision was hardest?
The hardest modelling decision was finding where conflict checking (preventing double-booking under FR-05) and appointment state management should live. Initial considerations was to include creating a separate `AppointmentManager` or `SchedulingEngine` service class. But, to avoid over-engineering at Stage 3 and maintain proper allocation, I kept booking state and basic transition checks directly inside `Appointment`, referencing valid `Patient` and `Practitioner` instances.

### 2. Where did AI over-design?
GitHub Copilot over-designed by proposing application-layer controller and service classes (`AppointmentManager` and `SchedulingEngine`). While these patterns are common in enterprise applications, introducing them in Stage 3 stripped proper responsibilities away from core domain entities and introduced unnecessary complexity without explicit requirement support.

### 3. What evidence supported your final choices?
Our final choices were supported directly by confirmed functional requirements:
* **FR-01, FR-02, FR-04:** Justified `Patient`, `Practitioner`, and `Appointment` as core domain entities.
* **FR-04 & FR-06:** Justified adding the `AppointmentStatus` enumeration to enforce legal state transitions (`Scheduled` -> `Cancelled`).
* **Lack of explicit requirements:** Justified rejecting `AppointmentManager` and excluding technical infrastructure concerns like databases or UI controllers.