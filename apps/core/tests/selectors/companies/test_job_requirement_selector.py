import pytest

from apps.companies.selectors.job_requirement_selector import (
    JobRequirementSelector,
)
from apps.core.exceptions.exceptions import ResourceNotFoundError


@pytest.mark.django_db
class TestJobRequirementSelectorList:

    def test_list_returns_only_user_job_requirements(
            self,
            user1,
            job_requirement1_user1,
            job_requirement1_user2,
    ):

        queryset = JobRequirementSelector.list(
            user=user1,
        )

        assert set(queryset) == {
            job_requirement1_user1,
        }

    def test_list_returns_all_user_job_requirements(
            self,
            user1,
            job_requirement1_user1,
            job_requirement2_user1,
    ):

        queryset = JobRequirementSelector.list(
            user=user1,
        )

        assert set(queryset) == {
            job_requirement1_user1,
            job_requirement2_user1,
        }

    def test_list_returns_empty_queryset_when_user_has_no_job_requirements(
            self,
            user1,
    ):

        queryset = JobRequirementSelector.list(
            user=user1,
        )

        assert list(queryset) == []


@pytest.mark.django_db
class TestJobRequirementSelectorGet:

    def test_get_returns_job_requirement(
            self,
            user1,
            job_requirement1_user1,
    ):

        job_requirement = JobRequirementSelector.get(
            user=user1,
            obj_id=job_requirement1_user1.pk,
        )

        assert job_requirement == job_requirement1_user1

    def test_get_foreign_job_requirement_raises_resource_not_found(
            self,
            user1,
            job_requirement1_user2,
    ):

        with pytest.raises(ResourceNotFoundError):

            JobRequirementSelector.get(
                user=user1,
                obj_id=job_requirement1_user2.pk,
            )

    def test_get_unknown_job_requirement_raises_resource_not_found(
            self,
            user1,
    ):

        with pytest.raises(ResourceNotFoundError):

            JobRequirementSelector.get(
                user=user1,
                obj_id=999999,
            )
