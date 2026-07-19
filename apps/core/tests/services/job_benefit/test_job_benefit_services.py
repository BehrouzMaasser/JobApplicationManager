from unittest.mock import patch

import pytest

from apps.companies.models import JobBenefit
from apps.companies.services.job_benefit_service import (
    JobBenefitService,
)

from apps.core.common.contexts.contexts import (
    EmptyContext,
    JobBenefitContext,
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

        dependencies = JobBenefitService._resolve_create_dependencies(
            user=user1,
            context=EMPTY_CONTEXT,
        )

        assert dependencies == {
            "user": user1
        }


# ============================================================================
# Create
# ============================================================================

class TestJobBenefitCreate:

    def test_create_returns_job_benefit(
        self,
        user1,
        job_benefit1_user1_valid_data,
    ):

        benefit = JobBenefitService.create(
            user=user1,
            context=EMPTY_CONTEXT,
            validated_data=job_benefit1_user1_valid_data,
        )

        assert benefit.id is not None
        assert benefit.user == user1
        assert benefit.name == (
            job_benefit1_user1_valid_data["name"]
        )
        assert benefit.description == (
            job_benefit1_user1_valid_data["description"]
        )


    def test_create_calls_model_validation(
        self,
        user1,
        job_benefit1_user1_valid_data,
    ):

        with patch(
            "apps.companies.models.JobBenefit.full_clean"
        ) as mock_clean:

            JobBenefitService.create(
                user=user1,
                context=EMPTY_CONTEXT,
                validated_data=job_benefit1_user1_valid_data,
            )

            mock_clean.assert_called_once()


# ============================================================================
# Update
# ============================================================================

class TestJobBenefitUpdate:

    def test_update_changes_fields(
        self,
        job_benefit1_user1,
        job_benefit1_user1_updated_valid_data,
    ):

        updated = JobBenefitService.update(
            user=job_benefit1_user1.user,
            context=JobBenefitContext(
                id=job_benefit1_user1.pk
            ),
            validated_data=job_benefit1_user1_updated_valid_data,
        )

        assert updated.id == job_benefit1_user1.id
        assert updated.name == (
            job_benefit1_user1_updated_valid_data["name"]
        )
        assert updated.description == (
            job_benefit1_user1_updated_valid_data["description"]
        )


    def test_partial_update_keeps_existing_fields(
        self,
        job_benefit1_user1,
        job_benefit1_user1_updated_valid_data,
    ):

        data = job_benefit1_user1_updated_valid_data.copy()

        data.pop("description")

        updated = JobBenefitService.update(
            user=job_benefit1_user1.user,
            context=JobBenefitContext(
                id=job_benefit1_user1.pk
            ),
            validated_data=data,
        )

        assert updated.name == data["name"]
        assert updated.description == (
            job_benefit1_user1.description
        )


    def test_update_calls_model_validation(
        self,
        job_benefit1_user1,
    ):

        with patch(
            "apps.companies.models.JobBenefit.full_clean"
        ) as mock_clean:

            JobBenefitService.update(
                user=job_benefit1_user1.user,
                context=JobBenefitContext(
                    id=job_benefit1_user1.pk
                ),
                validated_data={
                    "name": "Updated benefit",
                },
            )

            mock_clean.assert_called_once()


# ============================================================================
# Resolution
# ============================================================================

class TestJobBenefitResolution:

    def test_selector_is_used(
        self,
        job_benefit1_user1,
    ):

        with patch(
            "apps.companies.services.job_benefit_service."
            "JobBenefitSelector.get",
            return_value=job_benefit1_user1,
        ) as mock_get:

            JobBenefitService._resolve_instance(
                user=job_benefit1_user1.user,
                context=JobBenefitContext(
                    id=job_benefit1_user1.pk
                ),
            )

            mock_get.assert_called_once_with(
                user=job_benefit1_user1.user,
                obj_id=job_benefit1_user1.pk,
            )


# ============================================================================
# Aggregate validation
# ============================================================================

class TestValidateResolvedInstance:

    def test_requires_no_extra_validation(
        self,
        job_benefit1_user1,
    ):

        JobBenefitService._validate_resolved_instance(
            instance=job_benefit1_user1,
            context=JobBenefitContext(
                id=job_benefit1_user1.pk
            ),
        )


# ============================================================================
# Remove
# ============================================================================

class TestJobBenefitRemove:

    def test_remove_deletes_job_benefit(
        self,
        job_benefit1_user1,
    ):

        benefit_id = job_benefit1_user1.id

        JobBenefitService.remove(
            user=job_benefit1_user1.user,
            context=JobBenefitContext(
                id=benefit_id
            ),
        )

        assert not JobBenefit.objects.filter(
            id=benefit_id
        ).exists()
