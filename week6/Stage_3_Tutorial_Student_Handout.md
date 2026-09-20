# Assignment 2 - Case Study: Stage 3 Tutorial Activities
## From Requirements to Domain Models

---

## Candidate Concepts

| Candidate        | Class?  | Reason                                                                                                    |
|:-----------------|:--------|:----------------------------------------------------------------------------------------------------------|
| **Patient**      | **Yes** | Represents a core domain concept and care recipient supported directly by FR-01.                          |
| **Practitioner** | **Yes** | Represents a core domain concept and healthcare provider supported directly by FR-02.                     |
| **Appointment**  | **Yes** | Core domain entity linking patient, practitioner, date, and status, supported by FR-04.                   |
| **Name**         | **No**  | Represents a simple attribute/state value of Patient and Practitioner, not a standalone concept.          |
| **Clinic**       | **No**  | Represents organizational/architectural context rather than a domain entity required by functional rules. |
| **Database**     | **No**  | Technical persistence/infrastructure concern, not a business domain concept.                              |
| **Cancellation** | **No**  | Represents a business operation or state transition on an Appointment (`cancel()`), not an entity.        |
| **Status**       | **No**  | Modeled as an attribute or enumeration (`AppointmentStatus`) inside Appointment, not a standalone class.  |

---

## CRC Cards

### Class: Patient
* **Responsibilities:**
  * Maintain core patient details (`patient_id`, `name`, `contact_info`).
  * Validate that required patient details are present.
* **Collaborators:**
  * `Appointment`

### Class: Practitioner
* **Responsibilities:**
  * Maintain practitioner details (`practitioner_id`, `name`, `specialty`).
  * Validate practitioner profile completeness.
* **Collaborators:**
  * `Appointment`

### Class: Appointment
* **Responsibilities:**
  * Link exactly one `Patient` and one `Practitioner` to a date and time slot.
  * Enforce valid appointment lifecycle state transitions (e.g., `Scheduled` -> `Cancelled`).
* **Collaborators:**
  * `Patient`
  * `Practitioner`
  

## Relationship Reasoning

### Patient to Appointment: Which relationship and why?
* **Relationship:** Association (Multiplicity: `1` to `0..*`).
* **Reasoning:** A `Patient` can have zero or many (`0..*`) `Appointments` over time, but every individual `Appointment` must belong to exactly one (`1`) `Patient`. It is modeled as a simple association rather than composition or inheritance because `Patient` and `Appointment` are distinct domain entities with independent identities.

### Practitioner to Appointment: What multiplicity?
* **Multiplicity:** `1` to `0..*`.
* **Reasoning:** A `Practitioner` can be assigned to zero or many (`0..*`) `Appointments` on their schedule, while each individual `Appointment` is conducted by exactly one (`1`) `Practitioner`.

### Should Appointment inherit from Patient?
* **Answer:** No.
* **Reasoning:** Inheritance represents an "is-a" relationship (e.g., a Patient *is a* Person). An `Appointment` is a scheduled event/interaction between entities, not a type of `Patient`. Using inheritance here would violate object oriented principles and create invalid domains.

### Does Clinic need to own every object?
* **Answer:** No.
* **Reasoning:** Modeling `Clinic` as a top-level composite owner for every object creates unnecessary coupling and introduces a potential "God Class." Domain concepts like `Patient`, `Practitioner`, and `Appointment` exist meaningfully within the domain model without needing an explicit wrapper class to own their lifecycles.

## AI Model Critique

### Analysis of Proposed Manager, Controller, and Engine Classes

GitHub Copilot was asked to critique the introduction of six candidate support classes (`PatientManager`, `PractitionerManager`, `AppointmentManager`, `ClinicController`, `NotificationManager`, `ScheduleEngine`) against Domain-Driven Design and object-oriented principles.

#### Critique Summary Table

| Class Candidate           | Assessment            | Primary OO / Design Issue               | Justification                                                                                                                    |
|:--------------------------|:----------------------|:----------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------|
| **`PatientManager`**      | **Bad OO Design**     | Anemic domain model / Procedural design | Acts as a procedural CRUD wrapper around `Patient`. Patient-related state and validation belong directly in `Patient`.           |
| **`PractitionerManager`** | **Bad OO Design**     | Low cohesion                            | Symmetrical to `PatientManager`. Unnecessarily separates behavior from the state held within `Practitioner`.                     |
| **`AppointmentManager`**  | **Questionable**      | "Manager" anti-pattern                  | Hides domain operations (e.g., `cancel()`, `reschedule()`) that naturally belong inside `Appointment`.                           |
| **`ClinicController`**    | **Poor Design**       | God Class risk & High coupling          | Conflates UI/architectural layer concerns with the business domain. Centralizes all system logic into a single monolithic class. |
| **`NotificationManager`** | **Over-Engineering**  | YAGNI ("You Aren't Gonna Need It")      | Speculative design; no functional requirement in SmartCare v0.3 mandates notifications or reminders.                             |
| **`ScheduleEngine`**      | **Potentially Valid** | Domain Service candidate                | Double-booking checks (FR-05) span multiple entities. Valid if rules become complex, but unnecessary for initial v0.3 scope.     |

#### Architectural Recommendation
For Stage 3, the model remains restrained and expressive by focusing strictly on confirmed business entities: `Patient`, `Practitioner`, `Appointment`, and `AppointmentStatus` (enum). Operational workflows belong inside these domain entities rather than being offloaded to artificial manager or controller wrappers.