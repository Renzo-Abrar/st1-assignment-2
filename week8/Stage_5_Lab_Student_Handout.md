# Stage 5 Lab Activities: Refactoring SmartCare into a Layered Architecture

## Part A - Inspect SmartCare v0.4

### Identification of Mixed Responsibilities
In SmartCare v0.4, responsibilities across domain rules, workflow coordination, persistence, and presentation are currently mixed together within monolithic procedural scripts.

| Responsibility Area | Specific Misplaced Logic Identified | Problem Caused |
| :--- | :--- | :--- |
| **Presentation & Input** | Interactive `input()` prompts and menu rendering mixed with domain operations and database execution. | Direct coupling; impossible to unit test workflow or business rules without manual input. |
| **Workflow Coordination** | Use-case orchestration (verifying availability, checking patient status, calling database writes) handled inside CLI loops or domain methods. | Duplicated application logic across scripts and low cohesion. |
| **Domain Logic** | Enforcing appointment state transitions (`SCHEDULED` -> `CANCELLED`) intermingled with data storage operations. | Violates Single Responsibility Principle (SRP); business logic breaks if storage format changes. |
| **Data Access / Persistence** | Raw SQL queries (`INSERT INTO appointments`, `SELECT FROM patients`) embedded inside UI handlers and entity routines. | Rigid dependency on a concrete database provider (SQLite), leaking storage details across the codebase. |


## Part B  - Propose Architecture 
 
Drawing:

**Architecture Rules and Responsibilites** 

* **Presentation Layer:** Exclusively made for user interaction and output formatting. It depends only on the Service layer and has no database or domain rules.
* **Service Layer(`services/`):** Coordinates work flows like booking and cancelling appointments. It depends on the domain layer and interface, preventing coupling for the database.
* **Domain Layer(`domain/`):** Holds the core business entities (`Patient`, `Practitioner`, `Appointemnt`), the rules and transitions. It has zero dependencies on UI, Services or Persistance layers. 
* **Repository (`repositories/`):** Defines contract/interface for data storage operatiosn without exposing hwo data is saved or retrieved.
* **Persistance Layer(`persistance/`):** Implements the data access details. It executes the repository contract so that infrastructure can be swapped without modifying logic.

## Part C - Create Package Structure

To enforce separation of concerns, the system is organized into distinct packages following a layered architecture:

```text
smartcare/
│
├── domain/
│   ├── __init__.py
│   ├── appointment.py
│   ├── patient.py
│   └── practitioner.py
│
├── services/
│   ├── __init__.py
│   └── appointment_service.py
│
├── repositories/
│   ├── __init__.py
│   └── appointment_repository.py
│
├── persistence/
│   ├── __init__.py
│   └── sqlite_appointment_repository.py
│
├── presentation/
│   ├── __init__.py
│   └── cli.py
│
└── main.py
```

### Architectural Package Justification
* **`domain/`**: Houses core domain entities (`Patient`, `Practitioner`, `Appointment`), business rules, and state invariants. It has zero external dependencies on UI, application workflows, or storage engines.
* **`services/`**: Coordinates application use cases (e.g., booking and cancelling appointments). It depends on domain entities and repository abstractions, remaining decoupled from user interfaces and specific persistence technologies.
* **`repositories/`**: Defines abstract contracts and interfaces (`save()`, `find_by_id()`, `list_all()`) required by application services without tying the system to a specific database engine.
* **`persistence/`**: Implements the repository interfaces using concrete storage engines (e.g., SQLite, in-memory storage). It isolates SQL queries and database infrastructure from higher-level business policy.
* **`presentation/`**: Handles user interactions, terminal menus, and input validation, delegating business actions directly to the service layer.
* **`main.py`**: Serves as the application bootstrapper, instantiating repository implementations, injecting dependencies into services, and launching the user interface execution loop.


## Part D - Introduce AppointmentService

### Workflow Coordination Responsibility
The `AppointmentService` is responsible for orchestrating multi-entity workflows and managing application use cases without absorbing core domain rules or persisting data directly.

