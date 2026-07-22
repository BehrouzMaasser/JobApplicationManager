# Presentation Layer Contract

1. Purpose
2. Architectural Principles
3. Layer Responsibilities
4. Layer Boundaries
5. Request Lifecycle
6. Forms Contract
7. Django View Contract
8. DRF ViewSet Contract
9. Exception Handling Contract
10. Testing Contract
11. Checklist



## 1. Purpose

### Objective

The Presentation Layer is responsible for translating external HTTP requests into
application operations and translating application results into HTTP responses.

It acts as the boundary between clients (web browsers, REST clients, automated
consumers, etc.) and the application's business logic.

The Presentation Layer coordinates interactions with the application but does
not implement business behavior itself.

---

### Responsibilities

The Presentation Layer is responsible for:

- Receiving and interpreting HTTP requests.
- Authenticating and authorizing incoming requests.
- Parsing request data through Django Forms or DRF Serializers.
- Constructing the appropriate service context objects.
- Invoking Selectors for read operations.
- Invoking Services for write operations.
- Translating application results into HTML or JSON responses.
- Managing presentation concerns such as redirects, templates, pagination,
  success messages, and HTTP status codes.
- Translating application exceptions into appropriate user-facing responses.

---

### Non-Responsibilities

The Presentation Layer is **not** responsible for:

- Implementing business rules.
- Persisting domain objects.
- Executing ORM write operations.
- Enforcing domain invariants.
- Performing ownership or workspace validation.
- Performing cross-model business validation.
- Reimplementing logic already provided by Selectors or Services.

Business behavior belongs exclusively to the Application Layer.

---

### Design Philosophy

The Presentation Layer follows an orchestration model.

Presentation components coordinate interactions between HTTP clients and the
Application Layer while delegating all business decisions to Services and all
read operations to Selectors.

Presentation components should remain thin, deterministic, and easily testable.

Whenever business behavior is required, the Presentation Layer delegates that
behavior instead of implementing it.

---

## 2. Architectural Principles

The Presentation Layer follows the principles below. Every presentation
component (Django Views, Forms, DRF ViewSets, and Serializers) should be
designed in accordance with these rules.

---

### Principle 1 — Separation of Concerns

The Presentation Layer owns HTTP concerns only.

Business logic belongs to Services.

Data retrieval belongs to Selectors.

Persistence belongs to the ORM.

Presentation components should coordinate these layers without replacing them.

---

### Principle 2 — Orchestration over Implementation

Presentation components orchestrate application operations but do not implement
them.

Their responsibility is to:

- receive a request,
- validate transport-level input,
- invoke the appropriate application component,
- produce an HTTP response.

Business decisions must always be delegated.

---

### Principle 3 — Read and Write Separation

Read and write operations have different responsibilities.

Read operations should obtain data through Selectors.

Write operations should delegate mutations to Services.

Presentation components must not bypass these abstractions.

---

### Principle 4 — Transport Independence

Business behavior must not depend on how a request reaches the application.

Whether an operation originates from:

- a Django View,
- a DRF endpoint,
- a management command,
- a Celery task,
- or another entry point,

the same business rules should be enforced by the Service Layer.

---

### Principle 5 — Thin Presentation Components

Presentation components should remain small and deterministic.

They should primarily perform:

- request parsing,
- authentication,
- authorization,
- context construction,
- application orchestration,
- response generation.

Complex business behavior should never accumulate inside Views,
Forms, ViewSets, or Serializers.

---

### Principle 6 — Explicit Dependencies

Presentation components should interact with the application through explicit,
well-defined abstractions.

Whenever possible:

- read operations should depend on Selectors,
- write operations should depend on Services,
- shared context should be represented by Context objects.

Direct interaction with ORM models should be limited to presentation-specific
framework requirements.

Whenever presentation components need application data, they should obtain it
through Selectors rather than direct ORM queries.

Whenever presentation components need to modify application state, they should
delegate the operation to Services.

---

## 3. Layer Responsibilities

The Presentation Layer is responsible for coordinating interactions between HTTP
clients and the Application Layer.

Its responsibilities are intentionally limited to presentation concerns.

---

### 3.1 Request Processing

The Presentation Layer is responsible for:

- Receiving HTTP requests.
- Parsing request parameters.
- Parsing submitted form or JSON data.
- Validating transport-level input through Forms or Serializers.
- Determining which application operation has been requested.

---

### 3.2 Authentication and Authorization

The Presentation Layer is responsible for enforcing access to application
operations.

This includes:

- Authentication (identifying the current user).
- Authorization (ensuring the user has permission to perform the requested
  operation).

Authorization should determine **whether** an operation may be attempted.

Business rules determining **whether an operation is valid** remain the
responsibility of the Service Layer.

---

### 3.3 Context Construction

The Presentation Layer is responsible for constructing the Context objects
required by the Application Layer.

Context objects should be constructed from request routing information and other
resource identifiers required by the requested application operation.

Context objects describe the execution scope using identifiers (for example,
workspace IDs, company IDs, or resource IDs). They should not contain ORM model
instances or authenticated user objects.

The authenticated user is supplied separately to the Application Layer.

The Presentation Layer should not construct business entities directly.

---

### 3.4 Read Operations

All application read operations should be delegated to Selectors.

Presentation components may:

- invoke Selectors,
- apply presentation-specific filtering,
- paginate results,
- prepare data for rendering.

Business filtering and reusable query logic should remain inside Selectors.

---

### 3.5 Write Operations

All application write operations should be delegated to Services.

The Presentation Layer is responsible for:

- obtaining validated input,
- constructing the appropriate Context,
- invoking the correct Service method,
- handling the Service result.

The Presentation Layer must not perform write operations directly.

---

### 3.6 Response Generation

The Presentation Layer is responsible for generating appropriate HTTP responses.

Examples include:

- rendering templates,
- returning JSON responses,
- redirecting users,
- selecting HTTP status codes,
- displaying success and error messages,
- supporting pagination where appropriate.

---

### 3.7 Exception Translation

The Presentation Layer is responsible for translating application exceptions
into appropriate HTTP responses.

Examples include:

- rendering validation errors,
- returning HTTP 400 responses,
- returning HTTP 403 responses,
- returning HTTP 404 responses,
- displaying user-friendly error messages.

Application exceptions should not leak directly to end users.

---

### 3.8 Presentation State

The Presentation Layer may manage temporary presentation-specific state.

Examples include:

- pagination state,
- sorting preferences,
- search queries,
- success messages,
- redirect destinations.

Presentation state must not become business state.

---

## 4. Layer Boundaries

The Presentation Layer has strict boundaries that define what responsibilities
belong outside this layer.

These boundaries exist to prevent business logic from leaking into HTTP-facing
components and to preserve separation between presentation concerns and
application behavior.

Presentation components include:

- Django Views.
- Django Class-Based Views.
- DRF Views.
- DRF ViewSets.
- Forms.
- Serializers.
- Related presentation helpers.

The rules below apply to all Presentation Layer components.

---

## 4.1 Business Logic Boundary

The Presentation Layer MUST NOT implement business logic.

Presentation components must not:

- Calculate domain-specific values.
- Decide whether a business operation is allowed.
- Apply business rules.
- Enforce domain invariants.
- Determine relationships between domain entities.
- Implement workflows spanning multiple models.
- Duplicate logic already contained inside Services.

Business decisions belong exclusively to the Application Layer.

Example of prohibited behavior:

```python
if company.owner == request.user:
    company.status = "approved"
```

The View should delegate this decision to the appropriate Service instead.

---

## 4.2 Persistence Boundary

The Presentation Layer MUST NOT perform persistence operations directly.

Presentation components must not:

- Call `Model.objects.create()`.
- Call `Model.objects.update()`.
- Call `Model.objects.delete()`.
- Call `save()` on domain models.
- Call `delete()` on domain models.
- Modify database state directly.

All write operations must flow through Services.

Example of prohibited behavior:

```python
company = Company.objects.create(
    name=form.cleaned_data["name"]
)
```

The correct flow is:

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

The View coordinates the operation but does not own persistence.

---

## 4.3 ORM Query Boundary

Presentation components should obtain application data through Selectors.

Direct ORM queries should be avoided whenever they would duplicate application
retrieval logic or ownership enforcement.

