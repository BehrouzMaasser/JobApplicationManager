"""
Read-only query helpers for the JobApplication domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

# Models
from apps.applications.models import JobApplication

# Base Selector
from apps.core.common.selectors.base_selector import BaseSelector

# For typings
from apps.core.common.types.filters import JobApplicationQueryFilter
from django.db.models import QuerySet


class JobApplicationSelector(BaseSelector[JobApplication]):
    """
    Selector responsible for retrieving JobApplication objects.

    Provides reusable read operations while enforcing ownership
    restrictions defined by BaseSelector.
    """

    MODEL = JobApplication
    RESOURCE_NAME = "Job Application"
    LOOKUP_FIELD = "pk"
    OWNER_PATH = "owner"

    @classmethod
    def apply_filters(
            cls,
            queryset: QuerySet[JobApplication],
            filters: JobApplicationQueryFilter
    ) -> QuerySet[JobApplication]:

        if (workspace_id := filters.workspace_id) is not None:
            queryset = queryset.filter(workspace__workspace_id=workspace_id)

        if (company_id := filters.company_id) is not None:
            queryset = queryset.filter(job_position__company__pk=company_id)

        if (job_position_id := filters.job_position_id) is not None:
            queryset = queryset.filter(job_position__pk=job_position_id)

        if filters.id is not None:
            queryset = queryset.filter(pk=filters.id)

        if (status_id := filters.status_id) is not None:
            queryset = queryset.filter(status__pk=status_id)

        if (date_applied := filters.date_applied) is not None:
            queryset = queryset.filter(date_applied=date_applied)

        return queryset
