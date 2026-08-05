# Presentation Layer Contract

1. Purpose
2. Architectural Principles
3. Layer Responsibilities
4. Layer Boundaries
5. Application Component Responsibilities
6. Request Lifecycle
7. Forms Contract
8. Django View Contract
9. DRF ViewSet Contract
10. Exception Handling Contract
11. Testing Contract
12. Checklist

---

# 1. Purpose

The Presentation Layer is responsible for handling incoming requests,
coordinating application use-cases, and generating responses.

It acts as the boundary between external clients (such as web browsers or API
consumers) and the Application Layer. Its primary role is to translate
transport-specific data into application-specific inputs, delegate business
operations to the appropriate layer, and return an appropriate response.

The Presentation Layer must remain orchestration-focused. It coordinates the
flow of a request but does not implement business rules or perform data access.

This contract applies to all presentation components within the project,
including:

- Django Class-Based Views
- Django REST Framework ViewSets
- HTML Forms
- DRF Serializers (when used for request validation)
- Presentation Mixins
- Response generation

The goals of this contract are to:

- Clearly separate presentation concerns from business and persistence logic.
- Ensure a consistent request lifecycle across all presentation components.
- Prevent business rules from leaking into the Presentation Layer.
- Keep presentation components thin, predictable, and easy to maintain.
- Establish a common architecture for both HTML and REST interfaces.

---

# 2. Architectural Principles

The Presentation Layer shall adhere to the following architectural principles.

## 2.1 Separation of Concerns

The Presentation Layer is responsible solely for request orchestration and
response generation.

It translates transport-specific data into application-specific inputs,
delegates all business operations to the Application Layer, and prepares
responses for the client.

Business rules, domain invariants, and persistence logic must never be
implemented within the Presentation Layer.

---

## 2.2 Thin Presentation Components

Presentation components shall remain lightweight.

They should coordinate the request lifecycle rather than implement business
logic.

Their responsibilities include:

- Receiving and validating client input.
- Constructing Context and QueryFilter objects.
- Delegating read operations to Selectors.
- Delegating write operations to Services.
- Preparing the appropriate response.

---

## 2.3 Read / Write Separation

The Presentation Layer shall preserve the architectural separation between
read and write operations.

- Read operations shall be delegated exclusively to Selectors.
- Create, Update, and Delete operations shall be delegated exclusively to
  Services.

Presentation components must never perform ORM operations directly.

---

## 2.4 Transport Independence

Business operations shall remain independent of the transport mechanism.

The Presentation Layer is responsible for translating HTTP-specific concerns
(such as URL parameters, query parameters, request bodies, uploaded files, and
authentication information) into application-specific objects before invoking
Selectors or Services.

Neither Services nor Selectors shall depend on HTTP-specific concepts.

---

## 2.5 Explicit Request Lifecycle

Every request shall follow a predictable lifecycle.

Although the concrete implementation may differ between Django Views and DRF
ViewSets, each request should consistently follow the same architectural flow:

- Receive the request.
- Authenticate and authorize the user.
- Translate request data into application-specific inputs.
- Delegate the requested operation.
- Produce an appropriate response.

---

## 2.6 Framework Independence

Architectural responsibilities shall not depend on a specific presentation
framework.

Whether implemented using Django Class-Based Views, Django REST Framework
ViewSets, or another presentation technology, the same architectural
responsibilities and boundaries shall apply.

---

# 3. Layer Responsibilities

The Presentation Layer coordinates application use-cases by translating client
requests into application-specific inputs and generating responses.

It does not implement business rules or access the persistence layer directly.

Its responsibilities are divided into the following areas.

## 3.1 Request Handling

The Presentation Layer is responsible for receiving client requests and
extracting all transport-specific information required to execute the requested
operation.

This includes, but is not limited to:

- URL parameters.
- Query parameters.
- Request bodies.
- Uploaded files.
- Authenticated user information.

---

## 3.2 Input Translation

The Presentation Layer shall translate transport-specific data into
application-specific inputs before invoking the Application Layer.

Examples include:

- Constructing Context objects.
- Constructing QueryFilter objects.
- Producing validated input through Forms or Serializers.

The Application Layer shall never be responsible for interpreting HTTP
requests.

---

## 3.3 Input Validation

The Presentation Layer is responsible for validating the structure and format
of client input.

Examples include:

- Required fields.
- Field types.
- Length constraints.
- File validation.
- Presentation-specific validation.