Presentation-specific data access, such as configuring form field querysets,
should also use Selectors whenever application data is involved.

Example:

```python
form.fields["documents"].queryset = DocumentSelector.list(
    user=request.user
)
```


when the filtering represents application behavior.

Reusable retrieval logic belongs to Selectors.

---

## 4.4 Service Boundary

The Presentation Layer MUST interact with Services through their public
contract only.

Presentation components must not:

- Access Service internal implementation details.
- Bypass Service methods.
- Reproduce Service validation.
- Modify Service behavior from the presentation layer.
- Call lower-level persistence mechanisms instead of Services.

The Presentation Layer responsibilities are limited to:

1. Preparing validated input.
2. Constructing required Context objects.
3. Invoking the appropriate Service operation.
4. Translating the result into an HTTP response.

The Service Layer owns application behavior.

---

## 4.5 Selector Boundary

The Presentation Layer MUST use Selectors for application read operations.

Presentation components must not:

- Replace Selector logic with direct ORM queries.
- Duplicate filtering rules.
- Implement reusable data retrieval logic.
- Encode application-level query decisions.

Selectors answer:

> "What data should the application retrieve?"

Presentation components answer:

> "How should the retrieved data be presented?"

Selectors may also be used to restrict the set of resources presented to users.

Examples include:

- ModelChoiceField querysets.
- Form selection lists.
- API lookup data.

Presentation components should delegate these retrieval operations to Selectors
instead of constructing ORM queries directly.

---

## 4.6 Context Boundary

The Presentation Layer MUST construct Context objects but MUST NOT define
business behavior inside them.

Views should construct Context objects immediately before Service invocation. 
Context objects should not be cached on the View instance or mutated after creation.

Presentation components may:

- Collect resource identifiers from the request.
- Collect route parameters.
- Collect request metadata.
- Create Context instances.

Presentation components must not:

- Add business decisions into Context creation.
- Modify Context behavior.
- Use Context objects as a replacement for Services.

Context objects represent execution scope, not business rules.

---

## 4.7 Validation Boundary

The Presentation Layer MUST NOT replace Service validation with Forms or
Serializers.

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

A Serializer may validate:

```python
email = serializers.EmailField()
```

A Service must validate:

```text
This email belongs to the current workspace.
```

Transport validation and business validation are separate responsibilities.

---

## 4.8 Exception Boundary

The Presentation Layer MUST NOT hide or reinterpret application failures.

Presentation components must not:

- Catch exceptions only to bypass application rules.
- Convert business failures into successful responses.
- Duplicate exception handling logic from Services.
- Silently ignore application errors.

The Presentation Layer may translate application exceptions into transport
responses.

Example:

```text
BusinessRuleViolationError
        |
        v
HTTP 400 Response
```

The meaning of the exception remains owned by the Application Layer.

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

- Django Views.
- Templates.
- HTTP requests.
- DRF responses.
- Presentation-specific concepts.

The Application Layer must remain usable independently of HTTP delivery.

---

## 4.10 Code Duplication Boundary

The Presentation Layer MUST NOT become a second location for application
behavior.

If the same logic appears in multiple:

- Views.
- Forms.
- Serializers.
- ViewSets.

that logic should be evaluated for extraction into:

- A Service.
- A Selector.
- A Context object.
- Another application-level abstraction.

Repeated presentation logic usually indicates misplaced responsibility.

---

## 4.11 Review Rule

During code review, any Presentation Layer code that appears to make a business
decision should be considered a boundary violation until proven otherwise.

The default assumptions are:

- Views coordinate.
- Forms and Serializers validate transport input.
- Selectors retrieve data.
- Services implement behavior.
- ORM persists data.

A Presentation Layer component should explain:

"How does this HTTP request become an application operation?"

It should not explain:

"How does the business operation work?"

---

## 5. Request Lifecycle

The Presentation Layer follows a defined request lifecycle for transforming an
incoming HTTP request into an application operation and returning an HTTP
response.

The lifecycle applies to all presentation entry points, including:

- Django Views.
- Django Class-Based Views.
- DRF Views.
- DRF ViewSets.

The exact implementation may differ between HTML and API endpoints, but the
responsibility boundaries remain the same.

---

## 5.1 Request Lifecycle Overview

