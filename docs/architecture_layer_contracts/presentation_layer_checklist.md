# Presentation Layer Checklist

Every Presentation Layer component should satisfy the following checklist before
being considered complete.

## General

- [ ] The component only implements presentation responsibilities.
- [ ] Business logic is delegated to the Application Layer.
- [ ] Architectural boundaries are respected.

## Read Operations

- [ ] Read operations are delegated to Selectors.
- [ ] Reusable query logic is not implemented in the Presentation Layer.
- [ ] Presentation-specific filtering, ordering, or pagination does not duplicate Selector responsibilities.

## Write Operations

- [ ] Write operations are delegated to Services.
- [ ] The Presentation Layer does not call `save()`, `delete()`, `create()`, or other ORM write operations directly.
- [ ] The required Context object is constructed before invoking the Service.

## Forms

- [ ] Forms perform transport-level validation only.
- [ ] Business validation is delegated to the Service Layer.
- [ ] Forms do not perform persistence operations.

## Django Views

- [ ] Authentication is enforced where required.
- [ ] Authorization is enforced where required.
- [ ] Forms are validated before invoking Services.
- [ ] Templates or redirects are generated appropriately.
- [ ] User-facing success and error messages are handled consistently.

## Exception Handling

- [ ] Application exceptions are translated into appropriate presentation responses.
- [ ] Internal implementation details are not exposed to end users.
- [ ] Exception handling follows the project's shared exception handling mechanism.

## Testing

- [ ] Presentation tests verify presentation behavior only.
- [ ] Business behavior is verified by Service tests.
- [ ] View tests verify Selector and Service orchestration.
- [ ] Form tests verify transport validation only.

