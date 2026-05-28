from unittest.mock import patch

import pytest

from rest_framework.exceptions import ValidationError

from apps.companies.services.job_task_service import JobTaskService

#   ----------------------------------- ****** -----------------------------------


# Creation:

@pytest.mark.django_db
def test_create_job_task_successfully_returns_job_task(
        user, job_task_user1_valid_data
):

    job_task = JobTaskService.create(
        user=user,
        validated_data=job_task_user1_valid_data,
    )

    assert job_task.id is not None
    assert job_task.user == user
    assert job_task.title == job_task_user1_valid_data["title"]
    assert job_task.description == job_task_user1_valid_data["description"]


@pytest.mark.django_db
def test_create_job_task_calls_full_clean(user, job_task_user1_valid_data):

    with patch(
            "apps.companies.models.JobTask.full_clean"
    ) as mock_full_clean:

        JobTaskService.create(user=user, validated_data=job_task_user1_valid_data)

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_create_job_task_calls_save(user, job_task_user1_valid_data):

    with patch(
            "apps.companies.models.JobTask.save"
    ) as mock_save:

        JobTaskService.create(user=user, validated_data=job_task_user1_valid_data)

        mock_save.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Updating

@pytest.mark.django_db
def test_update_job_task_calls_full_clean(
        job_task_user1_updated_valid_data,
        job_task_user1
):

    with patch(
            "apps.companies.models.JobTask.full_clean"
    ) as mock_full_clean:

        JobTaskService.update(
            user=job_task_user1.user,
            validated_data=job_task_user1_updated_valid_data,
            job_task_id=job_task_user1.id
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_update_job_task_calls_save(
        job_task_user1_updated_valid_data,
        job_task_user1
):

    with patch(
            "apps.companies.models.JobTask.save"
    ) as mock_save:

        JobTaskService.update(
            user=job_task_user1.user,
            validated_data=job_task_user1_updated_valid_data,
            job_task_id=job_task_user1.id
        )

        mock_save.assert_called_once()


@pytest.mark.django_db
def test_update_job_task_calls_update_non_m2m_fields(
        job_task_user1_updated_valid_data, job_task_user1
):

    with patch(
            "apps.companies.services.job_task_service.JobTaskService."
            "_update_non_m2m_fields"
    ) as mock_update_non_m2m_fields:

        JobTaskService.update(
            user=job_task_user1.user,
            job_task_id=job_task_user1.id,
            validated_data=job_task_user1_updated_valid_data
        )

        mock_update_non_m2m_fields.assert_called_once()


@pytest.mark.django_db
def test_update_job_task_calls_resolve_job_task(
        job_task_user1_updated_valid_data,
        job_task_user1
):

    with patch(
            "apps.companies.services.job_task_service.JobTaskService."
            "_resolve_job_task"
    ) as mock_resolve_job_task:

        JobTaskService.update(
            user=job_task_user1.user,
            job_task_id=job_task_user1.id,
            validated_data=job_task_user1_updated_valid_data,
        )

        mock_resolve_job_task.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test Deleting

@pytest.mark.django_db
def test_remove_job_task_calls_resolve_job_task(job_task_user1):

    with patch(
            "apps.companies.services.job_task_service.JobTaskService."
            "_resolve_job_task"
    ) as mock_resolve_job_task:

        JobTaskService.remove(
            user=job_task_user1.user,
            job_task_id=job_task_user1.id,
        )

        mock_resolve_job_task.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test Retrieving

@pytest.mark.django_db
def test_access_to_job_task_of_another_user_raises_validation_error(
        other_user, job_task_user1
):

    # Job Task don't belong to user
    with pytest.raises(ValidationError):
        JobTaskService._resolve_job_task(
            user=other_user,
            job_task_id=job_task_user1.id,
        )

#   ----------------------------------- ****** -----------------------------------
