import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from apps.accounts.models import User
from apps.companies.models import JobRequirement


#   ----------------------------------- ****** -----------------------------------

# Invalid Creation:

@pytest.mark.django_db
def test_job_requirement_require_user():

    # User is None
    job_requirement = JobRequirement(
        user=None, title="Title", description="Some description"
    )

    with pytest.raises(ValidationError):
        job_requirement.full_clean()

    # User is not provided
    job_requirement = JobRequirement(
        title="Title", description="Some description"
    )

    with pytest.raises(ValidationError):
        job_requirement.full_clean()

    # User is not created in database
    job_requirement = JobRequirement(
        user=User(email="email@gmail.com"),
        title="Title",
        description="Some description"
    )

    with pytest.raises(ValidationError):
        job_requirement.full_clean()


@pytest.mark.django_db
def test_job_requirement_require_title(user):

    # Title is None
    job_requirement = JobRequirement(
        user=user, title=None, description="Some description"
    )

    with pytest.raises(ValidationError):
        job_requirement.full_clean()

    # Title is not provided
    job_requirement = JobRequirement(
        user=user, description="Some description"
    )

    with pytest.raises(ValidationError):
        job_requirement.full_clean()


@pytest.mark.django_db
def test_job_requirement_require_non_empty_title(user):

    job_requirement = JobRequirement(
        user=user, title="", description="Some description"
    )

    with pytest.raises(ValidationError):
        job_requirement.full_clean()


#   ----------------------------------- ****** -----------------------------------

# Constraint Tests:

@pytest.mark.django_db
def test_job_requirement_title_and_description_is_lower_unique_per_user(user):

    JobRequirement.objects.create(
        user=user,
        title="Job Requirement Title",
        description="Some description"
    )

    with transaction.atomic():
        with pytest.raises(IntegrityError):
            JobRequirement.objects.create(
                user=user,
                title="job Requirement Title",
                description="some DESCRIPTION"
            )

    # With no description
    JobRequirement.objects.create(
        user=user,
        title="Job Requirement Title",
    )

    with transaction.atomic():
        with pytest.raises(IntegrityError):
            JobRequirement.objects.create(
                user=user,
                title="Job Requirement Title",
            )


#   ----------------------------------- ****** -----------------------------------


# Valid Creation:

@pytest.mark.django_db
def test_job_requirement_valid_optional_description(user):

    # Description is not provided
    job_requirement = JobRequirement(
        user=user,
        title="Title1",
    )

    job_requirement.full_clean()
    job_requirement.save()

    assert job_requirement.title == "Title1"
    assert job_requirement.description == ""

    # Description is None
    job_requirement = JobRequirement(
        user=user,
        title="Title2",
        description=None
    )

    job_requirement.full_clean()
    job_requirement.save()

    assert job_requirement.title == "Title2"
    assert job_requirement.description == ""


@pytest.mark.django_db
def test_job_requirement_valid_with_description(user):

    job_requirement = JobRequirement(
        user=user,
        title="Job Requirement Title",
        description="Some description"
    )

    job_requirement.full_clean()
    job_requirement.save()

    assert job_requirement.title == "Job Requirement Title"
    assert job_requirement.description == "Some description"


#   ----------------------------------- ****** -----------------------------------
