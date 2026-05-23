from django.core.exceptions import ValidationError
from django.db import transaction

from apps.accounts.models import User
from apps.companies.models import JobRequirement

from apps.workspaces.services.base_service import BaseService


class JobRequirementService(BaseService):

    CREATE_REQUIRED_FIELDS = {
        "title",
        "description"
    }

    UPDATABLE_FIELDS = CREATE_REQUIRED_FIELDS

    @staticmethod
    @transaction.atomic
    def create(*, user: User, validated_data: dict) -> JobRequirement:

        instance = JobRequirement(
            user=user,
            title=validated_data.get("title"),
            description=validated_data.get("description")
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        try:
            instance.full_clean()
            instance.save()
        except Exception as e:
            raise ValidationError(
                {"Job Requirement": ["Invalid Data Given", str(e)]}
            )

        # ----------------------*****---------------------

        return instance

    @staticmethod
    @transaction.atomic
    def update(
            *, user: User, job_requirement_id: int, validated_data: dict
    ) -> JobRequirement:

        # Domain Correctness Validation:

        instance = JobRequirementService._resolve_job_requirement(
            user=user, job_requirement_id=job_requirement_id
        )

        # ----------------------*****---------------------

        # Applying changes:
        JobRequirementService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=JobRequirementService.UPDATABLE_FIELDS
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        try:
            instance.full_clean()
            instance.save()
        except Exception as e:
            raise ValidationError(
                {"Job Requirement": ["Invalid Data Given", str(e)]}
            )

        # ----------------------*****---------------------

        return instance

    @staticmethod
    def remove(*, user: User, job_requirement_id: int) -> None:

        # Domain Correctness Validation:

        instance = JobRequirementService._resolve_job_requirement(
            user=user, job_requirement_id=job_requirement_id
        )

        # ----------------------*****---------------------

        instance.delete()

    @staticmethod
    def _resolve_job_requirement(
            *, user: User, job_requirement_id: int
    ) -> JobRequirement:

        try:
            return JobRequirement.objects.get(user=user, pk=job_requirement_id)
        except JobRequirement.DoesNotExist:
            raise ValidationError(
                {"job_requirement": "Job Requirement does not exist"}
            )
