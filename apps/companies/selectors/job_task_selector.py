from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.companies.models import JobTask

# Exceptions
from apps.core.exceptions.exceptions import ResourceNotFoundError, AccessDeniedError


class JobTaskSelector:

    @staticmethod
    def get(*, user: User, job_task_id: int) -> JobTask | Exception:

        try:
            job_task = JobTask.objects.get(pk=job_task_id)
        except JobTask.DoesNotExist:
            raise ResourceNotFoundError(
                f"Job Task {job_task_id} does not exist"
            )

        if job_task.user != user:
            raise AccessDeniedError(
                f"Job Task {job_task_id} does not belong to {user}"
            )

        return job_task

    @staticmethod
    def list(user: User) -> QuerySet[JobTask]:

        return JobTask.objects.filter(user=user)
