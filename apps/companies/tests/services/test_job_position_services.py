import copy

import pytest

from unittest.mock import patch

from django.core.exceptions import ValidationError

from apps.companies.services.contexts.company_context import CompanyChildContext
from apps.companies.services.job_position_service import JobPositionService

#   ----------------------------------- ****** -----------------------------------


# Creation:

@pytest.mark.django_db
def test_create_job_position_successfully_returns_created_job_position(
        workspace_user1, co1_child_context_ws1_user1_no_id, job_pos_user1_valid_data
):

    job_position = JobPositionService.create(
        user=workspace_user1.owner,
        context=co1_child_context_ws1_user1_no_id,
        validated_data=job_pos_user1_valid_data,
    )

    assert job_position.id is not None
    assert job_position.company.workspace == workspace_user1
    assert job_position.title == job_pos_user1_valid_data["title"]
    assert job_position.description == job_pos_user1_valid_data["description"]

    assert (list(job_position.employment_types.all()) ==
            job_pos_user1_valid_data["employment_types"])

    assert (list(job_position.job_sites.all()) ==
            job_pos_user1_valid_data["job_sites"])

    assert list(job_position.tasks.all()) == job_pos_user1_valid_data["tasks"]

    assert (list(job_position.requirements.all()) ==
            job_pos_user1_valid_data["requirements"])


@pytest.mark.django_db
def test_create_calls_m2m_ownership_validation(
        workspace_user1,
        co1_child_context_ws1_user1_no_id,
        job_pos_user1_valid_data,
):

    with patch(
            'apps.companies.services.job_position_service.JobPositionService.'
            '_m2m_ownership_validation'
    ) as mock_m2m_ownership_validation:

        JobPositionService.create(
            user=workspace_user1.owner,
            context=co1_child_context_ws1_user1_no_id,
            validated_data=job_pos_user1_valid_data,
        )

        mock_m2m_ownership_validation.assert_called_once()


@pytest.mark.django_db
def test_create_raises_error_when_m2m_field_belong_to_another_user_is_used(
        workspace_user1,
        co1_child_context_ws1_user1_no_id,
        job_pos_user1_valid_data,
        job_benefit_user2
):

    # A job benefit that do not belong to the user
    invalid_data = copy.deepcopy(job_pos_user1_valid_data)
    invalid_data["benefits"] = [job_benefit_user2]

    with pytest.raises(ValidationError):
        JobPositionService.create(
            user=workspace_user1.owner,
            context=co1_child_context_ws1_user1_no_id,
            validated_data=invalid_data,
        )


@pytest.mark.django_db
def test_create_job_position_calls_resolve_company(
        co1_ws1_user1, co1_child_context_ws1_user1_no_id, job_pos_user1_valid_data
):

    with patch(
            'apps.companies.services.job_position_service.JobPositionService.'
            '_resolve_company',
    ) as mock_resolve_company:

        # Error due to fake company
        with pytest.raises(ValueError):
            JobPositionService.create(
                user=co1_ws1_user1.workspace.owner,
                context=co1_child_context_ws1_user1_no_id,
                validated_data=job_pos_user1_valid_data,
            )

        mock_resolve_company.assert_called_once()


