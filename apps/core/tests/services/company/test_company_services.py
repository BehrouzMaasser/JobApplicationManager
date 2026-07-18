from unittest.mock import patch

import pytest

from django.core.exceptions import ValidationError

from apps.companies.models import Company
from apps.companies.services.company_service import CompanyService

from apps.core.common.contexts.contexts import (
    CompanyContext,
    WorkspaceContext,
)

from apps.core.exceptions.exceptions import (
    DomainInvariantViolationError,
)


pytestmark = pytest.mark.django_db


@pytest.fixture
def co1_ws1_user1_valid_data():

    return {"name": "Company 1", "website": "https://www.google.com"}


@pytest.fixture
def co1_ws1_user1_updated_valid_data():

    return {"name": "Company 1 Updated", "website": "https://www.updatedgoogle.com"}


# ============================================================================
# Hooks
# ============================================================================

class TestCompanyServiceHooks:

    def test_resolve_create_dependencies_resolves_workspace(
        self,
        workspace1_user1,
        co1_ws1_user1_context_no_id,
    ):

        dependencies = CompanyService._resolve_create_dependencies(
            user=workspace1_user1.owner,
            context=co1_ws1_user1_context_no_id,
        )

        assert dependencies == {
            "workspace": workspace1_user1,
        }

    def test_resolve_create_dependencies_uses_workspace_service(
        self,
        workspace1_user1,
        co1_ws1_user1_context_no_id,
    ):

        with patch(
            "apps.companies.services.company_service."
            "WorkspaceService._resolve_instance"
        ) as mock_resolve:

            mock_resolve.return_value = workspace1_user1

            CompanyService._resolve_create_dependencies(
                user=workspace1_user1.owner,
                context=co1_ws1_user1_context_no_id,
            )

            mock_resolve.assert_called_once_with(
                user=workspace1_user1.owner,
                context=WorkspaceContext(
                    id=(
                        co1_ws1_user1_context_no_id
                        .workspace_id
                    )
                ),
            )


# ============================================================================
# Create
# ============================================================================

class TestCompanyCreate:

    def test_create_returns_company(
        self,
        workspace1_user1,
        co1_ws1_user1_context_no_id,
        co1_ws1_user1_valid_data,
    ):

        company = CompanyService.create(
            user=workspace1_user1.owner,
            context=co1_ws1_user1_context_no_id,
            validated_data=co1_ws1_user1_valid_data,
        )

        assert company.id is not None
        assert company.workspace == workspace1_user1
        assert company.name == (
            co1_ws1_user1_valid_data["name"]
        )
        assert company.website == (
            co1_ws1_user1_valid_data["website"]
        )

    def test_create_calls_model_validation(
        self,
        workspace1_user1,
        co1_ws1_user1_context_no_id,
        co1_ws1_user1_valid_data,
    ):

        with patch.object(
            Company,
            "full_clean",
        ) as mock_clean:

            CompanyService.create(
                user=workspace1_user1.owner,
                context=co1_ws1_user1_context_no_id,
                validated_data=co1_ws1_user1_valid_data,
            )

            mock_clean.assert_called_once()

    def test_create_rejects_invalid_model_data(
        self,
        workspace1_user1,
        co1_ws1_user1_context_no_id,
    ):

        with pytest.raises(
            ValidationError
        ):

            CompanyService.create(
                user=workspace1_user1.owner,
                context=co1_ws1_user1_context_no_id,
                validated_data={
                    "name": None,
                    "website": "invalid",
                },
            )

    def test_create_requires_accessible_workspace(
        self,
        user1,
        workspace2_user2,
        co1_ws1_user1_valid_data,
    ):

        with pytest.raises(Exception):

            CompanyService.create(
                user=user1,
                context=CompanyContext(
                    workspace_id=(
                        workspace2_user2.workspace_id
                    )
                ),
                validated_data=co1_ws1_user1_valid_data,
            )


# ============================================================================
# Update
# ============================================================================

