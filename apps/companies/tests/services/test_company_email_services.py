import pytest

from unittest.mock import patch

from rest_framework.exceptions import ValidationError, PermissionDenied

from apps.companies.services.company_email_service import CompanyEmailService
from apps.companies.services.contexts.company_context import CompanyChildContext


#   ----------------------------------- ****** -----------------------------------

# Creation:

@pytest.mark.django_db
def test_create_company_email_successfully_returns_company_email(
        co1_ws1_user1,
        co1_child_context_ws1_user1_no_id,
        co_email1_co1_ws1_user1_valid_data
):

    company_email = CompanyEmailService.create(
        user=co1_ws1_user1.workspace.owner,
        context=co1_child_context_ws1_user1_no_id,
        validated_data=co_email1_co1_ws1_user1_valid_data,
    )

    assert company_email.id is not None
    assert company_email.title == co_email1_co1_ws1_user1_valid_data["title"]
    assert company_email.email == co_email1_co1_ws1_user1_valid_data["email"]
    assert company_email.company == co1_ws1_user1


@pytest.mark.django_db
def test_create_company_email_calls_resolve_company(
        co1_ws1_user1,
        co_email1_co1_ws1_user1_valid_data,
        co1_child_context_ws1_user1_no_id
):

    with (
        patch(
            "apps.companies.services.company_email_service.CompanyEmailService."
            "_resolve_company"
        ) as mock_resolve_company
    ):

        # Error due to fake company
        with pytest.raises(ValueError):
            CompanyEmailService.create(
                user=co1_ws1_user1.workspace.owner,
                context=co1_child_context_ws1_user1_no_id,
                validated_data=co_email1_co1_ws1_user1_valid_data,
            )

        mock_resolve_company.assert_called_once()