Business validation and domain invariants shall be delegated to Services.

---

## 3.4 Request Orchestration

The Presentation Layer coordinates the request lifecycle.

It determines which application component should perform the requested
operation and delegates accordingly.

Specifically:

- Read operations shall be delegated to Selectors.
- Create operations shall be delegated to Services.
- Update operations shall be delegated to Services.
- Delete operations shall be delegated to Services.

Presentation components shall not implement business logic themselves.

---

## 3.5 Response Generation

The Presentation Layer is responsible for generating an appropriate response
for the client.

Depending on the interface, this may include:

- Rendering HTML templates.
- Returning JSON responses.
- Returning redirects.
- Returning file responses.
- Returning appropriate HTTP status codes.

---

## 3.6 Error Translation

The Presentation Layer is responsible for converting application exceptions
into appropriate client-facing responses.

Examples include:

- Displaying validation errors.
- Returning HTTP error responses.
- Rendering error pages.
- Redirecting with user-visible feedback.

Application exceptions shall not leak directly to the client.

---

## 3.7 Non-Responsibilities

The Presentation Layer shall not:

- Implement business rules.
- Enforce domain invariants.
- Perform ownership validation.
- Execute ORM queries directly.
- Persist model instances.
- Coordinate database transactions.
- Duplicate logic already implemented by Selectors or Services.

---

## 4. Layer Boundaries

The Presentation Layer coordinates application operations but must not assume
responsibilities that belong to other architectural layers.

The following boundaries define what presentation components must never do.

---

### 4.1 Business Logic

The Presentation Layer must not implement business logic.

Business rules belong exclusively to the Service Layer.

Examples include:

- determining whether an operation is permitted,
- enforcing workflow rules,
- coordinating multiple domain objects,
- applying business policies,
- enforcing domain invariants.

Whenever business behavior is required, the Presentation Layer must delegate the
operation to a Service.

---

### 4.2 Persistence

The Presentation Layer must not perform persistence operations directly.

Presentation components must not:

- call `save()`,
- call `delete()`,
- call `create()`,
- call `update()`,
- perform bulk write operations.

All domain mutations must be delegated to Services.

---

### 4.3 Data Access

The Presentation Layer must not contain reusable query logic.

Reusable data retrieval belongs to Selectors.

Presentation components may retrieve data through Selectors and may perform
presentation-specific operations such as pagination or ordering, but query
construction intended for reuse should remain inside Selectors.

---

### 4.4 Domain Validation

The Presentation Layer must not validate business rules.

Forms and Serializers are responsible for validating transport-level input.

Services are responsible for validating domain rules.

Presentation components must not duplicate business validation performed by
Services.

---

### 4.5 Ownership Validation

The Presentation Layer must not determine ownership of domain objects.

Ownership and tenant isolation belong to the Application Layer.

Presentation components should delegate ownership validation to Selectors and
Services.

---

### 4.6 Context Resolution

The Presentation Layer must not reconstruct domain relationships.

It may collect identifiers from the request and construct Context objects, but
it should not resolve business relationships independently.

Relationship resolution belongs to the Application Layer.

---

### 4.7 Exception Semantics

The Presentation Layer must not define application failure semantics.

Application exceptions should originate from the Application Layer.

The responsibility of the Presentation Layer is limited to translating those
exceptions into appropriate HTTP responses.

---

### 4.8 Business State

The Presentation Layer must not own business state.

Domain state belongs to domain models and the persistence layer.

Presentation components may maintain temporary presentation state only, such as:

- pagination,
- sorting,
- search parameters,
- redirect destinations,
- success messages,
- user interface state.

Business state must never be stored or managed by the Presentation Layer.

---

### 4.9 Duplication

The Presentation Layer must not duplicate logic already provided by another
architectural layer.

If logic already exists inside a Selector or Service, presentation components
should reuse that implementation rather than reimplement it.

Architectural consistency takes precedence over local convenience.

---

## 5. Application Component Responsibilities

### Django Views

Responsible for:
- authentication
- authorization
- form handling
- context construction
- invoking selectors/services
- rendering responses

### Forms

Responsible for:
- transport validation
- normalization
- cleaned_data

Not responsible for:
- business validation
- persistence

### DRF ViewSets

Responsible for:
- request routing
- serializer orchestration
- HTTP responses

### DRF Serializers

Responsible for:
- serialization
- deserialization
- transport validation

Not responsible for:
- business rules
- persistence

---

## 6. Request Lifecycle

