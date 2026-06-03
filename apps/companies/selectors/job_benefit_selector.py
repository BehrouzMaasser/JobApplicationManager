from django.db.models import QuerySet

from apps.accounts.models import User
from apps.companies.models import JobBenefit


class JobBenefitSelector:

    @staticmethod
    def list(user: User) -> QuerySet[JobBenefit]:

        return JobBenefit.objects.filter(user=user)
