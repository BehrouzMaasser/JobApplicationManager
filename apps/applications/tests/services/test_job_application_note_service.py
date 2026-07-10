import pytest

from unittest.mock import patch

from django.core.exceptions import ValidationError as DBValidationError

from apps.applications.services.application_note_service import (
    JobApplicationNoteService,
)
from apps.applications.services.contexts.application_context import (
    JobApplicationChildContext,
)


pytestmark = pytest.mark.django_db


# =========================================================
# Create
# =========================================================

class TestJobApplicationNoteServiceCreate:

    def test_successfully_returns_application_note(
        self,
        app_note1_context_with_no_id,
        app_note1_valid_data,
        user1,
    ):
        application_note = JobApplicationNoteService.create(
            user=user1,
            context=app_note1_context_with_no_id,
            validated_data=app_note1_valid_data,
        )

        assert application_note.id is not None
        assert (
            application_note.job_application.id
            == app_note1_context_with_no_id.job_application_id
        )
        assert application_note.title == app_note1_valid_data["title"]
        assert application_note.content == app_note1_valid_data["content"]

    def test_calls_resolve_job_application(
            self,
            user1,
            app_note1_context_with_no_id,
            app_note1_valid_data,
            job_application1,
    ):
        with patch(
                "apps.applications.services.application_note_service."
                "JobApplicationNoteService._resolve_job_application"
        ) as mock_resolve:
            mock_resolve.return_value = job_application1

            JobApplicationNoteService.create(
                user=user1,
                context=app_note1_context_with_no_id,
                validated_data=app_note1_valid_data,
            )

            mock_resolve.assert_called_once()

    def test_calls_full_clean(
        self,
        user1,
        app_note1_context_with_no_id,
        app_note1_valid_data,
    ):
        with patch(
            "apps.applications.models.JobApplicationNote.full_clean"
        ) as mock_full_clean:

            JobApplicationNoteService.create(
                user=user1,
                context=app_note1_context_with_no_id,
                validated_data=app_note1_valid_data,
            )

            mock_full_clean.assert_called_once()

    def test_calls_save(
        self,
        user1,
        app_note1_context_with_no_id,
        app_note1_valid_data,
    ):
        with patch(
            "apps.applications.models.JobApplicationNote.save"
        ) as mock_save:

            JobApplicationNoteService.create(
                user=user1,
                context=app_note1_context_with_no_id,
                validated_data=app_note1_valid_data,
            )

            mock_save.assert_called_once()

    def test_invalid_data_raises_validation_error(
        self,
        user1,
        app_note1_context_with_no_id,
        app_note1_valid_data,
    ):
        invalid_data = app_note1_valid_data.copy()
        invalid_data["title"] = ""

        with pytest.raises(DBValidationError):
            JobApplicationNoteService.create(
                user=user1,
                context=app_note1_context_with_no_id,
                validated_data=invalid_data,
            )


# =========================================================
# Update
# =========================================================

