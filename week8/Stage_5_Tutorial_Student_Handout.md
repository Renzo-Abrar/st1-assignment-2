# Stage 5 Tutorial Activities: Architecture and Responsibility

## Activity 1 - Where Does This Belong?

| Responsibility | Layer | Reason |
| :--- | :--- | :--- |
| **Read menu input** | Presentation | User interface interaction and keyboard capture belong strictly in the UI layer (`presentation/cli.py`). |
| **Check appointment status transition** | Domain | Business rules and invariant validation constraints belong inside core domain entities (`domain/appointment.py`). |
| **Coordinate booking use case** | Service | Use case orchestration and multi-entity workflow management belong in the application service layer (`services/appointment_service.py`). |
| **Execute SQLite INSERT** | Persistence | Low-level database SQL execution and driver interactions belong in concrete persistence classes (`persistence/sqlite_appointment_repository.py`). |
| **Format confirmation message** | Presentation | Display string formatting and user-facing output belong in the presentation layer (`presentation/cli.py`). |
| **Find appointment by ID** | Repository / Persistence | Data querying signature is defined by the repository contract (`repositories/`) and executed by the persistence implementation (`persistence/`). |

## Activity 2 - Architecture Smell Hunt

### Identified Architecture Problems & Proposed Layer Allocations

1. **User Input Handling (`input()`) mixed with Domain & Storage:**
   * **Problem:** Direct user input calls are scattered across logic files, preventing automation and making interface migration impossible.
   * **Proposed Layer:** `Presentation` (`presentation/cli.py`).

2. **Direct Database SQL Queries (`sqlite3` / raw SQL):**
   * **Problem:** Business rules are directly bound to raw database queries, preventing database migration and breaking unit tests.
   * **Proposed Layer:** `Persistence` (`persistence/sqlite_appointment_repository.py`).

3. **Appointment Conflict Validation Rules:**
   * **Problem:** Conflict and schedule rules are leaking outside the business entities into scripts or database code.
   * **Proposed Layer:** `Domain` (`domain/appointment.py`).

4. **Console Output Formatting (`print()` statements):**
   * **Problem:** UI presentation string formatting is embedded inside business logic, making logic un-reusable for web or mobile APIs.
   * **Proposed Layer:** `Presentation` (`presentation/cli.py`).

5. **Entity Validation Checks (e.g., patient/practitioner state checks):**
   * **Problem:** Validation checks are duplicated or missing across procedural scripts rather than encapsulated.
   * **Proposed Layer:** `Domain` (`domain/patient.py`, `domain/practitioner.py`, `domain/appointment.py`).

## Activity 3 - SOLID Without Overengineering

### Questions & Analysis

1. **ClinicManager handles every use case. Which principle is threatened?**
   * **Answer:** **Single Responsibility Principle (SRP)**.
   * **Reason:** When a single class handles user interface routing, business workflows, data validation, and storage operations, it has multiple  reasons to change. Any modification to storage, CLI formatting, or business rules risks breaking unrelated features.

2. **AppointmentService imports sqlite3 directly. What dependency concern exists?**
   * **Answer:** Violation of **Dependency Inversion Principle (DIP)**.
   * **Reason:** High-level application logic in `AppointmentService` becomes tightly coupled to a low-level database implementation (`sqlite3`). This prevents switching storage mechanisms and makes isolated unit testing impossible without connecting to a live database.

3. **A repository interface has 20 methods but a client needs two. What concern exists?**
   * **Answer:** Violation of **Interface Segregation Principle (ISP)**.
   * **Reason:** Exposing a bloated ("fat") interface forces client classes to depend on unused data access signatures. Interfaces should be split into smaller, focused contracts tailored to specific application capabilities.

4. **Should every class have an interface? Explain.**
   * **Answer:** **No**.
   * **Reason:** Creating interfaces for simple, stable, concrete internal objects (such as pure value objects or internal utility helpers) adds unnecessary abstraction boilerplate without providing clear architectural benefit. Interfaces should be reserved for boundaries where dependency inversion, diverse behavior, or mock testing are mainly required.


## Activity 4 - AI Architecture Critique

| AI Architectural Proposal | Decision | Reason |
| :--- | :--- | :--- |
| **Microservices Architecture** | **Reject** | Over-engineered for current scope. Monolithic 5-layer architecture provides sufficient modularity without adding distributed network complexity, deployment overhead, or IPC latency. |
| **Event Bus / Message Queue** | **Defer** | Unnecessary asynchronous overhead for synchronous CLI operations. Can be considered later if real-time notifications or decoupled background jobs are required. |
| **Six Abstract Interfaces** | **Reject** | Excessive abstraction. Only application boundary contracts (e.g., `AppointmentRepository`) provide immediate value for decoupling persistence engines. |
| **Dependency-Injection (DI) Framework** | **Reject** | Introduces unnecessary framework complexity. Simple constructor injection managed inside `main.py` is clean, lightweight, and fully sufficient for the system's needs. |