import pytest
from unittest.mock import patch

from apps.companies.services.company_email_service import CompanyEmailService

from apps.companies.services.contexts.company_context import CompanyChildContext

from apps.core.exceptions.exceptions import DomainInvariantViolationError


# -----------------------------------
# CREATE
# -----------------------------------

@pytest.mark.django_db
class TestCompanyEmailServiceCreate:

    def test_create_returns_company_email_successfully(
        self,
        co1_ws1_user1,
        co1_child_context_ws1_user1_no_id,
        co_email1_co1_ws1_user1_valid_data,
    ):
        result = CompanyEmailService.create(
            user=co1_ws1_user1.workspace.owner,
            context=co1_child_context_ws1_user1_no_id,
            validated_data=co_email1_co1_ws1_user1_valid_data,
        )

        assert result.id is not None
        assert result.title == co_email1_co1_ws1_user1_valid_data["title"]
        assert result.email == co_email1_co1_ws1_user1_valid_data["email"]
        assert result.company == co1_ws1_user1

    def test_create_calls_model_methods(
        self,
        co1_ws1_user1,
        co1_child_context_ws1_user1_no_id,
        co_email1_co1_ws1_user1_valid_data,
    ):
        with patch("apps.companies.models.CompanyEmail.full_clean") as mock_clean, \
             patch("apps.companies.models.CompanyEmail.save") as mock_save, \
             patch(
                 "apps.companies.services.company_email_service.CompanyEmailService."
                 "_resolve_company",
                 return_value=co1_ws1_user1,
             ):

            CompanyEmailService.create(
                user=co1_ws1_user1.workspace.owner,
                context=co1_child_context_ws1_user1_no_id,
                validated_data=co_email1_co1_ws1_user1_valid_data,
            )

            mock_clean.assert_called_once()
            mock_save.assert_called_once()


# -----------------------------------
# UPDATE
# -----------------------------------

@pytest.mark.django_db
class TestCompanyEmailServiceUpdate:

    def test_update_resolves_company_email(
        self,
        co1_ws1_user1,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user1_context_with_id,
        co_email1_co1_ws1_user1_updated_valid_data,
    ):
        with patch(
            "apps.companies.services.company_email_service.CompanyEmailService."
            "_resolve_company_email"
        ) as mock_resolve:

            mock_resolve.return_value = co_email1_co1_ws1_user1

            CompanyEmailService.update(
                user=co1_ws1_user1.workspace.owner,
                context=co_email1_co1_ws1_user1_context_with_id,
                validated_data=co_email1_co1_ws1_user1_updated_valid_data,
            )

            mock_resolve.assert_called_once()

    def test_update_calls_update_non_m2m_fields(
        self,
        co1_ws1_user1,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user1_context_with_id,
        co_email1_co1_ws1_user1_updated_valid_data,
    ):
        with patch(
            "apps.companies.services.company_email_service.CompanyEmailService."
            "_update_non_m2m_fields"
        ) as mock_update, patch(
            "apps.companies.services.company_email_service.CompanyEmailService."
            "_resolve_company_email",
            return_value=co_email1_co1_ws1_user1,
        ):

            CompanyEmailService.update(
                user=co1_ws1_user1.workspace.owner,
                context=co_email1_co1_ws1_user1_context_with_id,
                validated_data=co_email1_co1_ws1_user1_updated_valid_data,
            )

            mock_update.assert_called_once()

    def test_update_calls_model_methods(
        self,
        co1_ws1_user1,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user1_context_with_id,
        co_email1_co1_ws1_user1_updated_valid_data,
    ):
        with patch("apps.companies.models.CompanyEmail.full_clean") as mock_clean, \
             patch("apps.companies.models.CompanyEmail.save") as mock_save, \
             patch(
                 "apps.companies.services.company_email_service.CompanyEmailService."
                 "_resolve_company_email",
                 return_value=co_email1_co1_ws1_user1,
             ):

            CompanyEmailService.update(
                user=co1_ws1_user1.workspace.owner,
                context=co_email1_co1_ws1_user1_context_with_id,
                validated_data=co_email1_co1_ws1_user1_updated_valid_data,
            )

            mock_clean.assert_called_once()
            mock_save.assert_called_once()

    def test_partial_update_keeps_existing_fields(
        self,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user1_context_with_id,
        co_email1_co1_ws1_user1_updated_valid_data,
    ):
        data = co_email1_co1_ws1_user1_updated_valid_data.copy()
        data.pop("email")

        updated = CompanyEmailService.update(
            user=co_email1_co1_ws1_user1.company.workspace.owner,
            context=co_email1_co1_ws1_user1_context_with_id,
            validated_data=data,
        )

        assert updated.title == data["title"]
        assert updated.email == co_email1_co1_ws1_user1.email

    def test_full_update_updates_all_fields(
        self,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user1_context_with_id,
        co_email1_co1_ws1_user1_updated_valid_data,
    ):
        updated = CompanyEmailService.update(
            user=co_email1_co1_ws1_user1.company.workspace.owner,
            context=co_email1_co1_ws1_user1_context_with_id,
            validated_data=co_email1_co1_ws1_user1_updated_valid_data,
        )

        assert updated.title == co_email1_co1_ws1_user1_updated_valid_data["title"]
        assert updated.email == co_email1_co1_ws1_user1_updated_valid_data["email"]


# -----------------------------------
# REMOVE
# -----------------------------------

@pytest.mark.django_db
class TestCompanyEmailServiceRemove:

    def test_remove_resolves_company_email(
        self,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user1_context_with_id,
    ):
        with patch(
            "apps.companies.services.company_email_service.CompanyEmailService."
            "_resolve_company_email"
        ) as mock_resolve:

            mock_resolve.return_value = co_email1_co1_ws1_user1

            CompanyEmailService.remove(
                user=co_email1_co1_ws1_user1.company.workspace.owner,
                context=co_email1_co1_ws1_user1_context_with_id,
            )

            mock_resolve.assert_called_once()


# -----------------------------------
# RESOLVE
# -----------------------------------

@pytest.mark.django_db
class TestCompanyEmailServiceResolve:

    def test_returns_email_successfully(
        self,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user1_context_with_id,
    ):
        result = CompanyEmailService._resolve_company_email(
            user=co_email1_co1_ws1_user1.company.workspace.owner,
            context=co_email1_co1_ws1_user1_context_with_id,
        )

        assert result == co_email1_co1_ws1_user1

    def test_company_mismatch_raises_error(
        self,
        co_email1_co1_ws1_user1,
    ):
        with pytest.raises(DomainInvariantViolationError):
            CompanyEmailService._resolve_company_email(
                user=co_email1_co1_ws1_user1.company.workspace.owner,
                context=CompanyChildContext(
                    id=co_email1_co1_ws1_user1.id,
                    company_id=999999,
                    workspace_id=(
                        co_email1_co1_ws1_user1.company.workspace.workspace_id
                    ),
                ),
            )

    def test_workspace_mismatch_raises_error(
        self,
        co_email1_co1_ws1_user1,
    ):
        with pytest.raises(DomainInvariantViolationError):
            CompanyEmailService._resolve_company_email(
                user=co_email1_co1_ws1_user1.company.workspace.owner,
                context=CompanyChildContext(
                    id=co_email1_co1_ws1_user1.id,
                    company_id=co_email1_co1_ws1_user1.company.id,
                    workspace_id="wrong-workspace",
                ),
            )
