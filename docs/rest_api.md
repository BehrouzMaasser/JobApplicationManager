# REST API

## 1. Overview

The project provides a versioned REST API built with Django REST Framework.

The current API version is **V1** and is available under:

```text
/api/v1/
```

The API provides two ways to access resources:

1. **Flat endpoints** — used for general resource access. Every resource exposes flat `list` and `retrieve` endpoints. Some resources also expose write operations.
2. **Nested endpoints** — used for resources whose operations are performed in the context of a parent resource. These endpoints expose the full CRUD lifecycle for those resources.

The API is authenticated. Requests must be made by an authenticated user, and resources are restricted to the user's accessible data.

---

# 2. API conventions

## 2.1 Base URL

All V1 endpoints start with:

```text
/api/v1/
```

For example:

```http
GET /api/v1/companies/
```

---

## 2.2 HTTP methods

The API uses standard HTTP methods:

| Method   | Purpose                                |
| -------- | -------------------------------------- |
| `GET`    | Retrieve a list or individual resource |
| `POST`   | Create a resource                      |
| `PUT`    | Replace/update a resource              |
| `PATCH`  | Partially update a resource            |
| `DELETE` | Delete a resource                      |

The available methods depend on the endpoint.

---

## 2.3 List vs. detail endpoints

A collection endpoint does not contain a resource ID:

```http
GET /api/v1/companies/
```

A detail endpoint contains the resource ID:

```http
GET /api/v1/companies/{company_id}/
```

The same distinction applies to nested endpoints.

Collection:

```http
GET /api/v1/workspaces/{workspace_id}/companies/
```

Detail:

```http
GET /api/v1/workspaces/{workspace_id}/companies/{company_id}/
```

---

# 3. Flat endpoints

Flat endpoints provide direct access to resources without requiring their parent resources in the URL.

Every resource has flat `list` and `retrieve` endpoints.

Some resources also support create, update, partial update, and delete operations through their flat endpoint.

## 3.1 Flat endpoint rules

Use a flat endpoint when:

* you already know the resource ID and want to retrieve it;
* you want to list resources without expressing a parent relationship in the URL;
* you want to use the available query-parameter filters;
* the resource supports flat write operations.

Flat endpoints do **not** all provide full CRUD.

---

# 4. Flat API reference

