from django.db.models import QuerySet

# Models
from apps.accounts.models import User
from apps.companies.models import JobRequirement

# Exceptions
from apps.core.exceptions.exceptions import ResourceNotFoundError, AccessDeniedError


class JobRequirementSelector:

    @staticmethod
    def get(*, user: User, job_requirement_id: int) -> JobRequirement | Exception:

        try:
            job_requirement = JobRequirement.objects.get(pk=job_requirement_id)
        except JobRequirement.DoesNotExist:
            raise ResourceNotFoundError(
                f"Job Requirement {job_requirement_id} does not exist"
            )

        if job_requirement.user != user:
            raise AccessDeniedError(
                f"Job Requirement {job_requirement_id} does not belong to {user}"
            )

        return job_requirement

    @staticmethod
    def list(user: User) -> QuerySet[JobRequirement]:

        return JobRequirement.objects.filter(user=user)
