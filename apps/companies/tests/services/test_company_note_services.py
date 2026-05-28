import pytest

from unittest.mock import patch

from rest_framework.exceptions import ValidationError, PermissionDenied

from apps.companies.services.company_note_service import CompanyNoteService
from apps.companies.services.contexts.company_context import CompanyChildContext

#   ----------------------------------- ****** -----------------------------------


# Creation:

@pytest.mark.django_db
def test_create_company_note_successfully_returns_company_note(
        co1_ws1_user1,
        co_note1_co1_ws1_user1_valid_data,
        co1_child_context_ws1_user1_no_id
):

    company_note = CompanyNoteService.create(
        user=co1_ws1_user1.workspace.owner,
        context=co1_child_context_ws1_user1_no_id,
        validated_data=co_note1_co1_ws1_user1_valid_data,
    )

    assert company_note.id is not None
    assert company_note.company == co1_ws1_user1
    assert company_note.title == co_note1_co1_ws1_user1_valid_data["title"]
    assert company_note.content == co_note1_co1_ws1_user1_valid_data["content"]


@pytest.mark.django_db
def test_create_company_note_calls_resolve_company(
        co1_ws1_user1,
        co_note1_co1_ws1_user1_valid_data,
        co1_child_context_ws1_user1_no_id
):

    with (
        patch(
            "apps.companies.services.company_note_service.CompanyNoteService."
            "_resolve_company"
        ) as mock_resolve_company
    ):

        # Error due to fake company
        with pytest.raises(ValueError):
            CompanyNoteService.create(
                user=co1_ws1_user1.workspace.owner,
                context=co1_child_context_ws1_user1_no_id,
                validated_data=co_note1_co1_ws1_user1_valid_data,
            )

        mock_resolve_company.assert_called_once()


