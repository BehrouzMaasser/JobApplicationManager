import pytest

from apps.companies.selectors.job_benefit_selector import JobBenefitSelector


@pytest.mark.django_db
class TestJobBenefitSelector:

    def test_list_returns_only_user_owned_job_benefit(
        self,
        user,
        job_benefit_user1,
        job_benefit_user2,
    ):

        queryset = JobBenefitSelector.list(user=user)

        assert queryset.count() == 1
