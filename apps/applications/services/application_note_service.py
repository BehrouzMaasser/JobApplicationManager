"""
Service layer for JobApplicationNote domain logic.

This module handles creation, update, and deletion of job application
notes while enforcing workspace, company, job position, and job
application ownership rules.
"""

from typing import Any

from django.db import transaction

# Models
from apps.accounts.models import User
from apps.applications.models import JobApplicationNote

# Selectors
from apps.applications.selectors.application_note_selector import (
    JobApplicationNoteSelector,
)

# Services
from apps.applications.services.application_service import (
    JobApplicationService,
)

# Contexts
from apps.applications.services.contexts.application_context import (
    JobApplicationChildContext,
    JobApplicationContext,
)

# Exceptions
from apps.core.exceptions.exceptions import (
    DomainInvariantViolationError,
)


# Job Application Note Service
class JobApplicationNoteService(JobApplicationService):
    """
    Service responsible for managing JobApplicationNote domain operations.

    Ensures strict workspace, company, job position, and job application
    ownership validation for all operations.
    """

    CREATE_REQUIRED_FIELDS = {
        "title",
        "content",
    }

    UPDATABLE_FIELDS = CREATE_REQUIRED_FIELDS

    @staticmethod
    @transaction.atomic
    def create(
        *,
        user: User,
        context: JobApplicationChildContext,
        validated_data: dict[str, Any],
    ) -> JobApplicationNote:
        """
        Create a new JobApplicationNote under a JobApplication.

        Calls:
            - _resolve_job_application() to retrieve the parent job application.
            - django.db.models.base.Model.full_clean()
            - django.db.models.base.Model.save()

        Raises:
            ValidationError:
                If model validation fails.

            DomainInvariantViolationError:
                If the job application does not belong to the specified job
                position, company, or workspace.

        Returns:
            JobApplicationNote:
                The created job application note instance.
        """

        # Check if Context follows business rules and resolve Job Application
        job_application = JobApplicationNoteService._resolve_job_application(
            user=user,
            context=JobApplicationContext(
                id=context.job_application_id,
                workspace_id=context.workspace_id,
                company_id=context.company_id,
                job_position_id=context.job_position_id,
            ),
        )

        # ----------------------*****---------------------

        # Create the instance
        instance = JobApplicationNote(
            job_application=job_application,
            title=validated_data.get("title"),
            content=validated_data.get("content"),
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance
        instance.full_clean()
        instance.save()

        # ----------------------*****---------------------

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        user: User,
        context: JobApplicationChildContext,
        validated_data: dict[str, Any],
    ) -> JobApplicationNote:
        """
        Update an existing JobApplicationNote instance.

        Calls:
            - _resolve_job_application_note() to retrieve the target instance.
            - _update_non_m2m_fields() to apply updates.
            - django.db.models.base.Model.full_clean()
            - django.db.models.base.Model.save()

        Raises:
            ValidationError:
                If model validation fails.

            ResourceNotFoundError:
                If the JobApplicationNote does not exist.

            AccessDeniedError:
                If the user does not own the resource.

            DomainInvariantViolationError:
                If the note does not belong to the specified job application,
                job position, company, or workspace.

        Returns:
            JobApplicationNote:
                The updated job application note instance.
        """

        # Check if Context follows business rules and resolve Job Application Note
        instance = JobApplicationNoteService._resolve_job_application_note(
            user=user,
            context=context,
        )

        # ----------------------*****---------------------

        # Update scalar fields
        JobApplicationNoteService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=JobApplicationNoteService.UPDATABLE_FIELDS,
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance
        instance.full_clean()
        instance.save()

        # ----------------------*****---------------------

        return instance

    @staticmethod
    @transaction.atomic
    def remove(
        *,
        user: User,
        context: JobApplicationChildContext,
    ) -> None:
        """
        Remove a JobApplicationNote instance.

        Calls:
            - _resolve_job_application_note() to retrieve the target instance.
            - django.db.models.base.Model.delete()

        Raises:
            ResourceNotFoundError:
                If the JobApplicationNote does not exist.

            AccessDeniedError:
                If the user does not own the resource.

            DomainInvariantViolationError:
                If the note does not belong to the specified job application,
                job position, company, or workspace.

        Returns:
            None
        """

        # Check if Context follows business rules and resolve Job Application Note
        instance = JobApplicationNoteService._resolve_job_application_note(
            user=user,
            context=context,
        )

        # ----------------------*****---------------------

        instance.delete()

    @staticmethod
    def _resolve_job_application_note(
        *,
        user: User,
        context: JobApplicationChildContext,
    ) -> JobApplicationNote:
        """
        Resolve a JobApplicationNote and validate workspace, company,
        job position, and job application ownership.

        Calls:
            JobApplicationNoteSelector.get()

        Raises:
            ResourceNotFoundError:
                If the JobApplicationNote does not exist.

            AccessDeniedError:
                If the user does not own the resource.

            DomainInvariantViolationError:
                If the note does not belong to the specified job application,
                job position, company, or workspace.

        Returns:
            JobApplicationNote:
                The resolved job application note instance.
        """

        job_application_note = JobApplicationNoteSelector.get(
            user=user,
            application_note_id=context.id,
        )

        if job_application_note.job_application.pk != context.job_application_id:
            raise DomainInvariantViolationError(
                f"JobApplicationNote {context.id} does not belong to "
                f"JobApplication {context.job_application_id}"
            )

        if (
            job_application_note.job_application.job_position.pk
            != context.job_position_id
        ):
            raise DomainInvariantViolationError(
                f"JobApplicationNote {context.id}'s JobApplication "
                f"{context.job_application_id} does not belong to "
                f"JobPosition {context.job_position_id}"
            )

        if (
            job_application_note.job_application.job_position.company.pk
            != context.company_id
        ):
            raise DomainInvariantViolationError(
                f"JobApplicationNote {context.id}'s JobPosition "
                f"{context.job_position_id} does not belong to "
                f"Company {context.company_id}"
            )

        if (
            job_application_note.job_application.workspace.workspace_id
            != context.workspace_id
        ):
            raise DomainInvariantViolationError(
                f"JobApplicationNote {context.id}'s workspace does not belong "
                f"to Workspace {context.workspace_id}"
            )

        return job_application_note
