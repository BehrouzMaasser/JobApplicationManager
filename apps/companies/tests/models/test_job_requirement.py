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
    with pytest.raises(ValidationError):
        JobRequirement(
            user=None, title="Title", description="Some description"
        ).full_clean()

    # User is not provided
    with pytest.raises(ValidationError):
        JobRequirement(
            title="Title", description="Some description"
        ).full_clean()

    # User is not created in database
    with pytest.raises(ValidationError):
        JobRequirement(
            user=User(email="email@gmail.com"),
            title="Title",
            description="Some description"
        ).full_clean()


@pytest.mark.django_db
def test_job_requirement_require_title(user):

    # Title is None
    with pytest.raises(ValidationError):
        JobRequirement(
            user=user, title=None, description="Some description"
        ).full_clean()

    # Title is not provided
    with pytest.raises(ValidationError):
        JobRequirement(
            user=user, description="Some description"
        ).full_clean()


@pytest.mark.django_db
def test_job_requirement_require_non_empty_title(user):

    with pytest.raises(ValidationError):
        JobRequirement(
            user=user, title="", description="Some description"
        ).full_clean()


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
def test_job_requirement_description_is_optional(user):

    # Description is not provided
    job_requirement = JobRequirement(
        user=user,
        title="Title1",
    )

    job_requirement.full_clean()
    job_requirement.save()

    assert job_requirement.id is not None

    # Description is None
    job_requirement = JobRequirement(
        user=user,
        title="Title2",
        description=None
    )

    job_requirement.full_clean()
    job_requirement.save()

    assert job_requirement.id is not None


@pytest.mark.django_db
def test_job_requirement_with_description(user):

    job_requirement = JobRequirement(
        user=user,
        title="Job Requirement Title",
        description="Some description"
    )

    job_requirement.full_clean()
    job_requirement.save()

    assert job_requirement.id is not None
    assert job_requirement.title == "Job Requirement Title"
    assert job_requirement.description == "Some description"


@pytest.mark.django_db
def test_description_is_set_to_empty_string_if_not_given_or_none(user):

    job_requirement = JobRequirement(
        user=user,
        title="Job Requirement Title 1",
    )

    job_requirement.full_clean()
    job_requirement.save()

    assert job_requirement.description == ""

    job_requirement = JobRequirement(
        user=user,
        title="Job Requirement Title 2",
        description=None
    )

    job_requirement.full_clean()
    job_requirement.save()

    assert job_requirement.description == ""


#   ----------------------------------- ****** -----------------------------------
