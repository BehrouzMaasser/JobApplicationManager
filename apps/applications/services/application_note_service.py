from django.db import transaction

# Models
from apps.accounts.models import User
from apps.applications.models import JobApplicationNote

# Selectors
from apps.applications.selectors.application_note_selector import (
    JobApplicationNoteSelector
)

# Services
from apps.applications.services.application_service import (
    JobApplicationService
)

# Contexts
from apps.applications.services.contexts.application_context import (
    JobApplicationChildContext, JobApplicationContext
)

# Exceptions
from apps.core.exceptions.exceptions import BusinessRuleViolationError


class JobApplicationNoteService(JobApplicationService):

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
        validated_data: dict
    ) -> JobApplicationNote:

        # Domain Correctness Validation:

        # Check if Context follows business rules and resolve Job Application
        job_application = JobApplicationNoteService._resolve_job_application(
            user=user,
            context=JobApplicationContext(
                id=context.job_application_id,
                workspace_id=context.workspace_id,
                company_id=context.company_id,
                job_position_id=context.job_position_id,
            )
        )

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
        validated_data: dict
    ) -> JobApplicationNote:

        # Check if Context follows business rules and resolve Job Application Note
        instance = JobApplicationNoteService._resolve_job_application_note(
            user=user,
            context=context
        )

        # ----------------------*****---------------------

        # Update all fields:
        JobApplicationNoteService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=JobApplicationNoteService.UPDATABLE_FIELDS
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        instance.full_clean()
        instance.save()

        # ----------------------*****---------------------

        return instance

    @staticmethod
    @transaction.atomic
    def remove(*, user: User, context: JobApplicationChildContext) -> None:

        # Domain Correctness Validation:

        # Check if Context follows business rules and resolve Job Application Note
        instance = JobApplicationNoteService._resolve_job_application_note(
            user=user,
            context=context
        )

        # ----------------------*****---------------------

        instance.delete()

    @staticmethod
    def _resolve_job_application_note(
            user: User, context: JobApplicationChildContext
    ) -> JobApplicationNote:

        job_application_note = JobApplicationNoteSelector.get(
            user=user, application_note_id=context.id
        )

        if job_application_note.job_application.pk != context.job_application_id:
            raise BusinessRuleViolationError(
                f"Job Application Note {job_application_note.pk} does not belong to"
                f" Job Application {context.job_application_id}"
            )

        if (job_application_note.job_application.job_position.pk !=
                context.job_position_id):
            raise BusinessRuleViolationError(
                f"Job Position of Job Application Note {job_application_note.pk} "
                f"does not match the Job Position given {context.job_position_id}"
            )

        if (job_application_note.job_application.job_position.company.pk !=
                context.company_id):
            raise BusinessRuleViolationError(
                f"Company of Job Application Note {job_application_note.pk} "
                f"does not match the Company given {context.company_id}"
            )

        if (job_application_note.job_application.workspace.workspace_id !=
                context.workspace_id):
            raise BusinessRuleViolationError(
                f"Workspace of Job Application Note {job_application_note.pk} "
                f"does not match the Workspace given {context.workspace_id}"
            )

        return job_application_note
