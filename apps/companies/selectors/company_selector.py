"""
Read-only query helpers for the Company domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

# Models
from apps.companies.models import Company

# For typings
from django.db.models import QuerySet
from apps.core.common.types.filters import CompanyQueryFilter

# Base Selector
from apps.core.common.selectors.base_selector import BaseSelector


class CompanySelector(BaseSelector[Company]):
    """
    Selector responsible for retrieving Company objects.

    Provides reusable read operations while enforcing ownership
    restrictions defined by BaseSelector.
    """

    MODEL = Company
    RESOURCE_NAME = "Company"
    LOOKUP_FIELD = "pk"
    OWNER_PATH = "workspace.owner"

    @classmethod
    def apply_filters(
            cls,
            queryset: QuerySet[Company],
            filters: CompanyQueryFilter
    ) -> QuerySet[Company]:

        if (workspace_id := filters.workspace_id) is not None:
            queryset = queryset.filter(workspace__workspace_id=workspace_id)

        if filters.id is not None:
            queryset = queryset.filter(pk=filters.id)

        return queryset
