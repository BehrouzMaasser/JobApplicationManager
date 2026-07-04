import pytest

from apps.companies.selectors.job_benefit_selector import JobBenefitSelector

from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
)


@pytest.mark.django_db
class TestJobBenefitSelectorList:

    def test_list_returns_only_user_owned_job_benefits(
        self,
        user1,
        job_benefit1_user1,
        job_benefit1_user2,
    ):

        queryset = JobBenefitSelector.list(user=user1)

        assert set(queryset) == {job_benefit1_user1}

    def test_list_returns_all_user_owned_job_benefits(
        self,
        user1,
        job_benefit1_user1,
        job_benefit2_user1,
    ):

        queryset = JobBenefitSelector.list(user=user1)

        assert set(queryset) == {
            job_benefit1_user1,
            job_benefit2_user1,
        }

    def test_list_returns_empty_queryset_when_user_has_no_job_benefits(
        self,
        user1,
    ):

        queryset = JobBenefitSelector.list(user=user1)

        assert queryset.count() == 0


@pytest.mark.django_db
class TestJobBenefitSelectorGet:

    def test_get_returns_job_benefit_for_owner(
        self,
        user1,
        job_benefit1_user1,
    ):

        job_benefit = JobBenefitSelector.get(
            user=user1,
            job_benefit_id=job_benefit1_user1.pk,
        )

        assert job_benefit == job_benefit1_user1

    def test_get_raises_when_job_benefit_does_not_exist(
        self,
        user1,
    ):

        with pytest.raises(ResourceNotFoundError):
            JobBenefitSelector.get(
                user=user1,
                job_benefit_id=999999,
            )

    def test_get_raises_when_job_benefit_belongs_to_another_user(
        self,
        user1,
        job_benefit1_user2,
    ):

        with pytest.raises(AccessDeniedError):
            JobBenefitSelector.get(
                user=user1,
                job_benefit_id=job_benefit1_user2.pk,
            )
