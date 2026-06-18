# API Documentation

## Overview

The project exposes a REST API built with Django REST Framework.

The API reuses the same services and selectors as the web application.

This ensures consistent behavior across interfaces.

## API Design

The REST API is fully functional and shares the same
service and selector layers used by the web application.

Version 1 follows the ownership hierarchy of the domain
model, resulting in nested resource paths that make
ownership boundaries explicit.

Future versions may introduce flatter resource paths
to improve usability while preserving the same
authorization guarantees.

## Authentication

JWT System

### Authenticate Yourself

- Create an account using the web api first
- Ask for a key using your credentials:

POST api/v1/auth/

```json
{
  "email": "your-email@domain",
  "password": "your-password"
}
```

Response:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MTg5MzM1NSwiaWF0IjoxNzgxODA2OTU1LCJqdGkiOiJlNTNjNjczODZkODQ0YzgzYjQ2OTM4M2M5MTNmNDI0ZCIsInVzZXJfaWQiOiIxIn0.Si3sF5hHDRL6MfPLG_UEpjscEUvsjxSGOgG4TlaMdjY",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgxODkzMzU1LCJpYXQiOjE3ODE4MDY5NTUsImp0aSI6ImI5MGYyZTM5YjM2YjQ2ZDRiODU4MDdkYTM2ODJkYmI4IiwidXNlcl9pZCI6IjEifQ.-9jz1lrZzX-Tc_1rAFPX_6wQdFzygrfoJmSmtjDaQtc"
}
```
- Then use the `Key` in `Header` section for every request:

Header key = Authorization

Header Value = Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgxODkzMzU1LCJpYXQiOjE3ODE4MDY5NTUsImp0aSI6ImI5MGYyZTM5YjM2YjQ2ZDRiODU4MDdkYTM2ODJkYmI4IiwidXNlcl9pZCI6IjEifQ.-9jz1lrZzX-Tc_1rAFPX_6wQdFzygrfoJmSmtjDaQtc


## Design Notes

Version 1 reflects the ownership hierarchy used throughout the application.

Example:

/workspaces/{workspace_id}/companies/{company_id}/...

This structure prioritizes ownership clarity and validation.

## Future Improvements

A Version 2 API is planned.

Goals include:

- Flatter resource paths
- Improved discoverability
- Simpler client integration

## API Example

### Retrieve Workspaces

GET /api/v1/workspaces/

Response:

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

### Retrieve A Specific Workspace

GET api/v1/workspaces/ca97ec00-beb0-4c5e-9ea7-0425ba752a19/

```json
{
  "id": 5,
  "owner": 1,
  "workspace_id": "ca97ec00-beb0-4c5e-9ea7-0425ba752a19",
  "name": "German Jobs",
  "created_at": "2026-06-04T00:29:39.803263Z",
  "updated_at": "2026-06-04T00:29:39.803283Z"
}
```