A request should flow through the following stages:

```text
HTTP Request
      |
      v
Authentication
      |
      v
Authorization
      |
      v
Input Parsing
      |
      v
Transport Validation
      |
      v
Context Construction
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

Each stage has a defined responsibility and should not replace responsibilities
belonging to another layer.

---

## 5.2 Stage 1 — Request Reception

The Presentation Layer receives the incoming HTTP request.

Responsibilities include:

- Identifying the requested operation.
- Reading route parameters.
- Reading query parameters.
- Reading submitted form data.
- Reading request body data.
- Accessing authenticated user information.

The Presentation Layer should only interpret request data required to execute
the requested operation.

It should not make business decisions at this stage.

---

## 5.3 Stage 2 — Authentication

The Presentation Layer is responsible for identifying the requester.

Authentication determines:

> "Who is making this request?"

Examples include:

- Session authentication.
- Token authentication.
- JWT authentication.
- Other configured authentication mechanisms.

The authenticated user should be supplied directly to Selectors and Services as
a separate argument.

Authentication information should not be embedded inside Context objects.

Authentication does not determine whether the requested operation is valid.

---

## 5.4 Stage 3 — Authorization

The Presentation Layer is responsible for determining whether the requester is
allowed to attempt the operation.

Authorization determines:

> "Is this user allowed to access this endpoint or action?"

Examples:

- Is the user authenticated?
- Does the user have the required permission?
- Is the endpoint available to this user type?

Authorization should happen before invoking application operations.

Authorization must not replace Service-level business validation.

Example:

Authorization:

```text
User may edit companies.
```

Service validation:

```text
This user owns this specific company.
```

These are separate responsibilities.

---

## 5.5 Stage 4 — Input Parsing

The Presentation Layer parses incoming request data.

Examples:

HTML requests:

- Form data.
- URL parameters.
- Query parameters.

API requests:

- JSON payloads.
- Query parameters.
- Path parameters.

The output of this stage should be structured input suitable for validation.

Parsing concerns belong to the Presentation Layer.

Business interpretation does not.

---

## 5.6 Stage 5 — Transport Validation

The Presentation Layer validates whether the incoming data is structurally
acceptable.

Validation responsibilities include:

- Required fields.
- Data types.
- Formatting.
- Field-level constraints.
- Serialization requirements.

Examples:

Valid:

```text
Email field must contain a valid email format.
```

Not valid in this layer:

```text
Email must belong to the same company as the job application.
```

The second rule is a business rule and belongs to the Service Layer.

---

## 5.7 Stage 6 — Context Construction

Before invoking the Application Layer, the Presentation Layer constructs the
required Context object.

Context objects should contain only the identifiers required to describe the
execution scope of the application operation.

Examples include:

- workspace_id
- company_id
- job_position_id
- application_id

Context objects should not contain ORM model instances or authenticated users.

The Presentation Layer is responsible for assembling the Context.

The Application Layer is responsible for interpreting the Context.

---

## 5.8 Stage 7 — Application Layer Invocation

After authentication, authorization, validation, and context construction, the
Presentation Layer invokes the Application Layer.

The invocation rules are:

Read operation:

```text
View
    |
    | validated_data
    | context
    | user
    v
Service
    |
    |
    |
    v
Result
```

Write operation:

```text
View
    |
    | validated_data
    | context
    | user
    v
Service
    |
    |
    |
    v
Result
```

The Presentation Layer should not perform additional business processing after
the operation has been delegated.

---

## 5.9 Stage 8 — Result Handling

The Presentation Layer transforms application results into HTTP responses.

For HTML interfaces, this may include:

- Selecting templates.
- Preparing template context.
- Redirecting after successful operations.
- Displaying messages.

For APIs, this may include:

- Serializing response data.
- Selecting HTTP status codes.
- Returning JSON responses.
- Handling pagination metadata.

The Presentation Layer decides how results are represented externally.

It does not decide what the results mean.

---

## 5.10 Stage 9 — Exception Translation

Application exceptions should be translated into appropriate HTTP responses.

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
HTTP 400 Bad Request


PermissionError
        |
        v
HTTP 403 Forbidden


ObjectNotFoundError
        |
        v
HTTP 404 Not Found
```

