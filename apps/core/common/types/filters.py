from datetime import datetime
from dataclasses import dataclass
from uuid import UUID


@dataclass(slots=True, frozen=True)
class BaseQueryFilter:
    """Base class for selector query filters."""

    id: int | None = None


@dataclass(slots=True, frozen=True)
class WorkspaceQueryFilter(BaseQueryFilter):
    """Base filter for resources belonging to a workspace."""

    workspace_id: UUID | None = None


@dataclass(slots=True, frozen=True)
class CompanyQueryFilter(WorkspaceQueryFilter):
    """Base filter for resources belonging to a company."""

    pass


@dataclass(slots=True, frozen=True)
class CompanyChildQueryFilter(CompanyQueryFilter):
    """Base filter for resources belonging to objects belong to a company."""

    company_id: int | None = None


@dataclass(slots=True, frozen=True)
class CompanyEmailQueryFilter(CompanyChildQueryFilter):
    """Base filter for resources belonging to a company email."""

    pass


@dataclass(slots=True, frozen=True)
class CompanyNoteQueryFilter(CompanyChildQueryFilter):
    """Base filter for resources belonging to a company note."""

    pass


@dataclass(slots=True, frozen=True)
class JobPositionQueryFilter(CompanyChildQueryFilter):
    """Base filter for resources belonging to a job position."""

    pass


@dataclass(slots=True, frozen=True)
class DocumentQueryFilter(BaseQueryFilter):
    """Base filter for resources belonging to a document."""

    document_type_id: int | None = None


@dataclass(slots=True, frozen=True)
class DocumentTypeQueryFilter(BaseQueryFilter):
    """Base filter for resources belonging to a document type."""

    pass


@dataclass(slots=True, frozen=True)
class JobApplicationQueryFilter(CompanyChildQueryFilter):
    """Base filter for resources belonging to a job application."""

    job_position_id: int | None = None
    status_id: int | None = None
    date_applied: datetime | None = None


@dataclass(slots=True, frozen=True)
class JobApplicationNoteQueryFilter(CompanyChildQueryFilter):
    """Base filter for resources belonging to a job application note."""

    job_position_id: int | None = None
    job_application_id: int | None = None
