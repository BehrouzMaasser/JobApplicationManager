from django.db.models import QuerySet

from apps.companies.models import JobBenefit


class JobBenefitSelector:

    @staticmethod
    def list() -> QuerySet[JobBenefit]:

        return JobBenefit.objects.all()
