import pytest

from unittest.mock import patch

from django.core.exceptions import ValidationError

from apps.applications.services.application_service import JobApplicationService
from apps.applications.services.contexts.application_context import (
    JobApplicationContext
)

#   ----------------------------------- ****** -----------------------------------


# Creation:

@pytest.mark.django_db
def test_create_job_application_successfully_returns_job_application(
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
        job_application1_valid_data
):

    job_application = JobApplicationService.create(
        user=job_position1_co1_ws1_user1.company.workspace.owner,
        context=job_application_context_with_no_id,
        validated_data=job_application1_valid_data,
    )

    assert (job_application.owner ==
            job_position1_co1_ws1_user1.company.workspace.owner)

    assert job_application.workspace == job_position1_co1_ws1_user1.company.workspace
    assert job_application.job_position.id == job_position1_co1_ws1_user1.id

    assert job_application.status == job_application1_valid_data["status"]

    assert (list(job_application.emails.all()) ==
            job_application1_valid_data["emails"])


@pytest.mark.django_db
def test_create_job_application_calls_resolve_job_position(
        job_application_context_with_no_id,
        job_position1_co1_ws1_user1,
        job_application1_valid_data
):

    with patch(
            'apps.applications.services.application_service.JobApplicationService.'
            '_resolve_job_position',
    ) as mock_resolve_job_position:

        # Error due to fake job position
        with pytest.raises(ValidationError):
            JobApplicationService.create(
                user=job_position1_co1_ws1_user1.company.workspace.owner,
                context=job_application_context_with_no_id,
                validated_data=job_application1_valid_data,
            )

        mock_resolve_job_position.assert_called_once()


@pytest.mark.django_db
def test_create_job_application_calls_validate_emails_ownership(
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

        mock_validate_emails_ownership.assert_called_once()


@pytest.mark.django_db
def test_create_job_application_calls_validate_documents_ownership(
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

        mock_validate_documents_ownership.assert_called_once()


@pytest.mark.django_db
def test_create_job_application_calls_full_clean(
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
def test_create_job_application_calls_save(
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
        job_application1_valid_data
):

    with patch('apps.applications.models.JobApplication.save') as mock_save:

        # Error due to save not saving the instance
        with pytest.raises(ValidationError):

            JobApplicationService.create(
                user=job_position1_co1_ws1_user1.company.workspace.owner,
                context=job_application_context_with_no_id,
                validated_data=job_application1_valid_data,
            )

        mock_save.assert_called_once()


@pytest.mark.django_db
def test_create_job_application_calls_add_m2m_fields(
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
        job_application1_valid_data
):

    with patch(
            "apps.applications.services.application_service.JobApplicationService."
            "_add_m2m_fields"
    ) as mock_add_m2m_fields:

        # Validation error on empty Email field, because add function is fake
        with pytest.raises(ValidationError):
            JobApplicationService.create(
                user=job_position1_co1_ws1_user1.company.workspace.owner,
                context=job_application_context_with_no_id,
                validated_data=job_application1_valid_data,
            )

        mock_add_m2m_fields.assert_called_once()


@pytest.mark.django_db
def test_create_job_application_calls_m2m_non_empty_validation(
        job_position1_co1_ws1_user1,
        job_application_context_with_no_id,
        job_application1_valid_data
):

    with patch(
            "apps.applications.services.application_service.JobApplicationService."
            "_m2m_non_empty_validation"
    ) as mock_m2m_non_empty_validation:

        JobApplicationService.create(
            user=job_position1_co1_ws1_user1.company.workspace.owner,
            context=job_application_context_with_no_id,
            validated_data=job_application1_valid_data,
        )

        mock_m2m_non_empty_validation.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Updating

@pytest.mark.django_db
def test_update_job_application_successfully_returns_job_application(
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated
):

    job_application = JobApplicationService.update(
        user=job_application1.owner,
        context=job_application1_context,
        validated_data=job_application1_valid_data_updated,
    )

    assert job_application.owner == job_application1.owner

    assert job_application.workspace == job_application1.workspace
    assert job_application.job_position.id == job_application1.job_position.id

    assert job_application.status == job_application1_valid_data_updated["status"]

    assert (list(job_application.emails.all()) ==
            job_application1_valid_data_updated["emails"])


@pytest.mark.django_db
def test_update_job_application_calls_resolve_job_application(
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated
):

    with patch(
            "apps.applications.services.application_service.JobApplicationService."
            "_resolve_job_application"
    ) as mock_resolve_job_application:

        # Error due to fake instance in update function
        with pytest.raises(ValidationError):
            JobApplicationService.update(
                user=job_application1.owner,
                context=job_application1_context,
                validated_data=job_application1_valid_data_updated,
            )

        mock_resolve_job_application.assert_called_once()


@pytest.mark.django_db
def test_update_job_application_calls_validate_emails_ownership(
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

        mock_validate_emails_ownership.assert_called_once()


@pytest.mark.django_db
def test_update_job_application_calls_validate_documents_ownership(
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
def test_update_job_application_calls_update_non_m2m_fields(
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
def test_update_job_application_calls_update_m2m_fields(
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
def test_update_job_application_calls_full_clean(
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
def test_update_job_application_calls_save(
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
def test_update_job_application_calls_m2m_non_empty_validation(
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated
):

    with patch(
            "apps.applications.services.application_service.JobApplicationService."
            "_m2m_non_empty_validation"
    ) as mock_m2m_non_empty_validation:

        JobApplicationService.update(
            user=job_application1.owner,
            context=job_application1_context,
            validated_data=job_application1_valid_data_updated,
        )

        mock_m2m_non_empty_validation.assert_called_once()


@pytest.mark.django_db
def test_update_job_application_dont_raise_error_if_a_required_m2m_field_is_missing(
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated
):

    # Missing emails do NOT raise
    job_application1_valid_data_updated.pop("emails")

    JobApplicationService.update(
        user=job_application1.owner,
        context=job_application1_context,
        validated_data=job_application1_valid_data_updated,
    )


@pytest.mark.django_db
def test_update_job_application_raises_error_if_a_required_m2m_field_is_empty(
        job_application1,
        job_application1_context,
        job_application1_valid_data_updated
):

    # Empty list emails raise validation error
    job_application1_valid_data_updated["emails"] = []

    with pytest.raises(ValidationError):
        JobApplicationService.update(
            user=job_application1.owner,
            context=job_application1_context,
            validated_data=job_application1_valid_data_updated,
        )

#   ----------------------------------- ****** -----------------------------------


# Test Deleting

@pytest.mark.django_db
def test_remove_job_application_calls_resolve_job_application(
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
