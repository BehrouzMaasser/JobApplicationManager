import pytest

from apps.companies.selectors.job_benefit_selector import (
    JobBenefitSelector,
)
from apps.core.exceptions.exceptions import ResourceNotFoundError


@pytest.mark.django_db
class TestJobBenefitSelectorList:

    def test_list_returns_only_user_job_benefits(
            self,
            user1,
            job_benefit1_user1,
            job_benefit1_user2,
    ):

        queryset = JobBenefitSelector.list(
            user=user1,
        )

        assert set(queryset) == {
            job_benefit1_user1,
        }

    def test_list_returns_all_user_job_benefits(
            self,
            user1,
            job_benefit1_user1,
            job_benefit2_user1,
    ):

        queryset = JobBenefitSelector.list(
            user=user1,
        )

        assert set(queryset) == {
            job_benefit1_user1,
            job_benefit2_user1,
        }

    def test_list_returns_empty_queryset_when_user_has_no_job_benefits(
            self,
            user1,
    ):

        queryset = JobBenefitSelector.list(
            user=user1,
        )

        assert list(queryset) == []


@pytest.mark.django_db
class TestJobBenefitSelectorGet:

    def test_get_returns_job_benefit(
            self,
            user1,
            job_benefit1_user1,
    ):

        job_benefit = JobBenefitSelector.get(
            user=user1,
            obj_id=job_benefit1_user1.pk,
        )

        assert job_benefit == job_benefit1_user1

    def test_get_foreign_job_benefit_raises_resource_not_found(
            self,
            user1,
            job_benefit1_user2,
    ):

        with pytest.raises(ResourceNotFoundError):

            JobBenefitSelector.get(
                user=user1,
                obj_id=job_benefit1_user2.pk,
            )

    def test_get_unknown_job_benefit_raises_resource_not_found(
            self,
            user1,
    ):

        with pytest.raises(ResourceNotFoundError):

            JobBenefitSelector.get(
                user=user1,
                obj_id=999999,
            )