Every request processed by the Presentation Layer should follow the same
high-level lifecycle.

Each step has a single responsibility and delegates work to the appropriate
architectural layer.

---

### Step 1 — Receive the Request

The Presentation Layer receives an incoming HTTP request.

Depending on the endpoint, this may include:

- URL parameters,
- query parameters,
- form data,
- JSON payloads,
- uploaded files.

Authentication and authorization should be enforced before application
operations are performed.

---

### Step 2 — Parse and Validate Transport Data

Incoming request data should be parsed using the appropriate presentation
component.

Examples include:

- Django Forms,
- DRF Serializers.

These components are responsible only for validating transport-level concerns,
such as:

- required fields,
- data types,
- field formats,
- serialization.

Business validation must not occur at this stage.

---

### Step 3 — Construct the Application Context

The Presentation Layer constructs the appropriate Context object required by the
Application Layer.

Context objects should be built using information such as:

- authenticated user,
- URL parameters,
- routing information,
- request metadata.

The Presentation Layer should not resolve business relationships while
constructing the Context.

---

### Step 4 — Invoke the Application Layer

The Presentation Layer delegates the requested operation to the Application
Layer.

Read operations should invoke Selectors.

Write operations should invoke Services.

The Presentation Layer is responsible only for selecting the correct operation,
not implementing its behavior.

---

### Step 5 — Handle the Application Result

The Application Layer returns either:

- a successful result, or
- an application exception.

The Presentation Layer must not reinterpret business decisions returned by the
Application Layer.

---

### Step 6 — Translate the Result into an HTTP Response

The Presentation Layer converts the application result into the appropriate HTTP
response.

Depending on the endpoint, this may involve:

- rendering a template,
- returning JSON,
- redirecting,
- selecting an HTTP status code,
- displaying success messages,
- displaying validation errors.

Only presentation concerns should be handled during this step.

---

### Step 7 — Return the Response

The generated HTTP response is returned to the client.

At this point, all business operations have already been completed by the
Application Layer.

The Presentation Layer performs no additional business processing after the
response has been generated.

---

## 7. Forms Contract

Django Forms are presentation components responsible for translating user input
into validated application input.

Forms validate transport-level concerns and prepare data for the Application
Layer.

They do not implement business behavior.

---

### 7.1 Responsibilities

Forms are responsible for:

- Defining the fields expected from the user.
- Parsing submitted form data.
- Validating transport-level input.
- Normalizing user input.
- Producing `cleaned_data` for the Presentation Layer.
- Displaying validation errors to users.

Forms should remain deterministic and independent of business behavior.

---

### 7.2 Transport Validation

Forms validate whether incoming user input is structurally valid.

Examples include:

- required fields,
- field types,
- value formats,
- string lengths,
- email format,
- numeric ranges,
- field-to-field validation that depends only on submitted form data.

Transport validation ensures that the submitted request can be safely processed
by the Application Layer.

---

### 7.3 Business Validation

Forms must not perform business validation.

Business validation includes, but is not limited to:

- ownership checks,
- workspace access validation,
- uniqueness rules spanning multiple domain objects,
- workflow validation,
- permission decisions,
- domain invariants,
- business policies.

Business validation belongs exclusively to the Service Layer.

---

### 7.4 Persistence

Forms must not perform persistence operations.

Forms must not:

- create model instances,
- update model instances,
- delete model instances,
- call `save()`,
- call `delete()`.

All write operations must be delegated to Services.

---

### 7.5 Interaction with Services

A validated Form produces `cleaned_data`.

The Presentation Layer passes `cleaned_data` to the appropriate Service together
with the required Context object.

Forms should remain unaware of Service implementation details.

---

### 7.6 Interaction with Models

Forms may reference models for presentation purposes.

Examples include:

- `ModelForm` field generation,
- choice fields,
- display metadata.

Forms should not contain domain behavior that belongs to models or Services.

---

### 7.7 Error Reporting

Transport validation failures should be reported as Form validation errors.

Business validation failures should originate from the Service Layer and be
translated by the Presentation Layer into user-visible form errors or messages.

Forms should not generate business exceptions.

---

### 7.8 Testing

Form tests should verify only Form responsibilities.

Typical tests include:

- field validation,
- required fields,
- normalization,
- transport validation,
- generated `cleaned_data`.

Business rules should be tested through Service tests rather than Form tests.

---

## 8. Django View Contract

Django Views are presentation components responsible for orchestrating HTTP
requests and responses.

