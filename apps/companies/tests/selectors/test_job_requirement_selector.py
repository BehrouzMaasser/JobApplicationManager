import pytest

from apps.companies.selectors.job_requirement_selector import JobRequirementSelector

from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
)


@pytest.mark.django_db
class TestJobRequirementSelectorList:

    def test_list_returns_only_user_owned_job_requirements(
        self,
        user1,
        job_requirement1_user1,
        job_requirement1_user2,
    ):

        queryset = JobRequirementSelector.list(user=user1)

        assert set(queryset) == {job_requirement1_user1}

    def test_list_returns_all_user_owned_job_requirements(
        self,
        user1,
        job_requirement1_user1,
        job_requirement2_user1,
    ):

        queryset = JobRequirementSelector.list(user=user1)

        assert set(queryset) == {
            job_requirement1_user1,
            job_requirement2_user1,
        }

    def test_list_returns_empty_queryset_when_user_has_no_job_requirements(
        self,
        user1,
    ):

        queryset = JobRequirementSelector.list(user=user1)

        assert queryset.count() == 0


@pytest.mark.django_db
class TestJobRequirementSelectorGet:

    def test_get_returns_job_requirement_for_owner(
        self,
        user1,
        job_requirement1_user1,
    ):

        job_requirement = JobRequirementSelector.get(
            user=user1,
            job_requirement_id=job_requirement1_user1.pk,
        )

        assert job_requirement == job_requirement1_user1

    def test_get_raises_when_job_requirement_does_not_exist(
        self,
        user1,
    ):

        with pytest.raises(ResourceNotFoundError):
            JobRequirementSelector.get(
                user=user1,
                job_requirement_id=999999,
            )

    def test_get_raises_when_job_requirement_belongs_to_another_user(
        self,
        user1,
        job_requirement1_user2,
    ):

        with pytest.raises(AccessDeniedError):
            JobRequirementSelector.get(
                user=user1,
                job_requirement_id=job_requirement1_user2.pk,
            )
