"""
REST API views for managing the Companies domain.

This module defines DRF ViewSets that:
- Delegate read operations to selector layer
- Delegate write operations to service layer
- Enforce consistent lookup behavior for nested and flat resources
"""

from django.db.models import QuerySet

# Serializers
from apps.companies.api.v1.serializers import (
    CompanySerializer,
    CompanyNoteSerializer,
    CompanyEmailSerializer,
    JobBenefitSerializer,
    JobTaskSerializer,
    JobRequirementSerializer,
    JobPositionSerializer,
)

# Models (for typing only)
from apps.companies.models import (
    Company,
    CompanyNote,
    CompanyEmail,
    JobPosition,
    JobBenefit,
    JobTask,
    JobRequirement,
)

# Selectors
from apps.companies.selectors.company_selector import CompanySelector
from apps.companies.selectors.company_note_selector import CompanyNoteSelector
from apps.companies.selectors.company_email_selector import CompanyEmailSelector
from apps.companies.selectors.job_benefit_selector import JobBenefitSelector
from apps.companies.selectors.job_position_selector import JobPositionSelector
from apps.companies.selectors.job_requirement_selector import JobRequirementSelector
from apps.companies.selectors.job_task_selector import JobTaskSelector

# Services
from apps.companies.services.company_service import CompanyService
from apps.companies.services.company_note_service import CompanyNoteService
from apps.companies.services.company_email_service import CompanyEmailService
from apps.companies.services.job_benefit_service import JobBenefitService
from apps.companies.services.job_position_service import JobPositionService
from apps.companies.services.job_requirement_service import JobRequirementService
from apps.companies.services.job_task_service import JobTaskService

# Contexts
from apps.companies.services.contexts.company_context import (
    CompanyContext,
    CompanyChildContext,
)

# Base ViewSets
from apps.core.common.api.viewsets import (
    BaseReadOnlyViewSet,
    BaseContextServiceViewSet,
    BaseIdServiceViewSet,
)
from apps.core.common.types.filters import CompanyQueryFilter, \
    CompanyNoteQueryFilter, CompanyEmailQueryFilter, JobPositionQueryFilter


# =========================================================
# Company (root)
# =========================================================

class CompanyViewSet(BaseReadOnlyViewSet):
    """
    Read-only API for Company resources.

    Responsibilities:
    - Listing and retrieving companies
    - Delegating queries to CompanySelector
    - Supporting optional workspace filtering
    """

    serializer_class = CompanySerializer

    selector_class = CompanySelector
    selector_lookup_field = "company_id"

    lookup_url_kwarg = "id"

    def get_queryset(self) -> QuerySet[Company]:
        """
        Return filtered companies for the authenticated user.
        """

        return self.selector.list(
            user=self.request.user,
            filters=self._get_queryset_filters(),
        )

    def _get_queryset_filters(self) -> CompanyQueryFilter:
        """
        Build selector filter object from query parameters.
        """

        return self.selector.QueryFilter(
            workspace_id=self.request.query_params.get("workspace_id"),
        )


class NestedCompanyViewSet(BaseContextServiceViewSet):
    """
    Full CRUD API for Company resources in nested workspace context.

    Responsibilities:
    - Create/Update/Delete via CompanyService
    - Read via CompanySelector
    - Requires workspace context
    """

    service_class = CompanyService
    selector_class = CompanySelector

    read_serializer_class = CompanySerializer
    write_serializer_class = CompanySerializer

    lookup_url_kwarg = "id"
    selector_lookup_field = "company_id"

    def get_queryset(self) -> QuerySet[Company]:
        """
        Return companies scoped to a workspace.
        """

        return self.selector.list(
            user=self.request.user,
            filters=self._get_queryset_filters(),
        )

    def get_create_context(self) -> CompanyContext:
        """
        Context used when creating a company.
        """

        return CompanyContext(
            workspace_id=self.kwargs["workspace_id"],
            id=None,
        )

    def get_update_context(self) -> CompanyContext:
        """
        Context used when updating/deleting a company.
        """

        return CompanyContext(
            workspace_id=self.kwargs["workspace_id"],
            id=self.kwargs["id"],
        )

    def _get_queryset_filters(self) -> CompanyQueryFilter:
        return CompanyQueryFilter(
            workspace_id=self.kwargs["workspace_id"],
        )


# =========================================================
# Company Note
# =========================================================

class CompanyNoteViewSet(BaseReadOnlyViewSet):
    """
    Read-only API for Company Notes.

    Notes:
    - Company context is optional for listing
    """

    serializer_class = CompanyNoteSerializer

    selector_class = CompanyNoteSelector
    selector_lookup_field = "company_note_id"

    lookup_url_kwarg = "id"

    def get_queryset(self) -> QuerySet[CompanyNote]:
        return self.selector.list(
            user=self.request.user,
            filters=self._get_queryset_filters(),
        )

    def _get_queryset_filters(self) -> CompanyNoteQueryFilter:
        return CompanyNoteQueryFilter(
            workspace_id=self.request.query_params.get("workspace_id"),
            company_id=self.request.query_params.get("company_id"),
        )


class NestedCompanyNoteViewSet(BaseContextServiceViewSet):
    """
    Full CRUD API for Company Notes in nested context.

    Requires:
    - workspace_id
    - company_id
    """

    service_class = CompanyNoteService
    selector_class = CompanyNoteSelector

    read_serializer_class = CompanyNoteSerializer
    write_serializer_class = CompanyNoteSerializer

    lookup_url_kwarg = "id"
    selector_lookup_field = "company_note_id"

    def get_queryset(self) -> QuerySet[CompanyNote]:
        return self.selector.list(
            user=self.request.user,
            filters=self._get_queryset_filters(),
        )

    def get_create_context(self) -> CompanyChildContext:
        return CompanyChildContext(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            id=None,
        )

    def get_update_context(self) -> CompanyChildContext:
        return CompanyChildContext(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            id=self.kwargs["id"],
        )

    def _get_queryset_filters(self) -> CompanyNoteQueryFilter:
        return CompanyNoteQueryFilter(
            workspace_id=self.request.query_params.get("workspace_id"),
            company_id=self.request.query_params.get("company_id"),
        )


