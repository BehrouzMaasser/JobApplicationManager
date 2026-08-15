import pytest

from apps.applications.selectors.application_note_selector import (
    JobApplicationNoteSelector,
)
from apps.core.common.types.filters import JobApplicationNoteQueryFilter

from apps.core.exceptions.exceptions import ResourceNotFoundError


@pytest.mark.django_db
class TestJobApplicationNoteSelectorList:

    def test_list_returns_only_accessible_notes(
        self,
        user1,
        app_note1,
        app_note2,
        app_note1_user2,
    ):

        queryset = JobApplicationNoteSelector.list(user=user1)

        assert set(queryset) == {
            app_note1,
            app_note2,
        }

    def test_list_filters_by_workspace_id(
        self,
        user1,
        app_note1,
    ):

        filters = JobApplicationNoteQueryFilter(
            workspace_id=(
                app_note1
                .job_application
                .workspace
                .workspace_id
            ),
        )

        queryset = JobApplicationNoteSelector.list(
            user=user1,
            filters=filters,
        )

        assert set(queryset) == {app_note1}

    def test_list_filters_by_company_id(
        self,
        user1,
        app_note1,
    ):

        filters = JobApplicationNoteQueryFilter(
            company_id=(
                app_note1
                .job_application
                .job_position
                .company
                .pk
            ),
        )

        queryset = JobApplicationNoteSelector.list(
            user=user1,
            filters=filters,
        )

        assert set(queryset) == {app_note1}

    def test_list_filters_by_job_position_id(
        self,
        user1,
        app_note1,
    ):

        filters = JobApplicationNoteQueryFilter(
            job_position_id=(
                app_note1
                .job_application
                .job_position
                .pk
            ),
        )

        queryset = JobApplicationNoteSelector.list(
            user=user1,
            filters=filters,
        )

        assert set(queryset) == {app_note1}

    def test_list_filters_by_job_application_id(
        self,
        user1,
        app_note1,
    ):

        filters = JobApplicationNoteQueryFilter(
            job_application_id=(
                app_note1
                .job_application
                .pk
            ),
        )

        queryset = JobApplicationNoteSelector.list(
            user=user1,
            filters=filters,
        )

        assert set(queryset) == {app_note1}

    def test_list_filters_by_note_id(
        self,
        user1,
        app_note1,
    ):

        filters = JobApplicationNoteQueryFilter(
            id=app_note1.pk,
        )

        queryset = JobApplicationNoteSelector.list(
            user=user1,
            filters=filters,
        )

        assert set(queryset) == {app_note1}

    def test_list_applies_multiple_filters(
        self,
        user1,
        app_note1,
    ):

        filters = JobApplicationNoteQueryFilter(
            workspace_id=app_note1.job_application.workspace.workspace_id,
            company_id=app_note1.job_application.job_position.company.pk,
            job_position_id=app_note1.job_application.job_position.pk,
            job_application_id=app_note1.job_application.pk,
            id=app_note1.pk,
        )

        queryset = JobApplicationNoteSelector.list(
            user=user1,
            filters=filters,
        )

        assert set(queryset) == {app_note1}

    def test_list_does_not_return_foreign_note_even_with_matching_id(
        self,
        user1,
        app_note1_user2,
    ):

        filters = JobApplicationNoteQueryFilter(
            id=app_note1_user2.pk,
        )

        queryset = JobApplicationNoteSelector.list(
            user=user1,
            filters=filters,
        )

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_user_has_no_notes(
        self,
        user2,
    ):

        queryset = JobApplicationNoteSelector.list(user=user2)

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_filters_match_nothing(
        self,
        user1,
    ):

        filters = JobApplicationNoteQueryFilter(
            id=999999,
        )

        queryset = JobApplicationNoteSelector.list(
            user=user1,
            filters=filters,
        )

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_filters_conflict(
        self,
        user1,
        app_note1,
        app_note2,
    ):

        filters = JobApplicationNoteQueryFilter(
            job_application_id=app_note1.job_application.pk,
            id=app_note2.pk,
        )

        queryset = JobApplicationNoteSelector.list(
            user=user1,
            filters=filters,
        )

        assert queryset.count() == 0


@pytest.mark.django_db
class TestJobApplicationNoteSelectorGet:

    def test_get_returns_accessible_note(
        self,
        user1,
        app_note1,
    ):

        note = JobApplicationNoteSelector.get(
            user=user1,
            obj_id=app_note1.pk,
        )

        assert note == app_note1

    def test_get_raises_when_note_does_not_exist(
        self,
        user1,
    ):

        with pytest.raises(ResourceNotFoundError):

            JobApplicationNoteSelector.get(
                user=user1,
                obj_id=999999,
            )

    def test_get_raises_when_note_is_not_accessible(
        self,
        user1,
        app_note1_user2,
    ):

        with pytest.raises(ResourceNotFoundError):

            JobApplicationNoteSelector.get(
                user=user1,
                obj_id=app_note1_user2.pk,
            )
