from django.db import transaction

# Models
from apps.accounts.models import User
from apps.companies.models import JobTask

# Selectors
from apps.companies.selectors.job_task_selector import JobTaskSelector

# Services
from apps.workspaces.services.base_service import BaseService


class JobTaskService(BaseService):

    CREATE_REQUIRED_FIELDS = {"title", "description"}

    UPDATABLE_FIELDS = CREATE_REQUIRED_FIELDS

    @staticmethod
    @transaction.atomic
    def create(*, user: User, validated_data: dict) -> JobTask:

        instance = JobTask(
            user=user,
            title=validated_data.get("title"),
            description=validated_data.get("description")
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        instance.full_clean()
        instance.save()

        # ----------------------*****---------------------

        return instance

    @staticmethod
    @transaction.atomic
    def update(*, user: User, job_task_id: int, validated_data: dict) -> JobTask:

        # Domain Correctness Validation:

        instance = JobTaskService._resolve_job_task(
            user=user, job_task_id=job_task_id
        )

        # ----------------------*****---------------------

        # Applying changes:
        JobTaskService._update_non_m2m_fields(
            instance=instance,
            validated_data=validated_data,
            fields_to_update=JobTaskService.UPDATABLE_FIELDS
        )

        # ----------------------*****---------------------

        # Cleaning and saving the instance

        instance.full_clean()
        instance.save()

        # ----------------------*****---------------------

        return instance

    @staticmethod
    def remove(*, user: User, job_task_id: int) -> None:

        # Domain Correctness Validation:

        instance = JobTaskService._resolve_job_task(
            user=user, job_task_id=job_task_id
        )

        # ----------------------*****---------------------

        instance.delete()

    @staticmethod
    def _resolve_job_task(*, user: User, job_task_id: int) -> JobTask:

        return JobTaskSelector.get(user=user, job_task_id=job_task_id)
