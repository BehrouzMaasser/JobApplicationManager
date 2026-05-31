import pytest

from apps.applications.selectors.application_note_selector import (
    JobApplicationNoteSelector
)


@pytest.mark.django_db
class TestJobApplicationNoteSelector:

    def test_list_returns_only_user_notes(
            self,
            user,
            app_note1,
            app_note2,
            app_note1_user2,
    ):

        result = JobApplicationNoteSelector.list(user=user)

        assert len(result) == 2
        assert set(result) == {app_note1, app_note2}

    def test_list_filters_by_workspace_id(
            self,
            user,
            app_note1,
            app_note2,
    ):

        filters = JobApplicationNoteSelector.QueryFilter(
            workspace_id=app_note1.job_application.workspace.workspace_id
        )

        result = JobApplicationNoteSelector.list(
            user=user,
            filters=filters,
        )

        assert set(result) == {app_note1}

    def test_list_filters_by_company_id(
            self,
            user,
            app_note1,
            app_note2,
    ):
        filters = JobApplicationNoteSelector.QueryFilter(
            company_id=app_note1.job_application.job_position.company.pk
        )

        result = JobApplicationNoteSelector.list(
            user=user,
            filters=filters,
        )

        assert list(result) == [app_note1]

    def test_list_filters_by_job_position_id(
            self,
            user,
            app_note1,
            app_note2,
    ):

        filters = JobApplicationNoteSelector.QueryFilter(
            job_position_id=app_note1.job_application.job_position.pk
        )

        result = JobApplicationNoteSelector.list(
            user=user,
            filters=filters,
        )

        assert list(result) == [app_note1]

    def test_list_filters_by_job_application_id(
            self,
            user,
            app_note1,
            app_note2,
    ):

        filters = JobApplicationNoteSelector.QueryFilter(
            job_application_id=app_note1.job_application.pk
        )

        result = JobApplicationNoteSelector.list(
            user=user,
            filters=filters,
        )

        assert list(result) == [app_note1]

    def test_list_filters_by_id(
            self,
            user,
            app_note1,
            app_note2,
    ):

        filters = JobApplicationNoteSelector.QueryFilter(
            id=app_note1.pk
        )

        result = JobApplicationNoteSelector.list(
            user=user,
            filters=filters,
        )

        assert list(result) == [app_note1]

    def test_list_combines_filters(
            self,
            user,
            app_note1,
            app_note2,
    ):

        filters = JobApplicationNoteSelector.QueryFilter(
            workspace_id=app_note1.job_application.workspace.workspace_id,
            company_id=app_note1.job_application.job_position.company.pk,
            job_position_id=app_note1.job_application.job_position.pk,
            job_application_id=app_note1.job_application.pk,
        )

        result = JobApplicationNoteSelector.list(
            user=user,
            filters=filters,
        )

        assert list(result) == [app_note1]