| Resource             | Collection endpoint              | Detail endpoint                       | Available methods                       |
| -------------------- | -------------------------------- | ------------------------------------- | --------------------------------------- |
| Workspace            | `/api/v1/workspaces/`            | `/api/v1/workspaces/{id}/`            | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Company              | `/api/v1/companies/`             | `/api/v1/companies/{id}/`             | `GET`                                   |
| Company Note         | `/api/v1/company-notes/`         | `/api/v1/company-notes/{id}/`         | `GET`                                   |
| Company Email        | `/api/v1/company-emails/`        | `/api/v1/company-emails/{id}/`        | `GET`                                   |
| Job Benefit          | `/api/v1/job-benefits/`          | `/api/v1/job-benefits/{id}/`          | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Job Task             | `/api/v1/job-tasks/`             | `/api/v1/job-tasks/{id}/`             | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Job Requirement      | `/api/v1/job-requirements/`      | `/api/v1/job-requirements/{id}/`      | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Job Position         | `/api/v1/job-positions/`         | `/api/v1/job-positions/{id}/`         | `GET`                                   |
| Job Application      | `/api/v1/job-applications/`      | `/api/v1/job-applications/{id}/`      | `GET`                                   |
| Job Application Note | `/api/v1/job-application-notes/` | `/api/v1/job-application-notes/{id}/` | `GET`                                   |
| Document Type        | `/api/v1/document-types/`        | `/api/v1/document-types/{id}/`        | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |
| Document             | `/api/v1/documents/`             | `/api/v1/documents/{id}/`             | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` |

Resources that only expose `GET` through their flat endpoints use nested endpoints for their write operations.

---

# 5. Nested endpoints

Nested endpoints represent a resource in the context of its parent resource.

They are used when the relationship between resources is important to the operation.

For example, a company belongs to a workspace.

Instead of creating a company through:

```http
POST /api/v1/companies/
```

the API creates it through:

```http
POST /api/v1/workspaces/{workspace_id}/companies/
```

The parent resource is therefore part of the URL.

Nested endpoints provide the full CRUD lifecycle for the resources listed below.

---

# 6. Nested API reference

## 6.1 Companies

Companies belong to a workspace.

### Collection

```http
GET    /api/v1/workspaces/{workspace_id}/companies/
POST   /api/v1/workspaces/{workspace_id}/companies/
```

### Detail

```http
GET    /api/v1/workspaces/{workspace_id}/companies/{company_id}/
PUT    /api/v1/workspaces/{workspace_id}/companies/{company_id}/
PATCH  /api/v1/workspaces/{workspace_id}/companies/{company_id}/
DELETE /api/v1/workspaces/{workspace_id}/companies/{company_id}/
```

---

## 6.2 Company Notes

Company notes belong to a company.

### Collection

```http
GET    /api/v1/workspaces/{workspace_id}/companies/{company_id}/company-notes/
POST   /api/v1/workspaces/{workspace_id}/companies/{company_id}/company-notes/
```

### Detail

```http
GET    /api/v1/workspaces/{workspace_id}/companies/{company_id}/company-notes/{id}/
PUT    /api/v1/workspaces/{workspace_id}/companies/{company_id}/company-notes/{id}/
PATCH  /api/v1/workspaces/{workspace_id}/companies/{company_id}/company-notes/{id}/
DELETE /api/v1/workspaces/{workspace_id}/companies/{company_id}/company-notes/{id}/
```

---

## 6.3 Company Emails

Company emails belong to a company.

### Collection

```http
GET    /api/v1/workspaces/{workspace_id}/companies/{company_id}/company-emails/
POST   /api/v1/workspaces/{workspace_id}/companies/{company_id}/company-emails/
```

### Detail

```http
GET    /api/v1/workspaces/{workspace_id}/companies/{company_id}/company-emails/{id}/
PUT    /api/v1/workspaces/{workspace_id}/companies/{company_id}/company-emails/{id}/
PATCH  /api/v1/workspaces/{workspace_id}/companies/{company_id}/company-emails/{id}/
DELETE /api/v1/workspaces/{workspace_id}/companies/{company_id}/company-emails/{id}/
```

---

## 6.4 Job Positions

Job positions belong to a company.

### Collection

```http
GET    /api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/
POST   /api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/
```

### Detail

```http
GET    /api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{id}/
PUT    /api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{id}/
PATCH  /api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{id}/
DELETE /api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{id}/
```

---

## 6.5 Job Applications

Job applications belong to a job position.

### Collection

```http
GET
/api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/job-applications/

POST
/api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/job-applications/
```

### Detail

```http
GET
/api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/job-applications/{id}/

PUT
/api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/job-applications/{id}/

PATCH
/api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/job-applications/{id}/

DELETE
/api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/job-applications/{id}/
```

---

## 6.6 Job Application Notes

Job application notes belong to a job application.

### Collection

```http
GET
/api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/job-applications/{job_application_id}/job-application-notes/

POST
/api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/job-applications/{job_application_id}/job-application-notes/
```

### Detail

```http
GET
/api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/job-applications/{job_application_id}/job-application-notes/{id}/

PUT
/api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/job-applications/{job_application_id}/job-application-notes/{id}/

PATCH
/api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/job-applications/{job_application_id}/job-application-notes/{id}/

DELETE
/api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/job-applications/{job_application_id}/job-application-notes/{id}/
```

---

# 7. Choosing between flat and nested endpoints

The API provides both flat and nested access intentionally.

A useful rule is:

```text
Need to read a resource?
    ↓
Use the flat endpoint.

Need to list resources within a known parent?
    ↓
Use the nested endpoint.

Need to create/update/delete a resource that is managed
through a parent?
    ↓
Use the nested endpoint.

Need to create/update/delete a resource with its own
top-level API lifecycle?
    ↓
