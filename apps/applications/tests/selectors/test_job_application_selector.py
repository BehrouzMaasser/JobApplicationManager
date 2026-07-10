import pytest

from django.utils import timezone

from apps.applications.selectors.application_selector import JobApplicationSelector

from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
    InfraStructureViolationError,
)


@pytest.mark.django_db
class TestJobApplicationSelectorList:

    def test_list_returns_only_user_owned_applications(
        self,
        user1,
        job_application1,
        job_app1_pos1_co1_ws1_user2,
        job_app1_pos2_co1_ws1_user1,
    ):
        queryset = set(JobApplicationSelector.list(user=user1))

        assert queryset == {
            job_application1,
            job_app1_pos2_co1_ws1_user1,
        }

    def test_list_without_filters_returns_all_owned_applications(
        self,
        user1,
        job_application1,
        job_app1_pos2_co1_ws1_user1,
    ):
        queryset = JobApplicationSelector.list(user=user1)

        assert {
            job_application1,
            job_app1_pos2_co1_ws1_user1,
        } == set(queryset)

    def test_list_filters_by_workspace_id(
        self,
        user1,
        job_application1,
        job_app1_pos1_co1_ws2_user1,
    ):
        filters = JobApplicationSelector.QueryFilter(
            workspace_id=job_application1.workspace.workspace_id,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert {job_application1} == set(queryset)

    def test_list_filters_by_company_id(
        self,
        user1,
        job_application1,
        job_app1_pos1_co2_ws1_user1,
    ):
        filters = JobApplicationSelector.QueryFilter(
            company_id=job_application1.job_position.company.pk,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert {job_application1} == set(queryset)

    def test_list_filters_by_job_position_id(
        self,
        user1,
        job_application1,
    ):
        filters = JobApplicationSelector.QueryFilter(
            job_position_id=job_application1.job_position.pk,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert {job_application1} == set(queryset)

    def test_list_filters_by_application_id(
        self,
        user1,
        job_application1,
    ):
        filters = JobApplicationSelector.QueryFilter(
            id=job_application1.pk,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert {job_application1} == set(queryset)

    def test_list_filters_by_status_id(
        self,
        user1,
        job_application1,
        job_app1_pos2_co1_ws1_user1,
        status2,
    ):
        job_application1.status = status2
        job_application1.save()

        filters = JobApplicationSelector.QueryFilter(
            status_id=status2.pk,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert {job_application1} == set(queryset)

    def test_list_filters_by_date_applied(
        self,
        user1,
        job_application1,
    ):
        now = timezone.now()

        job_application1.date_applied = now
        job_application1.save()

        filters = JobApplicationSelector.QueryFilter(
            date_applied=now,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert {job_application1} == set(queryset)

    def test_list_applies_multiple_filters(
        self,
        user1,
        job_application1,
    ):
        filters = JobApplicationSelector.QueryFilter(
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

        assert set(queryset) == {job_application1}

    def test_list_never_returns_foreign_application_even_with_matching_id(
        self,
        user1,
        job_app1_pos1_co1_ws1_user2,
    ):
        filters = JobApplicationSelector.QueryFilter(
            id=job_app1_pos1_co1_ws1_user2.pk,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_user_has_no_applications(
        self,
        user2,
    ):
        queryset = JobApplicationSelector.list(user=user2)

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_filters_match_nothing(
        self,
        user1,
    ):
        filters = JobApplicationSelector.QueryFilter(
            id=999999,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_multiple_filters_do_not_match(
        self,
        user1,
        job_app1_pos2_co1_ws1_user1,
        co2_ws1_user1
    ):
        filters = JobApplicationSelector.QueryFilter(
            company_id=co2_ws1_user1.pk,
            id=job_app1_pos2_co1_ws1_user1.pk,
        )

        queryset = JobApplicationSelector.list(
            user=user1,
            filters=filters,
        )

        assert queryset.count() == 0


@pytest.mark.django_db
class TestJobApplicationSelectorGet:

    def test_get_returns_application_for_owner(
        self,
        user1,
        job_application1,
    ):
        application = JobApplicationSelector.get(
            user=user1,
            application_id=job_application1.pk,
        )

        assert application == job_application1

    def test_get_raises_when_application_does_not_exist(
        self,
        user1,
    ):
        with pytest.raises(ResourceNotFoundError):
            JobApplicationSelector.get(
                user=user1,
                application_id=999999,
            )

    def test_get_raises_when_application_belongs_to_another_user(
        self,
        user1,
        job_app1_pos1_co1_ws1_user2,
    ):
        with pytest.raises(AccessDeniedError):
            JobApplicationSelector.get(
                user=user1,
                application_id=job_app1_pos1_co1_ws1_user2.pk,
            )

    def test_get_raises_infrastructure_error_for_invalid_application_id(
        self,
        user1,
    ):
        with pytest.raises(InfraStructureViolationError):
            JobApplicationSelector.get(
                user=user1,
                application_id="invalid-id",
            )
