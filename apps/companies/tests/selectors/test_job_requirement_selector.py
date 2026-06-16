import pytest

from apps.companies.selectors.job_requirement_selector import JobRequirementSelector


@pytest.mark.django_db
class TestJobRequirementSelector:

    def test_list_returns_only_user_owned_job_requirements(
        self,
        user,
        job_requirement_user1,
        job_requirement_user2,
    ):

        queryset = JobRequirementSelector.list(user=user)

        assert queryset.count() == 1
        assert queryset.first() == job_requirement_user1
        assert queryset.first().user == user

    def test_list_returns_all_owned_job_requirements(
        self,
        user,
        job_requirement_user1,
        job_requirement2_user1
    ):

        queryset = JobRequirementSelector.list(user=user)

        assert queryset.count() == 2
        assert job_requirement_user1 in queryset
        assert job_requirement2_user1 in queryset
        assert queryset.first().user == user
        assert queryset.last().user == user
