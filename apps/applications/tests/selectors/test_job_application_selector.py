import pytest

from django.utils import timezone

from apps.applications.selectors.application_selector import (
    JobApplicationSelector,
)

from apps.core.common.types.filters import (
    JobApplicationQueryFilter,
)

from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
)


@pytest.mark.django_db
class TestJobApplicationSelectorList:
    """
    Covers:
    - S-03 Ownership Enforcement
    - S-05 Accessible Queryset
    - S-06 Query Filtering
    - S-12 Consistent list interface
    """

    def test_list_returns_only_user_applications(
            self,
            user1,
            job_application1,
            job_app1_pos1_co1_ws1_user2,
            job_app1_pos2_co1_ws1_user1,
    ):

        queryset = JobApplicationSelector.list(
            user=user1,
        )

        assert set(queryset) == {
            job_application1,
            job_app1_pos2_co1_ws1_user1,
        }

    def test_list_filters_by_workspace_id(
            self,
            user1,
            job_application1,
    ):

        filters = JobApplicationQueryFilter(
            workspace_id=job_application1.workspace.workspace_id,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert set(queryset) == {
            job_application1,
        }

    def test_list_filters_by_company_id(
            self,
            user1,
            job_application1,
    ):

        filters = JobApplicationQueryFilter(
            company_id=job_application1.job_position.company.pk,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert set(queryset) == {
            job_application1,
        }

    def test_list_filters_by_job_position_id(
            self,
            user1,
            job_application1,
    ):

        filters = JobApplicationQueryFilter(
            job_position_id=job_application1.job_position.pk,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert set(queryset) == {
            job_application1,
        }

    def test_list_filters_by_application_id(
            self,
            user1,
            job_application1,
    ):

        filters = JobApplicationQueryFilter(
            id=job_application1.pk,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert set(queryset) == {
            job_application1,
        }

    def test_list_filters_by_status_id(
            self,
            user1,
            job_application1,
            status2,
    ):

        job_application1.status = status2
        job_application1.save()

        filters = JobApplicationQueryFilter(
            status_id=status2.pk,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert set(queryset) == {
            job_application1,
        }

    def test_list_filters_by_date_applied(
            self,
            user1,
            job_application1,
    ):

        now = timezone.now()

        job_application1.date_applied = now
        job_application1.save()

        filters = JobApplicationQueryFilter(
            date_applied=now,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert set(queryset) == {
            job_application1,
        }

    def test_list_applies_multiple_filters(
            self,
            user1,
            job_application1,
    ):

        filters = JobApplicationQueryFilter(
            workspace_id=job_application1.workspace.workspace_id,
            company_id=job_application1.job_position.company.pk,
            job_position_id=job_application1.job_position.pk,
            id=job_application1.pk,
            status_id=job_application1.status.pk,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert set(queryset) == {
            job_application1,
        }

    def test_list_does_not_return_foreign_application_with_matching_id(
            self,
            user1,
            job_app1_pos1_co1_ws1_user2,
    ):

        filters = JobApplicationQueryFilter(
            id=job_app1_pos1_co1_ws1_user2.pk,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert list(queryset) == []

    def test_list_returns_empty_queryset_when_user_has_no_applications(
            self,
            user2,
    ):

        queryset = JobApplicationSelector.list(
            user=user2,
        )

        assert list(queryset) == []

    def test_list_returns_empty_queryset_when_filter_matches_nothing(
            self,
            user1,
    ):

        filters = JobApplicationQueryFilter(
            id=999999,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert list(queryset) == []

    def test_list_returns_empty_queryset_when_filters_conflict(
            self,
            user1,
            job_application1,
            co2_ws1_user1,
    ):

        filters = JobApplicationQueryFilter(
            company_id=co2_ws1_user1.pk,
            id=job_application1.pk,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert list(queryset) == []


@pytest.mark.django_db
class TestJobApplicationSelectorGet:
    """
    Covers:
    - S-03 Ownership Enforcement
    - S-07 Exception Translation
    - S-12 Consistent get interface
    """

    def test_get_returns_application(
            self,
            user1,
            job_application1,
    ):

        application = JobApplicationSelector.get(
            user=user1,
            obj_id=job_application1.pk,
        )

        assert application == job_application1

    def test_get_foreign_application_raises_resource_not_found(
            self,
            user1,
            job_app1_pos1_co1_ws1_user2,
    ):

        with pytest.raises(ResourceNotFoundError):

            JobApplicationSelector.get(
                user=user1,
                obj_id=job_app1_pos1_co1_ws1_user2.pk,
            )

    def test_get_missing_application_raises_resource_not_found(
            self,
            user1,
    ):

        with pytest.raises(ResourceNotFoundError):

            JobApplicationSelector.get(
                user=user1,
                obj_id=999999,
            )
