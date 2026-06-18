# Architecture

## Overview

Job Application Tracker is a Django-based platform for managing job search activities across multiple workspaces.

The application supports both server-rendered web views and REST API endpoints while maintaining a shared domain layer through dedicated service and selector patterns.

The architecture emphasizes:

- Centralized business logic.
- Separation of read and write operations.
- Workspace-based ownership boundaries.
- Transactional domain operations.
- Extensive automated testing.

This approach enables multiple interfaces to share the same business rules while reducing duplication and improving maintainability.

---

## Design Goals

The architecture is built around the following goals:

- Centralize business rules in a single location.
- Avoid duplicating validation logic across forms, serializers, views, and APIs.
- Support both Django web views and Django REST Framework endpoints.
- Enforce ownership and workspace isolation consistently.
- Improve testability through clear separation of concerns.
- Enable future expansion without requiring major architectural changes.

---

## Architectural Principles

### Business Logic Lives in Services

Business rules should not be implemented in views, forms, serializers, or API endpoints.

Instead, all domain operations are routed through dedicated services.

```text
View / API
    ↓
 Service
    ↓
 Model
```

Services are responsible for:

- Object creation
- Object updates
- Object deletion
- Ownership validation
- Relationship validation
- Transaction management

This ensures consistent behavior across both web and API interfaces.

---

### Read Operations Are Isolated

Read operations are handled through selectors.

```text
View / API
    ↓
 Selector
    ↓
 Database
```

Selectors are responsible for:

- Query construction
- Ownership-aware lookups
- Filtering
- Query reuse
- Query optimization

This prevents query duplication across multiple interfaces.

---

### Workspace-Based Ownership

Every major domain entity belongs directly or indirectly to a workspace.

```text
User
  ↓
Workspace
  ↓
Company
  ↓
Job Position
  ↓
Job Application
```

Workspaces provide:

- Ownership boundaries
- Data isolation
- Organizational separation
- Scalability opportunities
- Future multi-tenant capabilities

---

### Shared Domain Layer

Both the web application and REST API share the same services and selectors.

```text
Web Views
       \
        → Services
       /
REST API


Web Views
       \
        → Selectors
       /
REST API
```

This eliminates duplicated business rules and reduces maintenance overhead.

---

## Architectural Layers

### Presentation Layer

The presentation layer consists of:

- Django Class-Based Views
- Django Templates
- Django REST Framework Views
- Serializers
- Forms

Responsibilities:

- Handle HTTP requests
- Validate incoming data structure
- Render responses
- Delegate domain operations

This layer should not contain business rules.

---

### Service Layer

The service layer contains business logic and write operations.

Responsibilities:

- Create entities
- Update entities
- Delete entities
- Validate business rules
- Validate ownership
- Coordinate related objects
- Execute transactional operations

Services act as the single source of truth for domain behavior.

---

### Selector Layer

Selectors encapsulate read operations.

Responsibilities:

- Retrieve entities
- Build reusable queries
- Apply filters
- Enforce ownership constraints
- Centralize query logic

Conceptually:

```text
Selectors = Reads

Services = Writes
```

This separation improves maintainability and testability.

---

### Model Layer

Models are responsible for:

- Database schema
- Relationships
- Constraints
- Indexes

Business logic is intentionally kept outside models whenever possible.

---

## Request Lifecycle

### Write Operations

Create, update, and delete operations follow this flow:

```text
HTTP Request
    ↓
View / API Endpoint
    ↓
Form / Serializer Validation
    ↓
Service Layer
    ↓
Model Layer
    ↓
Database
```

Services perform all business validation and persistence.

---

### Read Operations

Read operations follow this flow:

```text
HTTP Request
    ↓
View / API Endpoint
    ↓
Selector Layer
    ↓
Database
```

Selectors are responsible for ownership-aware queries.

---

## Context Objects

Several services use context objects to group related identifiers and domain information.

Examples include:

- CompanyContext
- CompanyChildContext
- JobApplicationContext

Benefits:

- Explicit dependencies
- Cleaner service interfaces
- Improved readability
- Easier testing

Context objects reduce long parameter lists and provide a consistent way to pass domain context through the service layer.

---

## Validation Strategy

Validation occurs at multiple layers.

### Forms and Serializers

Responsible for:

- Field validation
- Request validation
- Input structure validation

### Services

Responsible for:

- Ownership validation
- Relationship validation
- Business rules
- Cross-model validation

### Models

Responsible for:

- Database constraints
- Integrity guarantees
- Schema-level validation

This layered approach ensures validation remains consistent across interfaces.

---

## Transaction Management

Write operations are executed through transactional services when appropriate.

The goal is simple:

- Either the entire operation succeeds.
- Or the entire operation fails.

This prevents partial updates and helps maintain domain consistency.

---

## Ownership Enforcement

Ownership validation is a core architectural concern.

Selectors and services enforce ownership boundaries before data is accessed or modified.

Typical validations include:

- Workspace ownership
- Company ownership
- Job position ownership
- Job application ownership
- Related object ownership

This approach helps prevent unauthorized access and cross-workspace data leakage.

---

## Testing Strategy

The project places significant emphasis on automated testing.

Tests cover:

- Models
- Services
- Selectors
- Forms
- Views
- API endpoints

The layered architecture improves testability by allowing business logic, query logic, and presentation logic to be tested independently.

---

## Future Improvements

Potential future improvements include:

- Enhanced filtering and search capabilities
- Improved error handling and user feedback
- REST API Version 2
- Additional reporting and analytics
- Shared workspace functionality
- Performance optimizations for larger datasets

The current architecture was designed to support these enhancements while minimizing large-scale refactoring.