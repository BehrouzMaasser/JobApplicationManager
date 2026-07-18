"""
Context objects used by the companies services layer.

These dataclasses encapsulate identifiers required to operate on company-related
resources in a workspace-aware manner.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BaseContext:
    id: int | str | None = None


@dataclass(frozen=True, slots=True)
class EmptyContext(BaseContext):
    """
    Base context for document-related operations.

    Attributes:
        id: None
    """
    id = None


@dataclass(frozen=True, slots=True)
class DocumentContext(BaseContext):
    """
    Base context for document-related operations.

    Attributes:
        id: Optional document identifier. Used when operating on a specific document
         or document entity.
    """
    pass


@dataclass(frozen=True, slots=True)
class DocumentTypeContext(BaseContext):
    """
    Base context for document-type-related operations.

    Attributes:
        id: Optional document type identifier. Used when operating on a specific
         document type.

        document_id: Optional document identifier. Used when operating on a specific
         document related entity.
    """
    document_id: int | None = None


@dataclass(frozen=True, slots=True)
class WorkspaceContext(BaseContext):
    """
    Base context for workspace-related operations.

    Attributes:
        id: Optional workspace identifier. Used when operating on a specific workspace
         or workspace entity.
         It represents the workspace_id field of the Workspace Model.
    """
    pass


@dataclass(frozen=True, slots=True)
class JobBenefitContext(BaseContext):
    """
    Base context for job benefit operations.

    Attributes:
        id: Optional job benefit identifier. Used when operating on a specific
         job benefit entity.
    """
    pass


@dataclass(frozen=True, slots=True)
class JobRequirementContext(BaseContext):
    """
    Base context for job requirement operations.

    Attributes:
        id: Optional job benefit identifier. Used when operating on a specific
         job requirement entity.
    """
    pass


@dataclass(frozen=True, slots=True)
class JobTaskContext(BaseContext):
    """
    Base context for job task operations.

    Attributes:
        id: Optional job benefit identifier. Used when operating on a specific
         job task entity.
    """
    pass


@dataclass(frozen=True, slots=True)
class CompanyContext(WorkspaceContext):
    """
    Base context for company-related operations.

    Attributes:
        id: Optional company identifier. Used when operating on a specific company
         or company entity.

        workspace_id: Identifier of the workspace that owns the company.
    """

    workspace_id: str | None = None


@dataclass(frozen=True, slots=True)
class CompanyChildContext(CompanyContext):
    """
    Extended context for company child entities.

    Used when operating on resources that belong to a specific company.

    Attributes:
        id: Optional company identifier. Used when operating on a specific company
         or company entity.

        workspace_id: Identifier of the workspace that owns the company.

        company_id: Optional company identifier. Used when operating on a specific
         child company entity owned by the company.
    """

    company_id: int | None = None


@dataclass(frozen=True, slots=True)
class JobApplicationContext(CompanyChildContext):
    """
    Base context for job application-related operations.

    Attributes:
        id: Optional company identifier. Used when operating on a specific company
         or company entity.

        workspace_id: Identifier of the workspace that owns the company.

        company_id: Optional company identifier. Used when operating on a specific
         child company entity owned by the company.

        job_position_id: Optional job position identifier. Used when operating a
         specific child of a job position entity owned by the job position.
    """

    job_position_id: int | None = None


@dataclass(frozen=True, slots=True)
class JobApplicationChildContext(JobApplicationContext):
    """
    Base context for job application note operations.

    Attributes:
        id: Optional company identifier. Used when operating on a specific company
         or company entity.

        workspace_id: Identifier of the workspace that owns the company.

        company_id: Optional company identifier. Used when operating on a specific
         child company entity owned by the company.

        job_position_id: Optional job position identifier. Used when operating a
         specific child of a job position entity owned by the job position.

        job_application_id: Optional job application identifier. Used when operating
         on a specific child of a job application entity owned by the
          job application.
    """

    job_application_id: int | None = None