class TestJobApplicationNoteServiceUpdate:

    def test_successfully_updates_application_note(
        self,
        app_note1,
        app_note1_context_with_id,
        app_note1_valid_data,
    ):
        updated_note = JobApplicationNoteService.update(
            user=app_note1.job_application.owner,
            context=app_note1_context_with_id,
            validated_data=app_note1_valid_data,
        )

        assert updated_note.id == app_note1.id
        assert updated_note.title == app_note1_valid_data["title"]
        assert updated_note.content == app_note1_valid_data["content"]

    def test_calls_resolve_job_application_note(
        self,
        app_note1,
        app_note1_context_with_id,
        app_note1_valid_data,
    ):
        with patch(
            "apps.applications.services.application_note_service."
            "JobApplicationNoteService._resolve_job_application_note"
        ) as mock_resolve:

            JobApplicationNoteService.update(
                user=app_note1.job_application.owner,
                context=app_note1_context_with_id,
                validated_data=app_note1_valid_data,
            )

            mock_resolve.assert_called_once()

    def test_calls_update_non_m2m_fields(
        self,
        app_note1,
        app_note1_context_with_id,
        app_note1_valid_data,
    ):
        with patch(
            "apps.applications.services.application_note_service."
            "JobApplicationNoteService._update_non_m2m_fields"
        ) as mock_update:

            JobApplicationNoteService.update(
                user=app_note1.job_application.owner,
                context=app_note1_context_with_id,
                validated_data=app_note1_valid_data,
            )

            mock_update.assert_called_once()

    def test_calls_full_clean(
        self,
        app_note1,
        app_note1_context_with_id,
        app_note1_valid_data,
    ):
        with patch(
            "apps.applications.models.JobApplicationNote.full_clean"
        ) as mock_full_clean:

            JobApplicationNoteService.update(
                user=app_note1.job_application.owner,
                context=app_note1_context_with_id,
                validated_data=app_note1_valid_data,
            )

            mock_full_clean.assert_called_once()

    def test_calls_save(
        self,
        app_note1,
        app_note1_context_with_id,
        app_note1_valid_data,
    ):
        with patch(
            "apps.applications.models.JobApplicationNote.save"
        ) as mock_save:

            JobApplicationNoteService.update(
                user=app_note1.job_application.owner,
                context=app_note1_context_with_id,
                validated_data=app_note1_valid_data,
            )

            mock_save.assert_called_once()

    def test_invalid_data_raises_validation_error(
        self,
        app_note1,
        app_note1_context_with_id,
        app_note1_valid_data,
    ):
        invalid_data = app_note1_valid_data.copy()
        invalid_data["title"] = ""

        with pytest.raises(DBValidationError):
            JobApplicationNoteService.update(
                user=app_note1.job_application.owner,
                context=app_note1_context_with_id,
                validated_data=invalid_data,
            )


# =========================================================
# Remove
# =========================================================

class TestJobApplicationNoteServiceRemove:

    def test_calls_resolve_job_application_note(
        self,
        app_note1,
        app_note1_context_with_id,
    ):
        with patch(
            "apps.applications.services.application_note_service."
            "JobApplicationNoteService._resolve_job_application_note"
        ) as mock_resolve:

            JobApplicationNoteService.remove(
                user=app_note1.job_application.owner,
                context=app_note1_context_with_id,
            )

            mock_resolve.assert_called_once()

    def test_calls_delete(
        self,
        app_note1,
        app_note1_context_with_id,
    ):
        with patch(
            "apps.applications.models.JobApplicationNote.delete"
        ) as mock_delete:

            JobApplicationNoteService.remove(
                user=app_note1.job_application.owner,
                context=app_note1_context_with_id,
            )

            mock_delete.assert_called_once()


# =========================================================
# Resolve
# =========================================================

class TestJobApplicationNoteServiceResolve:

    def test_returns_application_note(
        self,
        app_note1,
        app_note1_context_with_id,
    ):
        result = JobApplicationNoteService._resolve_job_application_note(
            user=app_note1.job_application.owner,
            context=app_note1_context_with_id,
        )

        assert result == app_note1

    def test_rejects_wrong_user(
        self,
        app_note1_context_with_id,
        user2,
    ):
        with pytest.raises(Exception):
            JobApplicationNoteService._resolve_job_application_note(
                user=user2,
                context=app_note1_context_with_id,
            )

    def test_rejects_wrong_job_application(
        self,
        app_note1,
        job_application2,
    ):
        context = JobApplicationChildContext(
            id=app_note1.id,
            workspace_id=app_note1.job_application.workspace.workspace_id,
            company_id=app_note1.job_application.job_position.company.id,
            job_position_id=app_note1.job_application.job_position.id,
            job_application_id=job_application2.id,
        )

        with pytest.raises(Exception):
            JobApplicationNoteService._resolve_job_application_note(
                user=app_note1.job_application.owner,
                context=context,
            )