# =========================================================
# Company Email
# =========================================================

class CompanyEmailViewSet(BaseReadOnlyViewSet):
    """
    Read-only API for Company Emails.
    """

    serializer_class = CompanyEmailSerializer

    selector_class = CompanyEmailSelector
    selector_lookup_field = "company_email_id"

    lookup_url_kwarg = "id"

    def get_queryset(self) -> QuerySet[CompanyEmail]:
        return self.selector.list(
            user=self.request.user,
            filters=self._get_queryset_filters(),
        )

    def _get_queryset_filters(self) -> CompanyEmailQueryFilter:
        return CompanyEmailQueryFilter(
            workspace_id=self.request.query_params.get("workspace_id"),
            company_id=self.request.query_params.get("company_id"),
        )


class NestedCompanyEmailViewSet(BaseContextServiceViewSet):
    """
    Full CRUD API for Company Emails in nested context.
    """

    service_class = CompanyEmailService
    selector_class = CompanyEmailSelector

    read_serializer_class = CompanyEmailSerializer
    write_serializer_class = CompanyEmailSerializer

    lookup_url_kwarg = "id"
    selector_lookup_field = "company_email_id"

    def get_queryset(self) -> QuerySet[CompanyEmail]:
        return self.selector.list(
            user=self.request.user,
            filters=self._get_queryset_filters(),
        )

    def get_create_context(self) -> CompanyChildContext:
        return CompanyChildContext(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            id=None,
        )

    def get_update_context(self) -> CompanyChildContext:
        return CompanyChildContext(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            id=self.kwargs["id"],
        )

    def _get_queryset_filters(self) -> CompanyEmailQueryFilter:
        return CompanyEmailQueryFilter(
            workspace_id=self.request.query_params.get("workspace_id"),
            company_id=self.request.query_params.get("company_id"),
        )


# =========================================================
# Job Benefit
# =========================================================

class JobBenefitViewSet(BaseIdServiceViewSet):
    """
    CRUD API for Job Benefits.
    """

    service_class = JobBenefitService
    selector_class = JobBenefitSelector

    read_serializer_class = JobBenefitSerializer
    write_serializer_class = JobBenefitSerializer

    lookup_url_kwarg = "id"
    selector_lookup_field = "job_benefit_id"
    service_lookup_id = "job_benefit_id"

    def get_queryset(self) -> QuerySet[JobBenefit]:
        return self.selector.list(user=self.request.user)


# =========================================================
# Job Task
# =========================================================

class JobTaskViewSet(BaseIdServiceViewSet):
    """
    CRUD API for Job Tasks.
    """

    service_class = JobTaskService
    selector_class = JobTaskSelector

    read_serializer_class = JobTaskSerializer
    write_serializer_class = JobTaskSerializer

    lookup_url_kwarg = "id"
    selector_lookup_field = "job_task_id"
    service_lookup_id = "job_task_id"

    def get_queryset(self) -> QuerySet[JobTask]:
        return self.selector.list(user=self.request.user)


# =========================================================
# Job Requirement
# =========================================================

class JobRequirementViewSet(BaseIdServiceViewSet):
    """
    CRUD API for Job Requirements.
    """

    service_class = JobRequirementService
    selector_class = JobRequirementSelector

    read_serializer_class = JobRequirementSerializer
    write_serializer_class = JobRequirementSerializer

    lookup_url_kwarg = "id"
    selector_lookup_field = "job_requirement_id"
    service_lookup_id = "job_requirement_id"

    def get_queryset(self) -> QuerySet[JobRequirement]:
        return self.selector.list(user=self.request.user)


# =========================================================
# Job Position
# =========================================================

class JobPositionViewSet(BaseReadOnlyViewSet):
    """
    Read-only API for Job Positions.
    """

    serializer_class = JobPositionSerializer

    selector_class = JobPositionSelector
    selector_lookup_field = "job_position_id"

    lookup_url_kwarg = "id"

    def get_queryset(self) -> QuerySet[JobPosition]:
        filters = self.selector.QueryFilter(
            workspace_id=self.request.query_params.get("workspace_id"),
            company_id=self.request.query_params.get("company_id"),
        )

        return self.selector.list(
            user=self.request.user,
            filters=filters,
        )


class NestedJobPositionViewSet(BaseContextServiceViewSet):
    """
    Full CRUD API for Job Positions in nested context.
    """

    service_class = JobPositionService
    selector_class = JobPositionSelector

    read_serializer_class = JobPositionSerializer
    write_serializer_class = JobPositionSerializer

    lookup_url_kwarg = "id"
    selector_lookup_field = "job_position_id"

    def get_queryset(self) -> QuerySet[JobPosition]:
        return self.selector.list(
            user=self.request.user,
            filters=self._get_queryset_filters(),
        )

    def get_create_context(self) -> CompanyChildContext:
        return CompanyChildContext(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            id=None,
        )

    def get_update_context(self) -> CompanyChildContext:
        return CompanyChildContext(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            id=self.kwargs["id"],
        )

    def _get_queryset_filters(self) -> JobPositionQueryFilter:
        return JobPositionQueryFilter(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            id=self.kwargs.get("id"),
        )
