from unittest.mock import patch

import pytest
from django.core.exceptions import ValidationError

from apps.applications.models import JobApplicationNote
from apps.applications.services.application_note_service import (
    JobApplicationNoteService,
)
from apps.applications.services.application_service import (
    JobApplicationService,
)
from apps.core.common.contexts.contexts import (
    JobApplicationChildContext,
)
from apps.core.exceptions.exceptions import (
    DomainInvariantViolationError,
)


pytestmark = pytest.mark.django_db


# ============================================================================
# Hooks
# ============================================================================

class TestResolveCreateDependencies:

    def test_resolves_job_application_dependency(
        self,
        user1,
        app_note1_context_with_no_id,
        job_application1,
    ):

        dependencies = (
            JobApplicationNoteService
            ._resolve_create_dependencies(
                user=user1,
                context=app_note1_context_with_no_id,
            )
        )

        assert dependencies["job_application"] == job_application1

    def test_resolves_job_application_through_service(
        self,
        user1,
        app_note1_context_with_no_id,
        job_application1,
    ):

        with patch.object(
            JobApplicationService,
            "_resolve_instance",
            return_value=job_application1,
        ) as mock_resolve:

            JobApplicationNoteService._resolve_create_dependencies(
                user=user1,
                context=app_note1_context_with_no_id,
            )

            mock_resolve.assert_called_once()


# ============================================================================
# Public API
# ============================================================================

class TestJobApplicationNoteCreate:

    def test_create_returns_note(
        self,
        user1,
        app_note1_context_with_no_id,
        app_note1_valid_data,
    ):

        note = JobApplicationNoteService.create(
            user=user1,
            context=app_note1_context_with_no_id,
            validated_data=app_note1_valid_data,
        )

        assert note.id is not None
        assert note.job_application_id == (
            app_note1_context_with_no_id.job_application_id
        )

        assert note.title == app_note1_valid_data["title"]
        assert note.content == app_note1_valid_data["content"]

    def test_create_invalid_data_raises_validation_error(
        self,
        user1,
        app_note1_context_with_no_id,
        app_note1_valid_data,
    ):

        data = app_note1_valid_data.copy()
        data["title"] = ""

        with pytest.raises(ValidationError):

            JobApplicationNoteService.create(
                user=user1,
                context=app_note1_context_with_no_id,
                validated_data=data,
            )


class TestJobApplicationNoteUpdate:

    def test_update_changes_fields(
        self,
        app_note1,
        app_note1_context_with_id,
        app_note1_valid_data_updated,
    ):

        updated = JobApplicationNoteService.update(
            user=app_note1.job_application.owner,
            context=app_note1_context_with_id,
            validated_data=app_note1_valid_data_updated,
        )

        assert updated.id == app_note1.id
        assert updated.title == (
            app_note1_valid_data_updated["title"]
        )
        assert updated.content == (
            app_note1_valid_data_updated["content"]
        )

    def test_partial_update_keeps_existing_fields(
        self,
        app_note1,
        app_note1_context_with_id,
        app_note1_valid_data_updated,
    ):

        data = app_note1_valid_data_updated.copy()
        data.pop("content")

        updated = JobApplicationNoteService.update(
            user=app_note1.job_application.owner,
            context=app_note1_context_with_id,
            validated_data=data,
        )

        assert updated.title == data["title"]
        assert updated.content == app_note1.content

    def test_update_invalid_data_raises_validation_error(
        self,
        app_note1,
        app_note1_context_with_id,
        app_note1_valid_data_updated,
    ):

        data = app_note1_valid_data_updated.copy()
        data["title"] = ""

        with pytest.raises(ValidationError):

            JobApplicationNoteService.update(
                user=app_note1.job_application.owner,
                context=app_note1_context_with_id,
                validated_data=data,
            )


# ============================================================================
# Domain invariants
# ============================================================================

class TestValidateResolvedInstance:

    def test_wrong_job_application_raises(
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

        with pytest.raises(DomainInvariantViolationError):

            JobApplicationNoteService._validate_resolved_instance(
                instance=app_note1,
                context=context,
            )

    def test_wrong_job_position_raises(
        self,
        app_note1,
        job_position2_co1_ws1_user1,
    ):

        context = JobApplicationChildContext(
            id=app_note1.id,
            workspace_id=app_note1.job_application.workspace.workspace_id,
            company_id=app_note1.job_application.job_position.company.id,
            job_position_id=job_position2_co1_ws1_user1.id,
            job_application_id=app_note1.job_application.id,
        )

        with pytest.raises(DomainInvariantViolationError):

            JobApplicationNoteService._validate_resolved_instance(
                instance=app_note1,
                context=context,
            )

    def test_wrong_company_raises(
        self,
        app_note1,
    ):

        context = JobApplicationChildContext(
            id=app_note1.id,
            workspace_id=app_note1.job_application.workspace.workspace_id,
            company_id=999999,
            job_position_id=app_note1.job_application.job_position.id,
            job_application_id=app_note1.job_application.id,
        )

        with pytest.raises(DomainInvariantViolationError):

            JobApplicationNoteService._validate_resolved_instance(
                instance=app_note1,
                context=context,
            )

    def test_wrong_workspace_raises(
        self,
        app_note1,
    ):

        context = JobApplicationChildContext(
            id=app_note1.id,
            workspace_id="00000000-0000-0000-0000-000000000000",
            company_id=app_note1.job_application.job_position.company.id,
            job_position_id=app_note1.job_application.job_position.id,
            job_application_id=app_note1.job_application.id,
        )

        with pytest.raises(DomainInvariantViolationError):

            JobApplicationNoteService._validate_resolved_instance(
                instance=app_note1,
                context=context,
            )


# ============================================================================
# Remove
# ============================================================================

class TestJobApplicationNoteRemove:

    def test_remove_deletes_note(
        self,
        app_note1,
        app_note1_context_with_id,
    ):

        note_id = app_note1.id

        JobApplicationNoteService.remove(
            user=app_note1.job_application.owner,
            context=app_note1_context_with_id,
        )

        assert not JobApplicationNote.objects.filter(
            id=note_id
        ).exists()
