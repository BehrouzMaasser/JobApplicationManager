"""
Read-only query helpers for the CompanyNote domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

# For typings
from django.db.models import QuerySet
from apps.core.common.types.filters import JobPositionQueryFilter

# Models
from apps.companies.models import JobPosition

# Base Selector
from apps.core.common.selectors.base_selector import BaseSelector


class JobPositionSelector(BaseSelector[JobPosition]):
    """
    Selector responsible for retrieving JobPosition objects.

    Provides reusable read operations while enforcing ownership
    restrictions defined by BaseSelector.
    """

    MODEL = JobPosition
    RESOURCE_NAME = "Job Position"
    LOOKUP_FIELD = "pk"
    OWNER_PATH = "company.workspace.owner"

    @classmethod
    def apply_filters(
            cls,
            queryset: QuerySet[JobPosition],
            filters: JobPositionQueryFilter
    ) -> QuerySet[JobPosition]:

        if workspace_id := filters.workspace_id:
            queryset = queryset.filter(company__workspace__workspace_id=workspace_id)

        if company_id := filters.company_id:
            queryset = queryset.filter(company__pk=company_id)

        if filters.id:
            queryset = queryset.filter(pk=filters.id)

        return queryset
