"""
Read-only query helpers for the JobBenefit domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

# Models
from apps.companies.models import JobBenefit

# Base Selector
from apps.core.common.selectors.base_selector import BaseSelector


class JobBenefitSelector(BaseSelector[JobBenefit]):
    """
    Selector responsible for retrieving JobBenefit objects.

    Provides reusable read operations while enforcing ownership
    restrictions defined by BaseSelector.
    """

    MODEL = JobBenefit
    RESOURCE_NAME = "Job Benefit"
    LOOKUP_FIELD = "pk"
    OWNER_PATH = "owner"
