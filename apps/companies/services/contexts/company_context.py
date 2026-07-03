"""
Context objects used by the companies services layer.

These dataclasses encapsulate identifiers required to operate on company-related
resources in a workspace-aware manner.
"""

from dataclasses import dataclass


@dataclass
class CompanyContext:
    """
    Base context for company-related operations.

    Attributes:
        id: Optional company identifier. Used when operating on a specific company
         or company entity.
        workspace_id: Identifier of the workspace that owns the company.
    """

    id: int | None
    workspace_id: str


@dataclass
class CompanyChildContext(CompanyContext):
    """
    Extended context for company child entities.

    Used when operating on resources that belong to a specific company.
    """

    company_id: int
