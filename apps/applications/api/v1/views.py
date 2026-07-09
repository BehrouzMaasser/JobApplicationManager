"""
REST API views for managing the Applications domain.

This module defines DRF ViewSets that:
- Delegate read operations to selector layer
- Delegate write operations to service layer
- Enforce consistent lookup behavior for nested resources
"""

from django.db.models import QuerySet

# Serializers
from apps.applications.api.v1.serializers import (
    JobApplicationSerializer,
    JobApplicationNoteSerializer,
)

# Models (for typing only)
from apps.applications.models import (
    JobApplication,
    JobApplicationNote,
)

# Selectors
from apps.applications.selectors.application_selector import (
    JobApplicationSelector,
)
from apps.applications.selectors.application_note_selector import (
    JobApplicationNoteSelector,
)

# Services
from apps.applications.services.application_service import (
    JobApplicationService,
)
from apps.applications.services.application_note_service import (
    JobApplicationNoteService,
)

# Contexts
from apps.applications.services.contexts.application_context import (
    JobApplicationContext,
    JobApplicationChildContext,
)

# Base ViewSets
from apps.core.common.api.viewsets import (
    BaseReadOnlyViewSet,
    BaseContextServiceViewSet,
)


# =========================================================
# Job Application
# =========================================================

class JobApplicationViewSet(BaseReadOnlyViewSet):
    """
    Read-only API for Job Applications.

    Responsibilities:
    - List and retrieve job applications
    - Delegate queries to JobApplicationSelector
    - Support optional filtering
    """

    serializer_class = JobApplicationSerializer

    selector_class = JobApplicationSelector
    selector_lookup_field = "application_id"

    lookup_url_kwarg = "id"

    def get_queryset(self) -> QuerySet[JobApplication]:
        """
        Return filtered job applications for the authenticated user.
        """

        return self.selector.list(
            user=self.request.user,
            filters=self._get_queryset_filters(),
        )

    def _get_queryset_filters(
        self,
    ) -> JobApplicationSelector.QueryFilter:
        """
        Build selector filter object from query parameters.
        """

        return JobApplicationSelector.QueryFilter(
            workspace_id=self.request.query_params.get("workspace_id"),
            company_id=self.request.query_params.get("company_id"),
            job_position_id=self.request.query_params.get("job_position_id"),
            status_id=self.request.query_params.get("status_id"),
            date_applied=self.request.query_params.get("date_applied"),
        )


class NestedJobApplicationViewSet(BaseContextServiceViewSet):
    """
    Full CRUD API for Job Applications in nested context.

    Requires:
    - workspace_id
    - company_id
    - job_position_id
    """

    service_class = JobApplicationService
    selector_class = JobApplicationSelector

    read_serializer_class = JobApplicationSerializer
    write_serializer_class = JobApplicationSerializer

    lookup_url_kwarg = "id"
    selector_lookup_field = "application_id"

    def get_queryset(self) -> QuerySet[JobApplication]:
        """
        Return job applications scoped to a job position.
        """

        return self.selector.list(
            user=self.request.user,
            filters=self._get_queryset_filters(),
        )

    def get_create_context(self) -> JobApplicationContext:
        """
        Context used when creating a job application.
        """

        return JobApplicationContext(
            id=None,
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            job_position_id=self.kwargs["job_position_id"],
        )

    def get_update_context(self) -> JobApplicationContext:
        """
        Context used when updating or deleting a job application.
        """

        return JobApplicationContext(
            id=self.kwargs["id"],
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            job_position_id=self.kwargs["job_position_id"],
        )

    def _get_queryset_filters(
        self,
    ) -> JobApplicationSelector.QueryFilter:
        return JobApplicationSelector.QueryFilter(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            job_position_id=self.kwargs["job_position_id"],
        )


# =========================================================
# Job Application Note
# =========================================================

class JobApplicationNoteViewSet(BaseReadOnlyViewSet):
    """
    Read-only API for Job Application Notes.

    Responsibilities:
    - List and retrieve application notes
    - Delegate queries to JobApplicationNoteSelector
    - Support optional filtering
    """

    serializer_class = JobApplicationNoteSerializer

    selector_class = JobApplicationNoteSelector
    selector_lookup_field = "application_note_id"

    lookup_url_kwarg = "id"

    def get_queryset(self) -> QuerySet[JobApplicationNote]:
        """
        Return filtered application notes for the authenticated user.
        """

        return self.selector.list(
            user=self.request.user,
            filters=self._get_queryset_filters(),
        )

    def _get_queryset_filters(
        self,
    ) -> JobApplicationNoteSelector.QueryFilter:
        """
        Build selector filter object from query parameters.
        """

        return JobApplicationNoteSelector.QueryFilter(
            workspace_id=self.request.query_params.get("workspace_id"),
            company_id=self.request.query_params.get("company_id"),
            job_position_id=self.request.query_params.get("job_position_id"),
            job_application_id=self.request.query_params.get(
                "job_application_id"
            ),
        )


class NestedJobApplicationNoteViewSet(BaseContextServiceViewSet):
    """
    Full CRUD API for Job Application Notes in nested context.

    Requires:
    - workspace_id
    - company_id
    - job_position_id
    - job_application_id
    """

    service_class = JobApplicationNoteService
    selector_class = JobApplicationNoteSelector

    read_serializer_class = JobApplicationNoteSerializer
    write_serializer_class = JobApplicationNoteSerializer

    lookup_url_kwarg = "id"
    selector_lookup_field = "application_note_id"

    def get_queryset(self) -> QuerySet[JobApplicationNote]:
        """
        Return application notes scoped to a job application.
        """

        return self.selector.list(
            user=self.request.user,
            filters=self._get_queryset_filters(),
        )

    def get_create_context(self) -> JobApplicationChildContext:
        """
        Context used when creating a job application note.
        """

        return JobApplicationChildContext(
            id=None,
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            job_position_id=self.kwargs["job_position_id"],
            job_application_id=self.kwargs["job_application_id"],
        )

    def get_update_context(self) -> JobApplicationChildContext:
        """
        Context used when updating or deleting a job application note.
        """

        return JobApplicationChildContext(
            id=self.kwargs["id"],
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            job_position_id=self.kwargs["job_position_id"],
            job_application_id=self.kwargs["job_application_id"],
        )

    def _get_queryset_filters(
        self,
    ) -> JobApplicationNoteSelector.QueryFilter:
        return JobApplicationNoteSelector.QueryFilter(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            job_position_id=self.kwargs["job_position_id"],
            job_application_id=self.kwargs["job_application_id"],
        )
