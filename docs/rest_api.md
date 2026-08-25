# REST API Documentation

## Overview

The project exposes a REST API built with Django REST Framework.

The API shares the same Application Layer as the server-rendered web application:

```text
REST API
   │
   ├── Selectors ── reads
   │
   └── Services ── writes
```

This keeps domain behavior independent of the transport mechanism.

The current API is versioned under:

```text
/api/v1/
```

---

## Authentication

The REST API uses JWT authentication through `djangorestframework-simplejwt`.

API authentication is configured globally with:

- `JWTAuthentication`
- `IsAuthenticated`

Therefore, API endpoints require an authenticated user unless an endpoint explicitly defines different behavior.

### Obtain Tokens

The token endpoint is:

```text
POST /api/v1/auth/
```

Request body:

```json
{
  "email": "your-email@domain",
  "password": "your-password"
}
```

The response contains an access token and a refresh token.

Example shape:

```json
{
  "refresh": "<refresh-token>",
  "access": "<access-token>"
}
```

Use the access token for authenticated API requests:

```text
Authorization: Bearer <access-token>
```

### Refresh an Access Token

The refresh endpoint is:

```text
POST /api/v1/auth/refresh/
```

Request body:

```json
{
  "refresh": "<refresh-token>"
}
```

The API returns a new access token.

The configured token lifetimes are:

- Access token: 1 day
- Refresh token: 1 day

---

## URL Structure

Version 1 exposes both **flat** and **nested** resources.

### Flat Resources

The following resources are registered through DRF's `DefaultRouter`:

```text
/api/v1/workspaces/
/api/v1/companies/
/api/v1/company-notes/
/api/v1/company-emails/
/api/v1/job-benefits/
/api/v1/job-tasks/
/api/v1/job-requirements/
/api/v1/job-positions/
/api/v1/job-applications/
/api/v1/job-application-notes/
/api/v1/document-types/
/api/v1/documents/
```

The standard ViewSet actions are exposed according to the router configuration, including list, retrieve, create, update, partial update, and destroy where implemented by the corresponding ViewSet.

### Nested Resources

Some resources also expose nested URLs so that their parent ownership context is explicit.

Companies:

```text
/api/v1/workspaces/{workspace_id}/companies/
/api/v1/workspaces/{workspace_id}/companies/{id}/
```

Company notes:

```text
/api/v1/workspaces/{workspace_id}/companies/{company_id}/company-notes/
/api/v1/workspaces/{workspace_id}/companies/{company_id}/company-notes/{id}/
```

Company emails:

```text
/api/v1/workspaces/{workspace_id}/companies/{company_id}/company-emails/
/api/v1/workspaces/{workspace_id}/companies/{company_id}/company-emails/{id}/
```

Job positions:

```text
/api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/
/api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{id}/
```

Job applications:

```text
/api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/job-applications/
/api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/job-applications/{id}/
```

Job application notes:

```text
/api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/job-applications/{job_application_id}/job-application-notes/
/api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/job-applications/{job_application_id}/job-application-notes/{id}/
```

Nested endpoints are primarily useful when the parent relationship is part of the operation's context.

---

## Ownership and Access

Authentication establishes the identity of the caller. Application-layer components enforce ownership boundaries.

Selectors are responsible for read-side ownership-aware retrieval.

Services are responsible for ownership validation and domain invariants during write operations.

The API intentionally does not expose a separate `AccessDeniedError` application exception.

When a user attempts to retrieve a resource outside their accessible ownership boundary, the application treats the resource as unavailable and returns the normal resource-not-found response.

For example:

```text
User A requests User B's company
             ↓
        Selector lookup
             ↓
       Resource not found
             ↓
        HTTP 404
```

This avoids revealing whether another user's resource exists.

### M2M Ownership During Writes

For resources such as Job Requirements, Job Tasks, and Job Benefits, there is an additional domain invariant.

The API may receive identifiers for these resources as part of a Job Position write operation. The Service verifies that the supplied objects belong to the current user before assigning them.

This is different from direct resource access:

```text
Direct GET of another user's requirement
        → 404 Not Found

Using another user's requirement in a job-position write
        → Domain invariant violation
        → HTTP 400
```

The distinction is intentional and documented in the domain and Service contracts.

---

## Request Validation

Serializers are responsible for transport-level validation, including:

- Required fields
- Field types
- Formatting
- Transport-specific constraints
- Deserialization

They do not own domain business rules or ownership enforcement.

After serializer validation succeeds, write operations are delegated to Services.

---

## API Error Handling

The project uses a custom DRF exception handler.

Application exceptions are translated into a consistent API envelope.

### Resource Not Found

```json
{
  "error": {
    "code": "resource_not_found",
    "message": "...",
    "details": {}
  }
}
```

Status:

```text
404 Not Found
```

### Business Rule Violation

Business-rule failures are returned as HTTP 400 responses.

The response preserves the service-provided message and details.

### Domain Invariant Violation

Domain invariant failures are treated as bad requests at the API boundary.

Status:

```text
400 Bad Request
```

The response does not expose internal implementation details.

### Infrastructure Failure

Infrastructure failures are translated into a generic HTTP 500 response.

Internal details are logged server-side rather than exposed to the client.

### Django Validation Errors

Django `ValidationError` instances are translated into a 400 response containing validation details.

### DRF Framework Exceptions

Exceptions not handled by the application's custom mappings are passed to DRF's standard exception handler and then normalized into the project's API error envelope.

---

## Pagination

The API uses the project's configured default pagination class.

The configured page size is:

```text
20
```

Paginated responses follow the standard project pagination representation.

Example shape:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": []
}
```

---

## Filtering

The API enables Django Filter's REST framework backend globally.

Endpoint-specific filtering depends on the corresponding ViewSet and selector implementation.

Transport-level filtering should remain presentation-oriented. Domain-specific filtering belongs in the Application Layer.

---

## Example

### Retrieve Workspaces

```text
GET /api/v1/workspaces/
```

A successful response has the general shape:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 5,
      "owner": 1,
      "workspace_id": "ca97ec00-beb0-4c5e-9ea7-0425ba752a19",
      "name": "German Jobs",
      "created_at": "2026-06-04T00:29:39.803263Z",
      "updated_at": "2026-06-04T00:29:39.803283Z"
    }
  ]
}
```

The exact serialized fields are defined by the corresponding serializer and may evolve with the API version.

---

## API Versioning

The current API is Version 1.

Version 1 intentionally contains both flat and nested resource access.

A future Version 2 may simplify resource paths or otherwise improve client ergonomics. Such changes should preserve the same ownership and domain guarantees.

The existence of a future Version 2 is not a current implementation requirement.

---

## Design Principles

The API follows these principles:

1. Authentication identifies the caller.
2. Selectors own read-side retrieval and ownership filtering.
3. Services own writes and domain behavior.
4. Serializers handle transport validation and representation.
5. Application exceptions are translated consistently at the API boundary.
6. Internal implementation details are not exposed to clients.
