"""
Read-only query helpers for the CompanyEmail domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

# Models
from apps.companies.models import CompanyEmail

# Base Selector
from apps.core.common.selectors.base_selector import BaseSelector

# For typings
from apps.core.common.types.filters import CompanyEmailQueryFilter
from django.db.models import QuerySet


class CompanyEmailSelector(BaseSelector[CompanyEmail]):
    """
    Selector responsible for retrieving CompanyEmail objects.

    Provides reusable read operations while enforcing ownership
    restrictions defined by BaseSelector.
    """

    MODEL = CompanyEmail
    RESOURCE_NAME = "Company Email"
    LOOKUP_FIELD = "pk"
    OWNER_PATH = "company.workspace.owner"

    @classmethod
    def apply_filters(
            cls,
            queryset: QuerySet[CompanyEmail],
            filters: CompanyEmailQueryFilter
    ) -> QuerySet[CompanyEmail]:

        if workspace_id := filters.workspace_id:
            queryset = queryset.filter(company__workspace__workspace_id=workspace_id)

        if company_id := filters.company_id:
            queryset = queryset.filter(company__pk=company_id)

        if filters.id:
            queryset = queryset.filter(id=filters.id)

        return queryset