They receive incoming requests, coordinate interactions with the Application
Layer, and generate HTML responses.

Views must remain thin and should not implement business behavior.

---

### 8.1 Responsibilities

Every Django View is responsible for:

- Receiving HTTP requests.
- Enforcing authentication and authorization.
- Instantiating and validating Forms when required.
- Constructing the appropriate Context object.
- Invoking Selectors for read operations.
- Invoking Services for write operations.
- Rendering templates.
- Redirecting after successful write operations.
- Displaying user-facing success and error messages.
- Translating application exceptions into appropriate responses.
```text

Request
↓

Authentication / Authorization
↓

Form (if applicable)
↓

Context
↓

Selector or Service
↓

Exception Translation
↓

Response

```

---

### 8.2 Read Operations

Views responsible for displaying data should retrieve domain objects through
Selectors.

Selectors encapsulate reusable query logic, ownership validation, and data
retrieval.

Views may perform presentation-specific operations such as:

- pagination,
- ordering,
- searching,
- filtering based on request parameters,
- template context construction.

Business query logic must remain inside Selectors.

---

### 8.3 Write Operations

Views responsible for modifying application state must delegate all write
operations to Services.

The expected workflow is:

1. Validate the submitted Form.
2. Construct the required Context object.
3. Invoke the appropriate Service.
4. Handle the Service result.
5. Generate the appropriate HTTP response.

Views must never modify domain objects directly.

---

### 8.4 Context Construction

Views are responsible for constructing the Context objects required by the
Application Layer.

Context objects should be derived from:

- authenticated user,
- URL parameters,
- request data,
- routing information.

Views should not resolve business relationships independently.

---

### 8.5 Form Handling

Views own the Form lifecycle.

This includes:

- creating Forms,
- validating Forms,
- rendering invalid Forms,
- passing `cleaned_data` to Services.

Views should not duplicate validation already performed by Forms or Services.

---

### 8.6 Response Generation

Views are responsible for producing HTML responses.

This includes:

- rendering templates,
- redirecting users,
- displaying success messages,
- displaying validation errors,
- selecting the appropriate HTTP status code when applicable.

---

### 8.7 Exception Handling

Views should translate application exceptions into presentation-specific
responses.

Typical examples include:

- rendering Form errors,
- displaying user-friendly messages,
- returning HTTP 403 responses,
- returning HTTP 404 responses,
- returning HTTP 400 responses when appropriate.

Views should not expose internal application exceptions directly to users.

---

### 8.8 CRUD View Expectations

Although Django provides multiple view implementations, CRUD views should follow
a consistent orchestration pattern.

#### List Views

List Views should:

- retrieve collections through Selectors,
- support presentation-specific pagination and filtering,
- render the resulting collection.

#### Detail Views

Detail Views should:

- retrieve a single object through a Selector,
- render the resulting object,
- avoid embedding business logic.

#### Create Views

Create Views should:

- validate submitted Forms,
- construct the required Context,
- invoke a Service to create the resource,
- redirect upon success,
- display validation failures appropriately.

#### Update Views

Update Views should:

- retrieve the target resource through a Selector,
- validate submitted Forms,
- construct the required Context,
- invoke a Service to perform the update,
- redirect upon success.

#### Delete Views

Delete Views should:

- retrieve the target resource through a Selector,
- invoke a Service to perform deletion,
- redirect after successful deletion,
- avoid performing persistence operations directly.

---

### 8.9 Testing

Django View tests should verify presentation behavior rather than business
behavior.

Typical View tests include:

- authentication,
- authorization,
- template rendering,
- redirects,
- Form handling,
- Service invocation,
- Selector usage,
- success messages,
- exception translation.

Business rules should be verified through Service tests rather than View tests.

---

## 9. DRF ViewSet Contract

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

# 9.1 ViewSet Responsibilities

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

# 9.2 ViewSet Non-Responsibilities

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

# 9.3 API Request Lifecycle

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

# 9.4 Authentication Contract

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

# 9.5 Permission Contract

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

The second rule belongs to the Service Layer.

---

# 9.6 `get_queryset()` Contract

ViewSets MUST use Selectors for application data retrieval.

Preferred:

```python
def get_queryset(self):
    return JobApplicationSelector.list(
        user=self.request.user
    )
```

Avoid:

```python
def get_queryset(self):
    return JobApplication.objects.filter(
        owner=self.request.user
    )
```

