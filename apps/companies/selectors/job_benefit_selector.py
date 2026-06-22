from django.db.models import QuerySet

from apps.accounts.models import User
from apps.companies.models import JobBenefit
from apps.core.exceptions.exceptions import ResourceNotFoundError, AccessDeniedError


class JobBenefitSelector:

    @staticmethod
    def get(*, user: User, job_benefit_id: int) -> JobBenefit | Exception:

        try:
            job_benefit = JobBenefit.objects.get(pk=job_benefit_id)
        except JobBenefit.DoesNotExist:
            raise ResourceNotFoundError(
                f"Job Benefit {job_benefit_id} does not exist"
            )

        if job_benefit.user != user:
            raise AccessDeniedError(
                f"Job Benefit {job_benefit_id} does not belong to {user}"
            )

        return job_benefit

    @staticmethod
    def list(user: User) -> QuerySet[JobBenefit]:

        return JobBenefit.objects.filter(user=user)
