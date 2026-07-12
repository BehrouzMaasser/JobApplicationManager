"""
Read-only query helpers for the JobApplicationNote domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

# Models
from apps.applications.models import JobApplicationNote

# Base Selector
from apps.core.common.selectors.base_selector import BaseSelector

# For typings
from apps.core.common.types.filters import JobApplicationNoteQueryFilter
from django.db.models import QuerySet


class JobApplicationNoteSelector(BaseSelector[JobApplicationNote]):
    """
    Selector responsible for retrieving JobApplicationNote objects.

    Provides reusable read operations while enforcing ownership
    restrictions defined by BaseSelector.
    """

    MODEL = JobApplicationNote
    RESOURCE_NAME = "Job Application Note"
    LOOKUP_FIELD = "pk"
    OWNER_PATH = "job_application.owner"

    @classmethod
    def apply_filters(
            cls,
            queryset: QuerySet[JobApplicationNote],
            filters: JobApplicationNoteQueryFilter
    ) -> QuerySet[JobApplicationNote]:

        if workspace_id := filters.workspace_id:
            queryset = queryset.filter(
                job_application__workspace__workspace_id=workspace_id
            )

        if company_id := filters.company_id:
            queryset = queryset.filter(
                job_application__job_position__company__pk=company_id
            )

        if job_position_id := filters.job_position_id:
            queryset = queryset.filter(
                job_application__job_position__pk=job_position_id
            )

        if job_application_id := filters.job_application_id:
            queryset = queryset.filter(
                job_application__pk=job_application_id
            )

        if filters.id:
            queryset = queryset.filter(pk=filters.id)

        return queryset
