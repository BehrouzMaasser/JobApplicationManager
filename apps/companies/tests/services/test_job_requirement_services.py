from unittest.mock import patch

import pytest

from rest_framework.exceptions import ValidationError

from apps.companies.services.job_requirement_service import JobRequirementService

#   ----------------------------------- ****** -----------------------------------


# Creation:

@pytest.mark.django_db
def test_create_job_requirement_successfully_returns_job_requirement(
        user, job_requirement_user1_valid_data
):

    job_requirement = JobRequirementService.create(
        user=user,
        validated_data=job_requirement_user1_valid_data,
    )

    assert job_requirement.id is not None
    assert job_requirement.title == job_requirement_user1_valid_data["title"]

    assert (job_requirement.description ==
            job_requirement_user1_valid_data["description"])


@pytest.mark.django_db
def test_create_job_requirement_calls_full_clean(
        user, job_requirement_user1_valid_data
):

    with patch(
            "apps.companies.models.JobRequirement.full_clean"
    ) as mock_full_clean:

        JobRequirementService.create(
            user=user, validated_data=job_requirement_user1_valid_data
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_create_job_requirement_calls_save(
        user, job_requirement_user1_valid_data
):

    with patch(
            "apps.companies.models.JobRequirement.save"
    ) as mock_save:

        JobRequirementService.create(
            user=user, validated_data=job_requirement_user1_valid_data
        )

        mock_save.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Updating

@pytest.mark.django_db
def test_update_job_requirement_calls_full_clean(
        job_requirement_user1_updated_valid_data, job_requirement_user1
):

    with patch(
            "apps.companies.models.JobRequirement.full_clean"
    ) as mock_full_clean:

        JobRequirementService.update(
            user=job_requirement_user1.user,
            validated_data=job_requirement_user1_updated_valid_data,
            job_requirement_id=job_requirement_user1.id
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_update_job_requirement_calls_save(
        job_requirement_user1_updated_valid_data, job_requirement_user1
):

    with patch(
            "apps.companies.models.JobRequirement.save"
    ) as mock_save:

        JobRequirementService.update(
            user=job_requirement_user1.user,
            validated_data=job_requirement_user1_updated_valid_data,
            job_requirement_id=job_requirement_user1.id
        )

        mock_save.assert_called_once()


@pytest.mark.django_db
def test_update_job_requirement_calls_update_non_m2m_fields(
        job_requirement_user1_updated_valid_data, job_requirement_user1
):

    with patch(
            "apps.companies.services.job_requirement_service.JobRequirementService."
            "_update_non_m2m_fields"
    ) as mock_update_non_m2m_fields:

        JobRequirementService.update(
            user=job_requirement_user1.user,
            job_requirement_id=job_requirement_user1.id,
            validated_data=job_requirement_user1_updated_valid_data
        )

        mock_update_non_m2m_fields.assert_called_once()


@pytest.mark.django_db
def test_update_job_requirement_calls_resolve_job_requirement(
        job_requirement_user1, job_requirement_user1_updated_valid_data
):

    with patch(
        "apps.companies.services.job_requirement_service.JobRequirementService."
        "_resolve_job_requirement"
    ) as mock_resolve_job_requirement:

        JobRequirementService.update(
            user=job_requirement_user1.user,
            job_requirement_id=job_requirement_user1.id,
            validated_data=job_requirement_user1_updated_valid_data,
        )

        mock_resolve_job_requirement.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test Deleting

@pytest.mark.django_db
def test_delete_job_requirement_calls_resolve_job_requirement(
        job_requirement_user1
):

    with patch(
        "apps.companies.services.job_requirement_service.JobRequirementService."
        "_resolve_job_requirement"
    ) as mock_resolve_job_requirement:

        JobRequirementService.remove(
            user=job_requirement_user1.user,
            job_requirement_id=job_requirement_user1.id,
        )

        mock_resolve_job_requirement.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test Retrieving

@pytest.mark.django_db
def test_access_to_job_requirement_of_another_user_raises_validation_error(
        other_user, job_requirement_user1
):

    # Job Requirement don't belong to user
    with pytest.raises(ValidationError):
        JobRequirementService._resolve_job_requirement(
            user=other_user,
            job_requirement_id=job_requirement_user1.id,
        )

#   ----------------------------------- ****** -----------------------------------
