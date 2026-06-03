from django.db.models import QuerySet

from apps.accounts.models import User
from apps.companies.models import JobTask


class JobTaskSelector:

    @staticmethod
    def list(user: User) -> QuerySet[JobTask]:

        return JobTask.objects.filter(user=user)
