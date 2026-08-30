import pytest
from unittest.mock import patch

from apps.companies.models import JobTask
from apps.companies.services.job_task_service import (
    JobTaskService,
)

from apps.core.common.contexts.contexts import (
    EmptyContext,
    JobTaskContext,
)


pytestmark = pytest.mark.django_db


EMPTY_CONTEXT = EmptyContext()


# ============================================================================
# Hooks
# ============================================================================

class TestResolveCreateDependencies:

    def test_resolves_user_dependency(
        self,
        user1,
    ):

        dependencies = JobTaskService._resolve_create_dependencies(
            user=user1,
            context=EMPTY_CONTEXT,
        )

        assert dependencies == {
            "user": user1
        }


# ============================================================================
# Create
# ============================================================================

class TestJobTaskCreate:

    def test_create_returns_job_task(
        self,
        user1,
        job_task1_user1_valid_data,
    ):

        task = JobTaskService.create(
            user=user1,
            context=EMPTY_CONTEXT,
            validated_data=job_task1_user1_valid_data,
        )

        assert task.id is not None
        assert task.user == user1

        assert task.title == (
            job_task1_user1_valid_data["title"]
        )

        assert task.description == (
            job_task1_user1_valid_data["description"]
        )


    def test_create_calls_model_validation(
        self,
        user1,
        job_task1_user1_valid_data,
    ):

        with patch(
            "apps.companies.models.JobTask.full_clean"
        ) as mock_clean:

            JobTaskService.create(
                user=user1,
                context=EMPTY_CONTEXT,
                validated_data=job_task1_user1_valid_data,
            )

            mock_clean.assert_called_once()


# ============================================================================
# Update
# ============================================================================

class TestJobTaskUpdate:

    def test_update_changes_fields(
        self,
        job_task1_user1,
        job_task1_user1_updated_valid_data,
    ):

        updated = JobTaskService.update(
            user=job_task1_user1.user,
            context=JobTaskContext(
                id=job_task1_user1.pk
            ),
            validated_data=(
                job_task1_user1_updated_valid_data
            ),
        )

        assert updated.id == job_task1_user1.id

        assert updated.title == (
            job_task1_user1_updated_valid_data["title"]
        )

        assert updated.description == (
            job_task1_user1_updated_valid_data["description"]
        )


    def test_partial_update_keeps_existing_fields(
        self,
        job_task1_user1,
        job_task1_user1_updated_valid_data,
    ):

        data = (
            job_task1_user1_updated_valid_data.copy()
        )

        data.pop("description")

        updated = JobTaskService.update(
            user=job_task1_user1.user,
            context=JobTaskContext(
                id=job_task1_user1.pk
            ),
            validated_data=data,
        )

        assert updated.title == data["title"]

        assert updated.description == (
            job_task1_user1.description
        )


    def test_update_calls_model_validation(
        self,
        job_task1_user1,
    ):

        with patch(
            "apps.companies.models.JobTask.full_clean"
        ) as mock_clean:

            JobTaskService.update(
                user=job_task1_user1.user,
                context=JobTaskContext(
                    id=job_task1_user1.pk
                ),
                validated_data={
                    "title": "Updated task",
                },
            )

            mock_clean.assert_called_once()


# ============================================================================
# Resolution
# ============================================================================

class TestJobTaskResolution:

    def test_selector_is_used(
        self,
        job_task1_user1,
    ):

        with patch(
            "apps.companies.services.job_task_service."
            "JobTaskSelector.get",
            return_value=job_task1_user1,
        ) as mock_get:

            JobTaskService._resolve_instance(
                user=job_task1_user1.user,
                context=JobTaskContext(
                    id=job_task1_user1.pk
                ),
            )

            mock_get.assert_called_once_with(
                user=job_task1_user1.user,
                obj_id=job_task1_user1.pk,
            )


# ============================================================================
# Aggregate validation
# ============================================================================

class TestValidateResolvedInstance:

    def test_requires_no_extra_validation(
        self,
        job_task1_user1,
    ):

        JobTaskService._validate_resolved_instance(
            instance=job_task1_user1,
            context=JobTaskContext(
                id=job_task1_user1.pk
            ),
        )


# ============================================================================
# Remove
# ============================================================================

class TestJobTaskRemove:

    def test_remove_deletes_task(
        self,
        job_task1_user1,
    ):

        task_id = job_task1_user1.id

        JobTaskService.remove(
            user=job_task1_user1.user,
            context=JobTaskContext(
                id=task_id
            ),
        )

        assert not JobTask.objects.filter(
            id=task_id,
        ).exists()
