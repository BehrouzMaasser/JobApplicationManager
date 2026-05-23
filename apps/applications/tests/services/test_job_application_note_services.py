import copy

import pytest

from unittest.mock import patch

from django.core.exceptions import ValidationError

from apps.applications.services.application_note_services import (
    JobApplicationNoteService
)
from apps.applications.services.contexts.application_context import \
    JobApplicationChildContext


#   ----------------------------------- ****** -----------------------------------


# Creation:

@pytest.mark.django_db
def test_create_application_note_successfully_returns_application_note(
        app_note1_context_with_no_id, app_note1_valid_data, user
):

    application_note = JobApplicationNoteService.create(
        user=user,
        context=app_note1_context_with_no_id,
        validated_data=app_note1_valid_data,
    )

    assert application_note.id is not None

    assert (application_note.job_application.id ==
            app_note1_context_with_no_id.job_application_id)

    assert (application_note.job_application.job_position.id ==
            app_note1_context_with_no_id.job_position_id)

    assert (application_note.job_application.workspace.workspace_id ==
            app_note1_context_with_no_id.workspace_id)

    assert (application_note.job_application.job_position.company.id ==
            app_note1_context_with_no_id.company_id)

    assert application_note.job_application.workspace.owner == user

    assert application_note.title == app_note1_valid_data["title"]
    assert application_note.content == app_note1_valid_data["content"]


@pytest.mark.django_db
def test_create_application_note_calls_resolve_job_application(
        user, app_note1_valid_data, app_note1_context_with_no_id
):

    with patch(
            'apps.applications.services.application_note_services.'
            'JobApplicationService._resolve_job_application',
    ) as mock_resolve_job_application:

        with pytest.raises(ValueError):
            JobApplicationNoteService.create(
                user=user,
                context=app_note1_context_with_no_id,
                validated_data=app_note1_valid_data,
            )

        mock_resolve_job_application.assert_called_once()


@pytest.mark.django_db
def test_create_application_note_calls_full_clean(
        user, app_note1_valid_data, app_note1_context_with_no_id
):

    # Empty title raise validation error
    invalid_data = copy.deepcopy(app_note1_valid_data)
    invalid_data["title"] = ""

    with pytest.raises(ValidationError):
        JobApplicationNoteService.create(
            user=user,
            context=app_note1_context_with_no_id,
            validated_data=invalid_data,
        )

    with patch(
            'apps.applications.models.JobApplicationNote.full_clean'
    ) as mock_full_clean:

        JobApplicationNoteService.create(
            user=user,
            context=app_note1_context_with_no_id,
            validated_data=app_note1_valid_data,
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_create_application_note_calls_save(
        user, app_note1_valid_data, app_note1_context_with_no_id
):

    with patch(
            'apps.applications.models.JobApplicationNote.save'
    ) as mock_save:

        JobApplicationNoteService.create(
            user=user,
            context=app_note1_context_with_no_id,
            validated_data=app_note1_valid_data,
        )

        mock_save.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Updating

@pytest.mark.django_db
def test_update_application_note_calls_full_clean(
        app_note1_context_with_id, app_note1, app_note1_valid_data
):

    # Empty title raise validation error
    invalid_data = copy.deepcopy(app_note1_valid_data)
    invalid_data["title"] = ""

    with pytest.raises(ValidationError):
        JobApplicationNoteService.update(
            user=app_note1.job_application.owner,
            context=app_note1_context_with_id,
            validated_data=invalid_data,
        )

    with patch(
            'apps.applications.models.JobApplicationNote.full_clean'
    ) as mock_full_clean:

        JobApplicationNoteService.update(
            user=app_note1.job_application.owner,
            context=app_note1_context_with_id,
            validated_data=app_note1_valid_data,
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_update_application_note_calls_save(
        app_note1_context_with_id, app_note1, app_note1_valid_data
):

    with patch(
            'apps.applications.models.JobApplicationNote.save'
    ) as mock_save:

        JobApplicationNoteService.update(
            user=app_note1.job_application.owner,
            context=app_note1_context_with_id,
            validated_data=app_note1_valid_data,
        )

        mock_save.assert_called_once()


@pytest.mark.django_db
def test_update_application_note_calls_resolve_application_note(
        app_note1_context_with_id, app_note1, app_note1_valid_data
):

    with patch(
            "apps.applications.services.application_note_services."
            "JobApplicationNoteService._resolve_job_application_note"
    ) as mock_resolve_application_note:

        JobApplicationNoteService.update(
            user=app_note1.job_application.owner,
            context=app_note1_context_with_id,
            validated_data=app_note1_valid_data,
        )

        mock_resolve_application_note.assert_called_once()


@pytest.mark.django_db
def test_update_application_note_calls_update_non_m2m_fields(
        app_note1_context_with_id, app_note1, app_note1_valid_data
):

    with patch(
            "apps.applications.services.application_note_services."
            "JobApplicationNoteService._update_non_m2m_fields"
    ) as mock_update_non_m2m_fields:

        JobApplicationNoteService.update(
            user=app_note1.job_application.owner,
            context=app_note1_context_with_id,
            validated_data=app_note1_valid_data,
        )

        mock_update_non_m2m_fields.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test Deleting

@pytest.mark.django_db
def test_remove_application_note_calls_resolve_application_note(
        app_note1_context_with_id, app_note1
):

    with patch(
            "apps.applications.services.application_note_services."
            "JobApplicationNoteService._resolve_job_application_note"
    ) as mock_resolve_application_note:

        JobApplicationNoteService.remove(
            user=app_note1.job_application.owner,
            context=app_note1_context_with_id,
        )

        mock_resolve_application_note.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test Retrieving

@pytest.mark.django_db
def test_retrieve_application_note_calls_resolve_job_application(
        app_note1_context_with_id, app_note1
):

    with patch(
            "apps.applications.services.application_note_services."
            "JobApplicationNoteService._resolve_job_application"
    ) as mock_resolve_job_application:

        JobApplicationNoteService._resolve_job_application_note(
            user=app_note1.job_application.owner,
            context=app_note1_context_with_id,
        )

        mock_resolve_job_application.assert_called_once()


@pytest.mark.django_db
def test_access_to_someone_else_application_note_raises_error(
        app_note1_context_with_id, other_user
):

    # Job Position don't belong to user
    with pytest.raises(ValidationError):
        JobApplicationNoteService._resolve_job_application_note(
            user=other_user,
            context=app_note1_context_with_id,
        )


@pytest.mark.django_db
def test_access_application_note_of_another_job_application_raises_error(
        job_application2, app_note1
):

    with pytest.raises(ValidationError):
        JobApplicationNoteService._resolve_job_application_note(
            user=app_note1.job_application.owner,
            context=JobApplicationChildContext(
                id=app_note1.id,
                workspace_id=app_note1.job_application.workspace.id,
                company_id=app_note1.job_application.job_position.company.id,
                job_position_id=app_note1.job_application.job_position.id,
                job_application_id=job_application2.id,
            ),
        )

#   ----------------------------------- ****** -----------------------------------
