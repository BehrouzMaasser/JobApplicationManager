from django.db import transaction

# Models
from apps.accounts.models import User
from apps.companies.models import JobPosition

# Selectors
from apps.companies.selectors.job_position_selector import JobPositionSelector

# Services
from apps.companies.services.company_service import CompanyService

# Contexts
from apps.companies.services.contexts.company_context import (
    CompanyChildContext
)

# Exceptions
from apps.core.exceptions.exceptions import (
    BusinessRuleViolationError,
    DomainInvariantViolationError
)


class JobPositionService(CompanyService):

    REQUIRED_M2M_FIELDS = {
        "employment_types",
        "job_sites",
        "tasks",
        "requirements",
    }

    M2M_FIELDS = {
        *REQUIRED_M2M_FIELDS,
        "benefits"
    }

    REQUIRED_NON_M2M_FIELDS = {
        "title",
        "description",
    }

    NON_M2M_FIELDS = {
        *REQUIRED_NON_M2M_FIELDS,
        "date_posted",
        "min_salary",
        "max_salary",
        "job_position_ad_url",
        "job_location_url",
        "job_portal_url",
        "portal_username",
        "portal_password",
    }

    CREATE_REQUIRED_FIELDS = {
        *REQUIRED_M2M_FIELDS,
        *REQUIRED_NON_M2M_FIELDS
    }

    UPDATABLE_NON_M2M_FIELDS = NON_M2M_FIELDS

    UPDATABLE_M2M_FIELDS = M2M_FIELDS

    M2M_FIELD_OWNERSHIP_MAP = {
        "tasks": "user",
        "requirements": "user",
        "benefits": "user",
    }

    @staticmethod
    @transaction.atomic
    def create(
        *,
        user: User,
        context: CompanyChildContext,
        validated_data: dict
    ) -> JobPosition:

        # Check if Context follows business rules and resolve Company
        company = JobPositionService._resolve_company(
            user=user,
            workspace_id=context.workspace_id,
            company_id=context.company_id
        )

        # ----------------------*****---------------------

        # Check validity of many-to-many fields before creating DB object
        JobPositionService._m2m_ownership_validation(
            user=user,
            validated_data=validated_data,
            ownership_map=JobPositionService.M2M_FIELD_OWNERSHIP_MAP
        )

        # ----------------------*****---------------------

        # Setting up the instance
        instance = JobPosition(
            company=company,
            title=validated_data.get("title"),
            date_posted=validated_data.get("date_posted"),
            description=validated_data.get("description"),
            min_salary=validated_data.get("min_salary"),
            max_salary=validated_data.get("max_salary"),
            job_position_ad_url=validated_data.get("job_position_ad_url"),
            job_location_url=validated_data.get("job_location_url"),
            job_portal_url=validated_data.get("job_portal_url"),
            portal_username=validated_data.get("portal_username"),
            portal_password=validated_data.get("portal_password"),
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        instance.full_clean()
        instance.save()

        # ----------------------*****---------------------

        # Add the many-to-many relations
        JobPositionService._add_m2m_fields(
            instance=instance,
            m2m_fields=JobPositionService.M2M_FIELDS,
            validated_data=validated_data
        )

        # ----------------------*****---------------------

        # Post many-to-many validation
        JobPositionService._m2m_non_empty_validation(
            instance=instance, required_fields=JobPositionService.REQUIRED_M2M_FIELDS
        )

        # ----------------------*****---------------------
        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        user: User,
        context: CompanyChildContext,
        validated_data: dict
    ) -> JobPosition:

        # Check if Context follows business rules and resolve job position
        instance = JobPositionService._resolve_job_position(
            user=user,
            context=context
        )

        # ----------------------*****---------------------

        # Check if date posted is not after any of job position's job application's
        #   date_applied
        JobPositionService._validate_date_posted(instance, validated_data)

        # ----------------------*****---------------------

        # Check validity of many-to-many fields
        JobPositionService._m2m_ownership_validation(
            user=user,
            validated_data=validated_data,
            ownership_map=JobPositionService.M2M_FIELD_OWNERSHIP_MAP
        )

        # ----------------------*****---------------------

        # Updating Scalar fields
        JobPositionService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=JobPositionService.NON_M2M_FIELDS
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        instance.full_clean()
        instance.save()

        # ----------------------*****---------------------

        # Updating Many-to-many fields
        JobPositionService._update_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=JobPositionService.M2M_FIELDS
        )

        # Post many-to-many validation
        JobPositionService._m2m_non_empty_validation(
            instance=instance, required_fields=JobPositionService.REQUIRED_M2M_FIELDS
        )

        # ----------------------*****---------------------

        return instance

    @staticmethod
    def remove(*, user: User, context: CompanyChildContext) -> None:

        # Domain Correctness Validation:

        # Check if Context follows business rules and resolve job position
        instance = JobPositionService._resolve_job_position(
            user=user,
            context=context
        )

        # ----------------------*****---------------------

        instance.delete()

    @staticmethod
    def _resolve_job_position(
            *,
            user: User,
            context: CompanyChildContext
    ) -> JobPosition:

        job_position = JobPositionSelector.get(user=user, job_position_id=context.id)

        if job_position.company.pk != context.company_id:
            raise DomainInvariantViolationError(
                f"Job position {context.id} don't belong to Company"
                f" {context.company_id}"
            )

        if job_position.company.workspace.workspace_id != context.workspace_id:
            raise DomainInvariantViolationError(
                f"Workspace of Job position {context.id} don't match the given"
                f" workspace_id = {context.workspace_id}"
            )

        return job_position

    @staticmethod
    def _validate_date_posted(instance: JobPosition, validated_data: dict) -> None:

        if date_posted := validated_data.get("date_posted"):
            for job_application in instance.job_applications.all():
                if (job_application.date_applied and
                        (job_application.date_applied < date_posted)):
                    raise BusinessRuleViolationError(
                        fields=["date_posted"],
                        messages=[
                            "Date posted cannot be after the job application's "
                            "date applied"
                        ]
                    )
