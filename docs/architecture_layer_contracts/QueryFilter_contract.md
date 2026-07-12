# Query Filter Contract

Query filters represent immutable query criteria passed from callers to
selectors.

They encapsulate filtering parameters while remaining independent of database
access, business logic, and application workflows.

---

## QF-01. Single Responsibility

A query filter represents filtering criteria for a selector.

It does not retrieve data or perform any business logic.

---

## QF-02. Immutable

Query filters are immutable value objects.

Once constructed, their state must not change.

---

## QF-03. No Business Logic

Query filters contain only data.

They must not:

- Access the database.
- Perform validation beyond basic type constraints.
- Execute business rules.
- Modify application state.

---

## QF-04. Selector-specific

Each selector should define a dedicated query filter describing the filtering
criteria it accepts.

---

## QF-05. Reuse Common Fields

Common filtering parameters should be shared through inheritance whenever
appropriate.

Examples include:

- `BaseQueryFilter`
- `WorkspaceQueryFilter`
- `CompanyQueryFilter`
- `CompanyEmailQueryFilter`
- `CompanyNoteQueryFilter`
- `JobApplicationQueryFilter`
- `DocumentQueryFilter`

         .
         .
         .

---

## QF-06. Framework-independent

Query filters should remain independent of Django ORM queries.

They describe *what* should be filtered, not *how* filtering is performed.

Filtering logic belongs exclusively to selectors.

---

# Implementation Guidelines

---

## GQF-01. Use Dataclasses

Query filters should be implemented as Python dataclasses.

---

## GQF-02. Use Immutable Dataclasses

Query filters should be declared with:

- `frozen=True`
- `slots=True`

to communicate that they are immutable value objects with a fixed structure.

---

## GQF-03. Keep Filters Lightweight

Query filters should only contain filtering parameters.

Helper methods, validation logic, or ORM operations should not be added.

---

## GQF-04. Pass Filters as a Single Object

Selectors should accept a single filter object rather than multiple optional
filter parameters.

Example:

```python
CompanySelector.list(
    user=user,
    filters=CompanyQueryFilter(
        workspace_id=workspace_id,
        name="Company 1",
    ),
)
```

This provides a stable, extensible, and self-documenting selector API.
