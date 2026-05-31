import pytest

from django.utils import timezone

from apps.applications.selectors.application_selector import JobApplicationSelector


@pytest.mark.django_db
class TestJobApplicationSelector:

    def test_list_returns_only_user_applications(
            self,
            user,
            job_application1,
            job_app1_pos1_co1_ws1_user2,
            job_app1_pos2_co1_ws1_user1,
    ):

        result = JobApplicationSelector.list(user=user)

        assert len(result) == 2
        assert set(result) == {job_application1, job_app1_pos2_co1_ws1_user1}

    def test_list_filters_by_workspace_id(
            self,
            user,
            job_application1,
            job_app1_pos1_co1_ws2_user1,
    ):
        
        filters = JobApplicationSelector.QueryFilter(
            workspace_id=job_application1.workspace.workspace_id
        )

        result = JobApplicationSelector.list(
            user=user,
            filters=filters,
        )

        assert list(result) == [job_application1]

    def test_list_filters_by_company_id(
            self,
            user,
            job_application1,
            job_app1_pos1_co2_ws1_user1,
    ):

        filters = JobApplicationSelector.QueryFilter(
            company_id=job_application1.job_position.company.pk
        )

        result = JobApplicationSelector.list(
            user=user,
            filters=filters,
        )

        assert list(result) == [job_application1]

    def test_list_filters_by_job_position_id(
            self,
            user,
            job_application1,
            job_app1_pos2_co1_ws1_user1,
    ):

        filters = JobApplicationSelector.QueryFilter(
            job_position_id=job_application1.job_position.pk
        )

        result = JobApplicationSelector.list(
            user=user,
            filters=filters,
        )

        assert list(result) == [job_application1]

    def test_list_filters_by_id(
            self,
            user,
            job_application1,
            job_app1_pos2_co1_ws1_user1,
    ):

        filters = JobApplicationSelector.QueryFilter(
            id=job_application1.pk
        )

        result = JobApplicationSelector.list(
            user=user,
            filters=filters,
        )

        assert list(result) == [job_application1]

    def test_list_filters_by_status_id(
            self,
            user,
            job_application1,
            job_app1_pos2_co1_ws1_user1,
            job_app1_pos1_co1_ws2_user1,
            status2
    ):

        job_application1.status = status2
        job_application1.save()
        job_application1.refresh_from_db()

        filters = JobApplicationSelector.QueryFilter(
            status_id=job_app1_pos2_co1_ws1_user1.status.pk
        )

        result = JobApplicationSelector.list(
            user=user,
            filters=filters,
        )

        assert len(result) == 2
        assert set(result) == {
            job_app1_pos1_co1_ws2_user1, job_app1_pos2_co1_ws1_user1
        }

    def test_list_filters_by_date_applied(
            self,
            user,
            job_application1,
            job_app1_pos2_co1_ws1_user1,
            job_app1_pos1_co1_ws2_user1,
    ):

        now = timezone.now()
        job_application1.date_applied = now
        job_application1.save()
        job_application1.refresh_from_db()

        filters = JobApplicationSelector.QueryFilter(
            date_applied=job_application1.date_applied
        )

        result = JobApplicationSelector.list(
            user=user,
            filters=filters,
        )

        assert list(result) == [job_application1]

    def test_list_combines_filters(
            self,
            user,
            job_application1,
            job_app1_pos2_co1_ws1_user1,
    ):

        filters = JobApplicationSelector.QueryFilter(
            workspace_id=job_application1.workspace.workspace_id,
            company_id=job_application1.job_position.company.pk,
            job_position_id=job_application1.job_position.pk,
        )

        result = JobApplicationSelector.list(
            user=user,
            filters=filters,
        )

        assert list(result) == [job_application1]
