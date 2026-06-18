from rest_framework.routers import DefaultRouter

# For Applications Apps Views
from apps.applications.api.views import (
    JobApplicationViewSet,
    JobApplicationNoteViewSet
)

# For Companies Apps Views
from apps.companies.api.v1.views import (
    CompanyViewSet,
    CompanyNoteViewSet,
    JobBenefitViewSet,
    JobTaskViewSet,
    JobRequirementViewSet,
    JobPositionViewSet,
    CompanyEmailViewSet
)

# For Documents Apps Views
from apps.documents.api.v1.views import DocumentTypeViewSet, DocumentViewSet
from apps.workspaces.api.v1.views import WorkspaceViewSet


router = DefaultRouter()

# Workspaces Apps

# Workspace:
router.register(r"workspaces", WorkspaceViewSet, basename="workspace")


# Companies Apps

# Company:
router.register(r"companies", CompanyViewSet, basename="company")

# Company Note:
router.register(r"company-notes", CompanyNoteViewSet, basename="company_note")

# Company Email:
router.register(
    r"company-emails", CompanyEmailViewSet, basename="company_email"
)

# Job Benefit:
router.register(r"job-benefits", JobBenefitViewSet, basename="job_benefit")

# Job Task:
router.register(r"job-tasks", JobTaskViewSet, basename="job_task")

# Job Requirement:
router.register(
    r"job-requirements", JobRequirementViewSet, basename="job_requirement"
)

# Job Position:
router.register(r"job-positions", JobPositionViewSet, basename="job_position")


# Applications Apps

# Job Application:
router.register(
    r"job-applications", JobApplicationViewSet, basename="job_application"
)

# Job Application Note:
router.register(
    r"job-application-notes",
    JobApplicationNoteViewSet,
    basename="job_application_notes"
)

# Documents Apps

# Document Type:
router.register(
    r"document-types", DocumentTypeViewSet, basename="document_type"
)

# Document:
router.register(r"documents", DocumentViewSet, basename="document")


urlpatterns = router.urls
