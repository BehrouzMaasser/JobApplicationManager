import pytest

from unittest.mock import patch

from rest_framework.exceptions import PermissionDenied, ValidationError

from apps.applications.services.application_service import JobApplicationService
from apps.applications.services.contexts.application_context import (
    JobApplicationContext
)

#   ----------------------------------- ****** -----------------------------------


# Creation:

@pytest.mark.django_db
def test_create_successfully_returns_job_application(
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
        job_application1_valid_data
):

    job_application = JobApplicationService.create(
        user=job_position1_co1_ws1_user1.company.workspace.owner,
        context=job_application_context_with_no_id,
        validated_data=job_application1_valid_data,
    )

    assert job_application.id is not None
    assert (job_application.owner ==
            job_position1_co1_ws1_user1.company.workspace.owner)

    assert (job_application.workspace.id ==
            job_position1_co1_ws1_user1.company.workspace.id)

    assert job_application.job_position.id == job_position1_co1_ws1_user1.id

    assert job_application.status == job_application1_valid_data["status"]

    if job_application1_valid_data.get("emails"):
        assert (list(job_application.emails.all()) ==
                job_application1_valid_data["emails"])

    if job_application1_valid_data.get("documents"):
        assert (list(job_application.documents.all()) ==
                job_application1_valid_data["documents"])


@pytest.mark.django_db
def test_create_calls_resolve_job_position(
        job_application_context_with_no_id,
        job_position1_co1_ws1_user1,
        job_application1_valid_data
):

    with patch(
            'apps.applications.services.application_service.JobApplicationService.'
            '_resolve_job_position',
    ) as mock_resolve_job_position:

        # Error due to fake job position
        with pytest.raises(PermissionDenied):
            JobApplicationService.create(
                user=job_position1_co1_ws1_user1.company.workspace.owner,
                context=job_application_context_with_no_id,
                validated_data=job_application1_valid_data,
            )

        mock_resolve_job_position.assert_called_once()


@pytest.mark.django_db
def test_create_calls_validate_emails_ownership_if_emails_given(
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
        job_application1_valid_data
):

    with patch(
            "apps.applications.services.application_service.JobApplicationService."
            "_validate_emails_ownership"
    ) as mock_validate_emails_ownership:

        JobApplicationService.create(
            user=job_position1_co1_ws1_user1.company.workspace.owner,
            context=job_application_context_with_no_id,
            validated_data=job_application1_valid_data,
        )

        if job_application1_valid_data.get("emails"):
            mock_validate_emails_ownership.assert_called_once()
        else:
            mock_validate_emails_ownership.assert_not_called()


@pytest.mark.django_db
def test_create_calls_validate_documents_ownership_if_documents_given(
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
        job_application1_valid_data
):

    with patch(
            "apps.applications.services.application_service.JobApplicationService."
            "_validate_documents_ownership"
    ) as mock_validate_documents_ownership:

        JobApplicationService.create(
            user=job_position1_co1_ws1_user1.company.workspace.owner,
            context=job_application_context_with_no_id,
            validated_data=job_application1_valid_data,
        )

        if job_application1_valid_data.get("documents"):
            mock_validate_documents_ownership.assert_called_once()
        else:
            mock_validate_documents_ownership.assert_not_called()


