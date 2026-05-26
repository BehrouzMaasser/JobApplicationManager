from typing import Iterable

from django.db import transaction
from rest_framework.exceptions import ValidationError, PermissionDenied

# Models
from apps.accounts.models import User
from apps.applications.models import JobApplication
from apps.companies.services.contexts.company_context import CompanyChildContext
from apps.documents.models import Document

from apps.companies.models import (
    JobPosition,
    CompanyEmail
)

# Contexts
from apps.applications.services.contexts.application_context import (
    JobApplicationContext
)

# Services
from apps.companies.services.job_position_service import JobPositionService


class JobApplicationService(JobPositionService):

    REQUIRED_M2M_FIELDS = set()

    NON_M2M_FIELDS = {
        "status",
        "date_applied"
    }

    CREATE_REQUIRED_FIELDS = {
        *REQUIRED_M2M_FIELDS,
        "status",
    }

    M2M_FIELDS = {
        *REQUIRED_M2M_FIELDS,
        "emails",
        "documents"
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
        validated_data: dict
    ) -> JobApplication:

        # Domain Correctness Validation

        # Check if Context follows business rules and resolve Job Position
        job_position = JobApplicationService._resolve_job_position(
            user=user,
            context=CompanyChildContext(
                id=context.job_position_id,
                workspace_id=context.workspace_id,
                company_id=context.company_id
            )
        )

        # Many-to-many fields ownership validations
        if validated_data.get("emails"):
            JobApplicationService._validate_emails_ownership(
                user=user,
                emails=validated_data["emails"],
                job_position=job_position
            )

        if validated_data.get("documents"):
            JobApplicationService._validate_documents_ownership(
                user=user,
                documents=validated_data["documents"],
            )

        instance = JobApplication(
            owner=user,
            workspace=job_position.company.workspace,
            job_position=job_position,
            status=validated_data.get("status"),
            date_applied=validated_data.get("date_applied")
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        instance.full_clean()
        instance.save()

        # ----------------------*****---------------------

        # Add the many-to-many relations, raise error something went wrong
        JobApplicationService._add_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            m2m_fields=JobApplicationService.M2M_FIELDS
        )

        # ----------------------*****---------------------

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        user: User,
        context: JobApplicationContext,
        validated_data: dict
    ) -> JobApplication:

        # Check if Context follows business rules and Get the cleaned Job Application

        instance = JobApplicationService._resolve_job_application(
            user=user,
            context=context
        )

        # Many-to-many fields ownership validations
        JobApplicationService._validate_emails_ownership(
            user=user,
            emails=validated_data.get("emails", []),
            job_position=instance.job_position
        )

        JobApplicationService._validate_documents_ownership(
            user=user,
            documents=validated_data.get("documents", []),
        )

        # ----------------------*****---------------------

        # Updating Scalar fields
        JobApplicationService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=JobApplicationService.NON_M2M_FIELDS
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        instance.full_clean()
        instance.save()

        # ----------------------*****---------------------
        # Updating Many-to-many fields
        JobApplicationService._update_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=JobApplicationService.M2M_FIELDS
        )

        # ----------------------*****---------------------

        return instance

    @staticmethod
    @transaction.atomic
    def remove(*, user: User, context: JobApplicationContext) -> None:

        # Domain Correctness Validation:

        # Check if Context follows business rules and Get the Job Application

        instance = JobApplicationService._resolve_job_application(
            user=user,
            context=context
        )

        # ----------------------*****---------------------

        instance.delete()

    @staticmethod
    def _validate_emails_ownership(
        *, user: User,
        emails: Iterable[CompanyEmail],
        job_position: JobPosition
    ):

        # Check if Emails follow the business rules:

        # Each Application Email belongs to User
        if any(user != email.company.workspace.owner for email in emails):
            raise PermissionDenied(
                {"Invalid Email": "Email Does Not Belong To User"}
            )

        # Each Email belongs to the company of JobApplication's JobPosition
        if any(job_position.company != email.company for email in emails):
            raise PermissionDenied(
                {
                    "Invalid Email":
                        ["Email must belong to the job application's company"]
                }
            )

    @staticmethod
    def _validate_documents_ownership(*, user: User, documents: Iterable[Document]):

        # Check if Documents follow the business rules:

        # Each Application Document belongs to User
        if any(user != document.owner for document in documents):
            raise PermissionDenied(
                {"Invalid Document": "Document Does Not Belong To User"}
            )

    @staticmethod
    def _resolve_job_application(
        *,
        user: User,
        context: JobApplicationContext
    ) -> JobApplication:

        # Check if context follows business rules to create a Job Application Note:

        # Context should follow business rules of job position at first place
        job_position = JobApplicationService._resolve_job_position(
            user=user, context=CompanyChildContext(
                id=context.job_position_id,
                workspace_id=context.workspace_id,
                company_id=context.company_id,
            )
        )

        # Job Application should belong to the job position above
        try:
            return job_position.job_applications.get(
                pk=context.id
            )
        except JobApplication.DoesNotExist:
            raise ValidationError(
                {"Job Application": ["Object Not Found"]}
            )
