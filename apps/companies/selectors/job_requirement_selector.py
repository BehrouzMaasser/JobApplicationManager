"""
Read-only query helpers for the JobRequirement domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

# Models
from apps.companies.models import JobRequirement

# Base Selector
from apps.core.common.selectors.base_selector import BaseSelector


class JobRequirementSelector(BaseSelector[JobRequirement]):
    """
    Selector responsible for retrieving JobRequirement objects.

    Provides reusable read operations while enforcing ownership
    restrictions defined by BaseSelector.
    """

    MODEL = JobRequirement
    RESOURCE_NAME = "Job Requirement"
    LOOKUP_FIELD = "pk"
    OWNER_PATH = "user"