The Presentation Layer should preserve the meaning of application exceptions while
adapting them to the delivery mechanism.

Exception translation should preferably be centralized through reusable
presentation components such as:

- View exception handler mixins.
- DRF exception handlers.
- Middleware.

Concrete Views and ViewSets should avoid duplicating identical translation
logic.

---

## 5.11 Stage 10 — Response Delivery

The final responsibility of the Presentation Layer is returning the HTTP
response.

The response may contain:

- HTML.
- JSON.
- Redirect responses.
- Status codes.
- Headers.
- Cookies.

After response generation, the Presentation Layer lifecycle is complete.

---

## 5.12 Lifecycle Invariants

The following invariants must always hold:

### Invariant 1 — Business Logic Is Never Executed During Request Handling

Request processing may prepare and delegate operations, but business behavior
must execute inside the Application Layer.

---

### Invariant 2 — All Writes Pass Through Services

No request lifecycle may directly modify persistent application state.

---

### Invariant 3 — All Reads Pass Through Selectors

No request lifecycle should contain reusable data retrieval logic.

---

### Invariant 4 — HTTP Concerns End at the Presentation Layer

The Application Layer must not know:

- Which HTTP framework is being used.
- Which endpoint triggered the operation.
- Whether the caller is a browser or API client.

---

### Invariant 5 — The Same Operation Has the Same Business Behavior

Whether an operation is triggered through:

- Django Views.
- DRF ViewSets.
- Management commands.
- Background workers.

the Application Layer remains the source of truth for business behavior.

---

## 6. Forms Contract

Django Forms belong to the Presentation Layer and are responsible for
processing and validating user input before invoking the Application Layer.

Forms provide a structured boundary between external input and application
operations.

Forms are responsible for answering:

> "Is this input correctly formatted and suitable for submission?"

Forms are not responsible for answering:

> "Is this operation allowed according to business rules?"

Business behavior remains the responsibility of Services.

---

## 6.1 Form Responsibilities

Forms are responsible for:

- Receiving user-submitted input.
- Parsing submitted data.
- Normalizing input values.
- Validating input structure.
- Validating field formats.
- Providing user-facing validation errors.
- Preparing validated data for the Application Layer.

Examples of form responsibilities:

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
- Perform domain operations.
- Modify persistent state directly.
- Call model `save()` for application entities.
- Replace Service validation.
- Enforce ownership rules.
- Enforce workspace boundaries.
- Perform cross-model business validation.

Forms should prepare data for the Application Layer, not execute application
behavior.

---

## 6.3 Form Validation Boundary

Form validation should only validate presentation-level requirements.

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
    if Company.objects.filter(name=self.cleaned_data["name"]).exists():
        raise ValidationError(
            "Company already exists."
        )
```

when uniqueness represents an application rule.

The correct responsibility is:

```text
Form
 |
 | validated input
 v
Service
 |
 | business validation
 v
Application result
```

---

## 6.4 Form `clean()` Contract

The `clean()` method may be used for validation involving multiple submitted
fields when the validation is purely related to input structure.

Examples of acceptable usage:

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

This is acceptable because it validates the submitted data itself.

The `clean()` method must not:

- Query application state.
- Check permissions.
- Verify ownership.
- Decide whether an operation is allowed.
- Execute workflows.

---

## 6.5 Form Data Retrieval Boundary

Forms should obtain application data through Selectors whenever application
retrieval logic is required.

Forms should avoid direct ORM queries that duplicate Selector behavior or
application access rules.

Forms must not:

- Query models to enforce business rules.
- Retrieve application data through direct ORM queries when a Selector is
  responsible for that retrieval.
- Duplicate Selector logic.
- Determine application state.

Forms may populate dynamic field choices using Selectors.

Examples include:

- ModelChoiceField querysets.
- Available document selections.
- Available company emails.
- Available employment types.

Example:

```python
form.fields["documents"].queryset = DocumentSelector.list(
    user=request.user,
)
```

---

## 6.6 Form Saving Contract

Forms MUST NOT directly persist application entities.

The following patterns are prohibited:

```python
form.save()
```

when it creates or updates domain objects directly.

```python
instance.save()
```

inside form logic.

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

- Which Service method will be called.
- How persistence works.
- Which business rules are applied.

The View coordinates the interaction.

---

## 6.8 Form Initialization Contract

Forms may receive presentation-related initialization data.

Examples:

- Presentation-specific initialization data.
- Available choices.
- UI configuration.
- Initial values.
- Field visibility settings.

Forms must not receive application objects in order to perform business logic.

Example:

Allowed:

```python
CompanyForm(
    initial={
        "name": company.name
    }
)
```

Not allowed:

```python
CompanyForm(
    company=company
)
```

if the purpose is to make business decisions inside the form.

---

## 6.9 Dynamic Fields Contract

Forms may dynamically modify fields when the behavior is presentation-related.

Dynamic field querysets should preferably be populated through Selectors.

Examples:

- Hiding fields.
- Showing fields conditionally.
- Limiting choices for user experience.
- Adjusting labels or help text.

Example:

```python
if not user.is_admin:
    self.fields.pop("internal_notes")
