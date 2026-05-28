import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from apps.accounts.models import User
from apps.companies.models import JobTask


#   ----------------------------------- ****** -----------------------------------

# Invalid Creation:

@pytest.mark.django_db
def test_job_task_require_user():

    # User is None
    with pytest.raises(ValidationError):
        JobTask(user=None, title="Title", description="Some description").full_clean()

    # User is not provided
    with pytest.raises(ValidationError):
        JobTask(title="Title", description="Some description").full_clean()

    # User is not created in database
    with pytest.raises(ValidationError):
        JobTask(
            user=User(email="email@gmail.com"),
            title="Title",
            description="Some description"
        ).full_clean()


@pytest.mark.django_db
def test_job_task_require_title(user):

    # Title is None
    with pytest.raises(ValidationError):
        JobTask(user=user, title=None, description="Some description").full_clean()

    # Title is not provided
    with pytest.raises(ValidationError):
        JobTask(user=user, description="Some description").full_clean()


@pytest.mark.django_db
def test_job_task_require_non_empty_title():

    with pytest.raises(ValidationError):
        JobTask(title="", description="Some description").full_clean()


#   ----------------------------------- ****** -----------------------------------

# Constraint Tests:

@pytest.mark.django_db
def test_job_task_title_and_description_is_lower_unique_per_user(user):

    JobTask.objects.create(
        user=user, title="Job Task Title", description="Some description"
    )

    with transaction.atomic():
        with pytest.raises(IntegrityError):
            JobTask.objects.create(
                user=user,
                title="job Task Title",
                description="some DESCRIPTION"
            )

    # No description given
    JobTask.objects.create(
        user=user,
        title="Job Task Title2",
    )

    with transaction.atomic():
        with pytest.raises(IntegrityError):
            JobTask.objects.create(
                user=user,
                title="Job Task Title2",
            )


#   ----------------------------------- ****** -----------------------------------


# Valid Creation:

@pytest.mark.django_db
def test_job_task_description_is_optional(user):

    # Description is not provided
    job_task = JobTask(
        user=user,
        title="Job Task Title",
    )

    job_task.full_clean()
    job_task.save()

    assert job_task.id is not None
    assert job_task.title == "Job Task Title"
    assert job_task.description == ""

    # Description is None
    job_task = JobTask(
        user=user,
        title="Job Task Title2",
        description=None
    )

    job_task.full_clean()
    job_task.save()

    assert job_task.id is not None
    assert job_task.title == "Job Task Title2"
    assert job_task.description == ""


@pytest.mark.django_db
def test_job_task_description_is_set_to_empty_if_not_given_or_is_none(user):

    # Description is not provided
    job_task = JobTask(
        user=user,
        title="Job Task Title",
    )

    job_task.full_clean()
    job_task.save()

    assert job_task.id is not None
    assert job_task.title == "Job Task Title"
    assert job_task.description == ""


@pytest.mark.django_db
def test_job_task_valid_with_description(user):

    job_task = JobTask(
        user=user,
        title="Job Task Title",
        description="Some description",
    )

    job_task.full_clean()
    job_task.save()

    assert job_task.id is not None
    assert job_task.title == "Job Task Title"
    assert job_task.description == "Some description"


#   ----------------------------------- ****** -----------------------------------
