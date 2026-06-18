# Domain Model

## Overview

Job Application Tracker is designed around the process of organizing and managing job search activities.

The domain is centered on a workspace-based ownership model that allows users to separate job searches into independent organizational units while maintaining consistent ownership and access boundaries.

The primary business flow is:

```text
Workspace
    ↓
Company
    ↓
Job Position
    ↓
Job Application
```

Supporting entities such as documents, emails, notes, requirements, tasks, and benefits provide additional context throughout the job search process.

---

## Workspace

A workspace is the primary organizational and ownership boundary within the system.

Each workspace belongs to a single user and acts as a container for job search activities.

Examples:

- Germany Job Search
- Remote Opportunities
- Backend Engineering Applications
- Graduate Positions

Responsibilities:

- Organize job search activities.
- Separate unrelated job searches.
- Provide ownership boundaries.
- Support future scalability and multi-tenant features.

Relationship:

```text
User
  └── Workspace
```

---

## Company

A company represents an organization that may offer one or more job positions.

Each company belongs to a workspace.

Responsibilities:

- Store employer information.
- Group related job positions.
- Store company contacts.
- Store company-specific notes.

Relationship:

```text
Workspace
  └── Company
```

Attributes include:

- Name
- Website

Related entities:

- Company Email
- Company Note
- Job Position

---

## Company Email

A company email represents a contact method associated with a company.

Examples:

- Recruiter
- Hiring Manager
- HR Department

Responsibilities:

- Store contact information.
- Associate communications with applications.

Relationship:

```text
Company
  └── Company Email
```

Company emails may be linked to one or more job applications.

---

## Company Note

A company note stores user-defined information related to a company.

Examples:

- Interview experiences
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

Job positions act as the bridge between companies and applications.

Responsibilities:

- Store role-specific information.
- Track job posting details.
- Define role requirements and expectations.

Related entities:

- Employment Types
- Job Sites
- Job Requirements
- Job Tasks
- Job Benefits
- Job Applications

---

## Employment Type

Employment types classify the nature of a position.

Examples:

- Full-Time
- Part-Time
- Internship
- Contract

Employment types are global reference data shared across positions.

Relationship:

```text
Employment Type
        ↕
  Job Position
```

---

## Job Site

Job sites represent where a position was discovered or advertised.

Examples:

- LinkedIn
- Indeed
- StepStone
- Company Website

Job sites are global reference data shared across positions.

Relationship:

```text
Job Site
    ↕
Job Position
```

---

## Job Requirement

Job requirements represent skills, qualifications, or expectations associated with a position.

Examples:

- Python
- Django
- AWS Experience

Requirements are user-owned reusable entities.

Relationship:

```text
User
  └── Job Requirement
          ↕
     Job Position
```

---

## Job Task

Job tasks represent responsibilities associated with a position.

Examples:

- Develop APIs
- Maintain Infrastructure
- Write Automated Tests

Tasks are user-owned reusable entities.

Relationship:

```text
User
  └── Job Task
          ↕
     Job Position
```

---

## Job Benefit

Job benefits represent advantages or incentives associated with a position.

Examples:

- Remote Work
- Health Insurance
- Relocation Assistance

Benefits are user-owned reusable entities.

Relationship:

```text
User
  └── Job Benefit
          ↕
     Job Position
```

---

## Job Application

A job application represents a user's application to a specific job position.

This is one of the central entities within the domain.

Relationship:

```text
Workspace
      ↓
Job Position
      ↓
Job Application
```

Each application belongs to:

- A user
- A workspace
- A job position
- A status

Responsibilities:

- Track application progress.
- Associate supporting documents.
- Associate company contacts.
- Store application notes.
- Record application dates.

Related entities:

- Application Status
- Documents
- Company Emails
- Job Application Notes

---

## Application Status

Application statuses represent the current state of a job application.

Examples:

- Applied
- Screening
- Interview
- Offer
- Rejected

The platform intentionally does not enforce a fixed workflow.

Different companies follow different hiring processes, and users may define workflows that fit their individual needs.

Statuses provide categorization without imposing a rigid progression model.

Relationship:

```text
Application Status
         ↓
   Job Application
```

---

## Job Application Note

Application notes store information specific to a particular application.

Examples:

- Interview feedback
- Recruiter discussions
- Follow-up reminders

Relationship:

```text
Job Application
       ↓
Job Application Note
```

---

## Document Type

Document types categorize uploaded documents.

Examples:

- Resume
- Cover Letter
- Portfolio
- Certificate

Document types are user-owned entities.

Relationship:

```text
User
  └── Document Type
```

---

## Document

Documents represent files uploaded by users.

Examples:

- Resume PDF
- Cover Letter
- Portfolio

Responsibilities:

- Store application materials.
- Prevent duplicate file storage.
- Support document reuse across applications.

Relationship:

```text
User
  └── Document
          ↕
     Job Application
```

The system calculates file hashes to identify identical files and avoid unnecessary duplication.

---

## Ownership Model

Ownership is enforced throughout the domain.

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

Additional user-owned resources include:

```text
Document Type
Document
Job Requirement
Job Task
Job Benefit
```

Ownership validation is enforced by the service and selector layers to prevent cross-workspace access and maintain data integrity.

---

## Domain Philosophy

The domain model is designed around three principles:

### Ownership

Every entity must belong to a clearly defined owner or ownership boundary.

### Reusability

Documents, requirements, benefits, tasks, and contacts can be reused across multiple parts of the system.

### Flexibility

The platform avoids enforcing rigid hiring workflows because recruitment processes vary significantly between organizations and industries.