```

However, dynamic fields must not be used as a replacement for authorization.

Example:

Incorrect:

```python
if user.is_admin:
    allow_company_deletion = True
```

Authorization must still be enforced by the appropriate application layer.

---

## 6.10 Form Error Handling Contract

Forms should provide user-friendly validation errors.

Forms should:

- Explain invalid input.
- Associate errors with fields where appropriate.
- Return normalized validation failures.

Forms should not:

- Hide business exceptions.
- Convert Service failures into fake validation results.
- Duplicate application exception handling.

Application errors should be translated by the Presentation Layer after the
Service invocation.

---

## 6.11 ModelForm Contract

`ModelForm` may be used when the form represents a simple mapping between
presentation input and model fields.

However, using `ModelForm` does not move business responsibility into the Form.

`ModelForm` must not be used to:

- Bypass Services.
- Call `save()` for domain entities.
- Implement business workflows.
- Replace Service-layer validation.

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

During code review, a Form should be checked against the following questions:

- Does the Form only validate input?
- Does the Form avoid business decisions?
- Does the Form avoid direct persistence?
- Does the Form avoid duplicating Service validation?
- Does the Form avoid reusable database queries?
- Are application operations delegated to Services?

If a Form answers "yes" to any of the following:

- "Should this rule apply outside this form?"
- "Does this require domain knowledge?"
- "Does this determine whether an operation is allowed?"

then the responsibility likely belongs outside the Form.

---

## 7. Django View Contract

Django Views belong to the Presentation Layer and are responsible for
translating HTTP requests into Application Layer operations.

A Django View coordinates:

- Request handling.
- Authentication.
- Authorization.
- Form processing.
- Context construction.
- Service invocation.
- Selector invocation.
- HTTP response generation.

A Django View must remain an orchestration component.

A View should answer:

> "Which application operation should happen for this request?"

A View should not answer:

> "How does the business operation work?"

---

# 7.1 View Responsibilities

Django Views are responsible for:

- Receiving HTTP requests.
- Handling HTTP methods.
- Performing authentication checks.
- Performing authorization checks.
- Loading presentation-specific data.
- Creating Forms.
- Validating Forms.
- Constructing Context objects.
- Calling Selectors for reads.
- Calling Services for writes.
- Returning HTTP responses.

---

# 7.2 View Non-Responsibilities

Django Views MUST NOT:

- Implement business rules.
- Modify database state directly.
- Call ORM write methods.
- Perform domain validation.
- Enforce workspace ownership rules.
- Implement workflows.
- Duplicate Service logic.
- Duplicate Selector logic.

The View is not the application layer.

---

# 7.3 HTTP Responsibility Boundary

Views own HTTP concerns.

Examples of View responsibilities:

- Choosing response type.
- Returning redirects.
- Selecting templates.
- Setting HTTP status codes.
- Handling request methods.
- Reading URL parameters.
- Reading query parameters.

Examples of non-View responsibilities:

- Deciding whether a company can be deleted.
- Determining whether a document belongs to a user.
- Calculating application state transitions.

---

# 7.4 Read Operation Contract

Read operations MUST use Selectors.

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
Template Context
      |
      v
HTTP Response
```

The View may:

- Pass request information.
- Apply pagination.
- Prepare template context.