Use its flat endpoint.
```

For example, to retrieve a company:

```http
GET /api/v1/companies/{company_id}/
```

To retrieve companies belonging to a particular workspace:

```http
GET /api/v1/workspaces/{workspace_id}/companies/
```

To create a company in a workspace:

```http
POST /api/v1/workspaces/{workspace_id}/companies/
```

To update that company:

```http
PATCH /api/v1/workspaces/{workspace_id}/companies/{company_id}/
```

---

# 8. Filtering

Filtering is available on selected **flat list endpoints**.

Filters are supplied as query parameters:

```text
/api/v1/<resource>/?<parameter>=<value>
```

Filtering is performed by the API's selector/query-filter layer.

The supported parameters are endpoint-specific.

---

## 8.1 Company filters

```http
GET /api/v1/companies/?workspace_id={workspace_id}
```

Supported parameter:

| Parameter      | Description                       |
| -------------- | --------------------------------- |
| `workspace_id` | Restrict companies to a workspace |

---

## 8.2 Company Note filters

```http
GET /api/v1/company-notes/?workspace_id={workspace_id}&company_id={company_id}
```

Supported parameters:

| Parameter      | Description                   |
| -------------- | ----------------------------- |
| `workspace_id` | Restrict notes to a workspace |
| `company_id`   | Restrict notes to a company   |

Parameters can be combined.

---

## 8.3 Company Email filters

```http
GET /api/v1/company-emails/?workspace_id={workspace_id}&company_id={company_id}
```

Supported parameters:

| Parameter      | Description                    |
| -------------- | ------------------------------ |
| `workspace_id` | Restrict emails to a workspace |
| `company_id`   | Restrict emails to a company   |

---

## 8.4 Job Position filters

```http
GET /api/v1/job-positions/?workspace_id={workspace_id}&company_id={company_id}
```

Supported parameters:

| Parameter      | Description                       |
| -------------- | --------------------------------- |
| `workspace_id` | Restrict positions to a workspace |
| `company_id`   | Restrict positions to a company   |

---

## 8.5 Job Application filters

Job applications support several filters:

```http
GET /api/v1/job-applications/
    ?workspace_id={workspace_id}
    &company_id={company_id}
    &job_position_id={job_position_id}
    &status_id={status_id}
    &date_applied={date}
```

Supported parameters:

| Parameter         | Description                               |
| ----------------- | ----------------------------------------- |
| `workspace_id`    | Restrict applications to a workspace      |
| `company_id`      | Restrict applications to a company        |
| `job_position_id` | Restrict applications to a job position   |
| `status_id`       | Restrict applications to a status         |
| `date_applied`    | Restrict applications by application date |

Multiple filters can be combined.

For example:

```http
GET /api/v1/job-applications/?workspace_id=1&status_id=2
```

returns applications matching both conditions.

---

## 8.6 Job Application Note filters

```http
GET /api/v1/job-application-notes/
    ?workspace_id={workspace_id}
    &company_id={company_id}
    &job_position_id={job_position_id}
    &job_application_id={job_application_id}
```

Supported parameters:

| Parameter            | Description                         |
| -------------------- | ----------------------------------- |
| `workspace_id`       | Restrict notes to a workspace       |
| `company_id`         | Restrict notes to a company         |
| `job_position_id`    | Restrict notes to a job position    |
| `job_application_id` | Restrict notes to a job application |

---

## 8.7 Document filters

Documents can be filtered by document type:

```http
GET /api/v1/documents/?document_type={document_type_id}
```

Supported parameter:

| Parameter       | Description                           |
| --------------- | ------------------------------------- |
| `document_type` | Restrict documents to a document type |

---

# 9. Nested URLs as contextual scoping

A nested URL does more than provide a different URL format. It expresses the parent-child context of the requested operation.

For example:

```http
GET /api/v1/workspaces/10/companies/20/job-positions/
```

means:

> List job positions associated with company `20` in workspace `10`.

Similarly:

```http
POST /api/v1/workspaces/10/companies/20/job-positions/
```

means:

> Create a job position in company `20` within workspace `10`.

The same parent context is used for updates and deletes:

```http
PATCH /api/v1/workspaces/10/companies/20/job-positions/30/
DELETE /api/v1/workspaces/10/companies/20/job-positions/30/
```

This makes nested URLs the preferred interface for CRUD operations on child resources.

---

# 9.1 Nested detail endpoints and resource lookup

Nested detail endpoints contain the complete parent hierarchy in the URL. However, the parent identifiers are not used as additional lookup conditions when retrieving an individual resource.

For example:

```http
GET /api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/
```

The `job_position_id` identifies the resource to retrieve.

The API retrieves the resource using its own ID together with the authenticated user's resource ownership. The `workspace_id` and `company_id` in the URL do not independently determine whether the resource is returned.

Therefore, a nested detail URL should be understood as:

```text
parent hierarchy + resource ID
            ↓
      identify the operation
```

rather than:

```text
parent hierarchy + resource ID
            ↓
