# SmartCare v0.3 - Domain Model Workbook

## Requirement-to-Concept Trace

| Requirement | Concept | State / Behaviour | Decision |
| :--- | :--- | :--- | :--- |
| FR-01: Maintain patient details | Patient | `patient_id`, `name`, `contact_info` / `validate()` | **Accept:** Core domain concept representing the care recipient. |
| FR-02: Maintain practitioner details | Practitioner | `practitioner_id`, `name`, `specialty` / `validate()` | **Accept:** Core domain concept representing the provider. |
| FR-04: Schedule appointment | Appointment | `appointment_id`, `date_time`, `status` / `schedule()` | **Accept:** Central domain object coordinating patient, practitioner, and time. |
| FR-05: Prevent double-booking | Appointment / Practitioner | `check_conflict()` | **Accept:** Core business logic placed within domain model validation. |
| FR-06: Cancel appointment | Appointment | `status` / `cancel()` | **Accept:** Encapsulates legal state transitions (`Scheduled` -> `Cancelled`). |
| System Architecture | Clinic | `clinic_name` / `get_schedule()` | **Reject / Defer:** Not required as a domain class; organizational context only. |
| Persistence / Storage | Database | N/A | **Reject:** Technical infrastructure concern, not a domain concept. |
| Notification Engine | NotificationManager | N/A | **Reject:** Out of scope for v0.3 domain model; over-engineering. |

## CRC Cards

### Class: Patient
* **Responsibilities:**
  * Maintain patient state (`patient_id`, `name`, `contact_info`).
  * Validate patient data completeness.
* **Collaborators:**
  * `Appointment`

### Class: Practitioner
* **Responsibilities:**
  * Maintain practitioner state (`practitioner_id`, `name`, `specialty`).
  * Validate practitioner availability and state.
* **Collaborators:**
  * `Appointment`

### Class: Appointment
* **Responsibilities:**
  * Hold references to `Patient` and `Practitioner`.
  * Track booking time and lifecycle status (`Scheduled`, `Completed`, `Cancelled`).
  * Enforce state transition rules (e.g., cannot cancel if already completed).
* **Collaborators:**
  * `Patient`
  * `Practitioner`

## UML Class Diagram



## Design Rationale

**Class Selection:** Only `Patient`, `Practioner`, and `Appointment` were chosen as domain classes because it directly represents real world domain entities
which is backed by confirmed requirements (FR-01, FR-02, FR-04). The technical concerns like databases and UI controllers were purposely excluded to maintain
a clean model for the domain.

**Responbility Allocation:** `Appointment` acts ad the primary coordinator holding references to both `Patient` and `Practitioner`. State transition logic like `cancel()`
is directly inside `Appointment` to make sure it maintains a high cohesion and protect state invariants.

**Key Relationships:** Both `Patient` and `Practitioner` have a `1` to `0..*` association with `Appointment`. An appointment needs to be linked to exactly one patient and one 
practitioner, while a patient or practitioner can have a zero or multiple appointments over time.

## AI Design Review Record from Microsoft Copilot

**Prompt:** Act as a software architect. Review the SmartCare v0.3 requirements (patient tracking, practitioner management, appointment scheduling, double-booking prevention, cancellation). Suggest candidate classes and relationships. Cite the supporting requirement ID for every element proposed, and highlight any manager, controller, or engine classes separately.

| AI Suggestion | Evidence | Decision | Reason | Model Change |
| :--- | :--- | :--- | :--- | :--- |
| **`AppointmentStatus` (Enum)** | **FR-04, FR-06:** Lifecycle states (`Scheduled`, `Completed`, `Cancelled`) are explicitly defined. | **Accept** | Prevents invalid string states and formalizes state transitions cleanly. | Added `AppointmentStatus` enumeration linked to `Appointment`. |
| **`SchedulingEngine`** | **FR-05:** Prevent double-booking rule exists, but does not justify a dedicated engine object in v0.3. | **Modify** | Double-booking logic can be handled directly as a method inside `Appointment` or checked against existing practitioner schedules without introducing an extra domain service class. | Kept conflict check logic co-located with `Appointment` state validation. |
| **`AppointmentManager`** | **None:** No requirement specifies a dedicated application-layer manager for v0.3 domain modeling. | **Reject** | Introduces accidental complexity and risks becoming a "God Class" that strips domain entities of their proper responsibilities. | Rejected. Coordination remains within domain entities for Stage 3. |