The View must not:

- Build reusable QuerySets.
- Apply business filtering.
- Encode access rules.

---

## 7.5 Presentation Data Retrieval Contract

Views may retrieve additional application data required exclusively for
presentation purposes.

Examples:

- Building navigation context.
- Generating related resource URLs.
- Displaying breadcrumbs.
- Preparing template metadata.

Such retrieval MUST:

- Use Selectors.
- Respect access rules.
- Avoid implementing business decisions.
- Avoid modifying application state.

Example:

```python
company = CompanySelector.get(
    user=request.user,
    obj_id=company_id,
)

return AppContext(
    workspace_id=company.workspace.workspace_id,
)
```

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

1. Receive submitted data.
2. Validate the Form.
3. Construct the Context.
4. Call the Service.
5. Handle the result.

The View must not perform the write itself.

---

# 7.7 `form_valid()` Contract

`form_valid()` should be used as an orchestration point.

Allowed:

```python
def form_valid(self, form):
  
    context = CompanyContext(
        workspace_id=self.object.workspace.workspace_id,
    )

    CompanyService.create(
        user=user,
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

- Passing initial values.
- Removing fields.
- Adjusting field visibility.
- Adjusting choices for presentation.
- Populating available choices through Selectors.

Example:

```python
def get_form(self, form_class=None):

    form = super().get_form(form_class)

    application = getattr(self, "object", None)
    
    if application:
        form.fields["emails"].queryset = CompanyEmailSelector.list(
            user=self.request.user,
            filters=CompanyEmailQueryFilter(
                company_id=application.job_position.company.pk,
            )
        )
    else:
        form.fields["emails"].queryset = CompanyEmailSelector.list(
            user=self.request.user,
            filters=CompanyEmailQueryFilter(
                company_id=self.kwargs["company_id"],
            )
        )

    form.fields["documents"].queryset = DocumentSelector.list(
        user=self.request.user
    )

    return form
