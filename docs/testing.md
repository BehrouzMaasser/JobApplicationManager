# Testing Strategy

## Overview

The project places a strong emphasis on automated testing.

The architecture was intentionally designed to improve testability by separating:

- Business logic
- Query logic
- Presentation logic

This allows each layer to be tested independently.

## Testing Philosophy

The project follows three principles:

- Business rules should be testable without HTTP requests.
- Query logic should be testable independently from views.
- API and web interfaces should share the same domain behavior.

## Test Categories

### Model Tests

Verify:

- Constraints
- Relationships
- Database integrity

### Service Tests

Verify:

- Business rules
- Ownership validation
- Transactional behavior

### Selector Tests

Verify:

- Query filtering
- Ownership boundaries
- Retrieval behavior

### Form Tests

Verify:

- Input validation
- User-facing validation rules

### View Tests

Verify:

- Authentication
- Permissions
- Response rendering

### API Tests

Verify:

- Serialization
- Endpoint behavior
- Permissions
- Integration with services

## Current Metrics

- 581 tests
- 94% code coverage

## Running Tests

```bash
pytest .
```

## Coverage

```bash
pytest --cov=apps --cov-report=term-missing
```