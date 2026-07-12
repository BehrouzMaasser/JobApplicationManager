"""
Read-only query helpers for the CompanyNote domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

# Models
from apps.companies.models import CompanyNote

# Base Selector
from apps.core.common.selectors.base_selector import BaseSelector

# For typings
from apps.core.common.types.filters import CompanyNoteQueryFilter
from django.db.models import QuerySet


class CompanyNoteSelector(BaseSelector[CompanyNote]):
    """
    Selector responsible for retrieving CompanyNote objects.

    Provides reusable read operations while enforcing ownership
    restrictions defined by BaseSelector.
    """

    MODEL = CompanyNote
    RESOURCE_NAME = "Company Note"
    LOOKUP_FIELD = "pk"
    OWNER_PATH = "company.workspace.owner"

    @classmethod
    def apply_filters(
            cls,
            queryset: QuerySet[CompanyNote],
            filters: CompanyNoteQueryFilter
    ) -> QuerySet[CompanyNote]:

        if workspace_id := filters.workspace_id:
            queryset = queryset.filter(company__workspace__workspace_id=workspace_id)

        if company_id := filters.company_id:
            queryset = queryset.filter(company__pk=company_id)

        if filters.id:
            queryset = queryset.filter(pk=filters.id)

        return queryset
