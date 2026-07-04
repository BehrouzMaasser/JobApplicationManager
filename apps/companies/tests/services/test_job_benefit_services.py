import pytest
from unittest.mock import patch

from apps.companies.services.job_benefit_service import JobBenefitService

from apps.core.exceptions.exceptions import AccessDeniedError


# -----------------------------------
# CREATE
# -----------------------------------

@pytest.mark.django_db
class TestJobBenefitServiceCreate:

    def test_create_returns_job_benefit_successfully(
        self,
        user1,
        job_benefit1_user1_valid_data,
    ):
        result = JobBenefitService.create(
            user=user1,
            validated_data=job_benefit1_user1_valid_data,
        )

        assert result.id is not None
        assert result.user == user1
        assert result.name == job_benefit1_user1_valid_data["name"]
        assert result.description == job_benefit1_user1_valid_data["description"]

    def test_create_calls_model_methods(
        self,
        user1,
        job_benefit1_user1_valid_data,
    ):
        with patch("apps.companies.models.JobBenefit.full_clean") as mock_clean, \
             patch("apps.companies.models.JobBenefit.save") as mock_save:

            JobBenefitService.create(
                user=user1,
                validated_data=job_benefit1_user1_valid_data,
            )

            mock_clean.assert_called_once()
            mock_save.assert_called_once()


# -----------------------------------
# UPDATE
# -----------------------------------

@pytest.mark.django_db
class TestJobBenefitServiceUpdate:

    def test_update_returns_updated_job_benefit(
        self,
        job_benefit1_user1,
        job_benefit1_user1_updated_valid_data,
    ):
        updated = JobBenefitService.update(
            user=job_benefit1_user1.user,
            job_benefit_id=job_benefit1_user1.id,
            validated_data=job_benefit1_user1_updated_valid_data,
        )

        assert updated.id == job_benefit1_user1.id
        assert updated.name == job_benefit1_user1_updated_valid_data["name"]
        assert (updated.description ==
                job_benefit1_user1_updated_valid_data["description"])

    def test_update_calls_update_non_m2m_fields(
        self,
        job_benefit1_user1,
        job_benefit1_user1_updated_valid_data,
    ):
        with patch(
            "apps.companies.services.job_benefit_service.JobBenefitService."
            "_update_non_m2m_fields"
        ) as mock_update:

            JobBenefitService.update(
                user=job_benefit1_user1.user,
                job_benefit_id=job_benefit1_user1.id,
                validated_data=job_benefit1_user1_updated_valid_data,
            )

            mock_update.assert_called_once()

    def test_update_calls_model_methods(
        self,
        job_benefit1_user1,
        job_benefit1_user1_updated_valid_data,
    ):
        with patch("apps.companies.models.JobBenefit.full_clean") as mock_clean, \
             patch("apps.companies.models.JobBenefit.save") as mock_save:

            JobBenefitService.update(
                user=job_benefit1_user1.user,
                job_benefit_id=job_benefit1_user1.id,
                validated_data=job_benefit1_user1_updated_valid_data,
            )

            mock_clean.assert_called_once()
            mock_save.assert_called_once()

    def test_partial_update_keeps_existing_fields(
        self,
        job_benefit1_user1,
        job_benefit1_user1_updated_valid_data,
    ):
        data = job_benefit1_user1_updated_valid_data.copy()
        data.pop("description")

        updated = JobBenefitService.update(
            user=job_benefit1_user1.user,
            job_benefit_id=job_benefit1_user1.id,
            validated_data=data,
        )

        assert updated.name == data["name"]
        assert updated.description == job_benefit1_user1.description


# -----------------------------------
# REMOVE
# -----------------------------------

@pytest.mark.django_db
class TestJobBenefitServiceRemove:

    def test_remove_resolves_job_benefit(
        self,
        job_benefit1_user1,
    ):
        with patch(
            "apps.companies.services.job_benefit_service.JobBenefitService."
            "_resolve_job_benefit"
        ) as mock_resolve:

            mock_resolve.return_value = job_benefit1_user1

            JobBenefitService.remove(
                user=job_benefit1_user1.user,
                job_benefit_id=job_benefit1_user1.id,
            )

            mock_resolve.assert_called_once()


# -----------------------------------
# RESOLVE
# -----------------------------------

@pytest.mark.django_db
class TestJobBenefitServiceResolve:

    def test_resolve_returns_job_benefit(
        self,
        job_benefit1_user1,
    ):
        result = JobBenefitService._resolve_job_benefit(
            user=job_benefit1_user1.user,
            job_benefit_id=job_benefit1_user1.id,
        )

        assert result == job_benefit1_user1

    def test_access_by_other_user_raises_error(
        self,
        user2,
        job_benefit1_user1,
    ):
        with pytest.raises(AccessDeniedError):
            JobBenefitService._resolve_job_benefit(
                user=user2,
                job_benefit_id=job_benefit1_user1.id,
            )
