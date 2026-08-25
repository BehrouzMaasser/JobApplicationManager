# Testing Strategy

## Overview

The project uses automated tests to verify that the implementation behaves according to the architecture and domain contracts.

The test suite is organized around architectural responsibilities rather than attempting to make every test exercise the entire application.

The central principle is:

> Each layer should be tested for what that layer is responsible for.

This prevents tests from merely increasing coverage while failing to verify the actual architectural behavior.

---

## Testing Philosophy

The project follows these principles:

- Business behavior is tested at the Service Layer.
- Query behavior and ownership-aware retrieval are tested at the Selector Layer.
- Persistence constraints and relationships are tested at the Model Layer.
- Transport validation is tested through Forms and Serializers.
- HTTP orchestration and response behavior are tested through Views and ViewSets.
- Shared exception translation is tested at the presentation boundary.
- Tests should verify observable responsibilities rather than duplicate lower-layer implementation details.

---

## Model Tests

Model tests verify persistence-related responsibilities.

Typical coverage includes:

- Field behavior.
- Model relationships.
- Database constraints.
- Uniqueness constraints.
- Default values.
- Persistence integrity.
- Model-level behavior that is explicitly part of the model contract.

Model tests should not become a substitute for Service tests.

Business workflows and application-level invariants belong in Service tests.

---

## Service Tests

Service tests are the primary tests for domain behavior and write operations.

They should verify:

- Creation.
- Updates.
- Deletion.
- Business rules.
- Ownership validation.
- Relationship validation.
- Domain invariants.
- Transactional behavior.
- Correct exception types.
- Correct behavior on invalid domain state.

### M2M Ownership Invariants

Special attention is required for reusable user-owned M2M resources such as:

- Job Requirements.
- Job Tasks.
- Job Benefits.

The tests must distinguish between:

```text
Direct resource access
    → Selector
    → 404-oriented resource lookup failure
```

and:

```text
Supplying another user's resource to a write operation
    → Service
    → Domain invariant violation
```

The latter is not a resource-access test. It verifies that the Service protects a domain invariant even if an invalid object reaches it.

---

## Selector Tests

Selector tests verify read behavior.

They should cover:

- Resource retrieval.
- Collection retrieval.
- Ownership filtering.
- Filtering behavior.
- Lookup failures.
- Query composition.
- Query optimization where optimization is part of the selector's contract.

Selectors should not be tested for business workflows or state mutations because those responsibilities belong to Services.

A simple `list()` operation that only constructs and evaluates an ownership-aware queryset does not need artificial exception tests for exceptions it cannot reasonably produce under normal operation.

---

## Form Tests

Form tests verify transport-specific HTML input behavior.

Typical tests include:

- Required fields.
- Field types.
- Formatting.
- Input normalization.
- Invalid transport input.
- Valid cleaned data.
- User-facing validation errors.

Forms may restrict selectable querysets for presentation purposes. For example, a Job Position form can populate M2M fields using selectors scoped to the current request user so that users are not presented with another user's requirements, tasks, or benefits.

That presentation filtering does not replace Service-level domain invariant validation.

Forms should not be relied upon as the final ownership boundary.

---

## Serializer Tests

Serializer tests verify REST transport behavior.

Typical tests include:

- Required fields.
- Deserialization.
- Serialization.
- Field validation.
- Input normalization.
- Transport-specific constraints.
- Representation of valid domain objects.

Serializers do not need to reproduce Service ownership or business-rule tests.

A serializer accepting an identifier does not imply that the serializer owns the domain authorization decision.

---

## Django View Tests

Django View tests verify presentation orchestration.

They should cover, where applicable:

- Authentication requirements.
- Correct HTTP methods.
- Context resolution.
- Form construction.
- Form validation.
- Selector invocation.
- Service invocation.
- Redirects.
- Template rendering.
- Success messages.
- Validation error presentation.
- Application exception translation.
- Appropriate HTTP responses.

View tests should not reproduce the complete business-rule matrix already covered by Service tests.

---

## DRF ViewSet / API Tests

API tests verify the observable API contract.

They should cover:

- Authentication requirements.
- HTTP methods.
- URL routing.
- Request validation.
- Serialization.
- Selector/Service orchestration.
- Response status codes.
- Response structure.
- Pagination where applicable.
- Filtering where applicable.
- Ownership boundaries.
- Exception translation.

The API tests should demonstrate that the REST interface correctly exposes the Application Layer without reimplementing its business logic.

---

## Exception Handler Tests

Exception handler tests verify translation between application/framework failures and transport responses.

They should verify at least:

### ResourceNotFoundError

```text
ResourceNotFoundError
        ↓
HTTP 404
```

### BusinessRuleViolationError

```text
BusinessRuleViolationError
        ↓
HTTP 400
```

### DomainInvariantViolationError

```text
DomainInvariantViolationError
        ↓
HTTP 400
```

### InfrastructureViolationError

```text
InfrastructureViolationError
        ↓
HTTP 500
```

### Django ValidationError

```text
ValidationError
        ↓
HTTP 400
```

### Framework Exceptions

Unhandled DRF framework exceptions should continue through DRF's standard exception machinery and be represented using the project's normalized API error response.

The handler must not expose internal infrastructure details to clients.

---

## Architectural Contract Tests

Where useful, tests should verify architectural boundaries themselves.

Examples:

- Views do not perform direct model writes.
- Services own write operations.
- Selectors own read operations.
- Forms and serializers do not become alternate business-rule implementations.
- Application exceptions are translated consistently.
- Ownership boundaries are enforced at the correct layer.

These tests are valuable when a regression could silently violate the architecture even though the feature still appears to work.

---

## Integration vs Unit Tests

Both levels have a purpose.

### Unit-oriented tests

Use isolation when the goal is to verify one component's behavior independently.

Examples:

- Service validation logic.
- Selector query construction.
- Exception translation.
- Form validation.

### Integration-oriented tests

Use real application components when the goal is to verify that multiple layers work together correctly.

Examples:

- A View invoking a real Service and persisting a record.
- An API request passing through authentication, serializer, Service, and persistence.
- A Selector enforcing ownership against real database records.

The test suite should not maximize one style at the expense of the other.

---

## Test Quality Standard

A test is valuable when its failure tells us something meaningful.

Tests should:

- Verify a documented responsibility.
- Fail when the intended behavior is broken.
- Avoid asserting irrelevant implementation details.
- Avoid duplicating another layer's responsibility.
- Use realistic domain scenarios.
- Explicitly test security-sensitive ownership boundaries.
- Prefer clear test names that describe behavior.

A large test count is not, by itself, evidence of quality.

Likewise, code coverage is a diagnostic metric, not a substitute for meaningful behavioral coverage.

---

## Running the Test Suite

Run the full suite with:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=apps --cov-report=term-missing
```

The exact number of tests and coverage percentage are intentionally not documented here because they change as the codebase evolves.

Before considering the project complete, the full test suite should pass and the final coverage report should be reviewed for meaningful gaps rather than judged by a fixed percentage alone.
