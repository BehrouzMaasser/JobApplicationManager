from django.db.models import QuerySet

from apps.companies.models import JobRequirement


class JobRequirementSelector:

    @staticmethod
    def list() -> QuerySet[JobRequirement]:

        return JobRequirement.objects.all()
