import pytest
from unittest.mock import patch

from apps.companies.services.job_requirement_service import JobRequirementService

from apps.core.exceptions.exceptions import AccessDeniedError


# -----------------------------------
# CREATE
# -----------------------------------

@pytest.mark.django_db
class TestJobRequirementServiceCreate:

    def test_create_returns_job_requirement_successfully(
        self,
        user1,
        job_requirement1_user1_valid_data,
    ):
        result = JobRequirementService.create(
            user=user1,
            validated_data=job_requirement1_user1_valid_data,
        )

        assert result.id is not None
        assert result.title == job_requirement1_user1_valid_data["title"]
        assert result.description == job_requirement1_user1_valid_data["description"]

    def test_create_calls_model_methods(
        self,
        user1,
        job_requirement1_user1_valid_data,
    ):
        with patch("apps.companies.models.JobRequirement.full_clean") as mock_clean, \
             patch("apps.companies.models.JobRequirement.save") as mock_save:

            JobRequirementService.create(
                user=user1,
                validated_data=job_requirement1_user1_valid_data,
            )

            mock_clean.assert_called_once()
            mock_save.assert_called_once()


# -----------------------------------
# UPDATE
# -----------------------------------

@pytest.mark.django_db
class TestJobRequirementServiceUpdate:

    def test_update_returns_updated_job_requirement(
        self,
        job_requirement1_user1,
        job_requirement1_user1_updated_valid_data,
    ):
        updated = JobRequirementService.update(
            user=job_requirement1_user1.user,
            job_requirement_id=job_requirement1_user1.id,
            validated_data=job_requirement1_user1_updated_valid_data,
        )

        assert updated.id == job_requirement1_user1.id
        assert updated.title == job_requirement1_user1_updated_valid_data["title"]
        assert (updated.description ==
                job_requirement1_user1_updated_valid_data["description"])

    def test_update_calls_update_non_m2m_fields(
        self,
        job_requirement1_user1,
        job_requirement1_user1_updated_valid_data,
    ):
        with patch(
            "apps.companies.services.job_requirement_service.JobRequirementService."
            "_update_non_m2m_fields"
        ) as mock_update:

            JobRequirementService.update(
                user=job_requirement1_user1.user,
                job_requirement_id=job_requirement1_user1.id,
                validated_data=job_requirement1_user1_updated_valid_data,
            )

            mock_update.assert_called_once()

    def test_update_calls_model_methods(
        self,
        job_requirement1_user1,
        job_requirement1_user1_updated_valid_data,
    ):
        with patch("apps.companies.models.JobRequirement.full_clean") as mock_clean, \
             patch("apps.companies.models.JobRequirement.save") as mock_save:

            JobRequirementService.update(
                user=job_requirement1_user1.user,
                job_requirement_id=job_requirement1_user1.id,
                validated_data=job_requirement1_user1_updated_valid_data,
            )

            mock_clean.assert_called_once()
            mock_save.assert_called_once()

    def test_partial_update_keeps_existing_fields(
        self,
        job_requirement1_user1,
        job_requirement1_user1_updated_valid_data,
    ):
        data = job_requirement1_user1_updated_valid_data.copy()
        data.pop("description")

        updated = JobRequirementService.update(
            user=job_requirement1_user1.user,
            job_requirement_id=job_requirement1_user1.id,
            validated_data=data,
        )

        assert updated.title == data["title"]
        assert updated.description == job_requirement1_user1.description


# -----------------------------------
# REMOVE
# -----------------------------------

@pytest.mark.django_db
class TestJobRequirementServiceRemove:

    def test_remove_resolves_job_requirement(
        self,
        job_requirement1_user1,
    ):
        with patch(
            "apps.companies.services.job_requirement_service.JobRequirementService."
            "_resolve_job_requirement"
        ) as mock_resolve:

            mock_resolve.return_value = job_requirement1_user1

            JobRequirementService.remove(
                user=job_requirement1_user1.user,
                job_requirement_id=job_requirement1_user1.id,
            )

            mock_resolve.assert_called_once()


# -----------------------------------
# RESOLVE
# -----------------------------------

@pytest.mark.django_db
class TestJobRequirementServiceResolve:

    def test_returns_job_requirement_successfully(
        self,
        job_requirement1_user1,
    ):
        result = JobRequirementService._resolve_job_requirement(
            user=job_requirement1_user1.user,
            job_requirement_id=job_requirement1_user1.id,
        )

        assert result == job_requirement1_user1

    def test_access_by_other_users_raises_error(
        self,
        user2,
        job_requirement1_user1,
    ):
        with pytest.raises(AccessDeniedError):
            JobRequirementService._resolve_job_requirement(
                user=user2,
                job_requirement_id=job_requirement1_user1.id,
            )
            