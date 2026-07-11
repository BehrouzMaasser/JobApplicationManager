# Model Layer Contract

## Purpose

The Model layer represents persisted domain entities.

Its responsibility is to define the structure of the data and guarantee that every model instance is internally consistent before it is persisted.

Models are the source of truth for entity state and domain invariants.

---

# M-01. Define the Persistence Schema

Models are responsible for defining the persistence structure of an entity.

This includes:

- Database fields
- Relationships
- Field options
- Database indexes
- Database constraints
- Default values
- Enumerations

---

# M-02. Enforce Domain Invariants

Models must enforce invariants that are intrinsic to the entity itself.

A domain invariant is a rule that must always be true for a valid instance, regardless of how it was created (service, Django admin, shell, tests, management commands, etc.).

Examples include:

- Date consistency
- Foreign-key ownership consistency
- Workspace consistency
- Cross-field validation

Domain invariants are implemented through Django model validation (`clean()`).

---

# M-03. Perform Persistence Normalization

Models may normalize their own data before persistence.

Normalization ensures that an entity is stored in a canonical form regardless of where it originated.

Examples include:

- Converting empty strings to `None`
- Converting `None` to an empty string when required by database constraints
- Trimming whitespace
- Normalizing casing when it is an intrinsic property of the field

Normalization must never depend on the current user, request, or workflow.

---

# M-04. Validation Scope

Model validation is limited to data that belongs to the model itself.

This includes:

- Scalar fields
- Foreign-key relationships
- One-to-one relationships
- Cross-field validation

Many-to-many validation is intentionally excluded because the related objects are not available during model validation before persistence.

Validation involving many-to-many relationships is the responsibility of the Service layer.

---

# M-05. Models Do Not Perform Business Workflows

Models must not contain business workflows.

Examples include:

- Creating other models
- Sending emails
- Creating notifications
- Triggering background tasks
- Calling services
- Managing transactions

These responsibilities belong to the Service layer.

---

# M-06. Models Do Not Perform Authorization

Models are independent of the current user.

They must never:

- Check permissions
- Validate resource access
- Determine ownership of the requesting user
- Inspect HTTP requests

Authorization belongs to higher layers.

---

# M-07. Models Do Not Validate Operation Context

Models validate the entity itself, not the operation being performed.

For example, a model must not validate whether:

- The URL hierarchy is correct
- A requested Company belongs to a requested Workspace
- A requested JobApplication belongs to a requested JobPosition supplied by the caller

These are operation-specific validations and belong to the Service layer.

---

# M-08. Exceptions

Models communicate invalid state using Django's `ValidationError`.

The Model layer does not raise service-level exceptions such as:

- `DomainInvariantViolationError`
- `AccessDeniedError`
- `ResourceNotFoundError`

Those exceptions belong to higher architectural layers.

---

# M-09. Testing Responsibilities

Model tests verify only model behavior.

This includes:

- Field definitions
- Constraints
- Validators
- `clean()`
- Persistence normalization
- Convenience properties and methods

Model tests must not verify:

- Authorization
- Business workflows
- Service behavior
- HTTP behavior
- API responses