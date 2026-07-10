from unittest.mock import patch

import pytest

from apps.applications.services.application_service import (
    JobApplicationService,
)
from apps.applications.services.contexts.application_context import (
    JobApplicationContext,
)

from apps.core.exceptions.exceptions import (
    DomainInvariantViolationError,
)


pytestmark = pytest.mark.django_db


# =========================================================
# Create
# =========================================================

class TestJobApplicationServiceCreate:

    def test_successfully_returns_job_application(
        self,
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
        job_application1_valid_data,
    ):

        job_application = JobApplicationService.create(
            user=job_position1_co1_ws1_user1.company.workspace.owner,
            context=job_application_context_with_no_id,
            validated_data=job_application1_valid_data,
        )

        assert job_application.id is not None
        assert (
            job_application.owner
            == job_position1_co1_ws1_user1.company.workspace.owner
        )
        assert (
            job_application.workspace
            == job_position1_co1_ws1_user1.company.workspace
        )
        assert job_application.job_position == job_position1_co1_ws1_user1
        assert job_application.status == job_application1_valid_data["status"]

    def test_calls_resolve_job_position(
        self,
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
        job_application1_valid_data,
    ):

        with patch(
            "apps.applications.services.application_service."
            "JobApplicationService._resolve_job_position"
        ) as mock_resolve:

            mock_resolve.return_value = job_position1_co1_ws1_user1

            JobApplicationService.create(
                user=job_position1_co1_ws1_user1.company.workspace.owner,
                context=job_application_context_with_no_id,
                validated_data=job_application1_valid_data,
            )

            mock_resolve.assert_called_once()

    def test_calls_validate_emails_ownership_when_emails_given(
        self,
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
        job_application1_valid_data,
    ):

        with patch(
            "apps.applications.services.application_service."
            "JobApplicationService._validate_emails_ownership"
        ) as mock_validate:

            JobApplicationService.create(
                user=job_position1_co1_ws1_user1.company.workspace.owner,
                context=job_application_context_with_no_id,
                validated_data=job_application1_valid_data,
            )

            if job_application1_valid_data.get("emails"):
                mock_validate.assert_called_once()
            else:
                mock_validate.assert_not_called()

    def test_calls_validate_documents_ownership_when_documents_given(
        self,
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
        job_application1_valid_data,
    ):

        with patch(
            "apps.applications.services.application_service."
            "JobApplicationService._validate_documents_ownership"
        ) as mock_validate:

            JobApplicationService.create(
                user=job_position1_co1_ws1_user1.company.workspace.owner,
                context=job_application_context_with_no_id,
                validated_data=job_application1_valid_data,
            )

            if job_application1_valid_data.get("documents"):
                mock_validate.assert_called_once()
            else:
                mock_validate.assert_not_called()

    def test_calls_full_clean(
        self,
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
        job_application1_valid_data,
    ):

        with patch(
            "apps.applications.models.JobApplication.full_clean"
        ) as mock_full_clean:

            JobApplicationService.create(
                user=job_position1_co1_ws1_user1.company.workspace.owner,
                context=job_application_context_with_no_id,
                validated_data=job_application1_valid_data,
            )

            mock_full_clean.assert_called_once()

    def test_calls_save(
        self,
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
        job_application1_valid_data,
    ):

        with patch(
            "apps.applications.models.JobApplication.save"
        ) as mock_save:

            with pytest.raises(ValueError):
                JobApplicationService.create(
                    user=job_position1_co1_ws1_user1.company.workspace.owner,
                    context=job_application_context_with_no_id,
                    validated_data=job_application1_valid_data,
                )

            mock_save.assert_called_once()

    def test_calls_add_m2m_fields(
        self,
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
        job_application1_valid_data,
    ):

        with patch(
            "apps.applications.services.application_service."
            "JobApplicationService._add_m2m_fields"
        ) as mock_add_m2m:

            JobApplicationService.create(
                user=job_position1_co1_ws1_user1.company.workspace.owner,
                context=job_application_context_with_no_id,
                validated_data=job_application1_valid_data,
            )

            mock_add_m2m.assert_called_once()


# =========================================================
# Update
# =========================================================

