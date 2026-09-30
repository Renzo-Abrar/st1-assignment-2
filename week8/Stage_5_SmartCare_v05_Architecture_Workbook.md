# SmartCare v0.5 - Architecture and Refactoring Workbook

## Current Architecture Problems

| Problem                         | Evidence                                                                                                       | Impact                                                                                             | Refactoring                                                                                                                 |
|:--------------------------------|:---------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------|
| **Monolithic File Structure**   | User interface, use case coordination, domain logic, and persistence were co-located in a single script.       | High coupling, impossible to modify interface or storage without risking domain logic regressions. | Decompose system into a 5-layer package architecture (`domain`, `services`, `repositories`, `persistence`, `presentation`). |
| **Direct Persistence Coupling** | Application code directly invoked raw dictionary operations or SQL statements during business logic execution. | Prevents database migration and makes unit testing without live storage engines impossible.        | Introduce an abstract `AppointmentRepository` interface contract to decouple service logic from storage mechanics.          |
| **UI and Domain Bleed**         | Print statements and console `input()` operations were directly embedded inside business logic workflows.      | Logic cannot be reused across other interfaces (e.g., Web API, Desktop GUI, or automated tests).   | Isolate all terminal input/output and formatting into the `presentation/cli.py` layer.                                      |
| **Leaky Invariants**            | Domain state validation and cancellation rules were checked manually across multiple places in the script.     | Inconsistent business logic enforcement and high risk of invalid state transitions.                | Encapsulate domain rules and state transition validation directly inside the `domain/` entities.                            |

## Layer Responsibilities

| Layer            | Responsibilities                                                                                                                                             | Must Not Contain                                                                                                      |
|:-----------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------|
| **Presentation** | Handles user interface interactions, formats console text/menus, captures keyboard input, and invokes service workflows.                                     | Business logic rules, direct entity attribute modifications, or raw database queries/SQL statements.                  |
| **Service**      | Coordinates application use cases (e.g., booking/cancelling appointments), shows domain entities, and controls transaction boundaries.                       | UI formatting, terminal `input()` / `print()` calls, or direct database driver implementation code.                   |
| **Domain**       | Summarises core business entities (`Patient`, `Practitioner`, `Appointment`), enforces invariant validation rules, and manages lifecycle status transitions. | Knowledge of user interface components, external database schemas, or infrastructure frameworks.                      |
| **Repository**   | Defines abstract interface contracts (`AppointmentRepository`) specifying data access signatures for storage operations.                                     | Concrete database connection strings, lower-level storage driver implementations, or business use case orchestration. |
| **Persistence**  | Implements repository contracts (`SQLiteAppointmentRepository`) to execute concrete data persistence, SQL queries, or dictionary storage.                    | Core business rules, status transition constraints, or user interface presentation formatting.                        |


### Architectural Key
1. **Presentation Layer (`presentation/`):** Invokes `AppointmentService` workflows.
2. **Service Layer (`services/`):** Coordinates application use cases and orchestrates domain logic.
3. **Domain Layer (`domain/`):** Contains core business entities and invariant validation rules.
4. **Repository Layer (`repositories/`):** Defines abstract interface signatures for storage operations.
5. **Persistence Layer (`persistence/`):** Implements repository contracts to manage data storage.

Diagram: 

## SOLID Review

| Principle | Relevant? | Evidence                                                                                                                               | Decision                                                                                                                                  |
|:----------|:----------|:---------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------|
| **SRP**   | **Yes**   | Split single monolithic file into distinct layers (`presentation/cli.py`, `services/appointment_service.py`, `domain/appointment.py`). | **Applied:** Each class now has a single reason to change. UI updates do not affect service or domain logic.                              |
| **OCP**   | **Yes**   | Persistence layer implements an abstract `AppointmentRepository` contract.                                                             | **Applied:** New storage engines (e.g., PostgreSQL or In-Memory) can be added without modifying existing service code.                    |
| **LSP**   | **Yes**   | `SQLiteAppointmentRepository` implements all methods defined in `AppointmentRepository`.                                               | **Applied:** Any concrete repository implementation can cleanly substitute `AppointmentRepository` without breaking `AppointmentService`. |
| **ISP**   | **Yes**   | `AppointmentRepository` defines only the specific methods required for appointment persistence operations.                             | **Applied:** Clean interface focusing solely on appointment CRUD operations without fat, unrelated methods.                               |
| **DIP**   | **Yes**   | `AppointmentService` depends on the abstract `AppointmentRepository` contract rather than `SQLiteAppointmentRepository`.               | **Applied:** High-level policy depends on abstraction; dependencies are injected at runtime in `main.py`.                                 |


## AI Architecture Review

| AI suggestion                                                             | Observed problem?                                                                              | Decision   | Reason                                                                                                                   | Verification                                                                                                          |
|:--------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------|:-----------|:-------------------------------------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------|
| **Embed raw SQL queries inside `AppointmentService`**                     | High-level service layer becomes tightly coupled to SQLite infrastructure details.             | **Reject** | Violates Dependency Inversion (DIP) and Layered Architecture; storage concerns must remain behind repository interfaces. | Verified that `services/appointment_service.py` contains no `sqlite3` imports or SQL strings.                         |
| **Combine `repositories/` and `persistence/` into a single folder**       | Obscures the boundary between abstract interface contracts and concrete implementations.       | **Reject** | Keeping contracts isolated in `repositories/` allows clean dependency inversion and flexible persistence swapping.       | Verified package structure contains separate `repositories/` and `persistence/` directories with `__init__.py` files. |
| **Inject repository instances into `AppointmentService` via constructor** | Manual object instantiations inside service methods cause rigid concrete coupling.             | **Keep**   | Supports Dependency Injection; enables runtime configuration in `main.py` and simplifies unit testing with mocks.        | Verified `AppointmentService.__init__` accepts `AppointmentRepository` abstract type parameter.                       |
| **Expose state mutation methods directly on domain attributes**           | Allows presentation layer to arbitrarily alter domain entity state bypassing validation rules. | **Reject** | Domain invariants and state transition rules (e.g., cancellation) must be strictly encapsulated inside domain entities.  | Verified `Appointment` manages status transitions through controlled domain methods (`cancel()`).                     |