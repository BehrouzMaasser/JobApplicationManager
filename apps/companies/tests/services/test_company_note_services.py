import pytest
from unittest.mock import patch

from apps.companies.services.company_note_service import CompanyNoteService

from apps.core.exceptions.exceptions import DomainInvariantViolationError


# -----------------------------------
# CREATE
# -----------------------------------

@pytest.mark.django_db
class TestCompanyNoteServiceCreate:

    def test_create_returns_company_note_successfully(
        self,
        co1_ws1_user1,
        co_note1_co1_ws1_user1_valid_data,
        co1_child_context_ws1_user1_no_id,
    ):
        note = CompanyNoteService.create(
            user=co1_ws1_user1.workspace.owner,
            context=co1_child_context_ws1_user1_no_id,
            validated_data=co_note1_co1_ws1_user1_valid_data,
        )

        assert note.id is not None
        assert note.company == co1_ws1_user1
        assert note.title == co_note1_co1_ws1_user1_valid_data["title"]
        assert note.content == co_note1_co1_ws1_user1_valid_data["content"]

    def test_create_calls_model_methods(
        self,
        co1_ws1_user1,
        co_note1_co1_ws1_user1_valid_data,
        co1_child_context_ws1_user1_no_id,
    ):
        with patch("apps.companies.models.CompanyNote.full_clean") as mock_clean, \
             patch("apps.companies.models.CompanyNote.save") as mock_save, \
             patch(
                 "apps.companies.services.company_note_service.CompanyNoteService."
                 "_resolve_company",
                 return_value=co1_ws1_user1,
             ):

            CompanyNoteService.create(
                user=co1_ws1_user1.workspace.owner,
                context=co1_child_context_ws1_user1_no_id,
                validated_data=co_note1_co1_ws1_user1_valid_data,
            )

            mock_clean.assert_called_once()
            mock_save.assert_called_once()


# -----------------------------------
# UPDATE
# -----------------------------------

@pytest.mark.django_db
class TestCompanyNoteServiceUpdate:

    def test_update_resolves_company_note(
        self,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_context_with_id,
        co_note1_co1_ws1_user1_updated_valid_data,
    ):
        with patch(
            "apps.companies.services.company_note_service.CompanyNoteService."
            "_resolve_company_note"
        ) as mock_resolve:

            mock_resolve.return_value = co_note1_co1_ws1_user1

            CompanyNoteService.update(
                user=co_note1_co1_ws1_user1.company.workspace.owner,
                context=co_note1_co1_ws1_user1_context_with_id,
                validated_data=co_note1_co1_ws1_user1_updated_valid_data,
            )

            mock_resolve.assert_called_once()

    def test_update_calls_update_non_m2m_fields(
        self,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_context_with_id,
        co_note1_co1_ws1_user1_updated_valid_data,
    ):
        with patch(
            "apps.companies.services.company_note_service.CompanyNoteService."
            "_update_non_m2m_fields"
        ) as mock_update, patch(
            "apps.companies.services.company_note_service.CompanyNoteService."
            "_resolve_company_note",
            return_value=co_note1_co1_ws1_user1,
        ):

            CompanyNoteService.update(
                user=co_note1_co1_ws1_user1.company.workspace.owner,
                context=co_note1_co1_ws1_user1_context_with_id,
                validated_data=co_note1_co1_ws1_user1_updated_valid_data,
            )

            mock_update.assert_called_once()

    def test_update_calls_model_methods(
        self,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_context_with_id,
        co_note1_co1_ws1_user1_updated_valid_data,
    ):
        with patch("apps.companies.models.CompanyNote.full_clean") as mock_clean, \
             patch("apps.companies.models.CompanyNote.save") as mock_save, \
             patch(
                 "apps.companies.services.company_note_service.CompanyNoteService."
                 "_resolve_company_note",
                 return_value=co_note1_co1_ws1_user1,
             ):

            CompanyNoteService.update(
                user=co_note1_co1_ws1_user1.company.workspace.owner,
                context=co_note1_co1_ws1_user1_context_with_id,
                validated_data=co_note1_co1_ws1_user1_updated_valid_data,
            )

            mock_clean.assert_called_once()
            mock_save.assert_called_once()

    def test_partial_update_keeps_existing_fields(
        self,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_context_with_id,
        co_note1_co1_ws1_user1_updated_valid_data,
    ):
        data = co_note1_co1_ws1_user1_updated_valid_data.copy()
        data.pop("content")

        updated = CompanyNoteService.update(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            context=co_note1_co1_ws1_user1_context_with_id,
            validated_data=data,
        )

        assert updated.title == data["title"]
        assert updated.content == co_note1_co1_ws1_user1.content

    def test_full_update_updates_all_fields(
        self,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_context_with_id,
        co_note1_co1_ws1_user1_updated_valid_data,
    ):
        updated = CompanyNoteService.update(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            context=co_note1_co1_ws1_user1_context_with_id,
            validated_data=co_note1_co1_ws1_user1_updated_valid_data,
        )

        assert updated.title == co_note1_co1_ws1_user1_updated_valid_data["title"]
        assert (updated.content ==
                co_note1_co1_ws1_user1_updated_valid_data["content"])


# -----------------------------------
# REMOVE
# -----------------------------------

@pytest.mark.django_db
class TestCompanyNoteServiceRemove:

    def test_remove_resolves_company_note(
        self,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_context_with_id,
    ):
        with patch(
            "apps.companies.services.company_note_service.CompanyNoteService."
            "_resolve_company_note"
        ) as mock_resolve:

            mock_resolve.return_value = co_note1_co1_ws1_user1

            CompanyNoteService.remove(
                user=co_note1_co1_ws1_user1.company.workspace.owner,
                context=co_note1_co1_ws1_user1_context_with_id,
            )

            mock_resolve.assert_called_once()


# -----------------------------------
# RESOLVE
# -----------------------------------

@pytest.mark.django_db
class TestCompanyNoteServiceResolve:

    def test_returns_note_successfully(
        self,
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_context_with_id,
    ):
        result = CompanyNoteService._resolve_company_note(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            context=co_note1_co1_ws1_user1_context_with_id,
        )

        assert result == co_note1_co1_ws1_user1

    def test_company_mismatch_raises_error(
        self,
        co_note1_co1_ws1_user1,
    ):
        with pytest.raises(DomainInvariantViolationError):
            CompanyNoteService._resolve_company_note(
                user=co_note1_co1_ws1_user1.company.workspace.owner,
                context=type("ctx", (), {
                    "id": co_note1_co1_ws1_user1.id,
                    "company_id": 999999,
                    "workspace_id": (
                        co_note1_co1_ws1_user1.company.workspace.workspace_id
                    ),
                })(),
            )

    def test_workspace_mismatch_raises_error(
        self,
        co_note1_co1_ws1_user1,
    ):
        with pytest.raises(DomainInvariantViolationError):
            CompanyNoteService._resolve_company_note(
                user=co_note1_co1_ws1_user1.company.workspace.owner,
                context=type("ctx", (), {
                    "id": co_note1_co1_ws1_user1.id,
                    "company_id": co_note1_co1_ws1_user1.company.id,
                    "workspace_id": "invalid-workspace",
                })(),
            )