* **Use Cases Handled:**
  1. `book_appointment()`: Validates inputs, checks for conflicting appointments using the repository, creates an `Appointment` domain object, and saves it.
  2. `cancel_appointment()`: Fetches the target appointment by ID, invokes the domain entity's `.cancel()` method to enforce status invariants, and persists the state change.
  3. `list_appointments()`: Retrieves stored appointment records via the repository boundary.

### Preserving Domain Invariants
* **Workflow vs. Domain Rules:** `AppointmentService` handles workflow coordination (fetching data, calling repositories, organizing sequences). It does **not** manage internal status transition logic or domain guard clauses. State validations (such as preventing cancellations on completed appointments) remain strictly encapsulated inside `Appointment.cancel()`.

## Part E - Repository Abstraction

### Purpose of Repository Contract
The `AppointmentRepository` defines an abstract interface (contract) isolating application services from underlying database and persistence mechanics.

### Key Abstract Operations Defined
* `save(appointment: Appointment) -> None`: Stores a new appointment or updates an existing entity.
* `find_by_id(appointment_id: str) -> Optional[Appointment]`: Retrieves an appointment by its unique primary identifier.
* `list_all() -> List[Appointment]`: Returns all stored appointments.

### Architectural Benefits
1. **Dependency Inversion:** High-level service policy depends on this abstract interface, not on a concrete database driver (e.g., SQLite).
2. **Testability:** Allows substituting in-memory mock repositories during testing without needing live database infrastructure.

## Part F - AI Architecture Review

### Copilot / AI Review Summary
During the architectural review of the layered design, the AI model evaluated layer responsibility distribution, dependency direction, and abstraction boundaries:

1. **Layer Separation & Boundaries:** 
   * Confirmed that `presentation/cli.py` only handles terminal interface and user interaction.
   * Confirmed that `services/appointment_service.py` coordinates application use cases (`book_appointment`, `cancel_appointment`) without absorbing domain status transition rules.
   * Verified that `domain/appointment.py` encapsulates state transition invariants (`_ensure_scheduled`).

2. **Dependency Inversion Principle:**
   * Validated that `AppointmentService` depends strictly on the `AppointmentRepository` abstract interface rather than the concrete `SQLiteAppointmentRepository` class.

3. **Evaluation of AI Over-Engineering Risks:**
   * **Rejected AI Suggestions:** Copilot initially suggested adding direct database persistence logic and SQL query strings directly inside `AppointmentService`.
   * **Resolution:** Rejected database calls inside the service layer to preserve clean separation of concerns. Database interactions remain strictly encapsulated behind repository abstractions.

## Part G - System Integration & Entry Point

### Component Wiring Sequence
The system bootstrap process is managed in `main.py` following strict Layered Architecture dependency directions:

1. **Persistence Layer Initialization:** Instantiate `SQLiteAppointmentRepository` to hold the persistent data store.
2. **Service Layer Injection:** Inject the concrete `SQLiteAppointmentRepository` instance into the `AppointmentService` constructor.
3. **Presentation Layer Injection:** Inject the initialized `AppointmentService` instance into the `CLI` presentation interface.
4. **Execution Launch:** Invoke `cli.run()` to initiate user interactions.

## Part H - Reflection & Exit Questions

### 1. Architectural Benefits of Layered Decomposition
Transitioning SmartCare from a monolithic script into a 5-layer architecture (`domain`, `services`, `repositories`, `persistence`, `presentation`) provided clear operational benefits:
* **Separation of Concerns:** UI changes (like migrating from CLI to a GUI) or storage changes (like switching from SQLite to PostgreSQL) can happen independently without altering domain rules or service workflows.
* **Maintainability & Testability:** Decoupling application services from persistence engines allows isolated unit testing using mock repositories.

### 2. Dependency Inversion in Practice
* High-level business logic in `AppointmentService` depends strictly on the `AppointmentRepository` abstract interface rather than concrete SQLite infrastructure.
* Dependencies are injected at runtime inside `main.py`, ensuring low coupling and high adaptability.

### 3. AI Copilot Review & Over-Engineering Evaluation
* **Assistance:** Copilot effectively generated repository interface templates and standard boilerplate code for system bootstrapping.
* **Over-Engineering Risks:** Copilot attempted to insert raw SQL queries and persistence calls directly into `AppointmentService`. This was rejected during the architecture review to prevent coupling application workflows directly to specific storage mechanisms.