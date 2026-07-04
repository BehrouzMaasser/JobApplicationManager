import pytest
from unittest.mock import patch

from apps.companies.services.job_task_service import JobTaskService

from apps.core.exceptions.exceptions import AccessDeniedError


# -----------------------------------
# CREATE
# -----------------------------------

@pytest.mark.django_db
class TestJobTaskServiceCreate:

    def test_create_returns_job_task_successfully(
        self,
        user1,
        job_task1_user1_valid_data,
    ):
        result = JobTaskService.create(
            user=user1,
            validated_data=job_task1_user1_valid_data,
        )

        assert result.id is not None
        assert result.user == user1
        assert result.title == job_task1_user1_valid_data["title"]
        assert result.description == job_task1_user1_valid_data["description"]

    def test_create_calls_model_methods(
        self,
        user1,
        job_task1_user1_valid_data,
    ):
        with patch("apps.companies.models.JobTask.full_clean") as mock_clean, \
             patch("apps.companies.models.JobTask.save") as mock_save:

            JobTaskService.create(
                user=user1,
                validated_data=job_task1_user1_valid_data,
            )

            mock_clean.assert_called_once()
            mock_save.assert_called_once()


# -----------------------------------
# UPDATE
# -----------------------------------

@pytest.mark.django_db
class TestJobTaskServiceUpdate:

    def test_update_returns_updated_job_task(
        self,
        job_task1_user1,
        job_task1_user1_updated_valid_data,
    ):
        updated = JobTaskService.update(
            user=job_task1_user1.user,
            job_task_id=job_task1_user1.id,
            validated_data=job_task1_user1_updated_valid_data,
        )

        assert updated.id == job_task1_user1.id
        assert updated.title == job_task1_user1_updated_valid_data["title"]
        assert (updated.description ==
                job_task1_user1_updated_valid_data["description"])

    def test_update_calls_update_non_m2m_fields(
        self,
        job_task1_user1,
        job_task1_user1_updated_valid_data,
    ):
        with patch(
            "apps.companies.services.job_task_service.JobTaskService."
            "_update_non_m2m_fields"
        ) as mock_update:

            JobTaskService.update(
                user=job_task1_user1.user,
                job_task_id=job_task1_user1.id,
                validated_data=job_task1_user1_updated_valid_data,
            )

            mock_update.assert_called_once()

    def test_update_calls_model_methods(
        self,
        job_task1_user1,
        job_task1_user1_updated_valid_data,
    ):
        with patch("apps.companies.models.JobTask.full_clean") as mock_clean, \
             patch("apps.companies.models.JobTask.save") as mock_save:

            JobTaskService.update(
                user=job_task1_user1.user,
                job_task_id=job_task1_user1.id,
                validated_data=job_task1_user1_updated_valid_data,
            )

            mock_clean.assert_called_once()
            mock_save.assert_called_once()

    def test_partial_update_keeps_existing_fields(
        self,
        job_task1_user1,
        job_task1_user1_updated_valid_data,
    ):
        data = job_task1_user1_updated_valid_data.copy()
        data.pop("description")

        updated = JobTaskService.update(
            user=job_task1_user1.user,
            job_task_id=job_task1_user1.id,
            validated_data=data,
        )

        assert updated.title == data["title"]
        assert updated.description == job_task1_user1.description


# -----------------------------------
# REMOVE
# -----------------------------------

@pytest.mark.django_db
class TestJobTaskServiceRemove:

    def test_remove_resolves_job_task(
        self,
        job_task1_user1,
    ):
        with patch(
            "apps.companies.services.job_task_service.JobTaskService."
            "_resolve_job_task"
        ) as mock_resolve:

            mock_resolve.return_value = job_task1_user1

            JobTaskService.remove(
                user=job_task1_user1.user,
                job_task_id=job_task1_user1.id,
            )

            mock_resolve.assert_called_once()


# -----------------------------------
# RESOLVE
# -----------------------------------

@pytest.mark.django_db
class TestJobTaskServiceResolve:

    def test_returns_job_task_successfully(
        self,
        job_task1_user1,
    ):
        result = JobTaskService._resolve_job_task(
            user=job_task1_user1.user,
            job_task_id=job_task1_user1.id,
        )

        assert result == job_task1_user1

    def test_access_by_other_users_raises_error(
        self,
        user2,
        job_task1_user1,
    ):
        with pytest.raises(AccessDeniedError):
            JobTaskService._resolve_job_task(
                user=user2,
                job_task_id=job_task1_user1.id,
            )
            