import copy
from datetime import timedelta
from unittest.mock import patch

import pytest
from django.utils import timezone

from apps.companies.services.job_position_service import JobPositionService
from apps.core.common.contexts.contexts import (
    CompanyChildContext,
    CompanyContext,
)
from apps.core.exceptions.exceptions import (
    DomainInvariantViolationError,
    BusinessRuleViolationError,
    ResourceNotFoundError,
)


pytestmark = pytest.mark.django_db


def company_child_context(position):
    return CompanyChildContext(
        id=position.id,
        company_id=position.company.id,
        workspace_id=position.company.workspace.workspace_id,
    )


# ============================================================================
# Dependency resolution
# ============================================================================

class TestResolveCreateDependencies:

    def test_resolves_company(
        self,
        co1_ws1_user1,
        co1_child_context_ws1_user1_no_id,
    ):

        dependencies = JobPositionService._resolve_create_dependencies(
            user=co1_ws1_user1.workspace.owner,
            context=co1_child_context_ws1_user1_no_id,
        )

        assert dependencies["company"] == co1_ws1_user1


    def test_resolves_company_through_company_service(
        self,
        co1_ws1_user1,
        co1_child_context_ws1_user1_no_id,
    ):

        with patch(
            "apps.companies.services.job_position_service."
            "CompanyService._resolve_instance"
        ) as mock:

            mock.return_value = co1_ws1_user1

            JobPositionService._resolve_create_dependencies(
                user=co1_ws1_user1.workspace.owner,
                context=co1_child_context_ws1_user1_no_id,
            )

            mock.assert_called_once_with(
                user=co1_ws1_user1.workspace.owner,
                context=CompanyContext(
                    id=(
                        co1_child_context_ws1_user1_no_id.company_id
                    ),
                    workspace_id=(
                        co1_child_context_ws1_user1_no_id.workspace_id
                    ),
                ),
            )


# ============================================================================
# Create
# ============================================================================

class TestJobPositionCreate:

    def test_create_returns_position(
        self,
        workspace1_user1,
        co1_child_context_ws1_user1_no_id,
        job_pos_user1_valid_data,
    ):

        result = JobPositionService.create(
            user=workspace1_user1.owner,
            context=co1_child_context_ws1_user1_no_id,
            validated_data=job_pos_user1_valid_data,
        )

        assert result.id is not None
        assert result.company.workspace == workspace1_user1


    def test_create_rejects_foreign_m2m_owner(
        self,
        workspace1_user1,
        co1_child_context_ws1_user1_no_id,
        job_pos_user1_valid_data,
        job_benefit1_user2,
    ):

        payload = copy.deepcopy(job_pos_user1_valid_data)
        payload["benefits"] = [job_benefit1_user2]

        with pytest.raises(DomainInvariantViolationError):

            JobPositionService.create(
                user=workspace1_user1.owner,
                context=co1_child_context_ws1_user1_no_id,
                validated_data=payload,
            )


# ============================================================================
# Update
# ============================================================================

class TestJobPositionUpdate:

    def test_update_changes_allowed_fields(
        self,
        job_position1_co1_ws1_user1,
        job_pos_user1_updated_valid_data,
    ):

        updated = JobPositionService.update(
            user=job_position1_co1_ws1_user1.company.workspace.owner,
            context=company_child_context(
                job_position1_co1_ws1_user1
            ),
            validated_data=job_pos_user1_updated_valid_data,
        )

        assert updated.title == (
            job_pos_user1_updated_valid_data["title"]
        )


    def test_partial_update_keeps_existing_fields(
        self,
        job_position1_co1_ws1_user1,
        job_pos_user1_updated_valid_data,
    ):

        data = job_pos_user1_updated_valid_data.copy()

        old_title = job_position1_co1_ws1_user1.title

        data.pop("title")

        updated = JobPositionService.update(
            user=job_position1_co1_ws1_user1.company.workspace.owner,
            context=company_child_context(
                job_position1_co1_ws1_user1
            ),
            validated_data=data,
        )

        assert updated.title == old_title


    def test_empty_required_m2m_rejected(
        self,
        job_position1_co1_ws1_user1,
        job_pos_user1_updated_valid_data,
    ):

        data = job_pos_user1_updated_valid_data.copy()
        data["tasks"] = []

        with pytest.raises(BusinessRuleViolationError):

            JobPositionService.update(
                user=job_position1_co1_ws1_user1.company.workspace.owner,
                context=company_child_context(
                    job_position1_co1_ws1_user1
                ),
                validated_data=data,
            )


    def test_foreign_m2m_owner_rejected(
        self,
        job_position1_co1_ws1_user1,
        job_pos_user1_updated_valid_data,
        job_task1_user2,
    ):

        data = job_pos_user1_updated_valid_data.copy()
        data["tasks"] = [job_task1_user2]

        with pytest.raises(DomainInvariantViolationError):

            JobPositionService.update(
                user=job_position1_co1_ws1_user1.company.workspace.owner,
                context=company_child_context(
                    job_position1_co1_ws1_user1
                ),
                validated_data=data,
            )


# ============================================================================
# Date validation
# ============================================================================

class TestJobPositionDateValidation:

    def test_date_posted_after_application_is_rejected(
        self,
        job_position1_co1_ws1_user1,
        job_application1,
    ):

        job_application1.date_applied = (
            timezone.now() - timedelta(days=1)
        )
        job_application1.save()

        with pytest.raises(BusinessRuleViolationError):

            JobPositionService.update(
                user=job_position1_co1_ws1_user1.company.workspace.owner,
                context=company_child_context(
                    job_position1_co1_ws1_user1
                ),
                validated_data={
                    "date_posted": (
                        job_application1.date_applied
                        + timedelta(hours=1)
                    )
                },
            )


# ============================================================================
# Resolution / invariants
# ============================================================================

class TestJobPositionResolution:

    def test_wrong_company_raises(
        self,
        job_position1_co1_ws1_user1,
        job_pos1_co2_ws1_user1,
    ):

        with pytest.raises(DomainInvariantViolationError):

            JobPositionService._resolve_instance(
                user=job_position1_co1_ws1_user1.company.workspace.owner,
                context=CompanyChildContext(
                    id=job_position1_co1_ws1_user1.id,
                    company_id=job_pos1_co2_ws1_user1.company.id,
                    workspace_id=(
                        job_pos1_co2_ws1_user1.company.workspace.workspace_id
                    ),
                ),
            )


    def test_other_user_cannot_access(
        self,
        job_position1_co1_ws1_user1,
        user2,
    ):

        with pytest.raises(ResourceNotFoundError):

            JobPositionService._resolve_instance(
                user=user2,
                context=company_child_context(
                    job_position1_co1_ws1_user1
                ),
            )


# ============================================================================
# Remove
# ============================================================================

class TestJobPositionRemove:

    def test_remove_deletes_position(
        self,
        job_position1_co1_ws1_user1,
    ):

        JobPositionService.remove(
            user=job_position1_co1_ws1_user1.company.workspace.owner,
            context=company_child_context(
                job_position1_co1_ws1_user1
            ),
        )

        assert not JobPositionService.MODEL.objects.filter(
            id=job_position1_co1_ws1_user1.id
        ).exists()