@pytest.mark.django_db
def test_create_job_position_calls_full_clean(
        workspace_user1, co1_child_context_ws1_user1_no_id, job_pos_user1_valid_data
):

    with patch('apps.companies.models.JobPosition.full_clean') as mock_full_clean:

        JobPositionService.create(
            user=workspace_user1.owner,
            context=co1_child_context_ws1_user1_no_id,
            validated_data=job_pos_user1_valid_data,
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_create_job_position_calls_save(
        workspace_user1, co1_child_context_ws1_user1_no_id, job_pos_user1_valid_data
):

    with patch('apps.companies.models.JobPosition.save') as mock_save:

        with pytest.raises(ValidationError):
            JobPositionService.create(
                user=workspace_user1.owner,
                context=co1_child_context_ws1_user1_no_id,
                validated_data=job_pos_user1_valid_data,
            )

        mock_save.assert_called_once()


@pytest.mark.django_db
def test_create_calls_add_m2m_fields(
        workspace_user1,
        co1_child_context_ws1_user1_no_id,
        job_pos_user1_valid_data,
):

    with patch(
            'apps.companies.services.job_position_service.JobPositionService.'
            '_add_m2m_fields'
    ) as mock_add_m2m_fields:

        # Error due to not actually adding the m2m fields
        with pytest.raises(ValidationError):
            JobPositionService.create(
                user=workspace_user1.owner,
                context=co1_child_context_ws1_user1_no_id,
                validated_data=job_pos_user1_valid_data,
            )

        mock_add_m2m_fields.assert_called_once()


@pytest.mark.django_db
def test_create_calls_m2m_non_empty_validation(
        workspace_user1,
        co1_child_context_ws1_user1_no_id,
        job_pos_user1_valid_data,
):

    with patch(
            'apps.companies.services.job_position_service.JobPositionService.'
            '_m2m_non_empty_validation'
    ) as mock_m2m_non_empty_validation:

        JobPositionService.create(
            user=workspace_user1.owner,
            context=co1_child_context_ws1_user1_no_id,
            validated_data=job_pos_user1_valid_data,
        )

        mock_m2m_non_empty_validation.assert_called_once()


@pytest.mark.django_db
def test_create_raises_error_if_a_required_m2m_field_is_empty(
        workspace_user1,
        co1_child_context_ws1_user1_no_id,
        job_pos_user1_valid_data,
):

    # Employment types is empty list
    job_pos_user1_valid_data["employment_types"] = []

    with pytest.raises(ValidationError):
        JobPositionService.create(
            user=workspace_user1.owner,
            context=co1_child_context_ws1_user1_no_id,
            validated_data=job_pos_user1_valid_data,
        )


@pytest.mark.django_db
def test_create_raises_error_if_a_required_m2m_field_is_missing(
        workspace_user1,
        co1_child_context_ws1_user1_no_id,
        job_pos_user1_valid_data,
):

    # Employment types is missing
    job_pos_user1_valid_data.pop("employment_types")

    with pytest.raises(ValidationError):
        JobPositionService.create(
            user=workspace_user1.owner,
            context=co1_child_context_ws1_user1_no_id,
            validated_data=job_pos_user1_valid_data,
        )

#   ----------------------------------- ****** -----------------------------------


# Updating

@pytest.mark.django_db
def test_update_job_position_successfully_returns_updated_job_position(
        job_position1_user1,
        job_position1_context,
        job_pos_user1_updated_valid_data
):

    job_position = JobPositionService.update(
            user=job_position1_user1.company.workspace.owner,
            context=job_position1_context,
            validated_data=job_pos_user1_updated_valid_data,
        )

    assert job_position.id == job_position1_user1.id
    assert job_position.company.workspace == job_position1_user1.company.workspace
    assert job_position.title == job_pos_user1_updated_valid_data["title"]

    assert (job_position.description ==
            job_pos_user1_updated_valid_data["description"])

    assert (list(job_position.employment_types.all()) ==
            job_pos_user1_updated_valid_data["employment_types"])

    assert (list(job_position.job_sites.all()) ==
            list(job_position1_user1.job_sites.all()))

    assert (list(job_position.tasks.all()) ==
            list(job_pos_user1_updated_valid_data["tasks"]))

    assert (list(job_position.job_sites.all()) ==
            list(job_pos_user1_updated_valid_data["job_sites"]))

    assert (list(job_position.requirements.all()) ==
            list(job_pos_user1_updated_valid_data["requirements"]))

    assert (list(job_position.benefits.all()) ==
            list(job_pos_user1_updated_valid_data["benefits"]))


@pytest.mark.django_db
def test_update_job_position_calls_resolve_job_position(
        job_position1_context,
        job_position1_user1,
        job_pos_user1_updated_valid_data,
):

    with patch(
            "apps.companies.services.job_position_service.JobPositionService."
            "_resolve_job_position"
    ) as mock_resolve_job_position:

        JobPositionService.update(
            user=job_position1_user1.company.workspace.owner,
            context=job_position1_context,
            validated_data=job_pos_user1_updated_valid_data,
        )

        mock_resolve_job_position.assert_called_once()


@pytest.mark.django_db
def test_update_calls_m2m_ownership_validation(
        workspace_user1,
        job_position1_context,
        job_pos_user1_updated_valid_data,
        job_task_user2
):

    with patch(
            'apps.companies.services.job_position_service.JobPositionService.'
            '_m2m_ownership_validation'
    ) as mock_m2m_ownership_validation:

        JobPositionService.update(
            user=workspace_user1.owner,
            context=job_position1_context,
            validated_data=job_pos_user1_updated_valid_data,
        )

        mock_m2m_ownership_validation.assert_called_once()


@pytest.mark.django_db
def test_update_calls_update_non_m2m_fields(
        workspace_user1,
        job_position1_context,
        job_pos_user1_updated_valid_data,
        job_task_user2
):

    with patch(
            'apps.companies.services.job_position_service.JobPositionService.'
            '_update_non_m2m_fields'
    ) as mock_update_non_m2m_fields:

        JobPositionService.update(
            user=workspace_user1.owner,
            context=job_position1_context,
            validated_data=job_pos_user1_updated_valid_data,
        )

        mock_update_non_m2m_fields.assert_called_once()


@pytest.mark.django_db
def test_update_calls_update_m2m_fields(
        workspace_user1,
        job_position1_context,
        job_pos_user1_updated_valid_data,
        job_task_user2
):

    with patch(
            'apps.companies.services.job_position_service.JobPositionService.'
            '_update_m2m_fields'
    ) as mock_update_m2m_fields:

        JobPositionService.update(
            user=workspace_user1.owner,
            context=job_position1_context,
            validated_data=job_pos_user1_updated_valid_data,
        )

        mock_update_m2m_fields.assert_called_once()


@pytest.mark.django_db
def test_update_raises_error_when_m2m_field_belong_to_another_user_is_used(
        workspace_user1,
        job_position1_context,
        job_pos_user1_updated_valid_data,
        job_task_user2
):

    # A job task that do not belong to the user
    job_pos_user1_updated_valid_data["tasks"] = [job_task_user2]

    with pytest.raises(ValidationError):
        JobPositionService.update(
            user=workspace_user1.owner,
            context=job_position1_context,
            validated_data=job_pos_user1_updated_valid_data,
        )


@pytest.mark.django_db
def test_update_job_position_calls_full_clean(
        workspace_user1,
        job_position1_context,
        job_pos_user1_updated_valid_data
):

    with patch('apps.companies.models.JobPosition.full_clean') as mock_full_clean:

        JobPositionService.update(
            user=workspace_user1.owner,
            context=job_position1_context,
            validated_data=job_pos_user1_updated_valid_data,
        )

        mock_full_clean.assert_called_once()


@pytest.mark.django_db
def test_update_job_position_calls_save(
        workspace_user1, job_position1_context, job_pos_user1_updated_valid_data
):

    with patch('apps.companies.models.JobPosition.save') as mock_save:

        JobPositionService.update(
            user=workspace_user1.owner,
            context=job_position1_context,
            validated_data=job_pos_user1_updated_valid_data,
        )

        mock_save.assert_called_once()


@pytest.mark.django_db
def test_update_job_position_dont_raise_error_if_a_required_m2m_field_is_missing(
        job_position1_user1,
        job_position1_context,
        job_pos_user1_updated_valid_data
):

    # Missing employment_types do NOT raise error
    job_pos_user1_updated_valid_data.pop("employment_types")

    JobPositionService.update(
        user=job_position1_user1.company.workspace.owner,
        context=job_position1_context,
        validated_data=job_pos_user1_updated_valid_data,
    )


@pytest.mark.django_db
def test_update_job_position_dont_raise_error_if_a_required_non_m2m_field_is_missing(
        job_position1_user1,
        job_position1_context,
        job_pos_user1_updated_valid_data
):

    # Missing title do NOT raise error
    job_pos_user1_updated_valid_data.pop("title")

    JobPositionService.update(
        user=job_position1_user1.company.workspace.owner,
        context=job_position1_context,
        validated_data=job_pos_user1_updated_valid_data,
    )


@pytest.mark.django_db
def test_update_calls_m2m_non_empty_validation(
        workspace_user1,
        job_position1_context,
        job_pos_user1_updated_valid_data,
):

    with patch(
            'apps.companies.services.job_position_service.JobPositionService.'
            '_m2m_non_empty_validation'
    ) as mock_m2m_non_empty_validation:

        JobPositionService.update(
            user=workspace_user1.owner,
            context=job_position1_context,
            validated_data=job_pos_user1_updated_valid_data,
        )

        mock_m2m_non_empty_validation.assert_called_once()


@pytest.mark.django_db
def test_update_raises_error_if_a_required_m2m_field_is_empty(
        workspace_user1,
        job_position1_context,
        job_pos_user1_updated_valid_data,
):

    # Job Tasks is empty
    job_pos_user1_updated_valid_data["tasks"] = []

    with pytest.raises(ValidationError):
        JobPositionService.update(
            user=workspace_user1.owner,
            context=job_position1_context,
            validated_data=job_pos_user1_updated_valid_data,
        )

#   ----------------------------------- ****** -----------------------------------

# Test Deleting


@pytest.mark.django_db
def test_remove_job_position_calls_resolve_job_position(
        job_position1_context,
        job_position1_user1,
):

    with patch(
            "apps.companies.services.job_position_service.JobPositionService."
            "_resolve_job_position"
    ) as mock_resolve_job_position:

        JobPositionService.remove(
            user=job_position1_user1.company.workspace.owner,
            context=job_position1_context,
        )

        mock_resolve_job_position.assert_called_once()

#   ----------------------------------- ****** -----------------------------------


# Test Retrieving

@pytest.mark.django_db
def test_retrieve_job_position_calls_resolve_company(user, job_position1_context):

    with patch(
            "apps.companies.services.job_position_service.JobPositionService."
            "_resolve_company"
    ) as mock_resolve_company:

        JobPositionService._resolve_job_position(
            user=user,
            context=job_position1_context,
        )

        mock_resolve_company.assert_called_once()


@pytest.mark.django_db
def test_retrieve_job_position_raises_error_if_not_found_in_company(
        job_position1_user1, job_pos1_co2_ws1_user1
):

    with pytest.raises(ValidationError):
        JobPositionService._resolve_job_position(
            user=job_position1_user1.company.workspace.owner,
            context=CompanyChildContext(
                id=job_position1_user1.id,
                workspace_id=job_pos1_co2_ws1_user1.company.workspace.workspace_id,
                company_id=job_pos1_co2_ws1_user1.company.id
            ),
        )


@pytest.mark.django_db
def test_retrieve_someone_else_job_position_raise_error(
        other_user, job_position1_context
):

    # Job Position don't belong to user
    with pytest.raises(ValidationError):
        JobPositionService._resolve_job_position(
            user=other_user,
            context=job_position1_context,
        )

#   ----------------------------------- ****** -----------------------------------
