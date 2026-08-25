# Exception Contract

The application distinguishes failures by semantic responsibility rather than by the framework exception that happens to occur underneath.

## ResourceNotFoundError

Represents a resource that cannot be resolved through the caller's access-scoped Selector. This includes resources that exist but are not accessible to the caller.

Presentation result:

- Django: HTTP 404
- DRF: HTTP 404

The project intentionally does not expose a separate access-denied application exception for resource ownership.

## BusinessRuleViolationError

Represents a legitimate business rule preventing an otherwise valid operation.

Examples include operation-specific business restrictions or required many-to-many conditions.

Presentation behavior:

- Django: handled as a form/service validation error where appropriate.
- DRF: HTTP 400.

## DomainInvariantViolationError

Represents a violation of a domain invariant detected while processing a write operation.

This includes supplied related objects that do not satisfy the required ownership or aggregate relationship.

Example:

```text
User submits a JobTask belonging to another user
        ↓
Service validates the supplied relation
        ↓
DomainInvariantViolationError
        ↓
HTTP 400
```

This differs from `ResourceNotFoundError`: the latter concerns access to the requested resource itself, while this exception concerns data supplied to a write operation.

## InfrastructureViolationError

Represents unexpected failures currently grouped under the project's broad infrastructure category.

The category may currently include:

- Database failures
- Unexpected ORM failures
- Framework/infrastructure failures
- Programming/runtime failures treated as infrastructure failures by the application

This category is intentionally broad for the current project and may be refined later.

Presentation result:

- Django: HTTP 500
- DRF: HTTP 500

Internal details must be logged rather than exposed to the client.

## Django ValidationError

`django.core.exceptions.ValidationError` represents invalid model state detected by model validation. Services delegate intrinsic model validation to `Model.full_clean()`.

## Exception Mapping

```text
ResourceNotFoundError
        ↓
      HTTP 404

BusinessRuleViolationError
        ↓
   Form error / HTTP 400

DomainInvariantViolationError
        ↓
      HTTP 400

InfrastructureViolationError
        ↓
      HTTP 500
```
