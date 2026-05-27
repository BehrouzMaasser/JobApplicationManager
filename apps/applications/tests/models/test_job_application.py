from datetime import timedelta

import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone

from apps.applications.models import JobApplication


#   ----------------------------------- ****** -----------------------------------

# Invalid Creation:

@pytest.mark.django_db
def test_job_application_requires_owner(
        job_position1_co2_ws1_user1,
        status1
):

    job_application = JobApplication(
        owner=None,
        workspace=job_position1_co2_ws1_user1.company.workspace,
        job_position=job_position1_co2_ws1_user1,
        status=status1
    )

    with pytest.raises(ValidationError):
        job_application.full_clean()

    job_application = JobApplication(
        workspace=job_position1_co2_ws1_user1.company.workspace,
        job_position=job_position1_co2_ws1_user1,
        status=status1
    )

    with pytest.raises(ValidationError):
        job_application.full_clean()


@pytest.mark.django_db
def test_job_application_requires_workspace(
        job_position1_co2_ws1_user1,
        status1
):

    job_application = JobApplication(
        owner=job_position1_co2_ws1_user1.company.workspace.owner,
        workspace=None,
        job_position=job_position1_co2_ws1_user1,
        status=status1
    )

    with pytest.raises(ValidationError):
        job_application.full_clean()

    job_application = JobApplication(
        owner=job_position1_co2_ws1_user1.company.workspace.owner,
        job_position=job_position1_co2_ws1_user1,
        status=status1
    )

    with pytest.raises(ValidationError):
        job_application.full_clean()


@pytest.mark.django_db
def test_job_application_requires_job_position(
        workspace_user1,
        status1
):

    job_application = JobApplication(
        owner=workspace_user1.owner,
        workspace=workspace_user1,
        job_position=None,
        status=status1
    )

    with pytest.raises(ValidationError):
        job_application.full_clean()

    job_application = JobApplication(
        owner=workspace_user1.owner,
        workspace=workspace_user1,
        status=status1
    )

    with pytest.raises(ValidationError):
        job_application.full_clean()


@pytest.mark.django_db
def test_job_application_date_applied_should_not_be_before_job_position_posted_date(
        job_position1_co2_ws1_user1,
        status1
):

    job_position1_co2_ws1_user1.date_posted = timezone.now()

    job_application = JobApplication(
        owner=job_position1_co2_ws1_user1.company.workspace.owner,
        workspace=job_position1_co2_ws1_user1.company.workspace,
        job_position=job_position1_co2_ws1_user1,
        status=status1,
        date_applied=timezone.now() - timedelta(days=1)
    )

    with pytest.raises(ValidationError):
        job_application.full_clean()


@pytest.mark.django_db
def test_job_application_date_applied_in_future_raises_error(
        job_position1_co2_ws1_user1,
        status1
):

    job_application = JobApplication(
        owner=job_position1_co2_ws1_user1.company.workspace.owner,
        workspace=job_position1_co2_ws1_user1.company.workspace,
        job_position=job_position1_co2_ws1_user1,
        status=status1,
        date_applied=timezone.now() + timedelta(days=1)
    )

    with pytest.raises(ValidationError):
        job_application.full_clean()


# Constraint Check:

@pytest.mark.django_db
def test_job_application_is_unique_for_each_job_position_in_workspace_belong_to_user(
        job_position1_co2_ws1_user1,
        status1
):

    JobApplication.objects.create(
        owner=job_position1_co2_ws1_user1.company.workspace.owner,
        workspace=job_position1_co2_ws1_user1.company.workspace,
        job_position=job_position1_co2_ws1_user1,
        status=status1
    )

    with pytest.raises(IntegrityError):
        JobApplication.objects.create(
            owner=job_position1_co2_ws1_user1.company.workspace.owner,
            workspace=job_position1_co2_ws1_user1.company.workspace,
            job_position=job_position1_co2_ws1_user1,
            status=status1
        )


#   ----------------------------------- ****** -----------------------------------


# Valid Creation:
@pytest.mark.django_db
def test_valid_job_application(
        job_position1_co2_ws1_user1,
        status1
):

    job_application = JobApplication(
        owner=job_position1_co2_ws1_user1.company.workspace.owner,
        workspace=job_position1_co2_ws1_user1.company.workspace,
        job_position=job_position1_co2_ws1_user1,
        status=status1
    )

    job_application.full_clean()
    job_application.save()

    assert job_application.id is not None
    assert (job_application.owner ==
            job_position1_co2_ws1_user1.company.workspace.owner)

    assert (job_application.workspace.id ==
            job_position1_co2_ws1_user1.company.workspace.id)

    assert job_application.job_position.id == job_position1_co2_ws1_user1.id
    assert job_application.status.id == status1.id


@pytest.mark.django_db
def test_date_applied_is_optional(
        job_position1_co2_ws1_user1,
        status1
):

    job_application1 = JobApplication(
        owner=job_position1_co2_ws1_user1.company.workspace.owner,
        workspace=job_position1_co2_ws1_user1.company.workspace,
        job_position=job_position1_co2_ws1_user1,
        status=status1,
        date_applied=None
    )

    job_application1.full_clean()
    job_application1.save()

    assert job_application1.date_applied is None

    job_application1.delete()

    # Empty string is allowed but is converted to None
    job_application2 = JobApplication(
        owner=job_position1_co2_ws1_user1.company.workspace.owner,
        workspace=job_position1_co2_ws1_user1.company.workspace,
        job_position=job_position1_co2_ws1_user1,
        status=status1,
        date_applied=""
    )

    job_application2.full_clean()
    job_application2.save()

    assert job_application2.date_applied is None

    job_application2.delete()

    # Missing applied_date sets it to None
    job_application3 = JobApplication(
        owner=job_position1_co2_ws1_user1.company.workspace.owner,
        workspace=job_position1_co2_ws1_user1.company.workspace,
        job_position=job_position1_co2_ws1_user1,
        status=status1,
    )

    job_application3.full_clean()
    job_application3.save()

    assert job_application3.date_applied is None


@pytest.mark.django_db
def test_job_application_with_valid_date_applied(
        job_position1_co2_ws1_user1,
        status1
):

    job_position1_co2_ws1_user1.date_posted = timezone.now() - timedelta(days=1)

    job_application = JobApplication(
        owner=job_position1_co2_ws1_user1.company.workspace.owner,
        workspace=job_position1_co2_ws1_user1.company.workspace,
        job_position=job_position1_co2_ws1_user1,
        status=status1,
        date_applied=timezone.now()
    )

    job_application.full_clean()
    job_application.save()


#   ----------------------------------- ****** -----------------------------------
