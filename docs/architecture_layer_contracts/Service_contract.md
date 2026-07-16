# Service Contract

## Purpose

A service encapsulates a write use-case of the domain.

Services are responsible for coordinating business operations, enforcing
business invariants, validating business rules, and persisting model
changes.

Services are the only layer responsible for mutating domain models.

Services coordinate business operations, enforce business invariants, delegate
entity validation to models, and persist changes.

---

# Responsibilities

A service is responsible for:

- Resolving aggregates and parent dependencies.
- Validating cross-aggregate relationships.
- Enforcing business rules.
- Validating ownership of related objects.
- Creating, updating and deleting model instances.
- Delegating model validation to `Model.full_clean()`.
- Persisting changes.

A service is **not** responsible for:

- Querying collections (Selectors).
- Authentication.
- Serialization.
- HTTP concerns.
- Business-independent model validation.

---

# Service Configuration

Every concrete service must define:

- `MODEL`
- `SELECTOR`
- `CREATE_FIELDS`
- `SCALAR_UPDATABLE_FIELDS`
- `M2M_UPDATABLE_FIELDS`
- `REQUIRED_M2M_FIELDS`
- `NON_EMPTY_M2M_FIELDS`
- `M2M_OWNER_FIELD_MAP`

These configuration values describe how the generic write workflow
operates for the concrete aggregate.

---

# Public API

Every service exposes three write operations:

- `create(...)`
- `update(...)`
- `remove(...)`

These methods define the public write API of the aggregate.

---

# Lifecycle

## Create

The create workflow executes in the following order:

1. Resolve creation dependencies.
2. Build the model instance.
3. Execute create-specific business validations.
4. Execute common pre-save validations.
5. Call `full_clean()`.
6. Persist the model.
7. Apply many-to-many relationships.
8. Validate required non-empty many-to-many relations.

---

## Update

The update workflow executes in the following order:

1. Resolve the target aggregate.
2. Validate the resolved aggregate against the supplied context.
3. Execute update-specific business validations.
4. Execute common pre-save validations.
5. Apply scalar field updates.
6. Call `full_clean()`.
7. Persist the model.
8. Apply many-to-many updates.
9. Validate required non-empty many-to-many relations.

---

# Instance Lifecycle

The model instance passed to service hooks is not always in the same
state.

Understanding the lifecycle of the instance is important when extending
`BaseService`.

| Hook | Instance State |
|------|----------------|
| `_build_model()` | A new model instance has been constructed in memory. It has **not** been validated or persisted. |
| `_create_validate()` | A new model instance exists in memory. It has **not** been validated or persisted. This hook should only validate create-specific business rules. |
| `_resolve_instance()` | A persisted model instance has been retrieved from the database. No modifications have been applied. |
| `_validate_resolved_instance()` | Receives the persisted instance returned by the selector. The instance is unchanged and should only be validated against the supplied context. |
| `_update_validate()` | Receives the persisted instance before any scalar updates have been applied. This hook should validate whether the requested update is allowed. |
| `_apply_scalar_updates()` | Applies scalar field updates **in memory only**. The instance has not yet been validated or saved. |
| `_save()` | Validates the instance using `full_clean()` and persists it. After this method returns successfully, the instance is synchronized with the database. |
| `_create_post_save()` | Receives a persisted instance. Many-to-many relations may safely be created or modified. |
| `_update_post_save()` | Receives a persisted instance after scalar updates have been saved. Many-to-many relations may safely be synchronized. |
| `_add_m2m_fields()` | Receives a persisted instance. Used only during creation to add many-to-many relations. |
| `_apply_m2m_updates()` | Receives a persisted instance. Used only during updates to synchronize many-to-many relations. |
| `_m2m_non_empty_validation()` | Receives a persisted instance with its many-to-many relations already applied. Validates that configured many-to-many relations are not empty. |

## Hook Guidelines

When implementing or overriding service hooks:

- Do not assume the instance has been persisted unless the lifecycle
  explicitly states so.
- Do not access many-to-many relationships before the instance has been
  saved.
- Do not call full_clean() or duplicate model validation inside service hooks.
  is delegated to `Model.full_clean()` through `_save()`.
- Business validation hooks should validate domain rules but should not
  persist changes.
- Field mutation should occur only through the provided helper methods
  (`_apply_scalar_updates()`, `_add_m2m_fields()`,
  `_apply_m2m_updates()`).

---

## Remove

The remove workflow executes in the following order:

1. Resolve the target aggregate.
2. Validate the resolved aggregate against the supplied context.
3. Delete the aggregate.

---

# Validation Responsibilities

A service enforces four kinds of validation.

## Domain relationship validation

Services validate that all supplied objects belong to the expected
aggregate hierarchy.

Examples include:

- Company belongs to Workspace.
- Job Position belongs to Company.
- Job Application belongs to Job Position.
- Context identifiers refer to the same aggregate.

---

## Business rule validation

Services enforce business rules that are independent of model
validation.

Examples include:

- Required many-to-many fields are supplied.
- Required many-to-many relations are not empty.
- Domain-specific workflow restrictions.

---

## Ownership validation

Services ensure that every supplied related object belongs to the
current user whenever ownership validation is configured.

---

## Model validation

Services delegate model validation to

```python
instance.full_clean()
```

Services must not duplicate model validation logic.

---

# Extension Points

Concrete services may override the following hooks when additional
behavior is required.

## `_resolve_create_dependencies()`

Resolve any related aggregates required during creation.

The default implementation returns empty dictionary `{}`.

---

## `_create_validate()`

Execute business validations specific to the create operation.

The default implementation performs no additional validation.

---

## `_update_validate()`

Execute business validations specific to the update operation.

The default implementation performs no additional validation.

---

## `_validate_resolved_instance()`

Validate that the resolved aggregate matches the supplied context.

Typical validations include checking parent-child relationships across
aggregate boundaries.

The default implementation performs no additional validation, although
most services are expected to override it.

---

# Exception Contract

Services may raise the following exceptions.

## ValidationError

Raised by `Model.full_clean()` when the model contract is violated.

Examples include:

- Missing required fields.
- Invalid field values.
- Uniqueness violations.
- Model-level validation errors.

---

## BusinessRuleViolationError

Raised when a business rule prevents the requested operation.

Examples include:

- Required many-to-many fields were not supplied.
- Required many-to-many relations are empty.
- Workflow-specific restrictions.

---

## DomainInvariantViolationError

Raised when supplied objects violate aggregate or ownership
relationships.

Examples include:

- Aggregate hierarchy mismatch.
- Workspace mismatch.
- Related object belongs to another aggregate.
- Related object is not owned by the current user.

---

## InfrastructureViolationError

Raised when an unexpected infrastructure failure prevents the service from
completing.

Examples include:

- database failures
- unexpected ORM errors
- invalid framework state
- unexpected runtime failures originating from the persistence layer

Services should translate unexpected persistence exceptions into
`InfrastructureViolationError` rather than allowing framework-specific
exceptions to propagate outside the service layer.

---

## Selector Exceptions

Services propagate exceptions raised by selectors, including:

- Aggregate not found.
- Access denied.

Services should not catch selector exceptions unless translating them
into a more specific domain exception.

---

# Design Rules

A service should:

- Contain business logic.
- Modify a single aggregate root.
- Delegate reads to selectors.
- Delegate model validation to models.
- Be deterministic for identical inputs.
- Avoid persistence logic outside the provided workflow hooks.

A service should not:

- Perform collection queries.
- Duplicate model validation.
- Contain HTTP-specific logic.
- Access the database directly when a selector already provides the
  required query.