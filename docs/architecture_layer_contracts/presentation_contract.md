# Presentation Layer Contract

1. Purpose
2. Architectural Principles
3. Layer Responsibilities
4. Layer Boundaries
5. Request Lifecycle
6. Forms Contract
7. Django View Contract
8. DRF ViewSet Contract
9. Template Contract
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

# 4. Layer Boundaries

The Presentation Layer has strict boundaries that define which responsibilities
belong inside and outside this layer.

These boundaries prevent business behavior, persistence logic, and application
rules from leaking into HTTP-facing components.

The rules below apply to all Presentation Layer components, including:

- Django Views.
- Django Class-Based Views.
- DRF Views.
- DRF ViewSets.
- Forms.
- Serializers.
- Presentation mixins.
- Presentation helpers.

---

## 4.1 Business Logic Boundary

The Presentation Layer MUST NOT implement business logic.

Presentation components must not:

- Apply business rules.
- Enforce domain invariants.
- Decide whether operations are allowed.
- Implement workflows involving domain entities.
- Duplicate logic already implemented by Services.

Business decisions belong to the Application Layer.

Example of prohibited behavior:

```python
if company.owner == request.user:
    company.status = "approved"
```

The View should delegate this decision to the appropriate Service.

---

## 4.2 Persistence Boundary

The Presentation Layer MUST NOT modify persistent state directly.

Presentation components must not:

- Create model instances directly.
- Update model instances directly.
- Delete model instances directly.
- Call model persistence methods such as `save()` or `delete()`.
- Perform database writes directly.

All write operations must be delegated to Services.

Correct flow:

```text
View
 |
 | validated input
 v
Service
 |
 | persistence
 v
ORM
```

The Presentation Layer coordinates the operation but does not own persistence.

---

## 4.3 Data Retrieval Boundary

Application data retrieval must be delegated to Selectors.

Presentation components must not:

- Execute ORM queries directly.
- Duplicate ownership filtering.
- Duplicate reusable retrieval logic.
- Reimplement Selector behavior.

Selectors are responsible for application-level retrieval rules.

Presentation components may use already retrieved objects for response
generation or presentation purposes.

Examples where Selectors should be used:

- Loading objects for detail, update, and delete operations.
- Populating form field querysets.
- Providing API lookup data.

Example:

```python
form.fields["documents"].queryset = DocumentSelector.list(
    user=request.user
)
```

---

## 4.4 Service Boundary

The Presentation Layer MUST interact with Services only through their public
contract.

Presentation components are responsible for:

1. Preparing validated input.
2. Constructing required Context objects.
3. Calling the appropriate Service operation.
4. Translating the result into a response.

Presentation components must not:

- Access Service internal implementation details.
- Reproduce Service validation.
- Bypass Services for write operations.
- Modify application behavior from the presentation layer.

Services own application behavior and write workflows.

---

## 4.5 Selector Boundary

The Presentation Layer MUST use Selectors for application read operations.

Presentation components must not:

- Replace Selector logic with direct ORM queries.
- Encode ownership enforcement rules.
- Implement reusable filtering behavior.
- Implement application-level retrieval decisions.

Selectors answer:

> "What data should the application retrieve?"

Presentation components answer:

> "How should retrieved data be presented?"

---

## 4.6 Context Boundary

The Presentation Layer is responsible for constructing Context objects
required by the Application Layer.

Presentation components may:

- Extract identifiers from URLs.
- Extract request-related information.
- Collect request metadata.
- Construct Context instances before Service invocation.

Context objects represent execution scope only.

Presentation components must not:

- Add business rules into Context creation.
- Modify Context behavior.
- Use Context objects as a replacement for Services.

---

## 4.7 Validation Boundary

Validation responsibilities must remain separated.

Forms and Serializers are responsible for:

- Parsing input.
- Validating input structure.
- Validating transport-level requirements.
- Providing normalized input data.

Services are responsible for:

- Business validation.
- Ownership validation.
- Workspace validation.
- Cross-model validation.
- Domain rules.
- State transition rules.

Example:

A Form or Serializer may validate:

```python
email = serializers.EmailField()
```

A Service validates:

```text
This email belongs to the current workspace.
```

Transport validation and business validation are separate responsibilities.

---

## 4.8 Exception Boundary

The Presentation Layer is responsible for translating application exceptions
into client-facing responses.

Expected application validation failures may be converted into presentation
feedback.

Examples:

```text
ValidationError
        |
        v
Form validation error
```

```text
BusinessRuleViolationError
        |
        v
User-visible validation message
```

The Presentation Layer must not:

- Hide unexpected application failures.
- Convert failures into successful responses.
- Silently ignore exceptions.

Unexpected application and infrastructure failures should propagate to the
appropriate exception handler.

---

## 4.9 Dependency Direction Boundary

Dependencies MUST flow toward the Application Layer.

Allowed dependency direction:

```text
Presentation
      |
      v
Application
      |
      v
Infrastructure
```

The Presentation Layer may depend on:

- Services.
- Selectors.
- Context objects.
- Forms.
- Serializers.

The Application Layer must not depend on:

- Views.
- Templates.
- HTTP requests.
- DRF responses.
- Presentation-specific concepts.

The Application Layer must remain independent from HTTP delivery.

---

## 4.10 Code Duplication Boundary

The Presentation Layer MUST NOT become a second location for application
behavior.

Repeated logic across:

- Views.
- Forms.
- Serializers.
- ViewSets.

should be evaluated for extraction into:

- Services.
- Selectors.
- Context objects.
- Other application-level abstractions.

Repeated presentation logic often indicates misplaced responsibility.

---

## 4.11 Review Rule

During code review, Presentation Layer code that makes business decisions
should be considered a boundary violation until proven otherwise.

The default assumptions are:

- Views coordinate.
- Forms and Serializers validate transport input.
- Selectors retrieve data.
- Services implement application behavior.
- ORM persists data.

A Presentation Layer component should explain:

> "How does this request become an application operation?"

It should not explain:

> "How does the business operation work?"

---

# 5. Request Lifecycle

