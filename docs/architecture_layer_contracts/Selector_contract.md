# Selector Contract

Selectors are responsible for retrieving persisted domain objects from the database.

They encapsulate query logic, enforce read access control, and translate
database exceptions into domain-level exceptions. Selectors are strictly
read-only and must never contain business logic or modify application state.


Models define and enforce the integrity of persisted data.

Selectors retrieve persisted data.

Services implement business workflows and state changes.

Views expose services through HTTP.

---

## S-01. Single Responsibility

A selector is responsible only for retrieving domain objects.

Selectors may:

- Retrieve a single object.
- Retrieve collections of objects.
- Apply query filters.
- Apply access restrictions.
- Optimize database queries.

Selectors must not:

- Create objects.
- Modify objects.
- Delete objects.
- Execute business workflows.

---

## S-02. Read-only

Selectors are strictly read-only.

Selectors must never call:

- `save()`
- `create()`
- `update()`
- `delete()`
- `bulk_create()`
- `bulk_update()`
- `update_or_create()`
- or any operation that mutates persisted state.

---

## S-03. Ownership Enforcement

Selectors are responsible for enforcing read access.

Whenever a resource belongs to a user or workspace, selectors must ensure
that only authorized users can retrieve it.

Ownership filtering should be applied before resources are returned.

Selectors representing globally accessible resources must explicitly override
`accessible_queryset()` to define their access policy.

The default behavior of `accessible_queryset`() is restrictive and must not
expose resources without explicit authorization rules.

---

## S-04. Base Queryset

Every selector exposes a base queryset representing all objects of its model.

Subclasses may customize the base queryset to optimize retrieval using
techniques such as:

- `select_related()`
- `prefetch_related()`
- annotations
- ordering

The base queryset must not apply user-specific filtering.

---

## S-05. Accessible Queryset

Selectors expose an accessible queryset representing the subset of resources
visible to a given user.

All retrieval operations (`get()`, `list()`, etc.) must operate on the
accessible queryset rather than directly on the model manager.

---

## S-06. Query Filtering

Filtering logic belongs inside selectors.

Domain-specific filtering must be implemented without duplicating ownership
checks.

Filters should only affect which objects are retrieved.

Filters must never perform business decisions.

---

## S-07. Exception Translation

Selectors translate persistence-layer exceptions into domain exceptions.

Typical translations include:

- missing resource → `ResourceNotFoundError`
- unexpected database failure → `InfrastructureViolationError`

Database-specific exceptions must not leak outside the selector layer.

---

## S-08. No Business Logic

Selectors determine **what data is retrieved**.

They never determine **what should happen**.

Validation, workflows, permissions beyond read access, and business rules
belong in the service layer.

---

## S-09. No Transactions

Selectors must not open or manage database transactions.

Transaction boundaries belong exclusively to services.

---

## S-10. Return Types

Selectors return domain model instances or Django querysets.

Selectors must never return:

- serializers
- HTTP responses
- dictionaries
- DTOs
- presentation objects

---

## S-11. Query Optimization

Selectors are the preferred location for ORM optimization.

Examples include:

- `select_related()`
- `prefetch_related()`
- `only()`
- `defer()`
- annotations
- aggregation

Services should remain unaware of ORM optimization details.

---

## S-12. Consistency

Every selector should expose a consistent public interface whenever applicable.

Typical operations include:

- `get()`
- `list()`

Additional retrieval methods may be added when they represent reusable query
operations for the domain.

---

## S-13. Testing

Selector tests verify:

- resource retrieval
- ownership enforcement
- filtering behavior
- query optimization (when applicable)
- exception translation

Selector tests do not verify business workflows or state mutations.

---

# Implementation Guidelines

The following guidelines describe the project's preferred implementation of
the Selector Contract. They are conventions rather than architectural
requirements.

---

## G-01. Inherit from `BaseSelector`

All selectors should inherit from `BaseSelector` to ensure a consistent public
API, centralized exception handling, and shared ownership enforcement.

---

## G-02. Define Required Configuration

Every selector must define:

- `MODEL`
- `RESOURCE_NAME`
- `LOOKUP_FIELD`

These values describe the selector's target model and retrieval strategy.

---

## G-03. Configure Ownership

Selectors for user-owned resources should define `OWNER_PATH`.

Selectors representing globally accessible resources should explicitly override 
`accessible_queryset()` to document their unrestricted access policy.

---

## G-04. Customize the Base Queryset

Override `base_queryset()` only to improve retrieval efficiency.

Typical customizations include:

- `select_related()`
- `prefetch_related()`
- annotations
- default ordering

Ownership filtering should not be implemented here.

---

## G-05. Implement Domain-specific Filtering

Override `apply_filters()` to implement domain-specific query filtering.

Filtering should build upon the queryset supplied by the base selector and must
not reimplement ownership restrictions.

---

## G-06. Keep Selectors Thin

Selectors should remain lightweight.

Whenever query logic starts involving business decisions, validation,
workflows, or state changes, it belongs in the corresponding service instead.

---

## G-07. Prefer Reusable Query Methods

If multiple services require the same complex retrieval logic, implement it as
a dedicated selector method rather than duplicating ORM queries.

Selectors should become the single source of truth for reusable read
operations.

---

## G-08. Optimize Before Exposing

Selectors should return querysets that are already optimized for their intended
use whenever reasonable.

Consumers should not need to remember additional
`select_related()` or `prefetch_related()` calls to avoid N+1 queries.

---

## G-09. Keep the Public API Consistent

Selectors should expose a predictable interface across the project.

When applicable, prefer the following methods:

- `get()`
- `list()`
- `base_queryset()`
- `accessible_queryset()`
- `apply_filters()`

Additional public methods should represent reusable domain queries rather than
one-off convenience wrappers.
