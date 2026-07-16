"""
Service layer for JobApplication domain logic.

This module handles creation, update, and deletion of job application
records while enforcing workspace, company, job position, document,
and email ownership rules.
"""

from typing import Any, Iterable

# Models
from apps.accounts.models import User
from apps.applications.models import JobApplication
from apps.companies.models import (
    CompanyEmail,
    JobPosition,
)
from apps.core.common.services.base_service import BaseService
from apps.documents.models import Document

# Selectors
from apps.applications.selectors.application_selector import (
    JobApplicationSelector,
)

# Contexts
from apps.core.common.contexts.base_context import (
    CompanyChildContext,
    JobApplicationContext,
)

# Exceptions
from apps.core.exceptions.exceptions import (
    BusinessRuleViolationError,
    DomainInvariantViolationError,
)

# Services
from apps.companies.services.job_position_service import JobPositionService


# Job Application Service
class JobApplicationService(BaseService):
    """
    Service responsible for managing JobApplication domain operations.

    Ensures strict workspace, company, job position, email, and document
    ownership validation for all operations.
    """

    MODEL = JobApplication
    SELECTOR = JobApplicationSelector

    CREATE_FIELDS = (
        "owner",
        "workspace",
        "job_position",
        "status",
        "date_applied",
    )
    SCALAR_UPDATABLE_FIELDS = (
        "status",
        "date_applied",
    )
    REQUIRED_M2M_FIELDS = ()
    M2M_UPDATABLE_FIELDS = (
        "emails",
        "documents",
    )
    NON_EMPTY_M2M_FIELDS = REQUIRED_M2M_FIELDS
    M2M_OWNER_FIELD_MAP = {}

    @classmethod
    def _create_validate(
            cls,
            *,
            user: User,
            instance: JobApplication,
            validated_data: dict[str, Any],
    ):

        if validated_data.get("emails"):
            cls._validate_emails_ownership(
                user=user,
                emails=validated_data["emails"],
                job_position=instance.job_position,
            )

        if validated_data.get("documents"):
            cls._validate_documents_ownership(
                user=user,
                documents=validated_data["documents"],
            )

    @classmethod
    def _update_validate(
            cls,
            *,
            user: User,
            instance: JobApplication,
            validated_data: dict[str, Any],
    ):

        cls._validate_emails_ownership(
            user=user,
            emails=validated_data.get("emails", []),
            job_position=instance.job_position,
        )

        cls._validate_documents_ownership(
            user=user,
            documents=validated_data.get("documents", []),
        )

    @classmethod
    def _resolve_create_dependencies(
            cls,
            user: User,
            context: JobApplicationContext
    ) -> dict[str, Any]:

        job_position: JobPosition = JobPositionService._resolve_instance(
            user=user,
            context=CompanyChildContext(
                id=context.company_id,
                workspace_id=context.workspace_id,
                company_id=context.company_id,
            ),
        )

        return {
            "owner": user,
            "job_position": job_position,
            "workspace": job_position.company.workspace,
        }

    @classmethod
    def _validate_resolved_instance(
        cls,
        *,
        instance: JobApplication,
        context: JobApplicationContext,
    ) -> None:

        if instance.job_position.pk != context.job_position_id:
            raise DomainInvariantViolationError(
                f"JobApplication {context.id} does not belong to "
                f"JobPosition {context.job_position_id}"
            )

        if instance.job_position.company.pk != context.company_id:
            raise DomainInvariantViolationError(
                f"JobApplication {context.id}'s JobPosition "
                f"{context.job_position_id} does not belong to "
                f"Company {context.company_id}"
            )

        if instance.workspace.workspace_id != context.workspace_id:
            raise DomainInvariantViolationError(
                f"JobApplication {context.id}'s workspace does not belong to "
                f"Workspace {context.workspace_id}"
            )

    @staticmethod
    def _validate_emails_ownership(
        *,
        user: User,
        emails: Iterable[CompanyEmail],
        job_position: JobPosition,
    ) -> None:
        """
        Validate ownership of application emails.

        Ensures that every email belongs to the user and to the same company
        as the JobApplication's JobPosition.

        Raises:
            BusinessRuleViolationError:
                If any email violates ownership or company constraints.
        """

        # Each Application Email belongs to User
        if any(user != email.company.workspace.owner for email in emails):
            raise BusinessRuleViolationError(
                fields=["emails"],
                messages=["Not All Emails Belong To User"],
            )

        # Each Email belongs to the JobApplication's company
        if any(job_position.company != email.company for email in emails):
            raise BusinessRuleViolationError(
                fields=["emails"],
                messages=["Not All Emails Belong To Job Application's Company"],
            )

    @staticmethod
    def _validate_documents_ownership(
        *,
        user: User,
        documents: Iterable[Document],
    ) -> None:
        """
        Validate ownership of application documents.

        Ensures that every document belongs to the user.

        Raises:
            BusinessRuleViolationError:
                If any document does not belong to the user.
        """

        if any(user != document.owner for document in documents):
            raise BusinessRuleViolationError(
                fields=["documents"],
                messages=["Not All Documents Belong To User"],
            )
