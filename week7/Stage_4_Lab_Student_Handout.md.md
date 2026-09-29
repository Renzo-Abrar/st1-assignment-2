# SmartCare v0.4 - Stage 4 Domain Design Review

## Approved UML Analysis & Responsibilities

### 1. Domain Entities & Responsibilities
* **Patient**: Holds `patient_id`, `name`, and `contact_info`. Responsible for encapsulating patient identity and validating core attribute completeness.
* **Practitioner**: Holds `practitioner_id`, `name`, and `specialty`. Responsible for holding provider identity and ensuring valid specialty/name data.
* **Appointment**: Holds `appointment_id`, references to `Patient` and `Practitioner`, `date_time`, and `status`. Responsible for managing appointment lifecycle transitions (`SCHEDULED`, `CANCELLED`, `COMPLETED`) and protecting status invariants.

### 2. Relationship Analysis
* **Appointment -> Patient**: Direct reference (association). An appointment must have exactly one patient.
* **Appointment -> Practitioner**: Direct reference (association). An appointment must have exactly one practitioner.
* **Lifecycle Semantics**: Retaining cancelled appointments requires keeping the `Appointment` instance in memory with a status flag of `CANCELLED` rather than destroying the object or its linked patient/practitioner references.

### 3. State & Validation Rules
* Raw strings for appointment status are replaced with an explicit `AppointmentStatus` Enum.
* Status changes must occur through explicit class methods (`cancel()`, `complete()`), prohibiting raw external mutation of private state.


