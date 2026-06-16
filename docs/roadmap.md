# Roadmap

## Completed
- Initial Django setup
- Environment variable configuration
- Project restructuring
- Document upload flow
- Storage architecture
- REST API
- Writing tests for REST API
- Applications app is evaluated, models, services and API views are corrected
- Applications app tests refind
- Models' integrity verified
- Tests cleaned
- Services contracts and structure is fixed
- Renamed some files to keep the similarity
- Resolved test warnings and errors
- Wrote tests for basic_services
- Wrote tests for Serializers
- Reviewed Selectors and wrote tests for them
- Reviewed accounts app and write tests for them
- Created views and templates for All Applications
- A well-structured template for UI is created
- Restricted Data access from other users for creating/updating documents and job 
   positions
- Added Application note detail HTML template
- Corrected the architecture for timezone handling(local for UI + UTC for backend)
- Modified Signup and Login pages
- Investigate why a job position with date_posted value before job application's
    date_applied value was allowed to be updated
- Added validation for job position's date_posted in its services
- Introduced service validation error mixin for handling web view form error messages
- Added tests for the new validation added to `JobPositionService.update()`
- Added tests for updated JobTaskSelector, JobBenefitSelector and JobRequirementSelector

## In Progress
- Clean the project files
- Modifying README
- Reviewing all created web views and resolving possible bugs and typos in 
    views/HTML templates/CSS

## Planned
- Refactor REST API to something similar to web views
- Think about modifying view contexts
- Think about moving JobTask, JobBenefit and JobRequirement logic from Companies to 
   accounts
- Come up with a good structure for error handling
- Authentication
- Search functionality
- Document categorization
- Docker deployment
- CI/CD