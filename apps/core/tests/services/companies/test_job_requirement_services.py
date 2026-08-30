from unittest.mock import patch

import pytest

from apps.companies.models import JobRequirement
from apps.companies.services.job_requirement_service import (
    JobRequirementService,
)

from apps.core.common.contexts.contexts import (
    EmptyContext,
    JobRequirementContext,
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

        dependencies = JobRequirementService._resolve_create_dependencies(
            user=user1,
            context=EMPTY_CONTEXT,
        )

        assert dependencies == {
            "user": user1
        }


# ============================================================================
# Create
# ============================================================================

class TestJobRequirementCreate:

    def test_create_returns_job_requirement(
        self,
        user1,
        job_requirement1_user1_valid_data,
    ):

        requirement = JobRequirementService.create(
            user=user1,
            context=EMPTY_CONTEXT,
            validated_data=job_requirement1_user1_valid_data,
        )

        assert requirement.id is not None
        assert requirement.user == user1

        assert requirement.title == (
            job_requirement1_user1_valid_data["title"]
        )

        assert requirement.description == (
            job_requirement1_user1_valid_data["description"]
        )


    def test_create_calls_model_validation(
        self,
        user1,
        job_requirement1_user1_valid_data,
    ):

        with patch(
            "apps.companies.models.JobRequirement.full_clean"
        ) as mock_clean:

            JobRequirementService.create(
                user=user1,
                context=EMPTY_CONTEXT,
                validated_data=job_requirement1_user1_valid_data,
            )

            mock_clean.assert_called_once()


# ============================================================================
# Update
# ============================================================================

class TestJobRequirementUpdate:

    def test_update_changes_fields(
        self,
        job_requirement1_user1,
        job_requirement1_user1_updated_valid_data,
    ):

        updated = JobRequirementService.update(
            user=job_requirement1_user1.user,
            context=JobRequirementContext(
                id=job_requirement1_user1.id
            ),
            validated_data=(
                job_requirement1_user1_updated_valid_data
            ),
        )

        assert updated.id == job_requirement1_user1.id

        assert updated.title == (
            job_requirement1_user1_updated_valid_data["title"]
        )

        assert updated.description == (
            job_requirement1_user1_updated_valid_data["description"]
        )


    def test_partial_update_keeps_existing_fields(
        self,
        job_requirement1_user1,
        job_requirement1_user1_updated_valid_data,
    ):

        data = (
            job_requirement1_user1_updated_valid_data.copy()
        )

        data.pop("description")

        updated = JobRequirementService.update(
            user=job_requirement1_user1.user,
            context=JobRequirementContext(
                id=job_requirement1_user1.id
            ),
            validated_data=data,
        )

        assert updated.title == data["title"]

        assert updated.description == (
            job_requirement1_user1.description
        )


    def test_update_calls_model_validation(
        self,
        job_requirement1_user1,
    ):

        with patch(
            "apps.companies.models.JobRequirement.full_clean"
        ) as mock_clean:

            JobRequirementService.update(
                user=job_requirement1_user1.user,
                context=JobRequirementContext(
                    id=job_requirement1_user1.id
                ),
                validated_data={
                    "title": "Updated requirement",
                },
            )

            mock_clean.assert_called_once()


# ============================================================================
# Resolution
# ============================================================================

class TestJobRequirementResolution:

    def test_selector_is_used(
        self,
        job_requirement1_user1,
    ):

        with patch(
            "apps.companies.services.job_requirement_service."
            "JobRequirementSelector.get",
            return_value=job_requirement1_user1,
        ) as mock_get:

            JobRequirementService._resolve_instance(
                user=job_requirement1_user1.user,
                context=JobRequirementContext(
                    id=job_requirement1_user1.id
                ),
            )

            mock_get.assert_called_once_with(
                user=job_requirement1_user1.user,
                obj_id=job_requirement1_user1.id,
            )


# ============================================================================
# Aggregate validation
# ============================================================================

class TestValidateResolvedInstance:

    def test_requires_no_extra_validation(
        self,
        job_requirement1_user1,
    ):

        JobRequirementService._validate_resolved_instance(
            instance=job_requirement1_user1,
            context=JobRequirementContext(
                id=job_requirement1_user1.id
            ),
        )


# ============================================================================
# Remove
# ============================================================================

class TestJobRequirementRemove:

    def test_remove_deletes_requirement(
        self,
        job_requirement1_user1,
    ):

        requirement_id = job_requirement1_user1.id

        JobRequirementService.remove(
            user=job_requirement1_user1.user,
            context=JobRequirementContext(
                id=requirement_id
            ),
        )

        assert not JobRequirement.objects.filter(
            id=requirement_id,
        ).exists()
