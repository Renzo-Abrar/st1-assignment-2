# Stage 4 Tutorial Student Handout: Object-Oriented Design Decisions

## Activity 1 - Encapsulation Review

| Class            | Protected state / invariant                                                                                                                      | Public operations                                                                                                                                                          |
|:-----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Patient**      | `_patient_id`, `_name`, `_contact_info`; ensures attributes cannot be blank or modified into invalid strings.                                    | `@property patient_id`, `@property name`, `@property contact_info`, `validate()`                                                                                           |
| **Practitioner** | `_practitioner_id`, `_name`, `_specialty`; protects internal provider metadata and enforces validity.                                            | `@property practitioner_id`, `@property name`, `@property specialty`, `validate()`                                                                                         |
| **Appointment**  | `_appointment_id`, `_patient`, `_practitioner`, `_date_time`, `_status`; protects lifecycle state transitions and prevents illegal status jumps. | `@property appointment_id`, `@property patient`, `@property practitioner`, `@property date_time`, `@property status`, `schedule()`, `cancel()`, `complete()`, `validate()` |

## Activity 2 - Composition or Inheritance?

* **Appointment and Patient** $\rightarrow$ **Composition/association**
  * **Reason:** An appointment holds a reference to a patient ("has-a" relationship). An appointment is an event linking entities, not a specialized type of patient.
* **Appointment and Practitioner** $\rightarrow$ **Composition/association**
  * **Reason:** An appointment references a assigned practitioner ("has-a" relationship) to coordinate schedules without inheriting practitioner properties.
* **Doctor and Practitioner (hypothetical)** $\rightarrow$ **Inheritance**
  * **Reason:** A doctor is a specific type of practitioner ("is-a" relationship) sharing common practitioner attributes like ID and name while extending specialized capabilities.
* **Clinic and Appointment** $\rightarrow$ **Composition/association**
  * **Reason:** A clinic contains or manages multiple appointments ("has-a" relationship). Inheriting from appointment would create invalid domain abstractions.

## Activity 3 - Responsibility Allocation

* **Who decides whether SCHEDULED can become CANCELLED?**
  * The `Appointment` domain object itself (guarded via its `cancel()` operation and internal state transition rules).
* **Who validates a patient name?**
  * The `Patient` domain object (via its `validate()` method or constructor property setters).
* **Should Appointment execute SQL? Why?**
  * **No.** Domain entities must remain persistence-ignorant to preserve clean separation of concerns and avoid coupling core business logic directly to database infrastructure.
* **Should the UI decide whether a status transition is legal?**
  * **No.** The UI may reflect state for user display, but the domain model (`Appointment`) must strictly enforce and validate business invariants to prevent inconsistent states from un-validated callers.

## Activity 4 - AI Code Critique

### 1. Design Problems Identified in AI-Generated Class

1. **Public Status Mutation:** The AI exposed raw public access to `status` string attributes, allowing unvalidated status modifications from external callers without state transition checks.
2. **Persistence Coupling inside Domain Entities:** Including SQL execution inside `cancel()` violates separation of concerns by coupling core domain logic directly to infrastructure/database execution layers.
3. **Over-Engineered Infrastructure Dependencies:** Injecting a `NotificationManager` introduces speculative complexity and tight coupling to external communication channels not required by core domain invariants.
4. **Incorrect Inheritance Abstraction:** Inheriting `Appointment` from `PatientRecord` violates the "is-a" principle, causing tight coupling and improper domain hierarchy abstraction.
5. **Lack of Type Safety & Custom Exception Handling:** Using generic strings or standard exceptions instead of an explicit `AppointmentStatus` Enum and custom domain exceptions (`InvalidStatusTransitionError`) weakens domain guardrails.

### 2. Corrective Actions Applied

* **Encapsulate State:** Made `_status` private with read-only `@property status` accessors and enforced transitions through public methods (`cancel()`, `complete()`).
* **Remove Persistence Logic:** Stripped out SQL execution to keep domain entities completely persistence-ignorant.
* **Remove Speculative Dependencies:** Removed `NotificationManager` to stick strictly to confirmed domain scope.
* **Eliminate Inheritance:** Replaced `PatientRecord` subclassing with explicit association-based composition (`Patient` reference).
* **Enforce Type Guardrails:** Implemented `AppointmentStatus` Enum and `InvalidStatusTransitionError` to strictly control valid state lifecycles.

---

## Exit Question

### Why can code be object-oriented syntactically but still have poor object-oriented design?
Syntax alone doesnt equal proper object oriented design. Code can use classes syntactically while remaining purely procedural under the hood like when entities act as a passive data container. While external "Manager" or "Controller" classes handle all business logic. Poor OO design occurs when core principles like encapsulation, single responsibility, high cohesian and domain invarient guarding are violated, regardless of how clean the definition classes look.