@pytest.mark.django_db
def test_create_calls_full_clean(
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
        job_application1_valid_data
):

    with patch(
            'apps.applications.models.JobApplication.full_clean'
    ) as mock_full_clean:

        JobApplicationService.create(
            user=job_position1_co1_ws1_user1.company.workspace.owner,
            context=job_application_context_with_no_id,
            validated_data=job_application1_valid_data,
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_create_calls_save(
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
        job_application1_valid_data
):

    with patch('apps.applications.models.JobApplication.save') as mock_save:

        # Error due to save not saving the instance and trying to assign m2m fields
        with pytest.raises(ValueError):

            JobApplicationService.create(
                user=job_position1_co1_ws1_user1.company.workspace.owner,
                context=job_application_context_with_no_id,
                validated_data=job_application1_valid_data,
            )

        mock_save.assert_called_once()


@pytest.mark.django_db
def test_create_calls_add_m2m_fields(
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
        job_application1_valid_data
):

    with patch(
            "apps.applications.services.application_service.JobApplicationService."
            "_add_m2m_fields"
    ) as mock_add_m2m_fields:

        JobApplicationService.create(
            user=job_position1_co1_ws1_user1.company.workspace.owner,
            context=job_application_context_with_no_id,
            validated_data=job_application1_valid_data,
        )

        mock_add_m2m_fields.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Updating

@pytest.mark.django_db
def test_update_successfully_returns_updated_job_application(
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated
):

    job_application = JobApplicationService.update(
        user=job_application1.owner,
        context=job_application1_context,
        validated_data=job_application1_valid_data_updated,
    )

    assert job_application.id == job_application1.id
    assert job_application.status == job_application1_valid_data_updated["status"]

    assert (list(job_application.emails.all()) ==
            job_application1_valid_data_updated["emails"])


@pytest.mark.django_db
def test_update_calls_resolve_job_application(
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated
):

    with patch(
            "apps.applications.services.application_service.JobApplicationService."
            "_resolve_job_application"
    ) as mock_resolve_job_application:

        # Fake job application leads to PermissionDeny when validating Emails
        with pytest.raises(PermissionDenied):
            JobApplicationService.update(
                user=job_application1.owner,
                context=job_application1_context,
                validated_data=job_application1_valid_data_updated,
            )

        mock_resolve_job_application.assert_called_once()


@pytest.mark.django_db
def test_update_calls_validate_emails_ownership_if_given(
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated
):

    with patch(
            "apps.applications.services.application_service.JobApplicationService."
            "_validate_emails_ownership"
    ) as mock_validate_emails_ownership:

        JobApplicationService.update(
            user=job_application1.owner,
            context=job_application1_context,
            validated_data=job_application1_valid_data_updated,
        )

        if job_application1_valid_data_updated.get("emails"):
            mock_validate_emails_ownership.assert_called_once()
        else:
            mock_validate_emails_ownership.assert_not_called()


@pytest.mark.django_db
def test_update_calls_validate_documents_ownership_if_given(
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated
):

    with patch(
            "apps.applications.services.application_service.JobApplicationService."
            "_validate_documents_ownership"
    ) as mock_validate_documents_ownership:

        JobApplicationService.update(
            user=job_application1.owner,
            context=job_application1_context,
            validated_data=job_application1_valid_data_updated,
        )

        mock_validate_documents_ownership.assert_called_once()


@pytest.mark.django_db
def test_update_calls_update_non_m2m_fields(
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated
):

    with patch(
            "apps.applications.services.application_service.JobApplicationService."
            "_update_non_m2m_fields"
    ) as mock_update_non_m2m_fields:

        # Error due to fake instance in update function
        JobApplicationService.update(
            user=job_application1.owner,
            context=job_application1_context,
            validated_data=job_application1_valid_data_updated,
        )

        mock_update_non_m2m_fields.assert_called_once()


@pytest.mark.django_db
def test_update_calls_update_m2m_fields(
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated
):

    with patch(
            "apps.applications.services.application_service.JobApplicationService."
            "_update_m2m_fields"
    ) as mock_update_m2m_fields:

        JobApplicationService.update(
            user=job_application1.owner,
            context=job_application1_context,
            validated_data=job_application1_valid_data_updated,
        )

        mock_update_m2m_fields.assert_called_once()


@pytest.mark.django_db
def test_update_calls_full_clean(
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated
):

    with patch(
            'apps.applications.models.JobApplication.full_clean'
    ) as mock_full_clean:

        JobApplicationService.update(
            user=job_application1.owner,
            context=job_application1_context,
            validated_data=job_application1_valid_data_updated,
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_update_calls_save(
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated
):

    with patch('apps.applications.models.JobApplication.save') as mock_save:

        JobApplicationService.update(
            user=job_application1.owner,
            context=job_application1_context,
            validated_data=job_application1_valid_data_updated,
        )

        mock_save.assert_called_once()


@pytest.mark.django_db
def test_update_dont_raise_error_if_a_required_m2m_field_is_missing(
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated
):

    # Missing Status do NOT raise
    job_application1_valid_data_updated.pop("status")

    JobApplicationService.update(
        user=job_application1.owner,
        context=job_application1_context,
        validated_data=job_application1_valid_data_updated,
    )

#   ----------------------------------- ****** -----------------------------------


# Test Deleting

@pytest.mark.django_db
def test_remove_calls_resolve_job_application(
        job_application1,
        job_application1_context,
):

    with patch(
            "apps.applications.services.application_service.JobApplicationService."
            "_resolve_job_application"
    ) as mock_resolve_job_application:

        JobApplicationService.remove(
            user=job_application1.owner,
            context=job_application1_context,
        )

        mock_resolve_job_application.assert_called_once()


#   ----------------------------------- ****** -----------------------------------

# Test Retrieving

@pytest.mark.django_db
def test_retrieve_job_application_calls_resolve_job_position(
        job_application1,
        job_application1_context,
):

    with patch(
            "apps.applications.services.application_service.JobApplicationService."
            "_resolve_job_position"
    ) as mock_resolve_job_position:

        JobApplicationService._resolve_job_application(
            user=job_application1.owner,
            context=job_application1_context,
        )

        mock_resolve_job_position.assert_called_once()


@pytest.mark.django_db
def test_access_to_job_application_from_another_job_position_raises_error(
        job_application1, job_application1_context, job_position2_co1_ws1_user1
):

    # Accessing Job Application 1 from another Job Position raises Error
    with pytest.raises(ValidationError):
        JobApplicationService._resolve_job_application(
            user=job_application1.owner,
            context=JobApplicationContext(
                id=job_application1.id,
                workspace_id=job_application1.workspace.workspace_id,
                company_id=job_application1.job_position.company.id,
                job_position_id=job_position2_co1_ws1_user1.id,
            ),
        )

#   ----------------------------------- ****** -----------------------------------
