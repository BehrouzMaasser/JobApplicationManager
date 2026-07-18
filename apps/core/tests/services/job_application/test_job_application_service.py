from unittest.mock import patch

import pytest

from apps.applications.models import JobApplication
from apps.applications.services.application_service import (
    JobApplicationService,
)
from apps.core.common.contexts.contexts import (
    CompanyChildContext,
)
from apps.core.exceptions.exceptions import (
    BusinessRuleViolationError,
    DomainInvariantViolationError,
)


pytestmark = pytest.mark.django_db


# ============================================================================
# Dependency resolution
# ============================================================================

class TestResolveCreateDependencies:

    def test_resolves_dependencies(
        self,
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
    ):

        dependencies = (
            JobApplicationService._resolve_create_dependencies(
                user=job_position1_co1_ws1_user1.company.workspace.owner,
                context=job_application_context_with_no_id,
            )
        )

        assert dependencies["owner"] == (
            job_position1_co1_ws1_user1.company.workspace.owner
        )

        assert dependencies["workspace"] == (
            job_position1_co1_ws1_user1.company.workspace
        )

        assert dependencies["job_position"] == (
            job_position1_co1_ws1_user1
        )


    def test_resolves_job_position_through_service(
        self,
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
    ):

        with patch(
            "apps.applications.services.application_service."
            "JobPositionService._resolve_instance"
        ) as mock:

            mock.return_value = job_position1_co1_ws1_user1

            JobApplicationService._resolve_create_dependencies(
                user=job_position1_co1_ws1_user1.company.workspace.owner,
                context=job_application_context_with_no_id,
            )

            mock.assert_called_once_with(
                user=job_position1_co1_ws1_user1.company.workspace.owner,
                context=CompanyChildContext(
                    id=(
                        job_application_context_with_no_id
                        .job_position_id
                    ),
                    workspace_id=(
                        job_application_context_with_no_id
                        .workspace_id
                    ),
                    company_id=(
                        job_application_context_with_no_id
                        .company_id
                    ),
                ),
            )


# ============================================================================
# Create
# ============================================================================

class TestJobApplicationCreate:

    def test_create_returns_application(
        self,
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
        job_application1_valid_data,
    ):

        application = JobApplicationService.create(
            user=job_position1_co1_ws1_user1.company.workspace.owner,
            context=job_application_context_with_no_id,
            validated_data=job_application1_valid_data,
        )

        assert application.owner == (
            job_position1_co1_ws1_user1.company.workspace.owner
        )

        assert application.workspace == (
            job_position1_co1_ws1_user1.company.workspace
        )

        assert application.job_position == (
            job_position1_co1_ws1_user1
        )

        assert application.status == (
            job_application1_valid_data["status"]
        )


# ============================================================================
# Update
# ============================================================================

class TestJobApplicationUpdate:

    def test_update_changes_fields(
        self,
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated,
    ):

        updated = JobApplicationService.update(
            user=job_application1.owner,
            context=job_application1_context,
            validated_data=job_application1_valid_data_updated,
        )

        assert updated.id == job_application1.id

        assert updated.status == (
            job_application1_valid_data_updated["status"]
        )


    def test_update_allows_partial_update(
        self,
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated,
    ):

        data = job_application1_valid_data_updated.copy()

        data.pop("status")

        updated = JobApplicationService.update(
            user=job_application1.owner,
            context=job_application1_context,
            validated_data=data,
        )

        assert updated.id == job_application1.id


# ============================================================================
# Domain invariants
# ============================================================================

class TestValidateResolvedInstance:

    def test_wrong_job_position_raises(
        self,
        job_application1,
        job_position2_co1_ws1_user1,
    ):

        with pytest.raises(DomainInvariantViolationError):

            JobApplicationService._validate_resolved_instance(
                instance=job_application1,
                context=type(
                    "Context",
                    (),
                    {
                        "id": job_application1.id,
                        "workspace_id": (
                            job_application1.workspace.workspace_id
                        ),
                        "company_id": (
                            job_application1.job_position.company.id
                        ),
                        "job_position_id": (
                            job_position2_co1_ws1_user1.id
                        ),
                    },
                )(),
            )


    def test_wrong_company_raises(
        self,
        job_application1,
    ):

        with pytest.raises(DomainInvariantViolationError):

            JobApplicationService._validate_resolved_instance(
                instance=job_application1,
                context=type(
                    "Context",
                    (),
                    {
                        "id": job_application1.id,
                        "workspace_id": (
                            job_application1.workspace.workspace_id
                        ),
                        "company_id": 999999,
                        "job_position_id": (
                            job_application1.job_position.id
                        ),
                    },
                )(),
            )


    def test_wrong_workspace_raises(
        self,
        job_application1,
    ):

        with pytest.raises(DomainInvariantViolationError):

            JobApplicationService._validate_resolved_instance(
                instance=job_application1,
                context=type(
                    "Context",
                    (),
                    {
                        "id": job_application1.id,
                        "workspace_id": "invalid",
                        "company_id": (
                            job_application1.job_position.company.id
                        ),
                        "job_position_id": (
                            job_application1.job_position.id
                        ),
                    },
                )(),
            )


# ============================================================================
# Email ownership
# ============================================================================

class TestValidateEmailsOwnership:

    def test_accepts_valid_emails(
        self,
        user1,
        co_email1_co1_ws1_user1,
        job_position1_co1_ws1_user1,
    ):

        JobApplicationService._validate_emails_ownership(
            user=user1,
            emails=[co_email1_co1_ws1_user1],
            job_position=job_position1_co1_ws1_user1,
        )


    def test_rejects_wrong_company(
        self,
        user1,
        co_email1_co1_ws1_user1,
        job_position1_co2_ws1_user1,
    ):

        with pytest.raises(BusinessRuleViolationError):

            JobApplicationService._validate_emails_ownership(
                user=user1,
                emails=[co_email1_co1_ws1_user1],
                job_position=job_position1_co2_ws1_user1,
            )


    def test_rejects_other_user_email(
        self,
        user1,
        job_position1_co1_ws1_user1,
        co_email1_co1_ws1_user2,
    ):

        with pytest.raises(BusinessRuleViolationError):

            JobApplicationService._validate_emails_ownership(
                user=user1,
                emails=[co_email1_co1_ws1_user2],
                job_position=job_position1_co1_ws1_user1,
            )


# ============================================================================
# Document ownership
# ============================================================================

class TestValidateDocumentsOwnership:

    def test_accepts_empty_documents(
        self,
        user1,
    ):

        JobApplicationService._validate_documents_ownership(
            user=user1,
            documents=[],
        )


    def test_accepts_owned_documents(
        self,
        user1,
        doc1_user1,
    ):

        JobApplicationService._validate_documents_ownership(
            user=user1,
            documents=[doc1_user1],
        )


    def test_rejects_foreign_documents(
        self,
        user1,
        doc1_user2,
    ):

        with pytest.raises(BusinessRuleViolationError):

            JobApplicationService._validate_documents_ownership(
                user=user1,
                documents=[doc1_user2],
            )


# ============================================================================
# Remove
# ============================================================================

class TestJobApplicationRemove:

    def test_remove_deletes_application(
        self,
        job_application1,
        job_application1_context,
    ):

        application_id = job_application1.id

        JobApplicationService.remove(
            user=job_application1.owner,
            context=job_application1_context,
        )

        assert not JobApplication.objects.filter(
            id=application_id
        ).exists()