@pytest.mark.django_db
def test_create_company_note_calls_full_clean(
        co1_ws1_user1,
        co_note1_co1_ws1_user1_valid_data,
        co1_child_context_ws1_user1_no_id
):

    with patch("apps.companies.models.CompanyNote.full_clean") as mock_full_clean:

        CompanyNoteService.create(
            user=co1_ws1_user1.workspace.owner,
            context=co1_child_context_ws1_user1_no_id,
            validated_data=co_note1_co1_ws1_user1_valid_data,
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_create_company_note_calls_save(
        co1_ws1_user1,
        co_note1_co1_ws1_user1_valid_data,
        co1_child_context_ws1_user1_no_id
):

    with patch("apps.companies.models.CompanyNote.save") as mock_save:

        CompanyNoteService.create(
            user=co1_ws1_user1.workspace.owner,
            context=co1_child_context_ws1_user1_no_id,
            validated_data=co_note1_co1_ws1_user1_valid_data,
        )

        mock_save.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Updating

@pytest.mark.django_db
def test_update_company_note_successfully_returns_updated_company_note(
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_updated_valid_data,
        co_note1_co1_ws1_user1_context_with_id
):

    updated_note = CompanyNoteService.update(
        user=co_note1_co1_ws1_user1.company.workspace.owner,
        context=co_note1_co1_ws1_user1_context_with_id,
        validated_data=co_note1_co1_ws1_user1_updated_valid_data,
    )

    assert updated_note.id == co_note1_co1_ws1_user1.id
    assert updated_note.company == co_note1_co1_ws1_user1.company
    assert updated_note.title == co_note1_co1_ws1_user1_updated_valid_data["title"]

    assert (updated_note.content ==
            co_note1_co1_ws1_user1_updated_valid_data["content"])


@pytest.mark.django_db
def test_update_company_note_calls_full_clean(
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_updated_valid_data,
        co_note1_co1_ws1_user1_context_with_id
):

    with patch("apps.companies.models.CompanyNote.full_clean") as mock_full_clean:

        CompanyNoteService.update(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            context=co_note1_co1_ws1_user1_context_with_id,
            validated_data=co_note1_co1_ws1_user1_updated_valid_data,
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_update_company_note_calls_save(
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_updated_valid_data,
        co_note1_co1_ws1_user1_context_with_id
):

    with patch("apps.companies.models.CompanyNote.save") as mock_save:

        CompanyNoteService.update(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            context=co_note1_co1_ws1_user1_context_with_id,
            validated_data=co_note1_co1_ws1_user1_updated_valid_data,
        )

        mock_save.assert_called_once()


@pytest.mark.django_db
def test_update_company_note_calls_resolve_company_note(
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_updated_valid_data,
        co_note1_co1_ws1_user1_context_with_id
):

    with (
        patch(
            "apps.companies.services.company_note_service.CompanyNoteService."
            "_resolve_company_note"
        ) as mock_resolve_company_note
    ):

        CompanyNoteService.update(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            context=co_note1_co1_ws1_user1_context_with_id,
            validated_data=co_note1_co1_ws1_user1_updated_valid_data,
        )

        mock_resolve_company_note.assert_called_once()


@pytest.mark.django_db
def test_update_company_note_calls_update_non_m2m_fields(
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_updated_valid_data,
        co_note1_co1_ws1_user1_context_with_id
):

    with patch(
            "apps.companies.services.company_note_service.CompanyNoteService."
            "_update_non_m2m_fields"
    ) as mock_update_non_m2m_fields:
        CompanyNoteService.update(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            context=co_note1_co1_ws1_user1_context_with_id,
            validated_data=co_note1_co1_ws1_user1_updated_valid_data,
        )

        mock_update_non_m2m_fields.assert_called_once()


@pytest.mark.django_db
def test_missing_required_field_dont_raises_error(
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_updated_valid_data,
        co_note1_co1_ws1_user1_context_with_id
):

    co_note1_co1_ws1_user1_updated_valid_data.pop("title")

    updated_note = CompanyNoteService.update(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            context=co_note1_co1_ws1_user1_context_with_id,
            validated_data=co_note1_co1_ws1_user1_updated_valid_data,
    )

    assert updated_note.id == co_note1_co1_ws1_user1.id
    assert updated_note.title == co_note1_co1_ws1_user1.title

    assert (updated_note.content ==
            co_note1_co1_ws1_user1_updated_valid_data["content"])


@pytest.mark.django_db
def test_update_only_the_fields_given(
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_updated_valid_data,
        co_note1_co1_ws1_user1_context_with_id
):

    co_note1_co1_ws1_user1_updated_valid_data.pop("content")

    updated_note = CompanyNoteService.update(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            context=co_note1_co1_ws1_user1_context_with_id,
            validated_data=co_note1_co1_ws1_user1_updated_valid_data,
    )

    assert updated_note.id == co_note1_co1_ws1_user1.id
    assert updated_note.title == co_note1_co1_ws1_user1_updated_valid_data["title"]
    assert updated_note.content == co_note1_co1_ws1_user1.content

#   ----------------------------------- ****** -----------------------------------


# Test Deleting

@pytest.mark.django_db
def test_update_company_note_calls_resolve_company_note(
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_context_with_id,
):

    with (
        patch(
            "apps.companies.services.company_note_service.CompanyNoteService."
            "_resolve_company_note"
        ) as mock_resolve_company_note
    ):

        CompanyNoteService.remove(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            context=co_note1_co1_ws1_user1_context_with_id,
        )

        mock_resolve_company_note.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test Retrieving

@pytest.mark.django_db
def test_retrieve_company_note_calls_resolve_company(
        co_note1_co1_ws1_user1,
        co_note1_co1_ws1_user1_context_with_id,
):

    with (
        patch(
            "apps.companies.services.company_note_service.CompanyNoteService."
            "_resolve_company"
        ) as mock_resolve_company
    ):

        CompanyNoteService._resolve_company_note(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            context=co_note1_co1_ws1_user1_context_with_id,
        )

        mock_resolve_company.assert_called_once()


@pytest.mark.django_db
def test_access_note_from_another_company_raises_error(
        co_note1_co1_ws1_user1, co_note1_co2_ws1_user1
):

    with pytest.raises(ValidationError):
        CompanyNoteService._resolve_company_note(
            user=co_note1_co1_ws1_user1.company.workspace.owner,
            context=CompanyChildContext(
                id=co_note1_co2_ws1_user1.id,
                workspace_id=co_note1_co1_ws1_user1.company.workspace.workspace_id,
                company_id=co_note1_co1_ws1_user1.company.id,
            ),
        )


@pytest.mark.django_db
def test_access_note_of_another_user_raises_error(
        other_user, co_note1_co1_ws1_user1_context_with_id
):

    with pytest.raises(PermissionDenied):
        CompanyNoteService._resolve_company_note(
            user=other_user,
            context=co_note1_co1_ws1_user1_context_with_id
        )

#   ----------------------------------- ****** -----------------------------------
