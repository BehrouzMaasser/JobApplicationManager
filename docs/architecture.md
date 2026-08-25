# Architecture

## Overview

Job Application Tracker is a Django-based platform for managing job search activities across multiple workspaces.

The application supports both server-rendered web views and REST API endpoints while maintaining a shared application layer through dedicated service and selector patterns.

The architecture emphasizes:

- Centralized business logic.
- Separation of read and write operations.
- Workspace-based ownership boundaries.
- Transactional domain operations.
- Automated testing.

Both the web interface and REST API use the same application-layer services and selectors so that domain behavior is not duplicated between transports.

---

## Design Goals

The architecture is built around the following goals:

- Centralize business rules in Services.
- Keep read/query behavior in Selectors.
- Keep transport-specific validation in Forms and Serializers.
- Enforce ownership and resource isolation consistently.
- Keep transaction boundaries inside Services.
- Make business behavior independently testable.

---

## Architectural Principles

### Business Logic Lives in Services

Business rules and write-side domain invariants are implemented in Services rather than in views, forms, serializers, or API endpoints.

```text
View / API
    ↓
 Service
    ↓
 Model
```

Services are responsible for creating, updating, deleting, validating write-side domain relationships and invariants, and coordinating transactions.

### Reads Are Isolated in Selectors

Read operations are handled through Selectors.

```text
View / API
    ↓
 Selector
    ↓
 Database
```

Selectors own query construction, access-scoped retrieval, filtering, and query optimization.

A resource that cannot be retrieved through the caller's access-scoped selector is represented as `ResourceNotFoundError`, resulting in HTTP 404 at the presentation boundary.

### Ownership and Access

Selectors enforce read access by restricting their accessible querysets. Services enforce ownership and aggregate relationships for objects supplied to write operations.

This distinction is intentional:

```text
Direct resource access
    ↓
Selector access scope
    ↓
ResourceNotFoundError
    ↓
404

Related object supplied during a write
    ↓
Service invariant validation
    ↓
DomainInvariantViolationError
    ↓
400
```

### Shared Application Layer

Both the web application and REST API use the same Services and Selectors.

```text
Web Views ───┐
             ├──→ Services / Selectors
REST API ────┘
```

---

## Architectural Layers

### Presentation Layer

The Presentation Layer consists of Django Views, DRF ViewSets, Forms, Serializers, and presentation mixins.

Responsibilities:

- Handle HTTP requests.
- Validate transport-specific input.
- Restrict presentation choices using access-scoped Selectors where necessary.
- Delegate reads to Selectors.
- Delegate writes to Services.
- Translate application exceptions into HTTP responses.

It does not implement business rules or persistence workflows.

### Service Layer

Services contain write-side application behavior.

Responsibilities:

- Create, update, and delete entities.
- Validate business rules.
- Validate aggregate relationships.
- Validate ownership of supplied related objects.
- Enforce many-to-many invariants.
- Manage transactions.
- Delegate intrinsic model validation to models.

### Selector Layer

Selectors encapsulate read operations.

Responsibilities:

- Retrieve entities.
- Apply access-scoped querysets.
- Apply reusable filters.
- Optimize queries.

Selectors do not mutate state or implement business workflows.

### Model Layer

Models define persistence schema, database constraints, and intrinsic entity validation.

Models do not perform authorization or application workflows.

---

## Validation Strategy

Validation is intentionally distributed by responsibility:

### Forms and Serializers

Validate transport-specific input such as field types, formatting, required input, and presentation-level constraints.

Forms may use access-scoped Selectors to ensure users are only offered resources they can access. They do not implement ownership rules themselves.

### Services

Validate business rules, aggregate relationships, supplied-object ownership, and write-side domain invariants.

### Models

Validate intrinsic entity state and enforce database-level integrity.

---

## Exception Strategy

The application uses the following application-level exception categories:

- `ResourceNotFoundError` — the requested resource cannot be resolved through the caller's access-scoped selector.
- `BusinessRuleViolationError` — a valid operation is rejected by a business rule.
- `DomainInvariantViolationError` — supplied or resolved data violates a write-side domain invariant, including ownership of related objects supplied to a write operation.
- `InfrastructureViolationError` — the current broad category for unexpected database, ORM, framework, or programming/infrastructure failures.

There is no separate `AccessDeniedError`. Inaccessible resources are represented as `ResourceNotFoundError` and presented as HTTP 404.

---

## Transaction Management

Public Service write operations execute within transaction boundaries. If a write operation fails, the transaction is rolled back so that partial state is not committed.

Selectors do not manage transactions.

---

## Testing Strategy

Tests are organized around architectural responsibilities:

- Models test intrinsic state, validation, and database constraints.
- Selectors test retrieval, access isolation, filtering, and applicable exception translation.
- Services test business rules, domain invariants, ownership validation, and transactional behavior.
- Forms and Serializers test transport validation.
- Views and ViewSets test orchestration and HTTP behavior.
- Exception-handler tests verify application-to-HTTP translation.

Coverage is a useful metric but is not itself evidence that the architecture is correctly tested.

---

## Architectural Boundary

The intended dependency direction is:

```text
Presentation
     ↓
Application (Services / Selectors)
     ↓
Models / Database
```

Lower layers remain independent of HTTP and presentation concerns.
