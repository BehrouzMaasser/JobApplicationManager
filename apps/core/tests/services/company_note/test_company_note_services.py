from unittest.mock import patch

import pytest
from django.core.exceptions import ValidationError

from apps.companies.models import CompanyNote
from apps.companies.services.company_note_service import (
    CompanyNoteService,
)

from apps.core.common.contexts.contexts import (
    CompanyContext,
    CompanyChildContext,
)

from apps.core.exceptions.exceptions import (
    DomainInvariantViolationError,
)


pytestmark = pytest.mark.django_db


# ============================================================================
# Hooks
# ============================================================================

class TestResolveCreateDependencies:

    def test_resolves_company_dependency(
        self,
        co1_ws1_user1,
        co1_child_context_ws1_user1_no_id,
    ):

        dependencies = CompanyNoteService._resolve_create_dependencies(
            user=co1_ws1_user1.workspace.owner,
            context=co1_child_context_ws1_user1_no_id,
        )

        assert dependencies == {
            "company": co1_ws1_user1
        }


    def test_resolves_company_through_company_service(
        self,
        co1_ws1_user1,
        co1_child_context_ws1_user1_no_id,
    ):

        with patch(
            "apps.companies.services.company_note_service."
            "CompanyService._resolve_instance"
        ) as mock_resolve:

            mock_resolve.return_value = co1_ws1_user1

            CompanyNoteService._resolve_create_dependencies(
                user=co1_ws1_user1.workspace.owner,
                context=co1_child_context_ws1_user1_no_id,
            )

            mock_resolve.assert_called_once_with(
                user=co1_ws1_user1.workspace.owner,
                context=CompanyContext(
                    id=(
                        co1_child_context_ws1_user1_no_id.company_id
                    ),
                    workspace_id=(
                        co1_child_context_ws1_user1_no_id.workspace_id
                    ),
                ),
            )


# ============================================================================
# Create
# ============================================================================

class TestCompanyNoteCreate:

    def test_create_creates_company_note(
        self,
        co1_ws1_user1,
        co_note1_co1_ws1_user1_valid_data,
        co1_child_context_ws1_user1_no_id,
    ):

        note = CompanyNoteService.create(
            user=co1_ws1_user1.workspace.owner,
            context=co1_child_context_ws1_user1_no_id,
            validated_data=(
                co_note1_co1_ws1_user1_valid_data
            ),
        )

        assert note.pk is not None
        assert note.company == co1_ws1_user1
        assert note.title == (
            co_note1_co1_ws1_user1_valid_data["title"]
        )
        assert note.content == (
            co_note1_co1_ws1_user1_valid_data["content"]
        )


    def test_create_delegates_model_validation(
        self,
        co1_ws1_user1,
        co_note1_co1_ws1_user1_valid_data,
        co1_child_context_ws1_user1_no_id,
    ):

        with patch(
            "apps.companies.models.CompanyNote.full_clean"
        ) as mock_clean:

            CompanyNoteService.create(
                user=co1_ws1_user1.workspace.owner,
                context=co1_child_context_ws1_user1_no_id,
                validated_data=(
                    co_note1_co1_ws1_user1_valid_data
                ),
            )

            mock_clean.assert_called_once()


    def test_create_rejects_invalid_model_data(
        self,
        co1_ws1_user1,
        co1_child_context_ws1_user1_no_id,
    ):

        with pytest.raises(ValidationError):

            CompanyNoteService.create(
                user=co1_ws1_user1.workspace.owner,
                context=co1_child_context_ws1_user1_no_id,
                validated_data={
                    "title": None,
                    "content": "Invalid",
                },
            )


# ============================================================================
# Update
# ============================================================================

