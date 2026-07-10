import pytest

from apps.applications.selectors.application_note_selector import (
    JobApplicationNoteSelector,
)

from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    AccessDeniedError,
    InfraStructureViolationError,
)


@pytest.mark.django_db
class TestJobApplicationNoteSelectorList:

    def test_list_returns_only_user_owned_notes(
        self,
        user1,
        app_note1,
        app_note2,
        app_note1_user2,
    ):
        queryset = set(JobApplicationNoteSelector.list(user=user1))

        assert queryset == {
            app_note1,
            app_note2,
        }

    def test_list_without_filters_returns_all_owned_notes(
        self,
        user1,
        app_note1,
        app_note2,
    ):
        queryset = JobApplicationNoteSelector.list(user=user1)

        assert {
            app_note1,
            app_note2,
        } == set(queryset)

    def test_list_filters_by_workspace_id(
        self,
        user1,
        app_note1,
        app_note2,
    ):
        filters = JobApplicationNoteSelector.QueryFilter(
            workspace_id=app_note1.job_application.workspace.workspace_id,
        )

        queryset = JobApplicationNoteSelector.list(
            user=user1,
            filters=filters,
        )

        assert {app_note1} == set(queryset)

    def test_list_filters_by_company_id(
        self,
        user1,
        app_note1,
    ):
        filters = JobApplicationNoteSelector.QueryFilter(
            company_id=app_note1.job_application.job_position.company.pk,
        )

        queryset = JobApplicationNoteSelector.list(
            user=user1,
            filters=filters,
        )

        assert {app_note1} == set(queryset)

    def test_list_filters_by_job_position_id(
        self,
        user1,
        app_note1,
    ):
        filters = JobApplicationNoteSelector.QueryFilter(
            job_position_id=app_note1.job_application.job_position.pk,
        )

        queryset = JobApplicationNoteSelector.list(
            user=user1,
            filters=filters,
        )

        assert {app_note1} == set(queryset)

    def test_list_filters_by_job_application_id(
        self,
        user1,
        app_note1,
    ):
        filters = JobApplicationNoteSelector.QueryFilter(
            job_application_id=app_note1.job_application.pk,
        )

        queryset = JobApplicationNoteSelector.list(
            user=user1,
            filters=filters,
        )

        assert {app_note1} == set(queryset)

    def test_list_filters_by_note_id(
        self,
        user1,
        app_note1,
    ):
        filters = JobApplicationNoteSelector.QueryFilter(
            id=app_note1.pk,
        )

        queryset = JobApplicationNoteSelector.list(
            user=user1,
            filters=filters,
        )

        assert {app_note1} == set(queryset)

    def test_list_applies_multiple_filters(
        self,
        user1,
        app_note1,
    ):
        filters = JobApplicationNoteSelector.QueryFilter(
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

    def test_list_never_returns_foreign_note_even_with_matching_id(
        self,
        user1,
        app_note1_user2,
    ):
        filters = JobApplicationNoteSelector.QueryFilter(
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
        filters = JobApplicationNoteSelector.QueryFilter(
            id=999999,
        )

        queryset = JobApplicationNoteSelector.list(
            user=user1,
            filters=filters,
        )

        assert queryset.count() == 0

    def test_list_returns_empty_queryset_when_multiple_filters_do_not_match(
        self,
        user1,
        app_note1,
        app_note2,
    ):
        filters = JobApplicationNoteSelector.QueryFilter(
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

    def test_get_returns_note_for_owner(
        self,
        user1,
        app_note1,
    ):
        note = JobApplicationNoteSelector.get(
            user=user1,
            application_note_id=app_note1.pk,
        )

        assert note == app_note1

    def test_get_raises_when_note_does_not_exist(
        self,
        user1,
    ):
        with pytest.raises(ResourceNotFoundError):
            JobApplicationNoteSelector.get(
                user=user1,
                application_note_id=999999,
            )

    def test_get_raises_when_note_belongs_to_another_user(
        self,
        user1,
        app_note1_user2,
    ):
        with pytest.raises(AccessDeniedError):
            JobApplicationNoteSelector.get(
                user=user1,
                application_note_id=app_note1_user2.pk,
            )

    def test_get_raises_infrastructure_error_for_invalid_note_id(
        self,
        user1,
    ):
        with pytest.raises(InfraStructureViolationError):
            JobApplicationNoteSelector.get(
                user=user1,
                application_note_id="invalid-id",
            )
            