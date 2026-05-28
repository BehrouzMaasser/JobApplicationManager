import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from apps.accounts.models import User
from apps.companies.models import JobBenefit


#   ----------------------------------- ****** -----------------------------------

# Invalid Creation:

@pytest.mark.django_db
def test_job_benefit_require_user():

    # User is None
    with pytest.raises(ValidationError):
        JobBenefit(user=None, name="Name").full_clean()

    # User is not provided
    with pytest.raises(ValidationError):
        JobBenefit(name="Name").full_clean()

    # User is not created in database
    with pytest.raises(ValidationError):
        JobBenefit(user=User(email="email@gmail.com"), name="Name").full_clean()


@pytest.mark.django_db
def test_job_benefit_require_name(user):

    # Name is None
    with pytest.raises(ValidationError):
        JobBenefit(user=user, name=None).full_clean()

    # Name is not provided
    with pytest.raises(ValidationError):
        JobBenefit(user=user).full_clean()


@pytest.mark.django_db
def test_job_benefit_require_non_empty_name(user):

    with pytest.raises(ValidationError):
        JobBenefit(user=user, name="").full_clean()


#   ----------------------------------- ****** -----------------------------------

# Constraint Tests:

@pytest.mark.django_db
def test_job_benefit_name_and_description_should_be_lower_unique_for_user(user):

    JobBenefit.objects.create(user=user, name="Insurance")

    with transaction.atomic():
        with pytest.raises(IntegrityError):
            JobBenefit.objects.create(user=user, name="iNsuraNCE")

    JobBenefit.objects.create(
        user=user, name="Insurance", description="Good Insurance"
    )

    with transaction.atomic():
        with pytest.raises(IntegrityError):
            JobBenefit.objects.create(
                user=user, name="Insurance", description="Good INSURANCE"
            )


#   ----------------------------------- ****** -----------------------------------


# Valid Creation:

@pytest.mark.django_db
def test_description_is_optional(user):

    # Description is None
    job_benefit = JobBenefit(user=user, name="Insurance", description=None)

    job_benefit.full_clean()
    job_benefit.save()

    assert job_benefit.id is not None


@pytest.mark.django_db
def test_description_is_set_to_empty_string_if_not_given_or_none(user):

    # Description is None
    job_benefit = JobBenefit(user=user, name="Insurance", description=None)

    job_benefit.full_clean()
    job_benefit.save()

    assert job_benefit.id is not None
    assert job_benefit.description == ""


@pytest.mark.django_db
def test_job_benefit_with_description(user):

    job_benefit = JobBenefit(
        user=user, name="Insurance", description="Good Insurance"
    )

    job_benefit.full_clean()
    job_benefit.save()

    assert job_benefit.id is not None
    assert job_benefit.name == "Insurance"
    assert job_benefit.description == "Good Insurance"


@pytest.mark.django_db
def test_job_benefit_with_same_name_and_description_is_valid_for_another_user(
        user, other_user
):

    job_benefit = JobBenefit(
        user=user, name="Insurance", description="Good Insurance"
    )

    job_benefit.full_clean()
    job_benefit.save()

    assert job_benefit.id is not None
    assert job_benefit.name == "Insurance"
    assert job_benefit.description == "Good Insurance"

    job_benefit = JobBenefit(
        user=other_user, name="Insurance", description="Good Insurance"
    )

    job_benefit.full_clean()
    job_benefit.save()

    assert job_benefit.id is not None
    assert job_benefit.name == "Insurance"
    assert job_benefit.description == "Good Insurance"


#   ----------------------------------- ****** -----------------------------------
