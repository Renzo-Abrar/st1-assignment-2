# SmartCare v0.4 - Stage 4 Domain Design Review

## A - Approved UML Analysis & Responsibilities

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


## E - Review Generated Code (Microsoft Copilot)

### Critique & Consistency Table

| Review Criterion | Observed in Copilot Code | Assessment & Refinement Decision |
| :--- | :--- | :--- |
| **Model Consistency** | Dataclass matching UML attributes (`appointment_id`, `patient`, `practitioner`, `date_time`, `status`). | **Conforms**: Matches approved UML attributes and relationships. |
| **Encapsulation & Mutation** | Public fields in dataclass, but state transitions are guarded via explicit transition methods (`cancel()`, `complete()`, `schedule()`). | **Acceptable**: Methods explicitly guard transition logic. Callers must use domain methods rather than mutating fields directly. |
| **Dependencies & Scope** | Excluded database, UI, and external service classes completely. | **Conforms**: Complies strictly with domain layer scope restrictions. |
| **Error Handling** | Custom `InvalidStatusTransitionError` raised when attempting illegal transitions. | **Conforms**: Accurately enforces domain transition constraints. |
| **Object Retention** | `cancel()` changes status to `CANCELLED` without destroying instance or references. | **Conforms**: Maintains in-memory audit trail semantics. |

## F - Manual Behaviour Checks

### Verification Scenarios & Observed Behaviour

| Scenario | Code Executed / Test Action | Observed Behaviour & Domain Result | Conforms to Requirements? |
| :--- | :--- | :--- | :--- |
| **1. Create Valid Object** | `Appointment("A001", patient, practitioner, appt_time)` | Successfully initializes instance with `status = AppointmentStatus.SCHEDULED`. `validate()` returns `True`. | **Yes**: Correct default state and valid entity initialization. |
| **2. Try Invalid Input/State** | `Appointment("", patient, practitioner, appt_time)` | Instance initializes, but `validate()` evaluates to `False` due to empty string ID check. | **Yes**: Properly flags invalid domain state. |
| **3. Cancel Appointment** | `appt.cancel()` | Status transitions from `SCHEDULED` to `CANCELLED`. Object remains intact in memory along with patient/practitioner references. | **Yes**: Preserves objects in memory for historical audit logs. |
| **4. Illegal Repeated Transition** | Calling `appt.cancel()` a second time on a `CANCELLED` appointment | Raises `InvalidStatusTransitionError: Cannot cancel appointment from status CANCELLED.` | **Yes**: Successfully guards state invariants and prevents illegal lifecycle transitions. |

## G - Refactor

### Before Refactoring (Unfactored Duplicate Logic)
Prior to refactoring, transition checks were duplicated across `schedule()`, `cancel()`, and `complete()` methods using redundant conditional checks:


```python
# Before: Duplicated check logic in appointment.py
def cancel(self) -> bool:
    if self._status != AppointmentStatus.SCHEDULED:
        raise InvalidStatusTransitionError("Only scheduled appointments can be cancelled.")
    self._status = AppointmentStatus.CANCELLED
    return True

# After: Refactored with private helper method in appointment.py
def _ensure_scheduled(self, action_name: str) -> None:
    if self._status != AppointmentStatus.SCHEDULED:
        raise InvalidStatusTransitionError(
            f"Cannot {action_name} appointment from current status {self._status.name}."
        )

def cancel(self) -> bool:
    self._ensure_scheduled("cancel")
    self._status = AppointmentStatus.CANCELLED
    return True

```

## H - AI Engineering Log & Reflection

### AI Assistance Log

| Step / Prompt                     | AI Tool & Prompt Used                                                                                                                                                         | Response Evaluation & Action Taken                                                                                                                                                                     |
|:----------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Stage 4 Domain Implementation** | **GitHub Copilot**: *"Implement the Appointment class based on the Stage 3 UML model. Include attributes, properties, status transitions, and exception handling."* | **Evaluated & Accepted**: Generated clean dataclass/class structure with `AppointmentStatus` Enum and transition methods. Excluded database and UI bloat to maintain strict domain boundary alignment. |
| **Refactoring Status Logic**      | **GitHub Copilot**: *"Refactor status validation logic across schedule(), cancel(), and complete() to avoid duplicated checks."*                                    | **Evaluated & Accepted**: Extracted repeated condition checks into a private `_ensure_scheduled()` helper method, improving DRY compliance without altering domain behaviour.                          |

---

### Reflection Questions

#### 1. How did AI assist in moving from the UML model to Python domain code?
AI transitioned from design to code by generating the inital Python class structure, dataclasses, properties and enum templated matching the UML specs that was approved. It made sure that the names and annotations were aligned directly with the domain model.

#### 2. What domain rules or edge cases did the AI miss that required manual intervention?
The AI initially allowed external callers to state variables directly without state transition checks and failed to guard illegal transitions. Manual logic was needed to summarise attributes being `@property` getters and introduce `InvalidStatusTransitionErrors` to protect the domain invariants.

#### 3. How did refactoring improve code quality while preserving domain invariants?
Refactoring duplicated status validation logic across multiple methods into a single main central helper method. This elimanted code duplication, imrpoved maintainability, and ensured all transitions enforced the rule that operations need to originate from a `SCHEDULED` status.