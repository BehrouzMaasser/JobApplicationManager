"""
Read-only query helpers for the JobTask domain.

Selectors encapsulate data retrieval logic while keeping business logic
inside services.
"""

# Models
from apps.companies.models import JobTask

# Base Selector
from apps.core.common.selectors.base_selector import BaseSelector


class JobTaskSelector(BaseSelector[JobTask]):
    """
    Selector responsible for retrieving JobTask objects.

    Provides reusable read operations while enforcing ownership
    restrictions defined by BaseSelector.
    """

    MODEL = JobTask
    RESOURCE_NAME = "Job Task"
    LOOKUP_FIELD = "pk"
    OWNER_PATH = "user"
