from unittest.mock import patch

import pytest

from rest_framework.exceptions import ValidationError

from apps.companies.services.job_benefit_service import JobBenefitService

#   ----------------------------------- ****** -----------------------------------


# Creation:

@pytest.mark.django_db
def test_create_job_benefit_successfully_returns_job_benefit(
        user, job_benefit1_user1_valid_data
):

    job_benefit = JobBenefitService.create(
        user=user,
        validated_data=job_benefit1_user1_valid_data,
    )

    assert job_benefit.id is not None
    assert job_benefit.user == user
    assert job_benefit.name == job_benefit1_user1_valid_data["name"]
    assert job_benefit.description == job_benefit1_user1_valid_data["description"]


@pytest.mark.django_db
def test_create_job_benefit_calls_full_clean(user, job_benefit1_user1_valid_data):

    with patch(
            "apps.companies.models.JobBenefit.full_clean"
    ) as mock_full_clean:

        JobBenefitService.create(
            user=user, validated_data=job_benefit1_user1_valid_data
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_create_job_benefit_calls_save(user, job_benefit1_user1_valid_data):

    with patch(
            "apps.companies.models.JobBenefit.save"
    ) as mock_save:

        JobBenefitService.create(
            user=user, validated_data=job_benefit1_user1_valid_data
        )

        mock_save.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Updating

@pytest.mark.django_db
def test_update_job_benefit_successfully_returns_updated_job_benefit(
        job_benefit_user1,
        job_benefit1_user1_updated_valid_data
):

    updated_job_benefit = JobBenefitService.update(
            user=job_benefit_user1.user,
            job_benefit_id=job_benefit_user1.id,
            validated_data=job_benefit1_user1_updated_valid_data
        )

    assert updated_job_benefit.id == job_benefit_user1.id
    assert updated_job_benefit.name == job_benefit1_user1_updated_valid_data["name"]

    assert (updated_job_benefit.description ==
            job_benefit1_user1_updated_valid_data["description"])


@pytest.mark.django_db
def test_update_job_benefit_calls_full_clean(
        job_benefit_user1,
        job_benefit1_user1_updated_valid_data
):

    with patch(
            "apps.companies.models.JobBenefit.full_clean"
    ) as mock_full_clean:

        JobBenefitService.update(
            user=job_benefit_user1.user,
            validated_data=job_benefit1_user1_updated_valid_data,
            job_benefit_id=job_benefit_user1.id
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_update_job_benefit_calls_save(
        job_benefit_user1,
        job_benefit1_user1_updated_valid_data
):

    with patch(
            "apps.companies.models.JobBenefit.save"
    ) as mock_save:

        JobBenefitService.update(
            user=job_benefit_user1.user,
            validated_data=job_benefit1_user1_updated_valid_data,
            job_benefit_id=job_benefit_user1.id
        )

        mock_save.assert_called_once()


@pytest.mark.django_db
def test_update_job_benefit_calls_update_non_m2m_fields(
        job_benefit_user1,
        job_benefit1_user1_updated_valid_data
):

    with patch(
            "apps.companies.services.job_benefit_service.JobBenefitService."
            "_update_non_m2m_fields"
    ) as mock_update_non_m2m_fields:

        JobBenefitService.update(
            user=job_benefit_user1.user,
            job_benefit_id=job_benefit_user1.id,
            validated_data=job_benefit1_user1_updated_valid_data
        )

        mock_update_non_m2m_fields.assert_called_once()


@pytest.mark.django_db
def test_update_job_benefit_calls_resolve_job_benefit(
        job_benefit_user1,
        job_benefit1_user1_updated_valid_data
):

    with patch(
            "apps.companies.services.job_benefit_service.JobBenefitService."
            "_resolve_job_benefit"
    ) as mock_resolve_job_benefit:

        JobBenefitService.update(
            user=job_benefit_user1.user,
            job_benefit_id=job_benefit_user1.id,
            validated_data=job_benefit1_user1_updated_valid_data
        )

        mock_resolve_job_benefit.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test Deleting

@pytest.mark.django_db
def test_delete_job_benefit_calls_resolve_job_benefit(job_benefit_user1):

    with patch(
            "apps.companies.services.job_benefit_service.JobBenefitService."
            "_resolve_job_benefit"
    ) as mock_resolve_job_benefit:

        JobBenefitService.remove(
            user=job_benefit_user1.user,
            job_benefit_id=job_benefit_user1.id,
        )

        mock_resolve_job_benefit.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test Retrieving

@pytest.mark.django_db
def test_access_to_job_benefit_of_another_user_raises_validation_error(
        other_user, job_benefit_user1
):

    # Job Benefit don't belong to user
    with pytest.raises(ValidationError):
        JobBenefitService._resolve_job_benefit(
            user=other_user,
            job_benefit_id=job_benefit_user1.id,
        )

#   ----------------------------------- ****** -----------------------------------