class TestJobApplicationServiceUpdate:

    def test_successfully_updates_job_application(
        self,
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated,
    ):

        application = JobApplicationService.update(
            user=job_application1.owner,
            context=job_application1_context,
            validated_data=job_application1_valid_data_updated,
        )

        assert application.id == job_application1.id
        assert (
            application.status
            == job_application1_valid_data_updated["status"]
        )

    def test_calls_resolve_job_application(
        self,
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated,
    ):

        with patch(
            "apps.applications.services.application_service."
            "JobApplicationService._resolve_job_application"
        ) as mock_resolve:

            mock_resolve.return_value = job_application1

            JobApplicationService.update(
                user=job_application1.owner,
                context=job_application1_context,
                validated_data=job_application1_valid_data_updated,
            )

            mock_resolve.assert_called_once()

    def test_calls_validate_emails_ownership(
        self,
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated,
    ):

        with patch(
            "apps.applications.services.application_service."
            "JobApplicationService._validate_emails_ownership"
        ) as mock_validate:

            JobApplicationService.update(
                user=job_application1.owner,
                context=job_application1_context,
                validated_data=job_application1_valid_data_updated,
            )

            mock_validate.assert_called_once()

    def test_calls_validate_documents_ownership(
        self,
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated,
    ):

        with patch(
            "apps.applications.services.application_service."
            "JobApplicationService._validate_documents_ownership"
        ) as mock_validate:

            JobApplicationService.update(
                user=job_application1.owner,
                context=job_application1_context,
                validated_data=job_application1_valid_data_updated,
            )

            mock_validate.assert_called_once()

    def test_calls_update_non_m2m_fields(
        self,
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated,
    ):

        with patch(
            "apps.applications.services.application_service."
            "JobApplicationService._update_non_m2m_fields"
        ) as mock_update:

            JobApplicationService.update(
                user=job_application1.owner,
                context=job_application1_context,
                validated_data=job_application1_valid_data_updated,
            )

            mock_update.assert_called_once()

    def test_calls_update_m2m_fields(
        self,
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated,
    ):

        with patch(
            "apps.applications.services.application_service."
            "JobApplicationService._update_m2m_fields"
        ) as mock_update:

            JobApplicationService.update(
                user=job_application1.owner,
                context=job_application1_context,
                validated_data=job_application1_valid_data_updated,
            )

            mock_update.assert_called_once()

    def test_calls_full_clean(
        self,
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated,
    ):

        with patch(
            "apps.applications.models.JobApplication.full_clean"
        ) as mock_full_clean:

            JobApplicationService.update(
                user=job_application1.owner,
                context=job_application1_context,
                validated_data=job_application1_valid_data_updated,
            )

            mock_full_clean.assert_called_once()

    def test_calls_save(
        self,
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated,
    ):

        with patch(
            "apps.applications.models.JobApplication.save"
        ) as mock_save:

            JobApplicationService.update(
                user=job_application1.owner,
                context=job_application1_context,
                validated_data=job_application1_valid_data_updated,
            )

            mock_save.assert_called_once()

    def test_allows_missing_status(
        self,
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated,
    ):

        job_application1_valid_data_updated.pop("status")

        JobApplicationService.update(
            user=job_application1.owner,
            context=job_application1_context,
            validated_data=job_application1_valid_data_updated,
        )


# =========================================================
# Remove
# =========================================================

class TestJobApplicationServiceRemove:

    def test_calls_resolve_job_application(
        self,
        job_application1,
        job_application1_context,
    ):

        with patch(
            "apps.applications.services.application_service."
            "JobApplicationService._resolve_job_application"
        ) as mock_resolve:

            mock_resolve.return_value = job_application1

            JobApplicationService.remove(
                user=job_application1.owner,
                context=job_application1_context,
            )

            mock_resolve.assert_called_once()

    def test_calls_delete(
        self,
        job_application1,
        job_application1_context,
    ):

        with patch(
            "apps.applications.models.JobApplication.delete"
        ) as mock_delete:

            JobApplicationService.remove(
                user=job_application1.owner,
                context=job_application1_context,
            )

            mock_delete.assert_called_once()


# =========================================================
# Resolve / Domain Rules
# =========================================================

class TestJobApplicationServiceResolve:

    def test_wrong_job_position_raises_error(
        self,
        job_application1,
        job_position2_co1_ws1_user1,
    ):

        with pytest.raises(DomainInvariantViolationError):

            JobApplicationService._resolve_job_application(
                user=job_application1.owner,
                context=JobApplicationContext(
                    id=job_application1.id,
                    workspace_id=job_application1.workspace.id,
                    company_id=job_application1.job_position.company.id,
                    job_position_id=job_position2_co1_ws1_user1.id,
                ),
            )

    def test_wrong_workspace_raises_error(
        self,
        job_application1,
    ):

        with pytest.raises(DomainInvariantViolationError):

            JobApplicationService._resolve_job_application(
                user=job_application1.owner,
                context=JobApplicationContext(
                    id=job_application1.id,
                    workspace_id=999999,
                    company_id=job_application1.job_position.company.id,
                    job_position_id=job_application1.job_position.id,
                ),
            )