The Presentation Layer follows a defined lifecycle for transforming an incoming
request into an application operation and returning an appropriate response.

The lifecycle applies to all presentation entry points, including:

- Django Views.
- Django Class-Based Views.
- DRF Views.
- DRF ViewSets.

The concrete implementation may differ between HTML and API interfaces, but the
responsibility boundaries remain the same.

---

## 5.1 Request Lifecycle Overview

A request should follow this lifecycle:

```text
HTTP Request
      |
      v
Authentication
      |
      v
Endpoint Authorization
      |
      v
Input Parsing
      |
      v
Transport Validation
      |
      v
Context / Filter Construction
      |
      v
Application Layer Invocation
      |
      v
Result Handling
      |
      v
Exception Translation
      |
      v
HTTP Response
```

Each stage has a specific responsibility and must not replace responsibilities
belonging to another layer.

---

## 5.2 Stage 1 — Request Reception

The Presentation Layer receives the incoming request and extracts the
transport-specific information required for the requested operation.

This includes:

- URL parameters.
- Query parameters.
- Form data.
- Request body data.
- Uploaded files.
- Authenticated user information.

The Presentation Layer should only interpret information required to execute the
requested application operation.

It must not make business decisions during request processing.

---

## 5.3 Stage 2 — Authentication

Authentication is responsible for identifying the requester.

The Presentation Layer consumes authentication information provided by the
framework.

Examples include:

- Session authentication.
- Token authentication.
- JWT authentication.

The authenticated user should be passed explicitly to Selectors and Services.

Authentication information should not be embedded inside Context objects.

Authentication determines:

> "Who is making this request?"

It does not determine whether the requested operation is valid.

---

## 5.4 Stage 3 — Endpoint Authorization

The Presentation Layer may enforce endpoint-level authorization.

Examples include:

- Requiring authentication.
- Checking framework permissions.
- Restricting access to specific endpoints.

Endpoint authorization determines:

> "Can this user access this endpoint?"

It does not replace application-level authorization.

Application authorization belongs to the Application Layer.

Example:

Presentation authorization:

```text
User may access company editing endpoints.
```

Application authorization:

```text
User owns this specific company.
```

---

## 5.5 Stage 4 — Input Parsing

The Presentation Layer parses incoming request data.

Examples:

HTML interfaces:

- Form data.
- URL parameters.
- Query parameters.

API interfaces:

- JSON payloads.
- Query parameters.
- Path parameters.

Parsing converts transport-specific input into structured data suitable for
validation.

Parsing must not contain business interpretation.

---

## 5.6 Stage 5 — Transport Validation

Forms and Serializers validate transport-level requirements.

Responsibilities include:

- Required fields.
- Data types.
- Formatting.
- Field constraints.
- Serialization rules.

Example:

Valid:

```text
Email must have a valid email format.
```

Not valid in this layer:

```text
Email must belong to the same company as the application.
```

Business validation belongs to Services.

---

## 5.7 Stage 6 — Context and Filter Construction

Before invoking the Application Layer, the Presentation Layer constructs the
required application inputs.

For write operations this includes:

- Context objects.
- Validated input data.

For read operations this includes:

- QueryFilter objects.
- Resource identifiers.

Context objects describe execution scope.

Examples:

- workspace_id.
- company_id.
- job_position_id.
- application_id.

The Presentation Layer constructs these objects but does not place business
logic inside them.

---

## 5.8 Stage 7 — Application Layer Invocation

After input preparation, the Presentation Layer delegates the operation to the
appropriate Application Layer component.

Read operations:

```text
View
 |
 | user
 | QueryFilter
 v
Selector
 |
 v
Result
```

Write operations:

```text
View
 |
 | user
 | Context
 | validated_data
 v
Service
 |
 v
Result
```

The Presentation Layer must not perform additional business processing after
delegation.

---

## 5.9 Stage 8 — Result Handling

The Presentation Layer converts application results into external responses.

For HTML interfaces this may include:

- Selecting templates.
- Preparing template context.
- Redirecting after successful operations.
- Displaying user feedback.

For APIs this may include:

- Serializing response data.
- Selecting HTTP status codes.
- Returning JSON responses.
- Handling pagination metadata.

The Presentation Layer decides how results are represented externally.

It does not determine their business meaning.

---

## 5.10 Stage 9 — Exception Translation

Application exceptions must be translated into appropriate delivery-specific
responses.

The general flow is:

```text
Application Exception
        |
        v
Presentation Translation
        |
        v
HTTP Response
```

Examples:

```text
ValidationError
        |
        v
Form validation feedback
```

```text
ResourceNotFoundError
        |
        v
HTTP 404
```

```text
AccessDeniedError
        |
        v
HTTP 403
```

```text
DomainInvariantViolationError
        |
        v
HTTP 400
```

Exception translation should be centralized through reusable presentation
components such as:

- View exception handler mixins.
- DRF exception handlers.
- Middleware.

Views and ViewSets should avoid duplicating exception translation logic.

---

## 5.11 Stage 10 — Response Delivery

The Presentation Layer returns the final response.

Responses may include:

- HTML.
- JSON.
- Redirect responses.
- Status codes.
- Headers.
- Cookies.

After response delivery, the Presentation Layer lifecycle is complete.

---

## 5.12 Lifecycle Invariants

The following invariants must always hold.

---

### Invariant 1 — Business Behavior Executes Outside the Presentation Layer

Presentation components coordinate operations but never implement business
behavior.

---

### Invariant 2 — Writes Are Delegated to Services

Persistent state changes must always flow through Services.

---

### Invariant 3 — Reads Are Delegated to Selectors

Reusable retrieval logic and ownership-aware querying must remain inside
Selectors.

---

### Invariant 4 — Application Code Remains Independent From HTTP

The Application Layer must not know:

- Which HTTP framework is used.
- Which endpoint triggered the operation.
- Whether the caller is a browser or API client.

---

### Invariant 5 — Presentation Components Share Application Behavior

The same operation must have identical business behavior regardless of whether
it is triggered through:

- Django Views.
- DRF ViewSets.
- Background workers.
- Other application entry points.