```

`get_form()` must not:

- Perform business validation.
- Enforce authorization.
- Decide whether an operation is allowed.
- Replace Service validation.

---

# 7.9 `dispatch()` Contract

`dispatch()` may handle request-level concerns.

Allowed:

- Authentication checks.
- Permission checks.
- HTTP method restrictions.
- Request initialization.
- Exception translation through reusable presentation mixins.

Example:

```python
def dispatch(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login")

    return super().dispatch(
        request,
        *args,
        **kwargs
    )
```

`dispatch()` must not:

- Execute business operations.
- Query application data unnecessarily.
- Replace Service authorization.

---

# 7.10 `get_queryset()` Contract

`get_queryset()` should delegate data retrieval to Selectors.

Preferred:

```python
def get_queryset(self):
    return JobPositionSelector.list(
        user=self.request.user,
        filters= ...
    )
```

Avoid:

```python
def get_queryset(self):
    return JobPosition.objects.filter(
        company=self.company
    )
```

when the query represents reusable application behavior.

`get_queryset()` should describe what data is displayed, not how application
data is managed.

---

# 7.11 Object Retrieval Contract

Views should avoid direct object retrieval when access rules exist.

Avoid:

```python
company = Company.objects.get(
    id=self.kwargs["pk"]
)
```

when retrieving the object requires:

- Workspace validation.
- Ownership checks.
- Permission checks.

Instead:

```python
company = CompanySelector.get(
    user=request.user,
    filters=...
)
```

Selectors should provide controlled data access.

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

- Add business rules during context construction.
- Modify context semantics.
- Use context objects to hide business logic.

---

# 7.13 Success and Redirect Handling

Views are responsible for deciding the HTTP response after successful
operations.

Examples:

- Redirecting after creation.
- Rendering a success page.
- Returning confirmation messages.

The View may decide:

```text
After creating a company:
redirect to company detail page.
```

The View must not decide:

```text
A company becomes active after creation.
```

The second decision belongs to the Service Layer.

---

# 7.14 Failure Handling

Views should translate application failures into user-facing responses.

Examples:

```text
BusinessRuleViolationError
        |
        v
Form error / HTTP response
```

Views should not:

- Ignore failures.
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
selector call

get_form()
    |
form customization

form_valid()
    |
service invocation

get_context_data()
    |
presentation data
```

A CBV should not become a replacement Application Layer.

---

# 7.16 View Composition Rule

When multiple Views share the same behavior, that behavior should be extracted
into the appropriate layer.

Possible destinations:

- Service.
- Selector.
- Form helper.
- Context object.
- Permission component.

Duplicating behavior between Views is discouraged.

---

# 7.17 Presentation Helper Contract

Presentation helper functions belong to the Presentation Layer and exist to
support HTTP representation and user interface composition.

Examples include:

- URL builders.
- Navigation helpers.
- Template context builders.
- Display formatting utilities.
- Presentation-specific data transformation helpers.

These helpers exist to simplify Views and templates.

They must not implement Application Layer behavior.

---

## Presentation Helper Responsibilities

Presentation helpers MAY:

- Build URLs.
- Construct navigation links.
- Prepare template-specific context.
- Format values for display.
- Transform application results into presentation structures.

Examples:

```python
def company_list_url(workspace_id):
    return reverse(
        "company-list-web",
        kwargs={"workspace_id": workspace_id}
    )


def build_company_navigation(company):
    return {
        "back_url": company_list_url(
            company.workspace_id
        )
    }
```

Incorrect Use:

```python

def can_delete_company(company):
    return not company.job_applications.exists()
```

Correct:
```python
CompanyService.remove(...)
```

---

# 7.18 Django View Review Checklist

During code review, verify:

- Does the View only coordinate application operations?
- Are reads delegated to Selectors?
- Are writes delegated to Services?
- Are Context objects constructed correctly?
- Is business logic absent from the View?
- Is ORM usage limited to presentation concerns?
- Are Forms used only for input validation?
- Are exceptions translated correctly?
- Are HTTP concerns kept inside the View?

A compliant Django View should be understandable by reading its orchestration
flow without needing to understand business rules.

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

## 9. Exception Handling Contract

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

## 9.1 Exception Ownership

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

## 9.2 Exception Translation Boundary

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

## 9.3 Business Exception Contract

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

## 9.4 Validation Exception Contract

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

## 9.5 Django View Exception Handling

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

### 9.5.1 Form-Based Service Validation Translation

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

## 9.6 DRF ViewSet Exception Handling

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

## 9.7 Global Exception Handling

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

## 9.8 Exception Mapping Contract

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

## 9.9 Exception Messages Contract

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

## 9.10 Exception Logging Contract

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

## 9.11 Exception Flow Invariants

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

## 9.12 Exception Handling Review Checklist

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

## 10. Testing Contract

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

# 10.1 Testing Responsibilities by Layer

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

# 10.2 View Testing Contract

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

# 10.3 View Tests MUST NOT Test Business Logic

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

# 10.4 View Mocking Contract

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

# 10.5 Form Testing Contract

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

# 10.6 Serializer Testing Contract

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

# 10.7 ViewSet Testing Contract

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

# 10.8 API Response Testing Contract

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

# 10.9 Integration Testing Contract

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

# 10.10 Database Usage Contract

Presentation tests should avoid unnecessary database interaction.

Use:

- Unit tests for orchestration.
- Integration tests when persistence behavior matters.

A View test should not require a large database setup simply to verify that a
Service was called correctly.

---

# 10.11 Request Factory and Client Usage

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

# 10.12 Test Isolation Contract

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

# 10.13 Error Handling Tests

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

# 10.14 Testing Invariants

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

# 10.15 Presentation Test Review Checklist

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

## 11. Checklist

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

# 11.1 General Presentation Layer Checklist

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

# 11.2 Django View Checklist

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

# 11.3 DRF ViewSet Checklist

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

# 11.4 Forms Checklist

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

# 11.5 Serializer Checklist

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

# 11.6 Exception Handling Checklist

- [ ] Application exceptions are translated into appropriate responses.
- [ ] HTTP responses are not created inside Services.
- [ ] Business exceptions retain their meaning.
- [ ] Internal implementation details are not exposed.
- [ ] Unexpected exceptions are logged appropriately.
- [ ] Exception translation is centralized where practical.

---

# 11.7 Testing Checklist

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

# 11.8 Code Review Questions

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

# 11.9 Final Presentation Layer Standard

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
