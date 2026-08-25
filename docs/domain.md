# Domain Model

## Overview

Job Application Tracker is a Django application for organizing and managing job-search activities.

The domain is organized around **user ownership** and **workspace boundaries**. A workspace is the primary organizational boundary for the core job-search data.

The central relationship is:

```text
User
  │
  └── Workspace
        │
        └── Company
              │
              └── Job Position
                    │
                    └── Job Application
```

Additional resources provide reusable or supporting information around this core flow.

---

## Workspace

A workspace is the primary organizational and ownership boundary for job-search data.

Each workspace belongs to one user.

Examples:

- Germany Job Search
- Remote Opportunities
- Backend Engineering Applications

Responsibilities:

- Organize job-search activity.
- Separate independent job searches.
- Establish an ownership boundary for workspace-scoped resources.

Relationship:

```text
User
  └── Workspace
```

---

## Company

A company represents an organization associated with one or more job positions.

Each company belongs to a workspace.

Responsibilities:

- Store employer information.
- Group job positions.
- Store company contacts.
- Store company-specific notes.

Relationship:

```text
Workspace
  └── Company
```

Related resources:

- Company Email
- Company Note
- Job Position

---

## Company Email

A company email represents contact information associated with a company.

Examples:

- Recruiter
- Hiring Manager
- HR Department

Relationship:

```text
Company
  └── Company Email
```

Company emails may also be associated with job applications.

---

## Company Note

A company note stores user-defined information associated with a company.

Examples:

- Interview observations
- Research findings
- Salary information
- Internal reminders

Relationship:

```text
Company
  └── Company Note
```

---

## Job Position

A job position represents a specific role offered by a company.

Examples:

- Backend Engineer
- Software Developer
- DevOps Engineer

Relationship:

```text
Company
  └── Job Position
```

A company may contain multiple job positions.

Related resources include:

- Employment Type
- Job Site
- Job Requirement
- Job Task
- Job Benefit
- Job Application

---

## Employment Type

Employment types classify the nature of a job position.

Examples:

- Full-Time
- Part-Time
- Internship
- Contract

Employment types are shared reference data.

Relationship:

```text
Employment Type
        ↕
  Job Position
```

---

## Job Site

Job sites represent where a job position was discovered or advertised.

Examples:

- LinkedIn
- Indeed
- StepStone
- Company Website

Job sites are shared reference data.

Relationship:

```text
Job Site
    ↕
Job Position
```

---

## Job Requirement

A job requirement represents a skill, qualification, or expectation associated with a job position.

Examples:

- Python
- Django
- AWS Experience

Requirements are reusable user-owned resources.

Relationship:

```text
User
  └── Job Requirement
          ↕
     Job Position
```

### M2M Ownership Invariant

When a requirement is assigned to a job position, the service layer verifies that the requirement belongs to the same user performing the operation.

This is deliberately treated as a **domain invariant**, not as a resource-access failure.

There is an important distinction:

1. **Direct access to a requirement**  
   A user attempting to retrieve another user's requirement receives the normal resource-not-found behavior from the Selector.

2. **Using a requirement while modifying a job position**  
   The requirement is supplied as part of a write operation. The Service must verify that the supplied domain object satisfies the ownership invariant. If it does not, the operation fails as a domain invariant violation.

The same distinction applies to Job Tasks and Job Benefits.

---

## Job Task

A job task represents a responsibility associated with a job position.

Examples:

- Develop APIs
- Maintain Infrastructure
- Write Automated Tests

Tasks are reusable user-owned resources.

Relationship:

```text
User
  └── Job Task
          ↕
     Job Position
```

Task ownership is verified by Services when tasks are assigned during a job-position write operation.

---

## Job Benefit

A job benefit represents an advantage or incentive associated with a job position.

Examples:

- Remote Work
- Health Insurance
- Relocation Assistance

Benefits are reusable user-owned resources.

Relationship:

```text
User
  └── Job Benefit
          ↕
     Job Position
```

Benefit ownership is verified by Services when benefits are assigned during a job-position write operation.

---

## Job Application

A job application represents an application to a specific job position.

It is one of the central domain entities.

Relationship:

```text
Workspace
    ↓
Company
    ↓
Job Position
    ↓
Job Application
```

An application is associated with:

- A user
- A workspace
- A job position
- An application status

Responsibilities include:

- Tracking application progress.
- Recording application dates.
- Associating supporting documents.
- Associating company contacts.
- Storing application-specific notes.

---

## Application Status

Application statuses represent the current state or category of a job application.

Examples:

- Applied
- Screening
- Interview
- Offer
- Rejected

The domain does not impose a universal hiring workflow. Statuses provide state classification without requiring every user or company to follow the same progression.

---

## Job Application Note

An application note stores information specific to a particular job application.

Examples:

- Interview feedback
- Recruiter discussions
- Follow-up information
- Preparation notes

Relationship:

```text
Job Application
       ↓
Job Application Note
```

---

## Document Type

A document type categorizes user documents.

Examples:

- Resume
- Cover Letter
- Portfolio
- Certificate

Document types are user-owned resources.

Relationship:

```text
User
  └── Document Type
```

---

## Document

A document represents a file uploaded by a user.

Examples:

- Resume PDF
- Cover Letter
- Portfolio

Responsibilities include:

- Storing application materials.
- Associating documents with applications.
- Supporting document reuse.
- Preventing duplicate files for the same user through file identity/hash rules.

Relationship:

```text
User
  └── Document
          ↕
     Job Application
```

---

## Ownership Model

The primary ownership hierarchy is:

```text
User
│
└── Workspace
    │
    └── Company
        │
        └── Job Position
            │
            └── Job Application
```

Other user-owned resources include:

```text
Document
Document Type
Job Requirement
Job Task
Job Benefit
```

Selectors enforce read-side ownership boundaries. Services enforce ownership and domain invariants during write operations.

A resource that is not accessible through the user's ownership boundary is normally treated as **not found**, rather than exposing the existence of another user's resource.

---

## Domain Philosophy

The domain is built around three principles:

### Ownership

Every resource has a clear owner or ownership boundary.

### Reusability

Resources such as documents, requirements, tasks, benefits, and contacts can be reused where the domain permits it.

### Flexibility

The application avoids imposing a universal recruitment workflow. Users can organize application statuses and job-search data according to their own process.