---

# 6. Forms Contract

Django Forms belong to the Presentation Layer and are responsible for
processing external input before invoking the Application Layer.

Forms create a boundary between transport data and application operations.

Forms answer:

> "Is this input structurally valid and suitable for submission?"

Forms do not answer:

> "Is this operation allowed according to business rules?"

Business validation and application behavior remain the responsibility of
Services.

---

## 6.1 Form Responsibilities

Forms are responsible for:

- Receiving user-submitted input.
- Parsing submitted data.
- Normalizing input values.
- Validating input structure.
- Validating field formats.
- Providing user-facing validation errors.
- Producing cleaned input data for the Application Layer.

Examples of Form responsibilities:

- Required fields.
- Maximum length validation.
- Date formatting.
- Email formatting.
- Choice validation.
- File validation.
- Input normalization.

---

## 6.2 Form Non-Responsibilities

Forms MUST NOT:

- Implement business rules.
- Execute application workflows.
- Modify persistent state directly.
- Call `save()` to perform domain operations.
- Replace Service validation.
- Enforce ownership rules.
- Enforce workspace boundaries.
- Perform business-level cross-model validation.

Forms prepare input.

Services execute application behavior.

---

## 6.3 Form Validation Boundary

Form validation must remain limited to presentation-level concerns.

Allowed validation:

```python
class CompanyForm(forms.Form):
    name = forms.CharField(
        max_length=255
    )
```

This validates:

- Input existence.
- Input type.
- Input constraints.

Not allowed:

```python
def clean_name(self):
    if Company.objects.filter(
        name=self.cleaned_data["name"]
    ).exists():
        raise ValidationError(
            "Company already exists."
        )
```

when the rule represents application behavior.

The correct flow is:

```text
Form
 |
 | cleaned_data
 v
Service
 |
 | business validation
 v
Application result
```

---

## 6.4 Form `clean()` Contract

The `clean()` method may validate relationships between submitted fields when
the validation only concerns the submitted data itself.

Example:

```python
def clean(self):
    cleaned_data = super().clean()

    start_date = cleaned_data.get("start_date")
    end_date = cleaned_data.get("end_date")

    if start_date and end_date and start_date > end_date:
        raise ValidationError(
            "End date must occur after start date."
        )

    return cleaned_data
```

This is acceptable because it validates input consistency.

The `clean()` method must not:

- Query application state.
- Check ownership.
- Verify permissions.
- Determine whether an operation is allowed.
- Execute application workflows.
- Replace Service validation.

---

## 6.5 Form Data Retrieval Boundary

Forms may require application data for presentation purposes.

When application retrieval logic is required, Forms should obtain that data
through Selectors.

Forms must not:

- Duplicate Selector filtering logic.
- Perform ownership-aware queries directly.
- Query application state to enforce business rules.
- Reimplement application retrieval behavior.

Valid examples include:

- Populating `ModelChoiceField` querysets.
- Limiting available user selections.
- Loading selectable related resources.

Example:

```python
form.fields["documents"].queryset = DocumentSelector.list(
    user=request.user
)
```

The Selector remains responsible for application-level retrieval rules.

---

## 6.6 Form Saving Contract

Forms MUST NOT directly persist application entities.

The following patterns are prohibited for domain operations:

```python
form.save()
```

```python
instance.save()
```

inside Form logic.

Application state changes must follow:

```text
Form
 |
 | cleaned_data
 v
Service
 |
 | persistence
 v
ORM
```

The Service Layer owns persistence decisions.

---

## 6.7 Form and Service Interaction

The recommended interaction pattern is:

```text
HTTP Request
      |
      v
Form
      |
      | cleaned_data
      v
Context Construction
      |
      v
Service
      |
      v
HTTP Response
```

The Form should not know:

- Which Service implementation performs the operation.
- How persistence works.
- Which business rules are executed.

The View coordinates the interaction between the Form and Service.

---

## 6.8 Form Initialization Contract

Forms may receive presentation-related initialization data.

Examples:

- Initial values.
- Available choices.
- UI configuration.
- Field visibility configuration.
- Presentation-specific options.

Forms may receive model instances or application objects when required for
presentation purposes.

Example:

```python
CompanyForm(
    initial={
        "name": company.name
    }
)
```

However, Forms must not use provided objects to implement business logic.

Not allowed:

```python
CompanyForm(
    company=company
)
```

if the purpose is to decide whether the operation is allowed.

---

## 6.9 Dynamic Fields Contract

Forms may dynamically modify fields when the behavior is presentation-related.

Examples:

- Removing fields from the UI.
- Adjusting labels.
- Adjusting help text.
- Configuring available choices.
- Limiting selectable options.

Dynamic field behavior may improve user experience.

Example:

```python
if not user.is_admin:
    self.fields.pop("internal_notes")
```

However, dynamic fields must not replace authorization.

Incorrect:

```python
if user.is_admin:
    allow_company_deletion = True
```

Authorization and business permissions remain the responsibility of the
appropriate application layer.

---

## 6.10 Form Error Handling Contract

Forms are responsible for presenting input validation errors.

Forms should:

- Provide clear validation messages.
- Associate errors with fields when possible.
- Return normalized validation failures.

Forms must not:

- Hide Service failures.
- Convert business failures into fake input errors.
- Duplicate application exception handling.

Service exceptions should be translated by the Presentation Layer.

Example:

```text
Service
 |
 | BusinessRuleViolationError
 v
Presentation Error Handling
 |
 v
Form Error
```

Reusable mechanisms such as `ServiceFormErrorMixin` should handle this
translation consistently.

---

## 6.11 ModelForm Contract

`ModelForm` may be used when a form represents a simple mapping between
presentation input and model fields.

Using `ModelForm` does not move application responsibility into the Form.

`ModelForm` must not:

- Bypass Services.
- Persist domain entities directly.
- Implement business workflows.
- Replace Service validation.
- Enforce application invariants.

The preferred pattern remains:

```text
ModelForm
      |
      | cleaned_data
      v
Service
      |
      v
ORM
```

---

## 6.12 Form Review Checklist

