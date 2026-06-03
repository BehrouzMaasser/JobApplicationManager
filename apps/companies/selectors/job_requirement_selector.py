from django.db.models import QuerySet

from apps.accounts.models import User
from apps.companies.models import JobRequirement


class JobRequirementSelector:

    @staticmethod
    def list(user: User) -> QuerySet[JobRequirement]:

        return JobRequirement.objects.filter(user=user)