class TestCompanyNoteUpdate:

    def test_update_changes_allowed_fields(
        self,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_context_with_id,
        co_note1_co1_ws1_user1_updated_valid_data,
    ):

        updated = CompanyNoteService.update(
            user=(
                co_note1_co1_ws1_user1
                .company
                .workspace
                .owner
            ),
            context=(
                co_note1_co1_ws1_user1_context_with_id
            ),
            validated_data=(
                co_note1_co1_ws1_user1_updated_valid_data
            ),
        )

        assert updated.title == (
            co_note1_co1_ws1_user1_updated_valid_data["title"]
        )

        assert updated.content == (
            co_note1_co1_ws1_user1_updated_valid_data["content"]
        )


    def test_update_allows_partial_update(
        self,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_context_with_id,
    ):

        old_content = co_note1_co1_ws1_user1.content

        updated = CompanyNoteService.update(
            user=(
                co_note1_co1_ws1_user1
                .company
                .workspace
                .owner
            ),
            context=(
                co_note1_co1_ws1_user1_context_with_id
            ),
            validated_data={
                "title": "Updated title",
            },
        )

        assert updated.title == "Updated title"
        assert updated.content == old_content


    def test_update_delegates_model_validation(
        self,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_context_with_id,
    ):

        with patch(
            "apps.companies.models.CompanyNote.full_clean"
        ) as mock_clean:

            CompanyNoteService.update(
                user=(
                    co_note1_co1_ws1_user1
                    .company
                    .workspace
                    .owner
                ),
                context=(
                    co_note1_co1_ws1_user1_context_with_id
                ),
                validated_data={
                    "title": "Updated title",
                },
            )

            mock_clean.assert_called_once()


# ============================================================================
# Resolution
# ============================================================================

class TestCompanyNoteResolution:

    def test_selector_is_used(
        self,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_context_with_id,
    ):

        with patch(
            "apps.companies.services.company_note_service."
            "CompanyNoteSelector.get",
            return_value=co_note1_co1_ws1_user1,
        ) as mock_get:

            CompanyNoteService._resolve_instance(
                user=(
                    co_note1_co1_ws1_user1
                    .company
                    .workspace
                    .owner
                ),
                context=(
                    co_note1_co1_ws1_user1_context_with_id
                ),
            )

            mock_get.assert_called_once_with(
                user=(
                    co_note1_co1_ws1_user1
                    .company
                    .workspace
                    .owner
                ),
                obj_id=(
                    co_note1_co1_ws1_user1_context_with_id.id
                ),
            )


# ============================================================================
# Domain invariants
# ============================================================================

class TestValidateResolvedInstance:

    def test_matching_context_passes(
        self,
        co_note1_co1_ws1_user1,
    ):

        CompanyNoteService._validate_resolved_instance(
            instance=co_note1_co1_ws1_user1,
            context=CompanyChildContext(
                id=co_note1_co1_ws1_user1.id,
                company_id=(
                    co_note1_co1_ws1_user1.company.id
                ),
                workspace_id=(
                    co_note1_co1_ws1_user1
                    .company
                    .workspace
                    .workspace_id
                ),
            ),
        )


    def test_wrong_company_raises(
        self,
        co_note1_co1_ws1_user1,
    ):

        with pytest.raises(
            DomainInvariantViolationError
        ):

            CompanyNoteService._validate_resolved_instance(
                instance=co_note1_co1_ws1_user1,
                context=CompanyChildContext(
                    id=co_note1_co1_ws1_user1.id,
                    company_id=999999,
                    workspace_id=(
                        co_note1_co1_ws1_user1
                        .company
                        .workspace
                        .workspace_id
                    ),
                ),
            )


    def test_wrong_workspace_raises(
        self,
        co_note1_co1_ws1_user1,
    ):

        with pytest.raises(
            DomainInvariantViolationError
        ):

            CompanyNoteService._validate_resolved_instance(
                instance=co_note1_co1_ws1_user1,
                context=CompanyChildContext(
                    id=co_note1_co1_ws1_user1.id,
                    company_id=(
                        co_note1_co1_ws1_user1.company.id
                    ),
                    workspace_id="invalid-workspace",
                ),
            )


# ============================================================================
# Remove
# ============================================================================

class TestCompanyNoteRemove:

    def test_remove_deletes_company_note(
        self,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_context_with_id,
    ):

        note_id = co_note1_co1_ws1_user1.id

        CompanyNoteService.remove(
            user=(
                co_note1_co1_ws1_user1
                .company
                .workspace
                .owner
            ),
            context=(
                co_note1_co1_ws1_user1_context_with_id
            ),
        )

        with pytest.raises(CompanyNote.DoesNotExist):

            CompanyNote.objects.get(
                id=note_id
            )