During code review, Forms should be checked against the following questions:

- Does the Form only validate presentation input?
- Does the Form avoid business decisions?
- Does the Form avoid direct persistence?
- Does the Form avoid duplicating Service validation?
- Does the Form avoid duplicating Selector behavior?
- Are application operations delegated to Services?
- Are dynamic fields used only for presentation purposes?

If a Form answers "yes" to any of the following:

- "Should this rule apply outside this Form?"
- "Does this require domain knowledge?"
- "Does this determine whether an operation is allowed?"

then the responsibility likely belongs outside the Form.

---

# 7. Django View Contract

Django Views belong to the Presentation Layer and are responsible for
translating HTTP requests into Application Layer operations.

A Django View coordinates:

- HTTP request handling.
- Authentication.
- Authorization.
- Form processing.
- Context construction.
- Selector invocation.
- Service invocation.
- HTTP response generation.

A Django View is an orchestration component.

A View should answer:

> "Which application operation should happen for this request?"

A View should not answer:

> "How does the business operation work?"

Business behavior belongs to the Application Layer.

---

# 7.1 View Responsibilities

Django Views are responsible for:

- Receiving HTTP requests.
- Handling HTTP methods.
- Performing request-level authentication checks.
- Performing request-level authorization checks.
- Creating and processing Forms.
- Constructing Application Context objects.
- Invoking Selectors for application reads.
- Invoking Services for application writes.
- Preparing presentation data.
- Returning HTTP responses.

Views coordinate application operations but do not implement them.

---

# 7.2 View Non-Responsibilities

Django Views MUST NOT:

- Implement business rules.
- Modify persistent application state directly.
- Call ORM write operations.
- Replace Service validation.
- Replace Selector access rules.
- Implement domain workflows.
- Enforce domain invariants.
- Duplicate Application Layer behavior.

A View is not an alternative location for application logic.

---

# 7.3 HTTP Responsibility Boundary

Views own HTTP-specific concerns.

Examples of View responsibilities:

- Reading request data.
- Reading URL parameters.
- Reading query parameters.
- Handling HTTP methods.
- Selecting templates.
- Returning redirects.
- Returning JSON responses.
- Selecting HTTP status codes.
- Setting response headers.

Examples of non-View responsibilities:

```text
Determining whether a company can be deleted.
        |
        v
Service
```

```text
Determining whether a document belongs to a workspace.
        |
        v
Selector / Service
```

```text
Determining application state transitions.
        |
        v
Service
```

---

# 7.4 Read Operation Contract

Read operations MUST use Selectors when application retrieval logic is
required.

The expected flow is:

```text
HTTP Request
      |
      v
View
      |
      v
Selector
      |
      v
Presentation Context
      |
      v
HTTP Response
```

The View may:

- Provide request information.
- Provide filtering parameters.
- Apply pagination.
- Prepare template context.

The View must not:

- Duplicate Selector filtering logic.
- Implement ownership checks.
- Encode reusable retrieval rules.
- Construct application QuerySets directly.

Selectors define application data retrieval.

---

# 7.5 Presentation Data Retrieval Contract

Views may retrieve additional data required only for presentation purposes.

Examples:

- Navigation data.
- Breadcrumb information.
- Template metadata.
- Related display information.
- UI-specific selection options.

Presentation retrieval MUST:

- Use Selectors when application data is involved.
- Respect access restrictions.
- Avoid modifying application state.
- Avoid implementing business decisions.

Example:

```python
company = CompanySelector.get(
    user=request.user,
    obj_id=company_id,
)

context = {
    "company": company,
    "workspace_id": company.workspace.workspace_id,
}
```

The View prepares presentation data.

It does not determine application behavior.

---

# 7.6 Write Operation Contract

Write operations MUST use Services.

The expected flow is:

```text
HTTP Request
      |
      v
View
      |
      v
Form
      |
      v
Context
      |
      v
Service
      |
      v
HTTP Response
```

The View responsibilities are:

1. Receive submitted input.
2. Validate transport data.
3. Construct Context objects.
4. Invoke the Service.
5. Translate the result into an HTTP response.

The View must not perform persistence directly.

---

# 7.7 `form_valid()` Contract

`form_valid()` is an orchestration point for successful Form validation.

Allowed:

```python
def form_valid(self, form):

    context = CompanyChildContext(
        workspace_id=self.object.workspace.workspace_id,
        company_id=self.object.pk,
    )

    CompanyService.create(
        user=self.request.user,
        context=context,
        validated_data=form.cleaned_data,
    )

    return redirect(self.success_url())
```

The View coordinates the operation.

The View must not:

```python
def form_valid(self, form):

    Company.objects.create(
        name=form.cleaned_data["name"]
    )
```

because persistence belongs to Services.

---

# 7.8 `get_form()` Contract

`get_form()` may customize Forms for presentation requirements.

Allowed responsibilities:

- Providing initial values.
- Adjusting field visibility.
- Removing presentation-only fields.
- Adjusting labels or help text.
- Populating choices through Selectors.

Example:

```python
def get_form(self, form_class=None):

    form = super().get_form(form_class)

    form.fields["documents"].queryset = DocumentSelector.list(
        user=self.request.user
    )

    return form
```

`get_form()` must not:

- Perform business validation.
- Determine whether an operation is allowed.
- Replace Service validation.
- Enforce domain rules.

---

# 7.9 `dispatch()` Contract

`dispatch()` handles request-level concerns before view execution.

Allowed responsibilities:

- Authentication checks.
- Permission checks.
- HTTP method restrictions.
- Request initialization.
- Shared exception translation.

Example:

```python
def dispatch(self, request, *args, **kwargs):

    if not request.user.is_authenticated:
        return redirect("login")

    return super().dispatch(
        request,
        *args,
        **kwargs,
    )
```

`dispatch()` must not:

- Execute application workflows.
- Perform business operations.
- Replace Service authorization.
- Load unnecessary application data.

---

# 7.10 `get_queryset()` Contract

`get_queryset()` should delegate application retrieval to Selectors when
retrieval rules exist.

Preferred:

```python
def get_queryset(self):

    return JobPositionSelector.list(
        user=self.request.user,
        filters=filters,
    )
```

Avoid:

```python
def get_queryset(self):

    return JobPosition.objects.filter(
        company_id=self.kwargs["company_id"]
    )
```

when the query represents reusable application behavior.

`get_queryset()` defines what data is displayed.

It does not define how application access rules work.

---

# 7.11 Object Retrieval Contract

Views should not directly retrieve application objects when access rules are
required.

Avoid:

```python
company = Company.objects.get(
    id=self.kwargs["pk"]
)
```

when retrieval requires:

- Ownership checks.
- Workspace restrictions.
- Permission rules.
- Application filtering.

Instead:

```python
company = CompanySelector.get(
    user=request.user,
    obj_id=self.kwargs["pk"],
)
```

Selectors provide controlled application data access.

---

# 7.12 Context Construction Contract

Views are responsible for constructing Application Context objects.

Context construction should happen immediately before Service invocation.

Example:

```python
context = CompanyChildContext(
    id=self.object.pk,
    workspace_id=self.object.company.workspace.workspace_id,
    company_id=self.object.company.pk,
)
```

Views must not:

- Add business decisions during construction.
- Modify Context behavior.
- Use Context objects as a replacement for Services.

Context objects represent execution scope only.

---

# 7.13 Success and Redirect Handling

Views are responsible for choosing the HTTP response after successful
operations.

Examples:

- Redirecting after creation.
- Rendering success pages.
- Returning serialized responses.
- Displaying messages.

The View may decide:

```text
After creating a company:
redirect to company details.
```

The View must not decide:

```text
A company becomes active after creation.
```

The second decision belongs to the Service Layer.

---

# 7.14 Failure Handling

Views translate application failures into presentation responses.

Example:

```text
BusinessRuleViolationError
        |
        v
HTTP 400 Response
```

Views should:

- Preserve application error meaning.
- Convert failures into appropriate HTTP responses.

Views must not:

- Ignore application failures.
- Return success after failed operations.
- Duplicate Service validation.

---

# 7.15 Class-Based View Guidelines

Class-Based Views should keep overridden methods focused.

Preferred responsibilities:

```text
dispatch()
    |
authentication / authorization


get_queryset()
    |
selector invocation


get_form()
    |
form customization


form_valid()
    |
service invocation


get_context_data()
    |
presentation preparation
```

A Class-Based View should remain an orchestration layer.

---

# 7.16 View Composition Rule

When multiple Views share behavior, the behavior should be extracted into the
appropriate layer.

Possible destinations:

- Service.
- Selector.
- Form helper.
- Context object.
- Permission component.
- Presentation utility.

Duplicating application behavior between Views is prohibited.

---

# 7.17 Presentation Helper Contract

Presentation helper functions belong to the Presentation Layer.

They exist to support HTTP representation and user interface composition.

Examples:

- URL builders.
- Navigation builders.
- Template context builders.
- Display formatting helpers.
- Presentation-only transformations.

Presentation helpers MAY:

- Build URLs.
- Format values.
- Prepare template structures.
- Transform application results into display structures.

Example:

```python
def company_list_url(workspace_id):

    return reverse(
        "company-list-web",
        kwargs={
            "workspace_id": workspace_id,
        },
    )
```

Incorrect:

```python
def can_delete_company(company):

    return not company.job_applications.exists()
```

Correct:

```python
CompanyService.remove(...)
```

Presentation helpers must not contain application behavior.

---

# 7.18 Django View Review Checklist

During code review, verify:

- Does the View only coordinate operations?
- Are reads delegated to Selectors?
- Are writes delegated to Services?
- Are Context objects constructed correctly?
- Is business logic absent?
- Are Forms limited to transport validation?
- Are exceptions translated correctly?
- Are HTTP concerns contained inside the View?
- Are reusable behaviors extracted into appropriate layers?

A compliant Django View should reveal the application flow without requiring
knowledge of business rules.

The View should explain:

> "How does this HTTP request become an application operation?"

It should not explain:

> "How does the business operation work?"

---

## 8. DRF ViewSet Contract

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

# 8.1 ViewSet Responsibilities

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

# 8.2 ViewSet Non-Responsibilities

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

# 8.3 API Request Lifecycle

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

# 8.4 Authentication Contract

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

# 8.5 Permission Contract

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

# 8.6 `get_queryset()` Contract

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

# 8.7 Serializer Boundary

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

# 8.8 Serializer `create()` Contract

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

# 8.9 Serializer `update()` Contract

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

# 8.10 Base ViewSet Write Orchestration

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

# 8.11 Context-Based Service Invocation

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

# 8.12 Concrete ViewSet Responsibilities

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

# 8.13 `create()` and `update()` Contract

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

# 8.14 Context Construction Contract

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

# 8.15 Response Contract

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

# 8.16 Exception Translation Contract

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

# 8.17 API Pagination Contract

Pagination is a Presentation Layer responsibility.

ViewSets may:

- Apply pagination classes.
- Format pagination metadata.
- Return paginated responses.

Selectors should provide query capability.

ViewSets should determine API representation.

---

# 8.18 API Filtering Contract

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

# 8.19 ViewSet Review Checklist

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

## 9. Template Contract



---

## 10. Exception Handling Contract

The Presentation Layer is responsible for translating Application Layer
exceptions into appropriate user-facing responses.

Exception handling follows the same separation of concerns as the rest of the
architecture:

- Services define application failures.
- Selectors may raise retrieval-related failures.
- Presentation components translate failures into HTTP responses.
- Clients receive transport-specific representations.

The Presentation Layer must not redefine the meaning of application errors.

---

## 10.1 Exception Ownership

Each layer owns different aspects of exception handling.

### Application Layer

The Application Layer is responsible for:

- Detecting business rule violations.
- Detecting access violations.
- Detecting missing application resources.
- Raising application-specific exceptions.
- Providing meaningful error messages for translation.

Examples:

```text
CompanyAccessDeniedError

DocumentOwnershipViolationError

InvalidApplicationStateError
```

The Application Layer answers:

> "Why did this operation fail?"

---

### Presentation Layer

The Presentation Layer is responsible for:

- Catching application exceptions where appropriate.
- Translating exceptions into HTTP responses.
- Displaying user-friendly error messages.
- Returning correct status codes.

The Presentation Layer answers:

> "How should this failure be communicated externally?"

---

## 10.2 Exception Translation Boundary

Application exceptions MUST NOT leak directly to clients.

The flow should be:

```text
Application Exception
        |
        v
Presentation Translation
        |
        v
HTTP Response
```

Example:

```text
BusinessRuleViolationError
        |
        v
HTTP 400 Bad Request
```

The client should understand the response.

The client should not need to understand internal application exceptions.

---

## 10.3 Business Exception Contract

Business failures should be represented using application-level exceptions.

Examples:

```python
raise BusinessRuleViolationError(
    "A job application cannot be closed."
)
```

The Service Layer owns when this exception occurs.

The View or ViewSet owns how this exception is exposed.

---

## 10.4 Validation Exception Contract

Validation failures must be separated by responsibility.

### Transport Validation

Owned by:

- Forms.
- Serializers.

Examples:

```text
Invalid email format.

Missing required field.

Incorrect date format.
```

---

## 10.5 Django View Exception Handling

Exception translation should preferably be centralized through reusable
presentation components.

Examples include:

- View mixins.
- Middleware.
- Shared exception handlers.

Individual Views should generally allow Application Layer exceptions to
propagate to the shared translation mechanism.

Example:

```text
Service
      |
      v
BusinessRuleViolationError
      |
      v
ViewExceptionHandlerMixin
      |
      v
HTTP Response
```

Views should only catch exceptions locally when a presentation-specific response
cannot be provided through the shared translation mechanism, such as attaching
an error to a submitted Form.

Exception translation should remain consistent across all Views.

### 10.5.1 Form-Based Service Validation Translation

HTML form-based write operations must translate recoverable application
validation failures back into form errors.

Recoverable validation failures include:

- `django.core.exceptions.ValidationError`
- `BusinessRuleViolationError`

These exceptions indicate that the submitted data cannot be accepted but that
the user may correct the input and try again.

Views should attach the validation messages to the appropriate form fields and
redisplay the form.

Example:

```python
try:
    service.update(
        user=self.request.user,
        context=context,
        validated_data=form.cleaned_data,
    )

except (ValidationError, BusinessRuleViolationError) as exc:
    self.add_service_errors_to_form(
        form=form,
        exception=exc,
    )

    return self.form_invalid(form)
```

---

## 10.6 DRF ViewSet Exception Handling

API exception translation should preferably be centralized through reusable DRF
exception handling mechanisms.

Examples include:

- DRF exception handlers.
- Shared API mixins.
- Common ViewSet infrastructure.

Concrete ViewSets should generally allow Application Layer exceptions to
propagate rather than translating them individually.

This ensures that identical application failures produce consistent API
responses across all endpoints.

---

## 10.7 Global Exception Handling

When possible, exception translation SHOULD be centralized.

Examples:

- Django middleware.
- Shared View mixins.
- DRF exception handlers.
- Shared presentation utilities.

Centralized translation prevents inconsistent API and web behavior.

Example:

```text
BusinessRuleViolationError
        |
        +----------------+
        |                |
        v                v

HTML Response       JSON Response
```

Both responses represent the same application failure.

---

## 10.8 Exception Mapping Contract

The Presentation Layer should maintain predictable mappings.

Example:

| Application Failure | HTTP Response |
| --- | --- |
| Authentication failure | 401 Unauthorized |
| Permission failure | 403 Forbidden |
| Missing resource | 404 Not Found |
| Invalid input | 400 Bad Request |
| Business rule violation | 400 Bad Request |
| Conflict with existing state | 409 Conflict |
| Unexpected failure | 500 Internal Server Error |

The exact mapping should be defined by the application and remain consistent
across all Presentation Layer entry points.

---

## 10.9 Exception Messages Contract

User-facing messages should be:

- Understandable.
- Actionable.
- Appropriate for the client.

Messages should not expose:

- Database details.
- Internal implementation details.
- Stack traces.
- Sensitive application information.

Example:

Acceptable:

```text
You cannot delete this company because it has active applications.
```

Not acceptable:

```text
Foreign key constraint failed on table company_job_application.
```

---

## 10.10 Exception Logging Contract

The Presentation Layer should not silently consume unexpected exceptions.

Unexpected failures should:

- Be logged.
- Preserve debugging information.
- Be handled by the application's error reporting system.

The Presentation Layer should avoid:

```python
except Exception:
    return error_response()
```

unless the exception is intentionally handled and logged.

Expected application exceptions should generally not be logged as unexpected
errors.

Only unexpected failures should produce error-level logs.

---

## 10.11 Exception Flow Invariants

The following rules must always hold:

### Invariant 1 — Services Own Business Failures

Views and ViewSets must not create business exceptions.

---

### Invariant 2 — Presentation Owns HTTP Translation

Services must not return:

- HTTP responses.
- Redirects.
- JSON payloads.
- Template responses.

---

### Invariant 3 — Same Failure, Same Meaning

The same application exception should represent the same business failure
regardless of whether the operation was triggered through:

- Django Views.
- DRF ViewSets.
- Background tasks.
- Management commands.

---

### Invariant 4 — Exceptions Must Not Become Control Flow

Exceptions should represent exceptional failures.

They should not replace normal application decisions.

---

## 10.12 Exception Handling Review Checklist

During code review, verify:

- Are business failures raised from Services?
- Are HTTP responses created only in the Presentation Layer?
- Are Forms and Serializers limited to transport validation?
- Are exceptions translated consistently?
- Are internal details hidden from clients?
- Are unexpected exceptions logged?
- Are View and ViewSet exception handlers free of business logic?

A compliant exception handling design preserves the separation between:

- Application meaning.
- Presentation communication.

---

## 11. Testing Contract

The Presentation Layer must be tested according to its responsibilities.

