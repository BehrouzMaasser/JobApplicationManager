from unittest.mock import patch

import pytest
from django.core.exceptions import ValidationError

from apps.companies.models import CompanyEmail
from apps.companies.services.company_email_service import (
    CompanyEmailService,
)

from apps.core.common.contexts.contexts import (
    CompanyContext,
    CompanyChildContext,
)

from apps.core.exceptions.exceptions import (
    DomainInvariantViolationError,
)


pytestmark = pytest.mark.django_db


@pytest.fixture
def co_email1_co1_ws1_user1_valid_data():

    return {"title": "Title", "email": "email1@gmail.com"}


@pytest.fixture
def co_email1_co1_ws1_user1_updated_valid_data():

    return {"title": "Title Updated", "email": "updatedemail1@gmail.com"}


# ============================================================================
# Hooks
# ============================================================================

class TestResolveCreateDependencies:

    def test_resolves_company_dependency(
        self,
        co1_ws1_user1,
        co1_child_context_ws1_user1_no_id,
    ):

        dependencies = CompanyEmailService._resolve_create_dependencies(
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
            "apps.companies.services.company_email_service."
            "CompanyService._resolve_instance"
        ) as mock_resolve:

            mock_resolve.return_value = co1_ws1_user1

            CompanyEmailService._resolve_create_dependencies(
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

class TestCompanyEmailCreate:

    def test_create_creates_company_email(
        self,
        co1_ws1_user1,
        co1_child_context_ws1_user1_no_id,
        co_email1_co1_ws1_user1_valid_data,
    ):

        email = CompanyEmailService.create(
            user=co1_ws1_user1.workspace.owner,
            context=co1_child_context_ws1_user1_no_id,
            validated_data=co_email1_co1_ws1_user1_valid_data,
        )

        assert email.pk is not None
        assert email.company == co1_ws1_user1
        assert email.title == (
            co_email1_co1_ws1_user1_valid_data["title"]
        )
        assert email.email == (
            co_email1_co1_ws1_user1_valid_data["email"]
        )

    def test_create_delegates_model_validation(
        self,
        co1_ws1_user1,
        co1_child_context_ws1_user1_no_id,
        co_email1_co1_ws1_user1_valid_data,
    ):

        with patch(
            "apps.companies.models.CompanyEmail.full_clean"
        ) as mock_clean:

            CompanyEmailService.create(
                user=co1_ws1_user1.workspace.owner,
                context=co1_child_context_ws1_user1_no_id,
                validated_data=(
                    co_email1_co1_ws1_user1_valid_data
                ),
            )

            mock_clean.assert_called_once()

    def test_create_rejects_invalid_model_data(
        self,
        co1_ws1_user1,
        co1_child_context_ws1_user1_no_id,
    ):

        with pytest.raises(ValidationError):

            CompanyEmailService.create(
                user=co1_ws1_user1.workspace.owner,
                context=co1_child_context_ws1_user1_no_id,
                validated_data={
                    "title": None,
                    "email": "invalid-email",
                },
            )


# ============================================================================
# Update
# ============================================================================

class TestCompanyEmailUpdate:

    def test_update_changes_allowed_fields(
        self,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user1_context_with_id,
        co_email1_co1_ws1_user1_updated_valid_data,
    ):

        updated = CompanyEmailService.update(
            user=(
                co_email1_co1_ws1_user1
                .company
                .workspace
                .owner
            ),
            context=(
                co_email1_co1_ws1_user1_context_with_id
            ),
            validated_data=(
                co_email1_co1_ws1_user1_updated_valid_data
            ),
        )

        assert updated.title == (
            co_email1_co1_ws1_user1_updated_valid_data["title"]
        )

        assert updated.email == (
            co_email1_co1_ws1_user1_updated_valid_data["email"]
        )

    def test_update_allows_partial_update(
        self,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user1_context_with_id,
    ):

        old_email = co_email1_co1_ws1_user1.email

        updated = CompanyEmailService.update(
            user=(
                co_email1_co1_ws1_user1
                .company
                .workspace
                .owner
            ),
            context=(
                co_email1_co1_ws1_user1_context_with_id
            ),
            validated_data={
                "title": "Updated title",
            },
        )

        assert updated.title == "Updated title"
        assert updated.email == old_email

    def test_update_delegates_model_validation(
        self,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user1_context_with_id,
    ):

        with patch(
            "apps.companies.models.CompanyEmail.full_clean"
        ) as mock_clean:

            CompanyEmailService.update(
                user=(
                    co_email1_co1_ws1_user1
                    .company
                    .workspace
                    .owner
                ),
                context=(
                    co_email1_co1_ws1_user1_context_with_id
                ),
                validated_data={
                    "title": "Updated title",
                },
            )

            mock_clean.assert_called_once()


# ============================================================================
# Resolution
# ============================================================================

class TestCompanyEmailResolution:

    def test_selector_is_used(
        self,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user1_context_with_id,
    ):

        with patch(
            "apps.companies.services.company_email_service."
            "CompanyEmailSelector.get",
            return_value=co_email1_co1_ws1_user1,
        ) as mock_get:

            CompanyEmailService._resolve_instance(
                user=(
                    co_email1_co1_ws1_user1
                    .company
                    .workspace
                    .owner
                ),
                context=(
                    co_email1_co1_ws1_user1_context_with_id
                ),
            )

            mock_get.assert_called_once_with(
                user=(
                    co_email1_co1_ws1_user1
                    .company
                    .workspace
                    .owner
                ),
                obj_id=(
                    co_email1_co1_ws1_user1_context_with_id.id
                ),
            )


# ============================================================================
# Domain invariants
# ============================================================================

class TestValidateResolvedInstance:

    def test_matching_context_passes(
        self,
        co_email1_co1_ws1_user1,
    ):

        CompanyEmailService._validate_resolved_instance(
            instance=co_email1_co1_ws1_user1,
            context=CompanyChildContext(
                id=co_email1_co1_ws1_user1.id,
                company_id=(
                    co_email1_co1_ws1_user1.company.id
                ),
                workspace_id=(
                    co_email1_co1_ws1_user1
                    .company
                    .workspace
                    .workspace_id
                ),
            ),
        )

    def test_wrong_company_raises(
        self,
        co_email1_co1_ws1_user1,
    ):

        with pytest.raises(
            DomainInvariantViolationError
        ):

            CompanyEmailService._validate_resolved_instance(
                instance=co_email1_co1_ws1_user1,
                context=CompanyChildContext(
                    id=co_email1_co1_ws1_user1.id,
                    company_id=999999,
                    workspace_id=(
                        co_email1_co1_ws1_user1
                        .company
                        .workspace
                        .workspace_id
                    ),
                ),
            )

    def test_wrong_workspace_raises(
        self,
        co_email1_co1_ws1_user1,
    ):

        with pytest.raises(
            DomainInvariantViolationError
        ):

            CompanyEmailService._validate_resolved_instance(
                instance=co_email1_co1_ws1_user1,
                context=CompanyChildContext(
                    id=co_email1_co1_ws1_user1.id,
                    company_id=(
                        co_email1_co1_ws1_user1.company.id
                    ),
                    workspace_id="invalid-workspace",
                ),
            )


# ============================================================================
# Remove
# ============================================================================

class TestCompanyEmailRemove:

    def test_remove_deletes_company_email(
        self,
        co_email1_co1_ws1_user1,
        co_email1_co1_ws1_user1_context_with_id,
    ):

        email_id = co_email1_co1_ws1_user1.id

        CompanyEmailService.remove(
            user=(
                co_email1_co1_ws1_user1
                .company
                .workspace
                .owner
            ),
            context=(
                co_email1_co1_ws1_user1_context_with_id
            ),
        )

        with pytest.raises(CompanyEmail.DoesNotExist):

            CompanyEmail.objects.get(
                id=email_id
            )
