from django.core.exceptions import ValidationError
from django.db import transaction

from apps.accounts.models import User
from apps.companies.models import JobBenefit

from apps.workspaces.services.base_service import BaseService


class JobBenefitService(BaseService):

    CREATE_REQUIRED_FIELDS = {"name"}

    UPDATABLE_FIELDS = {
        *CREATE_REQUIRED_FIELDS,
        "description",
    }

    @staticmethod
    @transaction.atomic
    def create(*, user: User, validated_data: dict) -> JobBenefit:

        instance = JobBenefit(
            user=user,
            name=validated_data.get("name"),
            description=validated_data.get("description"),
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        try:
            instance.full_clean()
            instance.save()
        except Exception as e:
            raise ValidationError({"Job Benefit": ["Invalid Data Given", str(e)]})

        # ----------------------*****---------------------

        return instance

    @staticmethod
    @transaction.atomic
    def update(
            *, user: User, job_benefit_id: int, validated_data: dict
    ) -> JobBenefit:

        # Domain Correctness Validation:

        instance = JobBenefitService._resolve_job_benefit(
            user=user,
            job_benefit_id=job_benefit_id
        )

        # ----------------------*****---------------------

        # Applying changes:
        JobBenefitService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=JobBenefitService.UPDATABLE_FIELDS
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        try:
            instance.full_clean()
            instance.save()
        except Exception as e:
            raise ValidationError({"Job Benefit": ["Invalid Data Given", str(e)]})

        # ----------------------*****---------------------

        return instance

    @staticmethod
    def remove(*, user: User, job_benefit_id: int) -> JobBenefit:

        # Domain Correctness Validation:

        instance = JobBenefitService._resolve_job_benefit(
            user=user,
            job_benefit_id=job_benefit_id
        )

        # ----------------------*****---------------------

        instance.delete()

    @staticmethod
    def _resolve_job_benefit(*, user: User, job_benefit_id: int):

        try:
            return JobBenefit.objects.get(user=user, pk=job_benefit_id)
        except JobBenefit.DoesNotExist:
            raise ValidationError("JobBenefit does not exist")
