import pytest

from unittest.mock import patch

from rest_framework.exceptions import PermissionDenied

from apps.companies.services.company_service import CompanyService

#   ----------------------------------- ****** -----------------------------------


# Creation:

@pytest.mark.django_db
def test_create_company_calls_resolve_workspace(
        workspace_user1, co1_ws1_user1_context_with_id, co1_ws1_user1_valid_data
):

    with (
        patch(
            "apps.companies.services.company_service.CompanyService."
            "_resolve_workspace"
        ) as mock_resolve_workspace
    ):

        # Error due to fake workspace
        with pytest.raises(ValueError):
            CompanyService.create(
                user=workspace_user1.owner,
                context=co1_ws1_user1_context_with_id,
                validated_data=co1_ws1_user1_valid_data,
            )

        mock_resolve_workspace.assert_called_once()


@pytest.mark.django_db
def test_create_company_calls_full_clean(
        workspace_user1, co1_ws1_user1_context_no_id, co1_ws1_user1_valid_data
):

    with patch("apps.companies.models.Company.full_clean") as mock_clean:
        CompanyService.create(
            user=workspace_user1.owner,
            context=co1_ws1_user1_context_no_id,
            validated_data=co1_ws1_user1_valid_data,
        )

        mock_clean.assert_called_once()


@pytest.mark.django_db
def test_create_company_calls_save(
        workspace_user1, co1_ws1_user1_context_no_id, co1_ws1_user1_valid_data
):

    with patch("apps.companies.models.Company.save") as mock_save:
        CompanyService.create(
            user=workspace_user1.owner,
            context=co1_ws1_user1_context_no_id,
            validated_data=co1_ws1_user1_valid_data,
        )

        mock_save.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Updating

@pytest.mark.django_db
def test_update_calls_resolve_company(
        co1_ws1_user1,
        co1_ws1_user1_context_with_id,
        co1_ws1_user1_updated_valid_data
):

    with (
        patch(
            "apps.companies.services.company_service.CompanyService._resolve_company"
        ) as mock_resolve_company
    ):

        CompanyService.update(
            user=co1_ws1_user1.workspace.owner,
            context=co1_ws1_user1_context_with_id,
            validated_data=co1_ws1_user1_updated_valid_data
        )

        mock_resolve_company.assert_called_once()


@pytest.mark.django_db
def test_update_company_calls_full_clean(
        co1_ws1_user1,
        co1_ws1_user1_context_with_id,
        co1_ws1_user1_updated_valid_data
):

    with patch("apps.companies.models.Company.full_clean") as mock_clean:
        CompanyService.update(
            user=co1_ws1_user1.workspace.owner,
            context=co1_ws1_user1_context_with_id,
            validated_data=co1_ws1_user1_updated_valid_data,
        )

        mock_clean.assert_called_once()


@pytest.mark.django_db
def test_update_company_calls_save(
        co1_ws1_user1,
        co1_ws1_user1_context_with_id,
        co1_ws1_user1_updated_valid_data
):

    with patch("apps.companies.models.Company.save") as mock_save:
        CompanyService.update(
            user=co1_ws1_user1.workspace.owner,
            context=co1_ws1_user1_context_with_id,
            validated_data=co1_ws1_user1_updated_valid_data,
        )

        mock_save.assert_called_once()


@pytest.mark.django_db
def test_update_company_calls_update_non_m2m_fields(
        co1_ws1_user1,
        co1_ws1_user1_context_with_id,
        co1_ws1_user1_updated_valid_data
):

    with patch(
            "apps.companies.services.company_service.CompanyService."
            "_update_non_m2m_fields"
    ) as mock_update_non_m2m_fields:
        CompanyService.update(
            user=co1_ws1_user1.workspace.owner,
            context=co1_ws1_user1_context_with_id,
            validated_data=co1_ws1_user1_updated_valid_data,
        )

        mock_update_non_m2m_fields.assert_called_once()


