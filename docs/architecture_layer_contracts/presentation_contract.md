# Presentation Layer Contract

## Table of Contents
- [1. Purpose](#1-purpose)
- [2. Architectural Principles](#2-architectural-principles)
- [3. Layer Responsibilities](#3-layer-responsibilities)
- [4. Layer Boundaries](#4-layer-boundaries)
- [5. Request Lifecycle](#5-request-lifecycle)
- [6. Django View Contract](#6-django-view-contract)
- [7. DRF ViewSet Contract](#7-drf-viewset-contract)
- [8. Exception Handling Contract](#8-exception-handling-contract)
- [9. Testing Contract](#9-testing-contract)
- [10. Presentation Layer Checklist](#10-presentation-layer-checklist)

---

# 1. Purpose

The Presentation Layer is responsible for handling incoming requests,
coordinating Application Layer components, and generating responses.

It forms the boundary between external clients (such as web browsers or API
consumers) and the Application Layer. Its primary responsibilities are to:

- translate transport-specific input into application-specific objects;
- delegate read operations to Selectors;
- delegate write operations to Services;
- translate application outcomes into transport-specific responses.

The Presentation Layer coordinates the request lifecycle but does not implement
business rules or perform persistence operations.

It is also responsible for translating application exceptions into appropriate
HTTP responses while avoiding unnecessary disclosure of internal implementation
details.

This contract applies to all Presentation Layer components within the project,
including:

- Django Class-Based Views;
- Django REST Framework ViewSets;
- HTML Forms;
- DRF Serializers (when used);
- Presentation Mixins;
- Response generation.

The goals of this contract are to:

- clearly separate presentation concerns from application and persistence
  logic;
- establish a consistent request lifecycle across all presentation components;
- prevent business rules from leaking into the Presentation Layer;
- keep presentation components thin, predictable, and maintainable;
- provide a consistent architecture for both HTML and REST interfaces.

## 1.1 Key terms

- Selector: an Application Layer component that owns read operations, lookup
  failures, ownership checks, and read authorization.
- Service: an Application Layer component that owns write operations, business
  rules, validation, state changes, and persistence.
- Context: a minimal data object containing the identifiers needed to scope an
  operation. It must not contain ORM model instances.
- Presentation component: a View, ViewSet, Form, Serializer, or mixin that
  handles transport concerns and delegates application behavior.

---

# 2. Architectural Principles

The Presentation Layer follows a small set of architectural principles that
govern how requests are handled and how responsibilities are distributed
throughout the application.

These principles apply equally to Django Class-Based Views, Django REST
Framework ViewSets, Forms, Serializers, and other Presentation Layer
components.

---

## 2.1 Separation of Concerns

Each architectural layer has a clearly defined responsibility.

The Presentation Layer is responsible only for request handling and response
generation.

Business rules belong exclusively to the Application Layer.

Persistence concerns belong to the ORM and underlying database.

Presentation components must not implement business rules, persistence logic,
or authorization logic that is already enforced by Application Layer
components.

---

## 2.2 Thin Presentation Components

Presentation components coordinate the request lifecycle but should contain
very little application logic.

They should primarily:

- validate transport-specific input;
- invoke Selectors or Services;
- translate application exceptions into HTTP responses;
- prepare the appropriate response.

Whenever presentation code becomes responsible for making business decisions,
that logic should be moved into the Application Layer.

---

## 2.3 Read/Write Separation

Read operations and write operations have different responsibilities and must
remain separate.

Read operations retrieve existing data through Selectors.

Write operations modify application state through Services.

Presentation components should never perform writes directly through models or
the ORM.

---

## 2.4 Transport Independence

Business behaviour must not depend on the transport mechanism.

Whether a request originates from:

- an HTML form;
- a REST API;
- a management command;
- a scheduled task;
- or another entry point,

the same Application Layer components should be used.

This ensures consistent behaviour across every interface.

---

## 2.5 Explicit Request Lifecycle

Every request should follow a predictable lifecycle.

A typical request consists of:

1. request validation;
2. application component invocation;
3. exception translation;
4. response generation.

Presentation components should avoid mixing these responsibilities together.

Keeping the lifecycle explicit improves readability, consistency, and
testability.

---

## 2.6 Application Layer Ownership

The Presentation Layer delegates application behaviour to the appropriate
Application Layer component.

Selectors own:

- object retrieval;
- ownership verification;
- read authorization;
- lookup failures.

Services own:

- state changes;
- business rules;
- write validation;
- persistence.

Presentation components coordinate these operations but must not duplicate
their responsibilities.

---

# 3. Layer Responsibilities

The Presentation Layer consists of multiple component types that collaborate to
handle requests.

Each component has a clearly defined responsibility.

Shared presentation responsibilities:

- receive the request;
- validate transport-specific input;
- delegate reads to Selectors;
- delegate writes to Services;
- translate application exceptions;
- generate the response.

No component should assume responsibilities assigned to another layer.

---

## 3.1 Django Views

Django Views coordinate HTML requests.

They apply the shared presentation responsibilities above and also:

- instantiate and validate Forms;
- select templates;
- construct template context;
- return HTTP responses.

Views must remain orchestration components and should avoid implementing
application logic directly.

---

## 3.2 Django REST Framework ViewSets

ViewSets coordinate API requests.

They apply the shared presentation responsibilities above and also:

- validate request data through Serializers;
- select serializers where appropriate;
- return HTTP responses.

ViewSets should expose HTTP behaviour only and should not contain business
logic.

---

## 3.3 Forms

Forms validate transport-specific HTML input.

Forms are responsible for:

- field validation;
- type conversion;
- format validation;
- presentation-oriented validation.

Forms must not:

- perform persistence;
- implement business rules;
- perform ownership or authorization decisions;
- invoke Services;
- retrieve arbitrary domain objects directly through the ORM.

Cross-entity validation belongs to the Application Layer.

---

## 3.4 Serializers

Serializers perform the equivalent role for REST APIs.

Their responsibilities include:

- request validation;
- serialization;
- deserialization;
- transport-specific validation.

Serializers follow the same architectural boundaries as Forms.

---

## 3.5 Selectors

Selectors own read operations.

Presentation components should use Selectors whenever existing application data
must be retrieved.

Selectors are responsible for:

- object retrieval;
- ownership verification;
- read authorization;
- lookup failures.

Presentation components should not duplicate these responsibilities.

---

## 3.6 Services

Services own write operations.

Presentation components should invoke Services whenever application state is
modified.

Services are responsible for:

- business rules;
- write validation;
- persistence;
- state transitions;
- domain invariants.

Presentation components should never perform writes directly through models.

---

## 3.7 Models

Models define the persistence structure of the application.

Models should not coordinate request handling or implement presentation
behaviour.

Models may define persistence-related behaviour and domain primitives but should
not replace Application Layer business logic.

---

## 3.8 Response Generation

The final responsibility of the Presentation Layer is to translate application
outcomes into transport-specific responses.

Examples include:

- rendering templates;
- redirects;
- JSON responses;
- HTTP status codes;
- user-facing messages.

Response generation should remain independent of application business rules.

---

# 4. Layer Boundaries

The Presentation Layer coordinates the request lifecycle but delegates
application behaviour to lower architectural layers.

Each layer has a well-defined dependency direction and ownership of
responsibilities.

Presentation components should communicate only through the public interfaces
defined by the Application Layer contracts.

---

## 4.1 Allowed Dependencies

The Presentation Layer may depend on:

- Django and Django REST Framework infrastructure;
- Forms and Serializers;
- Selectors;
- Services;
- presentation utilities and mixins.

Presentation components should not depend directly on persistence
implementation details beyond what is required by framework infrastructure.

---

## 4.2 Prohibited Responsibilities

Presentation components must not:

- implement business rules;
- perform persistence directly through models or the ORM;
- duplicate ownership or authorization checks already performed by Selectors;
- duplicate business validation already performed by Services;
- coordinate transactions;
- implement application workflows that belong in the Application Layer.

Whenever presentation code starts making domain decisions, that logic should be
moved into the Application Layer.

---

## 4.3 Communication with Selectors

Selectors are the exclusive interface for read operations.

Presentation components should retrieve existing domain objects through
Selectors rather than constructing authorization-aware querysets themselves.

Selectors are responsible for:

- object retrieval;
- ownership verification;
- lookup failures;
- read authorization.

Presentation components should treat retrieved objects as trusted application
inputs.

---

## 4.4 Communication with Services

Services are the exclusive interface for write operations.

Presentation components should invoke Services whenever application state is
created, updated, or deleted.

Services own:

- business rules;
- write validation;
- persistence;
- domain invariants;
- state transitions.

Presentation components should not modify models directly.

---

## 4.5 Forms and Serializers

Forms and Serializers are responsible for transport-specific validation. Forms may also use access-scoped Selectors to restrict the choices presented to the user.

They should validate:

- field types;
- formatting;
- required fields;
- transport-specific constraints.

They should not perform:

- business validation;
- ownership decisions;
- persistence;
- cross-entity consistency checks.

Those responsibilities belong to the Application Layer.

---

## 4.6 Exception Ownership

Presentation components are responsible for translating application exceptions
into transport-specific responses.

Selectors and Services define application failures.

Presentation components determine how those failures are presented to users or
API clients.

The Presentation Layer should not expose internal implementation details when
handling exceptions.

---

## 4.7 Dependency Direction

The dependency direction of the architecture is:

Presentation Layer
↓
Application Layer
↓
Persistence Layer

Dependencies must not point upward.

Lower layers must remain unaware of presentation concerns such as:

- HTTP requests
- templates
- redirects
- messages
- serializers
- forms

## 4.8 Framework Integration Exceptions

Certain framework-provided functionality may legitimately interact directly with
Django infrastructure without introducing an intermediate Application Layer
component.

Examples include:

- authentication;
- session management;
- login and logout;
- password management.

When using Django's built-in authentication framework, Presentation
components may invoke Django authentication APIs directly where doing so is the
framework's intended integration point.

Such exceptions should remain narrowly scoped and must not become a mechanism
for introducing general business logic into the Presentation Layer.

---

# 5. Request Lifecycle

Every request handled by the Presentation Layer should follow a predictable
lifecycle.

Although individual views may differ, the overall sequence of responsibilities
should remain consistent across the application.

Following a consistent request lifecycle improves readability, maintainability,
testability, and architectural separation.

---

## 5.1 Receive the Request

The Presentation Layer receives an incoming request through a Django View or a
DRF ViewSet.

At this stage the Presentation Layer is responsible only for interpreting the
transport-specific request.

No business logic should be executed during request reception.

---

## 5.2 Retrieve Existing Data

If the operation requires existing application data, the Presentation Layer
retrieves it through the appropriate Selector.

Selectors perform:

- object retrieval;
- ownership verification;
- read authorization;
- lookup validation.

Presentation components should not perform authorization-aware ORM queries
directly.

Operations that do not require existing data may skip this step.

---

## 5.3 Validate Transport Input

Incoming user input is validated using the appropriate presentation component.

Depending on the transport mechanism this may be:

- a Django Form;
- a DRF Serializer.

Validation performed here should be limited to transport-specific concerns,
including:

- required fields;
- type conversion;
- formatting;
- field constraints.

Business validation belongs to the Application Layer.

---

## 5.4 Invoke the Application Layer

Once transport-specific validation succeeds, the Presentation Layer delegates
the requested operation to the appropriate Application Layer component.

Read operations are delegated to Selectors.

Write operations are delegated to Services.

Presentation components should not implement business rules themselves.

---

## 5.5 Translate Application Exceptions

Selectors and Services may raise application exceptions to indicate lookup
failures, domain invariant violations, business rule violations, or infrastructure
failures.

The Presentation Layer is responsible for translating these exceptions into
appropriate transport-specific responses.

Exception translation should remain consistent throughout the application.

---

## 5.6 Generate the Response

After the Application Layer completes successfully, the Presentation Layer
constructs the appropriate response.

Examples include:

- rendering a template;
- redirecting to another page;
- returning serialized data;
- returning an appropriate HTTP status code;
- displaying success or informational messages.

Response generation should not introduce additional business logic.

---

## 5.7 Complete the Request

The request ends once the response has been generated.

At this point the Presentation Layer should have:

- delegated application behaviour;
- translated any application failures;
- generated the appropriate response.

The request lifecycle should remain deterministic and free of hidden
application behaviour.

---

# 6. Django View Contract

Django Class-Based Views coordinate HTML requests by orchestrating Presentation
Layer components and delegating application behaviour to the Application Layer.

Views should remain thin orchestration components and must not implement
business rules or persistence logic.

---

## 6.1 Responsibilities

Django Views are responsible for:

- receiving HTTP requests;
- retrieving existing domain objects through Selectors;
- instantiating and validating Forms;
- invoking Services for write operations;
- translating application exceptions into user-facing responses;
- selecting templates;
- constructing template context;
- returning HTTP responses.

Views coordinate the request lifecycle but do not own application behaviour.

---

## 6.2 Object Retrieval

Whenever a view requires existing domain objects, those objects should be
retrieved through the appropriate Selector.

Selectors are responsible for:

- object lookup;
- ownership verification;
- read authorization;
- lookup failures.

Views should not perform authorization-aware ORM queries directly.

Objects successfully returned by Selectors may be treated as trusted
application inputs.

---

## 6.3 Form Usage

Views are responsible for creating and validating Forms.

Forms should validate only transport-specific input.

Views may supply Forms with previously resolved domain objects when required
for presentation purposes.

Views should not expect Forms to perform business validation or persistence.

## 6.4 Context Validation

Some views require one or more parent domain objects before request processing
can continue.

When this occurs, the required context should be resolved and validated before
form validation or Service invocation begins.

Context resolution should be delegated to the appropriate Selectors.

If the required context cannot be resolved, the request should terminate using
the appropriate presentation response rather than continuing with incomplete
application state.

Presentation components should avoid constructing Forms or invoking Services
until the required application context has been successfully established.

---

## 6.5 Service Invocation

All operations that create, update, or delete application state must be
delegated to Services.

Views should pass validated input and any required domain objects to the
appropriate Service.

Views must not:

- call model save() directly;
- call model delete() directly;
- implement business rules;
- coordinate transactions.

---

## 6.6 Exception Translation

Views are responsible for translating application exceptions into appropriate
user-facing responses.

Typical responses include:

- rendering the current template;
- redirecting to another page;
- displaying form errors;
- displaying user-facing messages;
- returning an appropriate HTTP status.

Views should not expose internal implementation details when handling
exceptions.

---

## 6.7 Template Context

Views construct the template context required for rendering.

Context should contain only data required by the template.

Business computations required to construct the response should already have
been completed by the Application Layer.

---

## 6.8 Redirects and Responses

Views determine the appropriate response after successful completion of an
application operation.

Typical responses include:

- rendering a template;
- redirecting after successful writes;
- returning HTTP error responses when appropriate.

Response generation should remain independent of business logic.

---

## 6.9 View Composition

Views may use reusable presentation mixins to encapsulate common presentation
behaviour.

Typical presentation mixins may provide functionality such as:

- exception translation;
- form error handling;
- request preprocessing;
- context preparation;
- common response behaviour.

Presentation mixins should not implement business rules, persistence logic, or
authorization logic that belongs to the Application Layer.

Business behaviour shared across multiple views should be implemented within
the Application Layer rather than presentation mixins.

---

## 7. DRF ViewSet Contract

DRF ViewSets belong to the Presentation Layer and are responsible for
translating HTTP API requests into Application Layer operations.

A ViewSet coordinates:

- Request handling.
- Authentication.
- Authorization.
- Serializer usage.
- Context construction.
- Selector invocation.
- Service invocation.
- API response generation.

A ViewSet is an HTTP orchestration component.

A ViewSet should answer:

> "Which application operation should execute for this API request?"

A ViewSet should not answer:

> "How does the business operation work?"

Concrete ViewSets should inherit from reusable presentation base classes that
implement the common orchestration workflow.

These base classes provide consistent request validation, context construction,
Service invocation, and response generation.

Concrete ViewSets should primarily configure:

- selector_class
- service_class
- serializer classes
- context construction

---

# 7.1 ViewSet Responsibilities

DRF ViewSets are responsible for:

- Receiving API requests.
- Handling HTTP actions.
- Applying authentication.
- Applying permissions.
- Loading request-specific data.
- Instantiating Serializers.
- Validating request payloads.
- Constructing Application Context objects.
- Calling Selectors for reads.
- Calling Services for writes.
- Serializing responses.
- Returning appropriate HTTP status codes.

---

# 7.2 ViewSet Non-Responsibilities

DRF ViewSets MUST NOT:

- Implement business rules.
- Perform direct ORM writes.
- Call model `save()`.
- Call model `delete()`.
- Implement domain validation.
- Enforce workspace ownership rules.
- Duplicate Service logic.
- Duplicate Selector logic.
- Use Serializers as a replacement for Services.

The ViewSet is a transport boundary, not an application layer.

---

# 7.3 API Request Lifecycle

A typical API request should follow this flow:

```text
HTTP Request
      |
      v
Authentication
      |
      v
Permission Checks
      |
      v
Serializer Validation
      |
      v
Context Construction
      |
      v
Selector / Service Invocation
      |
      v
Serializer Response
      |
      v
HTTP Response
```

Each stage has a separate responsibility.

---

# 7.4 Authentication Contract

Authentication determines:

> "Who is making this request?"

ViewSets may rely on DRF authentication mechanisms:

Examples:

- Session authentication.
- Token authentication.
- JWT authentication.

The authenticated user should be supplied directly to Selectors and Services.

Authentication information should not be embedded inside Context objects.

Authentication must not implement business authorization.

---

# 7.5 Permission Contract

Permissions determine:

> "Is this requester allowed to access this API operation?"

ViewSets may use:

- DRF permission classes.
- Custom permission classes.
- Endpoint-level authorization.

Examples:

Allowed:

```text
Only authenticated users can create job applications.
```

Not allowed:

```text
This user owns this specific company.
```

Resource ownership is not enforced through DRF object-permission classes. Resource
access is enforced by access-scoped Selectors, while write invariants are enforced
by Services.

---

# 7.6 `get_queryset()` Contract

ViewSets MUST use Selectors for application data retrieval.

Preferred: delegate the queryset to a Selector that accepts the authenticated user.

Avoid: filtering directly on the ORM when the filtering represents application access rules.

`get_queryset()` determines which data is exposed through the API.

It must not implement business logic.

---

# 7.7 Serializer Boundary

Serializers are responsible for transport validation.

Serializers may:

- Parse JSON input.
- Validate field formats.
- Normalize input.
- Serialize application results.

Serializers must not:

- Implement business rules.
- Perform domain operations.
- Create application entities directly.
- Replace Services.
- Perform ownership validation.

---

# 7.8 Serializer `create()` Contract

Serializer `create()` MUST NOT perform application persistence.

The preferred flow is:

```text
Serializer
      |
      | validated_data
      v
ViewSet
      |
      v
Service
      |
      v
ORM
```

The Service Layer owns creation behavior.

---

# 7.9 Serializer `update()` Contract

Serializer `update()` MUST NOT perform application updates directly.

Prohibited:

```python
def update(self, instance, validated_data):
    instance.name = validated_data["name"]
    instance.save()

    return instance
```

Updates should follow:

```text
Serializer
      |
      v
ViewSet
      |
      v
Service
      |
      v
ORM
```

---

# 7.10 Base ViewSet Write Orchestration

Write operations should be orchestrated by reusable base ViewSet classes rather
than being reimplemented by every concrete ViewSet.

The base ViewSet is responsible for:

- Instantiating the write Serializer.
- Validating the incoming request.
- Constructing the required Context object.
- Invoking the appropriate Service method.
- Serializing the returned application object.
- Returning the appropriate HTTP response.

The write workflow should remain consistent across all API endpoints.

The expected flow is:

```text
HTTP Request
      |
      v
Write Serializer
      |
      | validated_data
      v
Context Construction
      |
      v
Service
      |
      v
Read Serializer
      |
      v
HTTP Response
```

Concrete ViewSets should only supply the resource-specific configuration and
Context construction required by the operation.

---

# 7.11 Context-Based Service Invocation

Write operations should invoke Services using explicit Context objects.

The ViewSet is responsible for constructing the appropriate Context from the
request URL, route parameters, and other request metadata before delegating the
operation to the Service.

Context objects should contain only the identifiers required to define the
execution scope of the operation.

Authenticated users should be supplied separately through the `user`
parameter.

Example shape: `user` is passed separately, and the Context contains only the
route identifiers needed to scope the Service call.

ViewSets must not:

- Embed business rules into Context construction.
- Pass ORM model instances as Context values.
- Modify Context semantics.

---

# 7.12 Concrete ViewSet Responsibilities

Concrete ViewSets should remain lightweight.

Their primary responsibilities are:

- Configuring the appropriate Selector.
- Configuring the appropriate Service.
- Configuring the read and write Serializers.
- Constructing the required Context objects.
- Delegating read operations to Selectors.
- Delegating write operations to Services.

Reusable request orchestration should remain inside the shared base ViewSet
classes.

A concrete ViewSet should primarily describe:

- what resource is exposed,
- which Context is required,
- which Selector performs reads,
- which Service performs writes.

It should not reimplement the common request lifecycle.

---

# 7.13 `create()` and `update()` Contract

Overriding ViewSet actions should preserve the orchestration model.

Allowed responsibilities:

- Request preparation.
- Serializer handling.
- Service invocation.
- Response formatting.

Not allowed:

- Business decisions.
- Database manipulation.
- Domain workflows.

Example shape: validate the write Serializer, call the Service with validated
data, then serialize the returned object for the response.

---

# 7.14 Context Construction Contract

ViewSets are responsible for creating Context objects required by Services.

Context information may come from:

- Request metadata.
- URL parameters.
- Existing resources.

Example shape: the Context should carry only identifiers derived from request
metadata or resolved resources, never ORM instances.

ViewSets must not:

- Add business decisions.
- Modify Context behavior.
- Use Contexts to hide application logic.

---

# 7.15 Response Contract

ViewSets are responsible for API response generation.

Responsibilities include:

- Selecting serializers.
- Returning status codes.
- Returning response headers.
- Handling pagination.
- Formatting API output.

Example shape: return the serialized payload with the appropriate HTTP status
code.

ViewSets must not determine the meaning of application results.

---

# 7.16 Exception Translation Contract

ViewSets translate Application Layer exceptions into API responses.

Example:

```text
BusinessRuleViolationError
        |
        v
HTTP 400 Response
```

Common mappings:

```text
Validation failure
        |
        v
HTTP 400 Bad Request


Resource access failure
        |
        v
HTTP 404 Not Found


Missing resource
        |
        v
HTTP 404 Not Found
```

Exception translation should preferably be centralized using reusable
presentation components such as:
- custom DRF exception handlers,
- shared ViewSet mixins,
- middleware.

Exception translation belongs in the Presentation Layer.

Exception meaning belongs in the Application Layer.

---

# 7.17 API Pagination Contract

Pagination is a Presentation Layer responsibility.

ViewSets may:

- Apply pagination classes.
- Format pagination metadata.
- Return paginated responses.

Selectors should provide query capability.

ViewSets should determine API representation.

---

# 7.18 API Filtering Contract

Filtering must respect the layer boundary.

Allowed:

```text
Request parameter:
?page=2
```

because pagination is presentation behavior.

Not allowed:

```text
Request parameter:
?show_active_companies_only=true
```

when "active company visibility" represents business logic.

Business filtering belongs in Selectors.

---

# 7.19 ViewSet Review Checklist

During code review, verify:

- Does the ViewSet only orchestrate API operations?
- Are reads delegated to Selectors?
- Are writes delegated to Services?
- Are Serializers limited to transport validation?
- Is direct ORM manipulation avoided?
- Are Context objects constructed correctly?
- Are HTTP concerns isolated inside the ViewSet?
- Are exceptions translated consistently?
- Is business logic absent from API endpoints?

A compliant ViewSet should expose application capabilities without becoming the
place where application behavior is implemented.

---

## 8. Exception Handling Contract

The Presentation Layer is responsible for translating application failures into
appropriate HTTP responses.

It does not determine whether an operation has failed; that responsibility
belongs to the Application Layer.

Presentation components should consistently translate application exceptions
into user-facing responses without exposing internal implementation details.

---

### 8.1 Responsibilities

The Presentation Layer is responsible for:

- Catching application exceptions.
- Translating exceptions into appropriate HTTP responses.
- Displaying user-friendly validation errors.
- Returning appropriate HTTP status codes.
- Displaying success and error messages where appropriate.
- Preventing internal exception details from reaching end users.

Business exceptions must never be ignored or silently suppressed.

---

### 8.2 Exception Ownership

Each architectural layer owns its own failures.

- Django and the framework raise framework exceptions.
- Selectors raise read-related application exceptions.
- Services raise business and write-related application exceptions.
- The Presentation Layer translates those exceptions into HTTP responses.

Presentation components should not redefine application failure semantics.

---

### 8.3 Framework Exceptions

Framework exceptions should be handled according to Django's standard behavior
unless the application explicitly defines an alternative presentation.

Examples include:

- HTTP 404 responses,
- permission failures,
- malformed requests,
- CSRF failures.

Framework behavior should remain predictable and consistent.

---

### 8.4 Selector Exceptions

Exceptions originating from Selectors represent failures to retrieve application
data.

Presentation components should translate these failures into the appropriate
presentation response.

Typical examples include:

- resource not found,
- inaccessible resource.

Views should not attempt to recover by performing alternative queries.

---

### 8.5 Service Exceptions

Exceptions originating from Services represent application-level failures.

These may include:

- business rule violations,
- domain validation failures,
- invalid application state,
- write operation failures.

Presentation components should translate these exceptions into user-visible
errors without modifying their meaning.

---

### 8.6 Validation Errors

Transport validation and business validation are handled separately.

Transport validation failures originate from Forms (or Serializers).

Business validation failures originate from Services.

The Presentation Layer is responsible for presenting both types of validation
errors consistently.

---

### 8.7 User Feedback

Presentation components should communicate failures using presentation-specific
mechanisms.

Examples include:

- Form field errors,
- non-field errors,
- error messages,
- HTTP status codes,
- error templates.

The presentation of an error should be understandable to end users while
avoiding unnecessary implementation details.

---

### 8.8 Information Disclosure

Presentation components must not expose internal implementation details.

Examples include:

- stack traces,
- database errors,
- ORM exceptions,
- implementation-specific exception messages.

Unexpected exceptions should be logged appropriately while presenting generic
user-facing error responses.

---

### 8.9 Exception Consistency

The same application exception should produce the same presentation behavior
throughout the application.

Equivalent failures should always result in equivalent HTTP responses and
consistent user feedback.

Presentation components should avoid implementing endpoint-specific exception
behavior unless explicitly required.

---

### 8.10 Testing

Exception handling tests should verify that presentation components correctly
translate application failures.

Typical tests include:

- Service exceptions become user-visible validation errors.
- Selector exceptions become appropriate HTTP responses.
- Framework exceptions are handled consistently.
- Unexpected exceptions do not expose internal implementation details.
- Success and failure messages are displayed appropriately.

---

## 9. Testing Contract

Presentation Layer tests verify that presentation components correctly
coordinate HTTP requests and responses.

Their purpose is to ensure that Views, Forms, and other presentation
components fulfill their presentation responsibilities while delegating
business behavior to the appropriate application layer.

Presentation tests should focus on presentation behavior rather than business
logic.

---

### 9.1 Scope

Presentation Layer tests should verify:

- request handling,
- authentication,
- authorization,
- Form validation,
- Context construction,
- Selector invocation,
- Service invocation,
- template rendering,
- redirects,
- response generation,
- success and error messages,
- exception translation.

Business behavior should be verified through Service tests rather than
Presentation Layer tests.

---

### 9.2 Django View Tests

Django View tests should verify that each View:

- accepts the appropriate HTTP methods,
- enforces authentication,
- enforces authorization,
- renders the correct template,
- constructs the expected Context object,
- invokes the appropriate Selector for read operations,
- invokes the appropriate Service for write operations,
- redirects appropriately after successful write operations,
- displays validation errors correctly,
- translates application exceptions consistently.

Views should be tested as orchestration components rather than business
components.

---

### 9.3 Form Tests

Form tests should verify only Form responsibilities.

Typical tests include:

- required fields,
- field validation,
- transport validation,
- data normalization,
- generated `cleaned_data`,
- presentation of validation errors.

Business rules should not be tested through Form tests.

---

### 9.4 Isolation

Presentation Layer tests should remain independent of business logic whenever
possible.

When verifying orchestration behavior, Services and Selectors may be mocked to
confirm that presentation components invoke the correct application operations.

Business behavior should not be duplicated within Presentation Layer tests.

---

### 9.5 Exception Handling Tests

Presentation tests should verify that application exceptions are translated into
the correct presentation behavior.

Typical tests include:

- validation errors are displayed correctly,
- resource lookup failures produce the expected response,
- inaccessible resources produce the expected 404 response,
- unexpected exceptions do not expose internal implementation details.

---

### 9.6 Response Verification

Presentation tests should verify the generated HTTP response.

Depending on the endpoint, this may include:

- rendered templates,
- template context,
- redirects,
- HTTP status codes,
- JSON responses,
- success messages,
- error messages.

Tests should verify the observable behavior presented to the client.

---

### 9.7 Layer Separation

Presentation tests should verify that architectural boundaries are respected.

Presentation components should delegate:

- read operations to Selectors,
- write operations to Services,
- business validation to the Application Layer.

Presentation tests should avoid asserting implementation details belonging to
other architectural layers.

---

### 9.8 Test Coverage

Collectively, Presentation Layer tests should demonstrate that presentation
components:

- correctly receive HTTP requests,
- correctly invoke the Application Layer,
- correctly handle successful operations,
- correctly handle application failures,
- consistently generate the expected HTTP responses.

The Presentation Layer should be fully validated without duplicating the
responsibilities of Models, Selectors, or Services.

---

## 10. Presentation Layer Checklist

The checklist has been moved to `presentation_layer_checklist.md` in the same
directory.
