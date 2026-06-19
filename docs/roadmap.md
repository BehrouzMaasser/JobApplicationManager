# Roadmap

## Short-Term

### Unify Document Accessing

Web and REST API views use the same structure to retrieve the document url path

- Add get_object_or_404() to DocumentSelector
- Add a MIXIN for open/download in web and REST API views
- Modify views

### Error Handling

Design a consistent error handling strategy for:

- Services
- Web views
- REST API endpoints

### Testing Refactor

Improve the organization and maintainability of the test suite.

### Project Cleanup

Review project structure and remove technical debt introduced during rapid development.

### Documentation

Continue improving developer and architecture documentation.

## Medium-Term

### Authentication

Expand authentication capabilities and API authentication workflows.

### Search Functionality

Provide advanced search capabilities across companies, positions, and applications.

### Document Categorization

Improve document organization and management.

---

## Long-Term

### REST API Version 2

Introduce flatter resource paths and improved usability.

### Shared Workspaces

Support collaboration between multiple users.

### Reporting and Analytics

Provide insights into job search activity and outcomes.

---

## Infrastructure

### Docker Deployment

Containerize the application for consistent local and production environments.

### Continuous Integration / Continuous Deployment

Automate testing and deployment workflows.