@pytest.mark.django_db
def test_update_only_updates_the_given_fields(
        co1_ws1_user1_context_with_id,
        co1_ws1_user1_updated_valid_data,
        co1_ws1_user1
):

    co1_ws1_user1_updated_valid_data.pop("website")

    updated_company = CompanyService.update(
        user=co1_ws1_user1.workspace.owner,
        context=co1_ws1_user1_context_with_id,
        validated_data=co1_ws1_user1_updated_valid_data
    )

    assert updated_company.id == co1_ws1_user1.id
    assert updated_company.workspace == co1_ws1_user1.workspace
    assert updated_company.name == co1_ws1_user1_updated_valid_data["name"]
    assert updated_company.website == co1_ws1_user1.website


@pytest.mark.django_db
def test_full_update_updates_all_updatable_fields(
        co1_ws1_user1_context_with_id,
        co1_ws1_user1_updated_valid_data,
        co1_ws1_user1
):

    updated_company = CompanyService.update(
        user=co1_ws1_user1.workspace.owner,
        context=co1_ws1_user1_context_with_id,
        validated_data=co1_ws1_user1_updated_valid_data
    )

    assert updated_company.id == co1_ws1_user1.id
    assert updated_company.workspace == co1_ws1_user1.workspace
    assert updated_company.name == co1_ws1_user1_updated_valid_data["name"]
    assert updated_company.website == co1_ws1_user1_updated_valid_data["website"]

#   ----------------------------------- ****** -----------------------------------


# Test Deleting

@pytest.mark.django_db
def test_remove_calls_resolve_company(
        co1_ws1_user1, co1_ws1_user1_context_with_id
):

    with (
        patch(
            "apps.companies.services.company_service.CompanyService._resolve_company"
        ) as mock_resolve_company
    ):

        CompanyService.remove(
            user=co1_ws1_user1.workspace.owner,
            context=co1_ws1_user1_context_with_id,
        )

        mock_resolve_company.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test Retrieving

@pytest.mark.django_db
def test_resolve_company_calls_resolve_workspace(
        co1_ws1_user1, co1_ws1_user1_context_with_id
):

    with (
        patch(
            "apps.companies.services.company_service.CompanyService."
            "_resolve_workspace"
        ) as mock_resolve_workspace
    ):

        CompanyService._resolve_company(
            user=co1_ws1_user1.workspace.owner,
            workspace_id=co1_ws1_user1_context_with_id.workspace_id,
            company_id=co1_ws1_user1_context_with_id.id,
        )

        mock_resolve_workspace.assert_called_once()


@pytest.mark.django_db
def test_resolve_company_returns_company_successfully(
        co1_ws1_user1, co1_ws1_user1_context_with_id
):

    company = CompanyService._resolve_company(
        user=co1_ws1_user1.workspace.owner,
        workspace_id=co1_ws1_user1.workspace.workspace_id,
        company_id=co1_ws1_user1_context_with_id.id,
    )

    assert company == co1_ws1_user1
    assert company.id == co1_ws1_user1_context_with_id.id
    assert company.workspace.workspace_id == co1_ws1_user1.workspace.workspace_id


@pytest.mark.django_db
def test_access_to_someone_else_company_raise_error(
        other_workspace_user1, other_user, co1_ws1_user1_context_with_id
):

    # Company belong to another user
    with pytest.raises(PermissionDenied):
        CompanyService._resolve_company(
            user=other_user,
            workspace_id=co1_ws1_user1_context_with_id.workspace_id,
            company_id=co1_ws1_user1_context_with_id.id,
        )


@pytest.mark.django_db
def test_get_company_from_another_workspace_raises_validation_error(
        co1_ws2_user1, co1_ws1_user1
):

    with pytest.raises(PermissionDenied):
        CompanyService._resolve_company(
            user=co1_ws1_user1.workspace.owner,
            workspace_id=co1_ws1_user1.workspace.id,
            company_id=co1_ws2_user1.id,
        )

#   ----------------------------------- ****** -----------------------------------
