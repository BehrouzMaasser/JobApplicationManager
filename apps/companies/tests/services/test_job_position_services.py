import copy
from unittest.mock import patch

import pytest

from apps.companies.services.job_position_service import JobPositionService

from apps.companies.services.contexts.company_context import CompanyChildContext

from apps.core.exceptions.exceptions import (
    DomainInvariantViolationError,
    BusinessRuleViolationError,
    AccessDeniedError
)


# =========================
# CREATE
# =========================

@pytest.mark.django_db
def test_create_job_position_success(
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
    assert result.title == job_pos_user1_valid_data["title"]
    assert result.description == job_pos_user1_valid_data["description"]

    assert (list(result.employment_types.all()) ==
            job_pos_user1_valid_data["employment_types"])

    assert list(result.job_sites.all()) == job_pos_user1_valid_data["job_sites"]
    assert list(result.tasks.all()) == job_pos_user1_valid_data["tasks"]

    assert (list(result.requirements.all()) ==
            job_pos_user1_valid_data["requirements"])


@pytest.mark.django_db
def test_create_rejects_foreign_m2m_user(
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


@pytest.mark.django_db
def test_create_calls_company_resolution(
    co1_ws1_user1,
    co1_child_context_ws1_user1_no_id,
    job_pos_user1_valid_data,
):
    with patch(
        "apps.companies.services.job_position_service.JobPositionService."
        "_resolve_company"
    ) as mock:
        with pytest.raises(Exception):
            JobPositionService.create(
                user=co1_ws1_user1.workspace.owner,
                context=co1_child_context_ws1_user1_no_id,
                validated_data=job_pos_user1_valid_data,
            )

        mock.assert_called_once()


# =========================
# UPDATE
# =========================

@pytest.mark.django_db
def test_update_job_position_success(
    job_position1_user1,
    job_position1_context,
    job_pos_user1_updated_valid_data,
):
    result = JobPositionService.update(
        user=job_position1_user1.company.workspace.owner,
        context=job_position1_context,
        validated_data=job_pos_user1_updated_valid_data,
    )

    assert result.id == job_position1_user1.id
    assert result.title == job_pos_user1_updated_valid_data["title"]
    assert result.description == job_pos_user1_updated_valid_data["description"]

    assert (list(result.employment_types.all()) ==
            job_pos_user1_updated_valid_data["employment_types"])

    assert (list(result.tasks.all()) ==
            job_pos_user1_updated_valid_data["tasks"])

    assert (list(result.requirements.all()) ==
            job_pos_user1_updated_valid_data["requirements"])

    assert (list(result.benefits.all()) ==
            job_pos_user1_updated_valid_data["benefits"])


@pytest.mark.django_db
def test_update_missing_optional_fields_does_not_crash(
    job_position1_user1,
    job_position1_context,
    job_pos_user1_updated_valid_data,
):
    payload = copy.deepcopy(job_pos_user1_updated_valid_data)
    payload.pop("title", None)
    payload.pop("employment_types", None)

    result = JobPositionService.update(
        user=job_position1_user1.company.workspace.owner,
        context=job_position1_context,
        validated_data=payload,
    )

    assert result.id == job_position1_user1.id


@pytest.mark.django_db
def test_update_empty_required_m2m_raises_business_rule_error(
    workspace1_user1,
    job_position1_context,
    job_pos_user1_updated_valid_data,
):
    payload = copy.deepcopy(job_pos_user1_updated_valid_data)
    payload["tasks"] = []

    with pytest.raises(BusinessRuleViolationError):
        JobPositionService.update(
            user=workspace1_user1.owner,
            context=job_position1_context,
            validated_data=payload,
        )


@pytest.mark.django_db
def test_update_foreign_m2m_ownership_is_rejected(
    workspace1_user1,
    job_position1_context,
    job_pos_user1_updated_valid_data,
    job_task1_user2,
):
    payload = copy.deepcopy(job_pos_user1_updated_valid_data)
    payload["tasks"] = [job_task1_user2]

    with pytest.raises(DomainInvariantViolationError):
        JobPositionService.update(
            user=workspace1_user1.owner,
            context=job_position1_context,
            validated_data=payload,
        )


@pytest.mark.django_db
def test_update_calls_resolve(
    job_position1_context,
    job_position1_user1,
    job_pos_user1_updated_valid_data,
):
    with patch(
        "apps.companies.services.job_position_service.JobPositionService."
        "_resolve_job_position"
    ) as mock:
        JobPositionService.update(
            user=job_position1_user1.company.workspace.owner,
            context=job_position1_context,
            validated_data=job_pos_user1_updated_valid_data,
        )
        mock.assert_called_once()


# =========================
# REMOVE
# =========================

@pytest.mark.django_db
def test_remove_job_position_calls_resolve(
    job_position1_context,
    job_position1_user1,
):
    with patch(
        "apps.companies.services.job_position_service.JobPositionService."
        "_resolve_job_position"
    ) as mock:
        JobPositionService.remove(
            user=job_position1_user1.company.workspace.owner,
            context=job_position1_context,
        )
        mock.assert_called_once()


# =========================
# RESOLVE
# =========================

@pytest.mark.django_db
def test_resolve_wrong_company_raises(
    job_position1_user1,
    job_pos1_co2_ws1_user1,
):
    with pytest.raises(DomainInvariantViolationError):
        JobPositionService._resolve_job_position(
            user=job_position1_user1.company.workspace.owner,
            context=CompanyChildContext(
                id=job_position1_user1.id,
                workspace_id=job_pos1_co2_ws1_user1.company.workspace.workspace_id,
                company_id=job_pos1_co2_ws1_user1.company.id,
            ),
        )


@pytest.mark.django_db
def test_resolve_other_user_raises_access_denied_error(
    user2,
    job_position1_context,
):
    with pytest.raises(AccessDeniedError):
        JobPositionService._resolve_job_position(
            user=user2,
            context=job_position1_context,
        )