when the filtering represents application access rules.

`get_queryset()` determines which data is exposed through the API.

It must not implement business logic.

---

# 9.7 Serializer Boundary

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

# 9.8 Serializer `create()` Contract

Serializer `create()` MUST NOT perform application persistence.

Prohibited:

```python
def create(self, validated_data):
    return Company.objects.create(
        **validated_data
    )
```

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

# 9.9 Serializer `update()` Contract

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

# 9.10 Base ViewSet Write Orchestration

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

# 9.11 Context-Based Service Invocation

Write operations should invoke Services using explicit Context objects.

The ViewSet is responsible for constructing the appropriate Context from the
request URL, route parameters, and other request metadata before delegating the
operation to the Service.

Example:

```python
context = CompanyChildContext(
    workspace_id=self.kwargs["workspace_id"],
    company_id=self.kwargs["company_id"],
)

return self.service.create(
    user=self.request.user,
    context=context,
    validated_data=serializer.validated_data,
)
```

Context objects should contain only the identifiers required to define the
execution scope of the operation.

Authenticated users should be supplied separately through the `user`
parameter.

ViewSets must not:

- Embed business rules into Context construction.
- Pass ORM model instances as Context values.
- Modify Context semantics.

---

# 9.12 Concrete ViewSet Responsibilities

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

# 9.13 `create()` and `update()` Contract

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

Example:

```python
def create(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    instance = self.service_create(
        validated_data=serializer.validated_data,
    )

    return Response(
        self.read_serializer(
            instance=instance, context=self.get_serializer_context()
        ).data,
        status=status.HTTP_201_CREATED,
    )
```

---

# 9.14 Context Construction Contract

ViewSets are responsible for creating Context objects required by Services.

Context information may come from:

- Request metadata.
- URL parameters.
- Existing resources.

Example:

```python
context = CompanyChildContext(
    id=self.object.pk,
    workspace_id=self.object.workspace.workspace_id,
    company_id=self.object.company.pk,
)
```

ViewSets must not:

- Add business decisions.
- Modify Context behavior.
- Use Contexts to hide application logic.

---

# 9.15 Response Contract

ViewSets are responsible for API response generation.

Responsibilities include:

- Selecting serializers.
- Returning status codes.
- Returning response headers.
- Handling pagination.
- Formatting API output.

Example:

```python
return Response(
    data,
    status=status.HTTP_201_CREATED,
)
```

ViewSets must not determine the meaning of application results.

---

# 9.16 Exception Translation Contract

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


Permission failure
        |
        v
HTTP 403 Forbidden


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

# 9.17 API Pagination Contract

Pagination is a Presentation Layer responsibility.

ViewSets may:

- Apply pagination classes.
- Format pagination metadata.
- Return paginated responses.

Selectors should provide query capability.

ViewSets should determine API representation.

---

# 9.18 API Filtering Contract

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

# 9.19 ViewSet Review Checklist

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

## 10. Exception Handling Contract

The Presentation Layer is responsible for translating application failures into
appropriate HTTP responses.

It does not determine whether an operation has failed; that responsibility
belongs to the Application Layer.

Presentation components should consistently translate application exceptions
into user-facing responses without exposing internal implementation details.

---

### 10.1 Responsibilities

The Presentation Layer is responsible for:

- Catching application exceptions.
- Translating exceptions into appropriate HTTP responses.
- Displaying user-friendly validation errors.
- Returning appropriate HTTP status codes.
- Displaying success and error messages where appropriate.
- Preventing internal exception details from reaching end users.

Business exceptions must never be ignored or silently suppressed.

---

### 10.2 Exception Ownership

Each architectural layer owns its own failures.

- Django and the framework raise framework exceptions.
- Selectors raise read-related application exceptions.
- Services raise business and write-related application exceptions.
- The Presentation Layer translates those exceptions into HTTP responses.

Presentation components should not redefine application failure semantics.

---

### 10.3 Framework Exceptions

Framework exceptions should be handled according to Django's standard behavior
unless the application explicitly defines an alternative presentation.

Examples include:

- HTTP 404 responses,
- permission failures,
- malformed requests,
- CSRF failures.

Framework behavior should remain predictable and consistent.

---

### 10.4 Selector Exceptions

Exceptions originating from Selectors represent failures to retrieve application
data.

Presentation components should translate these failures into the appropriate
presentation response.

Typical examples include:

- resource not found,
- inaccessible resource,
- unauthorized access.