Presentation tests should verify that HTTP requests are correctly translated
into Application Layer operations and that application results are correctly
translated into HTTP responses.

Presentation tests must not become a replacement for Application Layer tests.

The purpose of Presentation tests is:

> "Does this HTTP boundary correctly communicate with the application?"

The purpose of Service tests is:

> "Does the application behavior work correctly?"

---

# 11.1 Testing Responsibilities by Layer

Each layer should test its own responsibilities.

| Layer | Primary Testing Responsibility |
| --- | --- |
| Views | HTTP orchestration and responses |
| ViewSets | API orchestration and responses |
| Forms | Input parsing and transport validation |
| Serializers | API input/output validation |
| Services | Business behavior |
| Selectors | Data retrieval behavior |

Tests should remain aligned with these boundaries.

---

# 11.2 View Testing Contract

Django View tests should verify:

- Correct HTTP methods are accepted.
- Authentication requirements work.
- Authorization requirements work.
- Correct Forms are used.
- Correct Services are invoked.
- Correct Selectors are invoked.
- Correct responses are returned.
- Redirect behavior works.
- Template rendering works.

Example:

```text
POST /companies/create/

        |
        v

CompanyForm

        |
        v

CompanyService.create()

        |
        v

HTTP Redirect
```

The test should verify the orchestration flow.

---

# 11.3 View Tests MUST NOT Test Business Logic

View tests should not verify:

- Complex business rules.
- Domain invariants.
- Ownership rules.
- State transitions.
- Cross-model behavior.

Those belong to Service tests.

Example:

Incorrect:

```python
def test_user_cannot_delete_company():
    ...
```

if the reason is a business ownership rule.

Correct separation:

```text
Service Test:
    User cannot delete another workspace's company.

View Test:
    Failed deletion produces the correct HTTP response.
```

---

# 11.4 View Mocking Contract

Presentation unit tests should isolate the Application Layer where appropriate.

Selectors and Services may be mocked when verifying orchestration behavior.

Integration tests should exercise the complete request lifecycle without
mocking the Application Layer.

Examples:

Mock:

- Services.
- Selectors.

Avoid testing Views by depending on real business behavior.

Example:

```python
mock_service.create.return_value = company
```

The purpose is to verify:

- Was the Service called?
- Was the correct Context passed?
- Was the correct response returned?

---

# 11.5 Form Testing Contract

Form tests should verify:

- Required fields.
- Field validation.
- Input normalization.
- Error messages.
- Invalid input handling.

Form tests should not verify:

- Business permissions.
- Ownership rules.
- Workspace isolation.
- Domain workflows.

Those belong to Services.

---

# 11.6 Serializer Testing Contract

Serializer tests should verify:

- Input parsing.
- Field validation.
- Serialization output.
- Required fields.
- Data formatting.

Serializer tests should not verify:

- Business rules.
- Permission decisions.
- Application workflows.
- Database mutations.

---

# 11.7 ViewSet Testing Contract

DRF ViewSet tests should verify:

- Correct HTTP methods.
- Correct Context construction.
- Authentication behavior.
- Permission behavior.
- Serializer usage.
- Service invocation.
- Selector invocation.
- HTTP status codes.
- Response structure.

Example:

```text
POST /api/companies/

        |
        v

Serializer Validation

        |
        v

CompanyService.create()

        |
        v

HTTP 201 Response
```

The test verifies the API boundary.

---

# 11.8 API Response Testing Contract

API tests should verify:

- HTTP status codes.
- Response schema.
- Returned fields.
- Pagination format.
- Error format.

API tests should not verify:

- Internal Service implementation.
- ORM behavior.
- Database query optimization.

---

# 11.9 Integration Testing Contract

Integration tests may verify complete flows across layers.

Examples:

```text
HTTP Request
      |
      v
View
      |
      v
Form
      |
      v
Service
      |
      v
Database
      |
      v
HTTP Response
```

Integration tests are useful for:

- Critical user workflows.
- Authentication flows.
- Permission flows.
- Complex interactions.

However, integration tests should complement, not replace, isolated tests.

---

# 11.10 Database Usage Contract

Presentation tests should avoid unnecessary database interaction.

Use:

- Unit tests for orchestration.
- Integration tests when persistence behavior matters.

A View test should not require a large database setup simply to verify that a
Service was called correctly.

---

# 11.11 Request Factory and Client Usage

Use Django testing tools according to the test purpose.

Examples:

Unit-style View tests:

```python
RequestFactory
```

Useful for:

- Testing View behavior directly.
- Testing orchestration.

Integration-style tests:

```python
Client
```

Useful for:

- Testing URLs.
- Middleware.
- Authentication.
- Complete request lifecycle.

---

# 11.12 Test Isolation Contract

Presentation tests should isolate external dependencies where appropriate.

Examples:

Mock:

- Services.
- Selectors.
- External APIs.

Do not mock:

- The behavior being tested.

The goal is to verify the Presentation Layer, not duplicate Application Layer
tests.

---

# 11.13 Error Handling Tests

Presentation tests should verify that application failures are translated
correctly.

Examples:

Service raises:

```text
BusinessRuleViolationError
```

Presentation layer returns:

```text
Form validation error
```

API returns:

```text
HTTP 400 response
```

The test verifies translation, not the reason for the failure.

---

# 11.14 Testing Invariants

The following invariants should always hold:

## Invariant 1 — Every Layer Tests Its Own Responsibility

Presentation tests should not become Service tests.

---

## Invariant 2 — Business Rules Are Tested Independently

Critical business behavior must have Service-level tests.

---

## Invariant 3 — HTTP Behavior Is Tested at the Boundary

Status codes, responses, redirects, and rendering belong to Presentation tests.

---

## Invariant 4 — Tests Should Detect Architectural Violations

Tests should make it difficult to accidentally introduce:

- Direct ORM writes in Views.
- Business logic in Forms.
- Business logic in Serializers.
- Selector duplication.
- Service bypassing.

---

# 11.15 Presentation Test Review Checklist

During code review, verify:

- Does the test verify Presentation responsibilities?
- Is business logic tested in Services instead?
- Are Services and Selectors mocked where appropriate?
- Are HTTP responses verified?
- Are validation errors verified?
- Are permissions tested at the boundary?
- Are tests avoiding duplicated business assertions?

A good Presentation Layer test suite proves that the HTTP boundary is correct
without becoming responsible for proving the entire application.

---

## 12. Checklist

This checklist provides a practical review guide for ensuring that Presentation
Layer components follow the architectural contract.

The checklist applies to:

- Django Views.
- Django Class-Based Views.
- DRF Views.
- DRF ViewSets.
- Forms.
- Serializers.
- Presentation helpers.

A Presentation Layer component should satisfy all applicable requirements before
being considered complete.

---

# 12.1 General Presentation Layer Checklist

## Responsibilities

- [ ] The component only handles presentation concerns.
- [ ] The component coordinates application operations instead of implementing
      them.
- [ ] Business behavior is delegated to Services.
- [ ] Data retrieval is delegated to Selectors.
- [ ] HTTP concerns remain inside the Presentation Layer.

---

## Boundaries

- [ ] No business rules are implemented in the Presentation Layer.
- [ ] No domain invariants are enforced in Views, Forms, or Serializers.
- [ ] No direct persistence operations are performed.
- [ ] No reusable ORM query logic exists in presentation code.
- [ ] No Service or Selector logic is duplicated.

---

# 12.2 Django View Checklist

## Request Handling

- [ ] Authentication requirements are enforced.
- [ ] Authorization requirements are enforced.
- [ ] Request data is parsed correctly.
- [ ] URL and query parameters are handled appropriately.

---

## Reads

- [ ] Read operations use Selectors.
- [ ] Query logic is not duplicated inside the View.
- [ ] Presentation-specific filtering is separated from business filtering.
- [ ] Dynamic Form querysets are populated through Selectors.

---

## Writes

- [ ] Write operations use Services.
- [ ] Forms provide validated input only.
- [ ] Context objects are constructed correctly.
- [ ] The View does not call ORM write methods.
- [ ] The View does not call model `save()` or `delete()`.

---

## Responses

- [ ] Correct templates are rendered.
- [ ] Correct redirects are returned.
- [ ] Correct HTTP status codes are used.
- [ ] Success and error messages are handled appropriately.

---

# 12.3 DRF ViewSet Checklist

## API Handling

- [ ] Authentication is configured correctly.
- [ ] Permissions are enforced correctly.
- [ ] Request payloads are validated through Serializers.
- [ ] Responses are returned using appropriate serializers.

---

## Reads

- [ ] `get_queryset()` delegates retrieval to Selectors.
- [ ] Query filtering does not contain business logic.
- [ ] Pagination is handled at the API boundary.

---

## Writes

- [ ] `create()` delegates mutations to Services.
- [ ] `update()` delegates mutations to Services.
- [ ] Serializers do not replace Services.

---

## Responses

- [ ] Correct HTTP status codes are returned.
- [ ] Response schemas are consistent.
- [ ] API errors are translated correctly.

---

# 12.4 Forms Checklist

## Validation

- [ ] Forms validate input structure.
- [ ] Forms normalize user input where appropriate.
- [ ] Forms provide clear validation messages.
- [ ] Forms do not implement business rules.

---

## Persistence

- [ ] Forms do not directly create domain objects.
- [ ] Forms do not directly update domain objects.
- [ ] Forms do not call model `save()`.

---

## Separation

- [ ] Business validation remains inside Services.
- [ ] Ownership validation remains inside Services.
- [ ] Workspace validation remains inside Services.

## Data Retrieval

- [ ] Dynamic querysets are populated through Selectors.
- [ ] Forms do not duplicate Selector logic.

---

# 12.5 Serializer Checklist

## Input Handling

- [ ] Serializers validate transport-level data.
- [ ] Serializers normalize input correctly.
- [ ] Serializers provide clear validation errors.

---

## Application Boundary

- [ ] Serializers do not implement business rules.
- [ ] Serializers do not perform domain operations.
- [ ] Serializers do not bypass Services.
- [ ] Serializers do not directly manipulate persistent entities.

---

# 12.6 Exception Handling Checklist

- [ ] Application exceptions are translated into appropriate responses.
- [ ] HTTP responses are not created inside Services.
- [ ] Business exceptions retain their meaning.
- [ ] Internal implementation details are not exposed.
- [ ] Unexpected exceptions are logged appropriately.
- [ ] Exception translation is centralized where practical.

---

# 12.7 Testing Checklist

## Presentation Tests

- [ ] Tests verify HTTP behavior.
- [ ] Tests verify orchestration.
- [ ] Tests verify response generation.
- [ ] Tests verify error translation.

---

## Separation

- [ ] Business logic is tested in Services.
- [ ] Data retrieval logic is tested in Selectors.
- [ ] Forms and Serializers are tested for transport validation.
- [ ] Tests do not duplicate responsibilities from other layers.

---

# 12.8 Code Review Questions

Before approving Presentation Layer code, ask:

## Responsibility

> "Is this code translating HTTP requests into application operations, or is it
implementing application behavior?"

---

## Business Logic

> "Would this rule still exist if the operation was triggered by a different
entry point?"

If yes, it does not belong in the Presentation Layer.

---

## Data Access

> "Is this query required only for presentation, or is it application logic?"

If it is application logic, move it to a Selector.

---

## Persistence

> "Is this code changing application state?"

If yes, it belongs in a Service.

---

## Validation

> "Is this validation about input format or business correctness?"

Input format belongs to Forms/Serializers.

Business correctness belongs to Services.

---

# 12.9 Final Presentation Layer Standard

A compliant Presentation Layer should satisfy the following statement:

> The Presentation Layer receives external requests, validates transport input,
> coordinates Application Layer operations, and returns appropriate responses.
> It does not contain business behavior.

The final responsibility boundaries are:

```text
Presentation Layer
        |
        | coordinates
        v

Application Layer
        |
        | implements behavior
        v

Infrastructure Layer
        |
        | persists data
        v

Database
```

The architecture remains predictable when each layer owns only its defined
responsibilities.
