"""
Service layer for JobApplication domain logic.

This module handles creation, update, and deletion of job application
records while enforcing workspace, company, job position, document,
and email ownership rules.
"""

from typing import Any, Iterable

from django.db import transaction

# Models
from apps.accounts.models import User
from apps.applications.models import JobApplication
from apps.companies.models import (
    CompanyEmail,
    JobPosition,
)
from apps.documents.models import Document

# Selectors
from apps.applications.selectors.application_selector import (
    JobApplicationSelector,
)

# Contexts
from apps.applications.services.contexts.application_context import (
    JobApplicationContext,
)
from apps.companies.services.contexts.company_context import (
    CompanyChildContext,
)

# Exceptions
from apps.core.exceptions.exceptions import (
    BusinessRuleViolationError,
    DomainInvariantViolationError,
)

# Services
from apps.companies.services.job_position_service import JobPositionService


# Job Application Service
class JobApplicationService(JobPositionService):
    """
    Service responsible for managing JobApplication domain operations.

    Ensures strict workspace, company, job position, email, and document
    ownership validation for all operations.
    """

    REQUIRED_M2M_FIELDS = set()

    NON_M2M_FIELDS = {
        "status",
        "date_applied",
    }

    CREATE_REQUIRED_FIELDS = {
        *REQUIRED_M2M_FIELDS,
        "status",
    }

    M2M_FIELDS = {
        *REQUIRED_M2M_FIELDS,
        "emails",
        "documents",
    }

    UPDATABLE_FIELDS = {
        *CREATE_REQUIRED_FIELDS,
        *M2M_FIELDS,
        "date_applied",
    }

    M2M_FIELD_OWNERSHIP_MAP = {
        "emails": "owner",
        "documents": "owner",
    }

    @staticmethod
    @transaction.atomic
    def create(
        *,
        user: User,
        context: JobApplicationContext,
        validated_data: dict[str, Any],
    ) -> JobApplication:
        """
        Create a new JobApplication under a JobPosition.

        Calls:
            - _resolve_job_position() to retrieve the parent job position.
            - _validate_emails_ownership() to validate email ownership.
            - _validate_documents_ownership() to validate document ownership.
            - django.db.models.base.Model.full_clean()
            - django.db.models.base.Model.save()
            - _add_m2m_fields() to add many-to-many relationships.

        Raises:
            ValidationError:
                If model validation fails.

            BusinessRuleViolationError:
                If the provided emails or documents violate ownership rules.

            DomainInvariantViolationError:
                If the job position does not belong to the specified company or
                workspace.

        Returns:
            JobApplication:
                The created job application instance.
        """

        # Check if Context follows business rules and resolve Job Position
        job_position = JobApplicationService._resolve_job_position(
            user=user,
            context=CompanyChildContext(
                id=context.job_position_id,
                workspace_id=context.workspace_id,
                company_id=context.company_id,
            ),
        )

        # ----------------------*****---------------------

        # Validate many-to-many ownership
        if validated_data.get("emails"):
            JobApplicationService._validate_emails_ownership(
                user=user,
                emails=validated_data["emails"],
                job_position=job_position,
            )

        if validated_data.get("documents"):
            JobApplicationService._validate_documents_ownership(
                user=user,
                documents=validated_data["documents"],
            )

        # ----------------------*****---------------------

        # Create the instance
        instance = JobApplication(
            owner=user,
            workspace=job_position.company.workspace,
            job_position=job_position,
            status=validated_data.get("status"),
            date_applied=validated_data.get("date_applied"),
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance
        instance.full_clean()
        instance.save()

        # ----------------------*****---------------------

        # Add many-to-many relations
        JobApplicationService._add_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            m2m_fields=JobApplicationService.M2M_FIELDS,
        )

        # ----------------------*****---------------------

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        user: User,
        context: JobApplicationContext,
        validated_data: dict[str, Any],
    ) -> JobApplication:
        """
        Update an existing JobApplication instance.

        Calls:
            - _resolve_job_application() to retrieve the target instance.
            - _validate_emails_ownership() to validate email ownership.
            - _validate_documents_ownership() to validate document ownership.
            - _update_non_m2m_fields() to update scalar fields.
            - django.db.models.base.Model.full_clean()
            - django.db.models.base.Model.save()
            - _update_m2m_fields() to update many-to-many relationships.

        Raises:
            ValidationError:
                If model validation fails.

            ResourceNotFoundError:
                If the JobApplication does not exist.

            AccessDeniedError:
                If the user does not own the resource.

            BusinessRuleViolationError:
                If the provided emails or documents violate ownership rules.

            DomainInvariantViolationError:
                If the job application does not belong to the specified job
                position, company, or workspace.

        Returns:
            JobApplication:
                The updated job application instance.
        """

        # Check if Context follows business rules and resolve Job Application
        instance = JobApplicationService._resolve_job_application(
            user=user,
            context=context,
        )

        # ----------------------*****---------------------

        # Validate many-to-many ownership
        JobApplicationService._validate_emails_ownership(
            user=user,
            emails=validated_data.get("emails", []),
            job_position=instance.job_position,
        )

        JobApplicationService._validate_documents_ownership(
            user=user,
            documents=validated_data.get("documents", []),
        )

        # ----------------------*****---------------------

        # Update scalar fields
        JobApplicationService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=JobApplicationService.NON_M2M_FIELDS,
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance
        instance.full_clean()
        instance.save()

        # ----------------------*****---------------------

        # Update many-to-many relationships
        JobApplicationService._update_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=JobApplicationService.M2M_FIELDS,
        )

        # ----------------------*****---------------------

        return instance

    @staticmethod
    @transaction.atomic
    def remove(
        *,
        user: User,
        context: JobApplicationContext,
    ) -> None:
        """
        Remove a JobApplication instance.

        Calls:
            - _resolve_job_application() to retrieve the target instance.
            - django.db.models.base.Model.delete()

        Raises:
            ResourceNotFoundError:
                If the JobApplication does not exist.

            AccessDeniedError:
                If the user does not own the resource.

            DomainInvariantViolationError:
                If the job application does not belong to the specified job
                position, company, or workspace.

        Returns:
            None
        """

        # Check if Context follows business rules and resolve Job Application
        instance = JobApplicationService._resolve_job_application(
            user=user,
            context=context,
        )

        # ----------------------*****---------------------

        instance.delete()

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

    @staticmethod
    def _resolve_job_application(
        *,
        user: User,
        context: JobApplicationContext,
    ) -> JobApplication:
        """
        Resolve a JobApplication and validate workspace, company, and job
        position ownership.

        Calls:
            JobApplicationSelector.get()

        Raises:
            ResourceNotFoundError:
                If the JobApplication does not exist.

            AccessDeniedError:
                If the user does not own the resource.

            DomainInvariantViolationError:
                If the job application does not belong to the specified job
                position, company, or workspace.

        Returns:
            JobApplication:
                The resolved job application instance.
        """

        job_application = JobApplicationSelector.get(
            user=user,
            application_id=context.id,
        )

        if job_application.job_position.pk != context.job_position_id:
            raise DomainInvariantViolationError(
                f"JobApplication {context.id} does not belong to "
                f"JobPosition {context.job_position_id}"
            )

        if job_application.job_position.company.pk != context.company_id:
            raise DomainInvariantViolationError(
                f"JobApplication {context.id}'s JobPosition "
                f"{context.job_position_id} does not belong to "
                f"Company {context.company_id}"
            )

        if job_application.workspace.workspace_id != context.workspace_id:
            raise DomainInvariantViolationError(
                f"JobApplication {context.id}'s workspace does not belong to "
                f"Workspace {context.workspace_id}"
            )

        return job_application
