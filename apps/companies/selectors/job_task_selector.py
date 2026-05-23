from django.db.models import QuerySet

from apps.companies.models import JobTask


class JobTaskSelector:

    @staticmethod
    def list() -> QuerySet[JobTask]:

        return JobTask.objects.all()