Views should not attempt to recover by performing alternative queries.

---

### 10.5 Service Exceptions

Exceptions originating from Services represent application-level failures.

These may include:

- business rule violations,
- domain validation failures,
- invalid application state,
- write operation failures.

Presentation components should translate these exceptions into user-visible
errors without modifying their meaning.

---

### 10.6 Validation Errors

Transport validation and business validation are handled separately.

Transport validation failures originate from Forms (or Serializers).

Business validation failures originate from Services.

The Presentation Layer is responsible for presenting both types of validation
errors consistently.

---

### 10.7 User Feedback

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

### 10.8 Information Disclosure

Presentation components must not expose internal implementation details.

Examples include:

- stack traces,
- database errors,
- ORM exceptions,
- implementation-specific exception messages.

Unexpected exceptions should be logged appropriately while presenting generic
user-facing error responses.

---

### 10.9 Exception Consistency

The same application exception should produce the same presentation behavior
throughout the application.

Equivalent failures should always result in equivalent HTTP responses and
consistent user feedback.

Presentation components should avoid implementing endpoint-specific exception
behavior unless explicitly required.

---

### 10.10 Testing

Exception handling tests should verify that presentation components correctly
translate application failures.

Typical tests include:

- Service exceptions become user-visible validation errors.
- Selector exceptions become appropriate HTTP responses.
- Framework exceptions are handled consistently.
- Unexpected exceptions do not expose internal implementation details.
- Success and failure messages are displayed appropriately.

---

## 11. Testing Contract

Presentation Layer tests verify that presentation components correctly
coordinate HTTP requests and responses.

Their purpose is to ensure that Views, Forms, and other presentation
components fulfill their presentation responsibilities while delegating
business behavior to the appropriate application layer.

Presentation tests should focus on presentation behavior rather than business
logic.

---

### 11.1 Scope

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

### 11.2 Django View Tests

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

### 11.3 Form Tests

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

### 11.4 Isolation

Presentation Layer tests should remain independent of business logic whenever
possible.

When verifying orchestration behavior, Services and Selectors may be mocked to
confirm that presentation components invoke the correct application operations.

Business behavior should not be duplicated within Presentation Layer tests.

---

### 11.5 Exception Handling Tests

Presentation tests should verify that application exceptions are translated into
the correct presentation behavior.

Typical tests include:

- validation errors are displayed correctly,
- resource lookup failures produce the expected response,
- permission failures are presented consistently,
- unexpected exceptions do not expose internal implementation details.

---

### 11.6 Response Verification

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

### 11.7 Layer Separation

Presentation tests should verify that architectural boundaries are respected.

Presentation components should delegate:

- read operations to Selectors,
- write operations to Services,
- business validation to the Application Layer.

Presentation tests should avoid asserting implementation details belonging to
other architectural layers.

---

### 11.8 Test Coverage

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

## 12. Presentation Layer Checklist

Every Presentation Layer component should satisfy the following checklist before
being considered complete.

### General

- [ ] The component only implements presentation responsibilities.
- [ ] Business logic is delegated to the Application Layer.
- [ ] Architectural boundaries are respected.

### Read Operations

- [ ] Read operations are delegated to Selectors.
- [ ] Reusable query logic is not implemented in the Presentation Layer.
- [ ] Presentation-specific filtering, ordering, or pagination does not
      duplicate Selector responsibilities.

### Write Operations

- [ ] Write operations are delegated to Services.
- [ ] The Presentation Layer does not call `save()`, `delete()`, `create()`, or
      other ORM write operations directly.
- [ ] The required Context object is constructed before invoking the Service.

### Forms

- [ ] Forms perform transport-level validation only.
- [ ] Business validation is delegated to the Service Layer.
- [ ] Forms do not perform persistence operations.

### Django Views

- [ ] Authentication is enforced where required.
- [ ] Authorization is enforced where required.
- [ ] Forms are validated before invoking Services.
- [ ] Templates or redirects are generated appropriately.
- [ ] User-facing success and error messages are handled consistently.

### Exception Handling

- [ ] Application exceptions are translated into appropriate presentation
      responses.
- [ ] Internal implementation details are not exposed to end users.
- [ ] Exception handling follows the project's shared exception handling
      mechanism.

### Testing

- [ ] Presentation tests verify presentation behavior only.
- [ ] Business behavior is verified by Service tests.
- [ ] View tests verify Selector and Service orchestration.
- [ ] Form tests verify transport validation only.