require the resource to match every parent ID
```

This differs from nested collection endpoints.

For a nested collection:

```http
GET /api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/
```

the parent identifiers are used to scope the collection to job positions belonging to that workspace and company.

The distinction is:

| Operation             | How the parent IDs are used                                          |
| --------------------- | -------------------------------------------------------------------- |
| Nested list           | Parent IDs scope the returned collection                             |
| Nested create         | Parent IDs establish the parent context for creation                 |
| Nested update         | Parent IDs provide the context used by the update operation          |
| Nested partial update | Parent IDs provide the context used by the update operation          |
| Nested delete         | Parent IDs provide the context used by the delete operation          |
| Nested retrieve       | Resource is looked up by its own ID and authenticated-user ownership |

Consequently, clients should use the canonical parent hierarchy when constructing nested URLs, but should not treat the parent IDs in a nested detail URL as additional lookup filters for the individual resource.

---

# 10. Resource hierarchy

The main resource hierarchy exposed by the nested API is:

```text
Workspace
└── Company
    ├── Company Note
    ├── Company Email
    └── Job Position
        └── Job Application
            └── Job Application Note
```

This hierarchy determines the nested URL structure.

For example:

```text
Workspace
    ↓
Company
    ↓
Job Position
    ↓
Job Application
    ↓
Job Application Note
```

becomes:

```text
/api/v1/workspaces/{workspace_id}
/companies/{company_id}
/job-positions/{job_position_id}
/job-applications/{job_application_id}
/job-application-notes/
```

---

# 11. Resources without nested CRUD

The following resources have independent API lifecycles and therefore expose their CRUD operations directly through flat endpoints:

* Workspace
* Job Benefit
* Job Task
* Job Requirement
* Document Type
* Document

For example:

```http
POST   /api/v1/job-benefits/
GET    /api/v1/job-benefits/{id}/
PATCH  /api/v1/job-benefits/{id}/
DELETE /api/v1/job-benefits/{id}/
```

These resources do not require a parent identifier in the URL for their CRUD operations.

---

# 12. Resources with nested CRUD

The following resources use nested endpoints for create, update, partial update, and delete:

* Company
* Company Note
* Company Email
* Job Position
* Job Application
* Job Application Note

Their flat endpoints remain available for `GET` list/retrieve operations.

For example, a job position can be retrieved through:

```http
GET /api/v1/job-positions/{id}/
```

but its CRUD operations are performed through:

```http
POST   /api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/
GET    /api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{id}/
PUT    /api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{id}/
PATCH  /api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{id}/
DELETE /api/v1/workspaces/{workspace_id}/companies/{company_id}/job-positions/{id}/
```

---

# 13. Practical usage examples

## Retrieve a resource

If the resource ID is already known:

```http
GET /api/v1/companies/{company_id}/
```

---

## List all accessible resources

```http
GET /api/v1/companies/
```

The response contains the companies accessible to the authenticated user.

---

## List resources within a parent

If the parent is known, use the nested collection endpoint:

```http
GET /api/v1/workspaces/{workspace_id}/companies/
```

---

## Create a child resource

Use the nested collection endpoint:

```http
POST /api/v1/workspaces/{workspace_id}/companies/
```

with the resource representation in the request body.

---

## Update a child resource

Use the nested detail endpoint:

```http
PATCH /api/v1/workspaces/{workspace_id}/companies/{company_id}/
```

---

## Delete a child resource

Use the nested detail endpoint:

```http
DELETE /api/v1/workspaces/{workspace_id}/companies/{company_id}/
```

---

## Filter a flat list

Add supported query parameters:

```http
GET /api/v1/job-applications/?status_id={status_id}
```

Multiple supported filters can be combined:

```http
GET /api/v1/job-applications/?workspace_id={workspace_id}&status_id={status_id}
```

---

# 14. Summary

The V1 API follows two complementary access patterns.

### Flat endpoints

```text
/api/v1/<resource>/
/api/v1/<resource>/{id}/
```

Use these for general resource access.

All resources support:

```text
GET collection
GET detail
```

Some resources additionally support:

```text
POST
PUT
PATCH
DELETE
```

Selected flat collection endpoints support query-parameter filtering.

### Nested endpoints

```text
/api/v1/<parent>/{parent_id}/<child>/
/api/v1/<parent>/{parent_id}/<child>/{child_id}/
```

Use these when operating on resources that are managed within a parent context.

Nested CRUD resources support:

```text
GET
POST
PUT
PATCH
DELETE
```

The parent hierarchy is represented directly in the URL and is used to scope the operation.

In short:

```text
Flat API
    → general read access
    → optional query-parameter filtering
    → direct CRUD for independent resources

Nested API
    → parent-contextual access
    → parent-scoped collection operations
    → CRUD for child resources
```
