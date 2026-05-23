# Service Layer Contracts

This document defines the **formal contracts** for service-layer operations.

The purpose is to clearly separate **responsibilities**, define **guarantees**, and establish a consistent standard for behavior across the application.

---

# Global Invariants (All Methods)

The following guarantees hold true after any successful service method call:

* Domain invariants → Model (`full_clean()`, `save()`)
* Many-to-many invariants → Service layer (post-save validation)
* Required many-to-many fields:
  - must be present and non-empty on create
  - must not be empty if provided on update
  - may be omitted on update
* Ownership of related objects must be validated before assignment
* Operations are **atomic** (no partial writes)

---

# create()

## Description

Create a new `Model Instance`.

## Preconditions

* `user` is authenticated
* `context` or in some cases the instance `id`, references a valid information leading to the instance owned by the user
* `validated_data`:
  - has already passed field-level validation by a serializer or a form 
  - contains all required non-M2M fields
  - contains required many-to-many fields (may be empty but will be validated)

## Business Rules

* All required many-to-many fields must be present in `validated_data`
* Required many-to-many fields must not be empty
* All related objects must belong to the user where applicable.
* The target `instance` must belong to the user via series of relations.

## Postconditions

* An `Instance` is created and persisted
* All required `many-to-many` relations are assigned
* The object satisfies all model invariants

## Side Effects

* Database insert (Instance)
* Database insert (M2M relations)

## Failure Guarantees

* No object is created on failure
* No partial many-to-many assignments occur
* Raises `ValidationError` on invalid data or domain violation

---

# update() (Partial Update / PATCH-like)

## Description

Update an existing `object`. Behaves as a partial update and tolerates omitted fields (practical PATCH).

## Preconditions

* Target `object` exists
* Target object belongs to the user
* `validated_data` has already passed field-level validation by a serializer or a form 
* `validated_data` is structurally valid

## Business Rules

* Missing fields are ignored
* Only provided fields are modified
* Required field constraints apply only if the field is explicitly modified
* Provided many-to-many fields must be valid and satisfy ownership constraints
* If required many-to-many fields are provided, they must not be empty
* If omitted, existing values must remain valid
* Required many-to-many fields:
  - must not be empty if provided
  - may be omitted
  - if omitted, existing values must remain valid

## Postconditions

* Object remains in valid state
* Only provided fields are updated
* Unspecified fields remain unchanged
* Provided many-to-many relations are replaced (set semantics)

## Side Effects

* Database update (Instance)
* Database updates (M2M tables)

## Failure Guarantees

* Operation is atomic (all database changes are rolled back on failure)
* Partial updates are allowed

---

# remove()

## Description

Delete an existing `Object`.

## Preconditions

* Target `Object` exists
* Target object belongs to the user


## Postconditions

* `Object` is deleted
* Related many-to-many relations are removed via cascade

## Side Effects

* Database delete operation

## Failure Guarantees

* Operation fails if the object does not belong to the user

---

# Cross-Cutting Rules

## Ownership Enforcement

All operations must ensure:

* Users can only access and modify their own data

---

## Atomicity

All service methods must:

* Run inside a transaction
* Guarantee all-or-nothing behavior

---

## Validation Authority

* Structural validation → Serializer layer
* Domain invariants → Model (`full_clean()`)
* Cross-entity and ownership validation → Service layer

---

## Many-to-Many Constraints

* Required many-to-many fields must not be empty after any operation
* Ownership of related objects must be validated

---

# Design Principle Summary

* **Serializer** → Validates input shape and types
* **Service** → Enforces business rules and orchestrates operations
* **Model** → Enforces domain invariants and data integrity

---

This contract serves as the single source of truth for how `ObjectService` must behave and should guide both implementation and testing.
