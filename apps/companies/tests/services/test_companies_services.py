import pytest
from unittest.mock import patch

from apps.companies.services.company_service import CompanyService

from apps.core.exceptions.exceptions import DomainInvariantViolationError


# -----------------------------------
# CREATE
# -----------------------------------

@pytest.mark.django_db
class TestCompanyServiceCreate:

    def test_create_resolves_workspace(
            self,
            workspace1_user1,
            co1_ws1_user1_context_with_id,
            co1_ws1_user1_valid_data
    ):

        with patch(
            "apps.companies.services.company_service.CompanyService."
            "_resolve_workspace",
            return_value=workspace1_user1
        ) as mock_resolve:

            CompanyService.create(
                user=workspace1_user1.owner,
                context=co1_ws1_user1_context_with_id,
                validated_data=co1_ws1_user1_valid_data,
            )

            mock_resolve.assert_called_once()

    def test_create_calls_model_methods(
            self,
            workspace1_user1,
            co1_ws1_user1_context_with_id,
            co1_ws1_user1_valid_data
    ):

        with patch("apps.companies.models.Company.full_clean") as mock_clean, \
             patch("apps.companies.models.Company.save") as mock_save, \
             patch(
                 "apps.companies.services.company_service.CompanyService."
                 "_resolve_workspace",
                 return_value=workspace1_user1
             ):

            CompanyService.create(
                user=workspace1_user1.owner,
                context=co1_ws1_user1_context_with_id,
                validated_data=co1_ws1_user1_valid_data,
            )

            mock_clean.assert_called_once()
            mock_save.assert_called_once()


# -----------------------------------
# UPDATE
# -----------------------------------

@pytest.mark.django_db
class TestCompanyServiceUpdate:

    def test_update_resolves_company(
            self,
            co1_ws1_user1,
            co1_ws1_user1_context_with_id,
            co1_ws1_user1_updated_valid_data
    ):

        with patch(
            "apps.companies.services.company_service.CompanyService._resolve_company"
        ) as mock_resolve:

            mock_resolve.return_value = co1_ws1_user1

            CompanyService.update(
                user=co1_ws1_user1.workspace.owner,
                context=co1_ws1_user1_context_with_id,
                validated_data=co1_ws1_user1_updated_valid_data,
            )

            mock_resolve.assert_called_once()

    def test_update_calls_update_non_m2m_fields(
            self,
            co1_ws1_user1,
            co1_ws1_user1_context_with_id,
            co1_ws1_user1_updated_valid_data
    ):

        with patch(
            "apps.companies.services.company_service.CompanyService."
            "_update_non_m2m_fields"
        ) as mock_update, \
             patch(
                 "apps.companies.services.company_service.CompanyService."
                 "_resolve_company",
                 return_value=co1_ws1_user1
             ):

            CompanyService.update(
                user=co1_ws1_user1.workspace.owner,
                context=co1_ws1_user1_context_with_id,
                validated_data=co1_ws1_user1_updated_valid_data,
            )

            mock_update.assert_called_once()

    def test_partial_update_does_not_override_missing_fields(
        self,
        co1_ws1_user1,
        co1_ws1_user1_context_with_id,
        co1_ws1_user1_updated_valid_data,
    ):
        data = co1_ws1_user1_updated_valid_data.copy()
        data.pop("website")

        updated = CompanyService.update(
            user=co1_ws1_user1.workspace.owner,
            context=co1_ws1_user1_context_with_id,
            validated_data=data,
        )

        assert updated.name == data["name"]
        assert updated.website == co1_ws1_user1.website

    def test_full_update_updates_all_fields(
        self,
        co1_ws1_user1,
        co1_ws1_user1_context_with_id,
        co1_ws1_user1_updated_valid_data,
    ):
        updated = CompanyService.update(
            user=co1_ws1_user1.workspace.owner,
            context=co1_ws1_user1_context_with_id,
            validated_data=co1_ws1_user1_updated_valid_data,
        )

        assert updated.name == co1_ws1_user1_updated_valid_data["name"]
        assert updated.website == co1_ws1_user1_updated_valid_data["website"]


# -----------------------------------
# REMOVE
# -----------------------------------

@pytest.mark.django_db
class TestCompanyServiceRemove:

    def test_remove_resolves_company(
            self, co1_ws1_user1, co1_ws1_user1_context_with_id
    ):

        with patch(
            "apps.companies.services.company_service.CompanyService._resolve_company"
        ) as mock_resolve:

            mock_resolve.return_value = co1_ws1_user1

            CompanyService.remove(
                user=co1_ws1_user1.workspace.owner,
                context=co1_ws1_user1_context_with_id,
            )

            mock_resolve.assert_called_once()


# -----------------------------------
# RESOLVE COMPANY
# -----------------------------------

@pytest.mark.django_db
class TestCompanyServiceResolveCompany:

    def test_returns_company_successfully(
            self, co1_ws1_user1, co1_ws1_user1_context_with_id
    ):

        result = CompanyService._resolve_company(
            user=co1_ws1_user1.workspace.owner,
            workspace_id=co1_ws1_user1.workspace.workspace_id,
            company_id=co1_ws1_user1.id,
        )

        assert result == co1_ws1_user1

    def test_workspace_mismatch_raises_domain_error(self, co1_ws1_user1):

        with pytest.raises(DomainInvariantViolationError):
            CompanyService._resolve_company(
                user=co1_ws1_user1.workspace.owner,
                workspace_id="different-workspace-id",
                company_id=co1_ws1_user1.id,
            )

    def test_selector_is_used(self, co1_ws1_user1):

        with patch(
            "apps.companies.services.company_service.CompanySelector.get",
            return_value=co1_ws1_user1
        ) as mock_get:

            CompanyService._resolve_company(
                user=co1_ws1_user1.workspace.owner,
                workspace_id=co1_ws1_user1.workspace.workspace_id,
                company_id=co1_ws1_user1.id,
            )

            mock_get.assert_called_once()
