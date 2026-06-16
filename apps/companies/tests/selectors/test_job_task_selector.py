import pytest

from apps.companies.selectors.job_task_selector import JobTaskSelector


@pytest.mark.django_db
class TestJobTaskSelector:

    def test_list_returns_only_user_owned_job_tasks(
        self,
        user,
        job_task_user1,
        job_task_user2
    ):

        queryset = JobTaskSelector.list(user=user)

        assert queryset.count() == 1
        assert queryset.first() == job_task_user1
        assert queryset.first().user == user

    def test_list_returns_all_owned_job_tasks(
        self,
        user,
        job_task_user1,
        job_task2_user1
    ):

        queryset = JobTaskSelector.list(user=user)

        assert queryset.count() == 2
        assert job_task_user1 in queryset
        assert job_task2_user1 in queryset
        assert queryset.first().user == user
        assert queryset.last().user == user