class TestCompanyUpdate:

    def test_update_changes_scalar_fields(
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

        assert updated.id == co1_ws1_user1.id
        assert updated.name == (
            co1_ws1_user1_updated_valid_data["name"]
        )
        assert updated.website == (
            co1_ws1_user1_updated_valid_data["website"]
        )

    def test_partial_update_keeps_missing_fields(
        self,
        co1_ws1_user1,
        co1_ws1_user1_context_with_id,
        co1_ws1_user1_updated_valid_data,
    ):

        data = (
            co1_ws1_user1_updated_valid_data.copy()
        )

        data.pop("website")

        updated = CompanyService.update(
            user=co1_ws1_user1.workspace.owner,
            context=co1_ws1_user1_context_with_id,
            validated_data=data,
        )

        assert updated.name == data["name"]
        assert updated.website == (
            co1_ws1_user1.website
        )

    def test_update_calls_model_validation(
        self,
        co1_ws1_user1,
        co1_ws1_user1_context_with_id,
    ):

        with patch.object(
            Company,
            "full_clean",
        ) as mock_clean:

            CompanyService.update(
                user=co1_ws1_user1.workspace.owner,
                context=co1_ws1_user1_context_with_id,
                validated_data={
                    "name": "Updated name",
                },
            )

            mock_clean.assert_called_once()

    def test_update_rejects_workspace_mismatch(
        self,
        co1_ws1_user1,
        workspace2_user2,
    ):

        with pytest.raises(
            DomainInvariantViolationError
        ):

            CompanyService.update(
                user=co1_ws1_user1.workspace.owner,
                context=CompanyContext(
                    id=co1_ws1_user1.id,
                    workspace_id=(
                        workspace2_user2.workspace_id
                    ),
                ),
                validated_data={
                    "name": "Invalid update",
                },
            )


# ============================================================================
# Remove
# ============================================================================

class TestCompanyRemove:

    def test_remove_deletes_company(
        self,
        co1_ws1_user1,
        co1_ws1_user1_context_with_id,
    ):

        company_id = co1_ws1_user1.id

        CompanyService.remove(
            user=co1_ws1_user1.workspace.owner,
            context=co1_ws1_user1_context_with_id,
        )

        assert not Company.objects.filter(
            id=company_id,
        ).exists()

    def test_remove_rejects_workspace_mismatch(
        self,
        co1_ws1_user1,
        workspace2_user2,
    ):

        with pytest.raises(
            DomainInvariantViolationError
        ):

            CompanyService.remove(
                user=co1_ws1_user1.workspace.owner,
                context=CompanyContext(
                    id=co1_ws1_user1.id,
                    workspace_id=(
                        workspace2_user2.workspace_id
                    ),
                ),
            )


# ============================================================================
# Resolution
# ============================================================================

class TestCompanyResolution:

    def test_selector_is_used(
        self,
        co1_ws1_user1,
        co1_ws1_user1_context_with_id,
    ):

        with patch.object(
            CompanyService.SELECTOR,
            "get",
            return_value=co1_ws1_user1,
        ) as mock_get:

            CompanyService._resolve_instance(
                user=co1_ws1_user1.workspace.owner,
                context=co1_ws1_user1_context_with_id,
            )

            mock_get.assert_called_once_with(
                user=co1_ws1_user1.workspace.owner,
                obj_id=(
                    co1_ws1_user1_context_with_id.id
                ),
            )


# ============================================================================
# Domain invariants
# ============================================================================

class TestValidateResolvedInstance:

    def test_workspace_mismatch_raises(
        self,
        co1_ws1_user1,
    ):

        context = CompanyContext(
            id=co1_ws1_user1.id,
            workspace_id="different-workspace-id",
        )

        with pytest.raises(
            DomainInvariantViolationError
        ):

            CompanyService._validate_resolved_instance(
                instance=co1_ws1_user1,
                context=context,
            )

    def test_matching_workspace_passes(
        self,
        co1_ws1_user1,
    ):

        context = CompanyContext(
            id=co1_ws1_user1.id,
            workspace_id=(
                co1_ws1_user1.workspace.workspace_id
            ),
        )

        CompanyService._validate_resolved_instance(
            instance=co1_ws1_user1,
            context=context,
        )