@pytest.mark.django_db
def test_create_company_email_calls_full_clean(
        co1_ws1_user1,
        co1_child_context_ws1_user1_no_id,
        co_email1_co1_ws1_user1_valid_data
):

    with patch("apps.companies.models.CompanyEmail.full_clean") as mock_full_clean:
        CompanyEmailService.create(
            user=co1_ws1_user1.workspace.owner,
            context=co1_child_context_ws1_user1_no_id,
            validated_data=co_email1_co1_ws1_user1_valid_data,
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_create_company_email_calls_save(
        co1_ws1_user1,
        co1_child_context_ws1_user1_no_id,
        co_email1_co1_ws1_user1_valid_data
):

    with patch("apps.companies.models.CompanyEmail.save") as mock_save:
        CompanyEmailService.create(
            user=co1_ws1_user1.workspace.owner,
            context=co1_child_context_ws1_user1_no_id,
            validated_data=co_email1_co1_ws1_user1_valid_data,
        )

        mock_save.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Updating

@pytest.mark.django_db
def test_update_company_email_calls_full_clean(
        co1_ws1_user1,
        co_email1_co1_ws1_user1_context_with_id,
        co_email1_co1_ws1_user1_updated_valid_data
):

    with patch("apps.companies.models.CompanyEmail.full_clean") as mock_full_clean:
        CompanyEmailService.update(
            user=co1_ws1_user1.workspace.owner,
            context=co_email1_co1_ws1_user1_context_with_id,
            validated_data=co_email1_co1_ws1_user1_updated_valid_data,
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_update_company_email_calls_save(
        co1_ws1_user1,
        co_email1_co1_ws1_user1_context_with_id,
        co_email1_co1_ws1_user1_updated_valid_data
):

    with patch("apps.companies.models.CompanyEmail.save") as mock_save:
        CompanyEmailService.update(
            user=co1_ws1_user1.workspace.owner,
            context=co_email1_co1_ws1_user1_context_with_id,
            validated_data=co_email1_co1_ws1_user1_updated_valid_data,
        )

        mock_save.assert_called_once()


@pytest.mark.django_db
def test_update_company_email_calls_update_non_m2m_fields(
        co1_ws1_user1,
        co_email1_co1_ws1_user1_context_with_id,
        co_email1_co1_ws1_user1_updated_valid_data
):

    with patch(
            "apps.companies.services.company_email_service.CompanyEmailService."
            "_update_non_m2m_fields"
    ) as mock_update_non_m2m_fields:
        CompanyEmailService.update(
            user=co1_ws1_user1.workspace.owner,
            context=co_email1_co1_ws1_user1_context_with_id,
            validated_data=co_email1_co1_ws1_user1_updated_valid_data,
        )

        mock_update_non_m2m_fields.assert_called_once()


@pytest.mark.django_db
def test_update_company_email_calls_resolve_company_email(
        co1_ws1_user1,
        co_email1_co1_ws1_user1_context_with_id,
        co_email1_co1_ws1_user1_updated_valid_data
):

    with (
        patch(
            "apps.companies.services.company_email_service.CompanyEmailService."
            "_resolve_company_email"
        ) as mock_resolve_company_email
    ):

        CompanyEmailService.update(
            user=co1_ws1_user1.workspace.owner,
            context=co_email1_co1_ws1_user1_context_with_id,
            validated_data=co_email1_co1_ws1_user1_updated_valid_data,
        )

        mock_resolve_company_email.assert_called_once()


@pytest.mark.django_db
def test_update_company_email_successfully_returns_updated_company_email(
        co_email1_co1_ws1_user1_context_with_id,
        co_email1_co1_ws1_user1_updated_valid_data,
        co_email1_co1_ws1_user1
):

    updated_email = CompanyEmailService.update(
        user=co_email1_co1_ws1_user1.company.workspace.owner,
        context=co_email1_co1_ws1_user1_context_with_id,
        validated_data=co_email1_co1_ws1_user1_updated_valid_data,
    )

    assert updated_email.id == co_email1_co1_ws1_user1.id
    assert updated_email.company == co_email1_co1_ws1_user1.company
    assert updated_email.email == co_email1_co1_ws1_user1_updated_valid_data["email"]
    assert updated_email.title == co_email1_co1_ws1_user1_updated_valid_data["title"]


@pytest.mark.django_db
def test_update_company_email_dont_raise_error_if_a_required_field_is_missing(
        co_email1_co1_ws1_user1_context_with_id,
        co_email1_co1_ws1_user1_updated_valid_data,
        co_email1_co1_ws1_user1
):

    co_email1_co1_ws1_user1_updated_valid_data.pop("email")

    updated_email = CompanyEmailService.update(
        user=co_email1_co1_ws1_user1.company.workspace.owner,
        context=co_email1_co1_ws1_user1_context_with_id,
        validated_data=co_email1_co1_ws1_user1_updated_valid_data,
    )

    assert updated_email.id == co_email1_co1_ws1_user1.id
    assert updated_email.company == co_email1_co1_ws1_user1.company
    assert updated_email.email == co_email1_co1_ws1_user1.email
    assert updated_email.title == co_email1_co1_ws1_user1_updated_valid_data["title"]

#   ----------------------------------- ****** -----------------------------------


# Test Deleting

@pytest.mark.django_db
def test_remove_company_email_calls_resolve_company_email(
        co_email1_co1_ws1_user1, co_email1_co1_ws1_user1_context_with_id
):

    with (
        patch(
            "apps.companies.services.company_email_service.CompanyEmailService."
            "_resolve_company_email"
        ) as mock_resolve_company_email
    ):

        CompanyEmailService.remove(
            user=co_email1_co1_ws1_user1.company.workspace.owner,
            context=co_email1_co1_ws1_user1_context_with_id,
        )

        mock_resolve_company_email.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test Retrieving

@pytest.mark.django_db
def test_retrieve_company_email_calls_resolve_company(
        co_email1_co1_ws1_user1, co_email1_co1_ws1_user1_context_with_id
):

    with (
        patch(
            "apps.companies.services.company_email_service.CompanyEmailService."
            "_resolve_company"
        ) as mock_resolve_company
    ):

        CompanyEmailService._resolve_company_email(
            user=co_email1_co1_ws1_user1.company.workspace.owner,
            context=co_email1_co1_ws1_user1_context_with_id,
        )

        mock_resolve_company.assert_called_once()


@pytest.mark.django_db
def test_access_to_email_from_another_company_raises_error(
        co_email1_co2_ws1_user1, co_email1_co1_ws1_user1
):

    with pytest.raises(ValidationError):
        CompanyEmailService._resolve_company_email(
            user=co_email1_co1_ws1_user1.company.workspace.owner,
            context=CompanyChildContext(
                id=co_email1_co2_ws1_user1.id,
                company_id=co_email1_co1_ws1_user1.company.id,
                workspace_id=co_email1_co1_ws1_user1.company.workspace.workspace_id,
            ),
        )


@pytest.mark.django_db
def test_access_to_email_of_another_user_raises_error(
        other_user,
        co_email1_co1_ws1_user1_context_with_id
):

    with pytest.raises(PermissionDenied):
        CompanyEmailService._resolve_company_email(
            user=other_user,
            context=co_email1_co1_ws1_user1_context_with_id
        )

#   ----------------------------------- ****** -----------------------------------
