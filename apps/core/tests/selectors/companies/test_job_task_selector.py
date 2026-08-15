import pytest

from apps.companies.selectors.job_task_selector import (
    JobTaskSelector,
)
from apps.core.exceptions.exceptions import ResourceNotFoundError


@pytest.mark.django_db
class TestJobTaskSelectorList:

    def test_list_returns_only_user_job_tasks(
            self,
            user1,
            job_task1_user1,
            job_task1_user2,
    ):

        queryset = JobTaskSelector.list(
            user=user1,
        )

        assert set(queryset) == {
            job_task1_user1,
        }

    def test_list_returns_all_user_job_tasks(
            self,
            user1,
            job_task1_user1,
            job_task2_user1,
    ):

        queryset = JobTaskSelector.list(
            user=user1,
        )

        assert set(queryset) == {
            job_task1_user1,
            job_task2_user1,
        }

    def test_list_returns_empty_queryset_when_user_has_no_job_tasks(
            self,
            user1,
    ):

        queryset = JobTaskSelector.list(
            user=user1,
        )

        assert list(queryset) == []


@pytest.mark.django_db
class TestJobTaskSelectorGet:

    def test_get_returns_job_task(
            self,
            user1,
            job_task1_user1,
    ):

        job_task = JobTaskSelector.get(
            user=user1,
            obj_id=job_task1_user1.pk,
        )

        assert job_task == job_task1_user1

    def test_get_foreign_job_task_raises_resource_not_found(
            self,
            user1,
            job_task1_user2,
    ):

        with pytest.raises(ResourceNotFoundError):

            JobTaskSelector.get(
                user=user1,
                obj_id=job_task1_user2.pk,
            )

    def test_get_unknown_job_task_raises_resource_not_found(
            self,
            user1,
    ):

        with pytest.raises(ResourceNotFoundError):

            JobTaskSelector.get(
                user=user1,
                obj_id=999999,
            )
