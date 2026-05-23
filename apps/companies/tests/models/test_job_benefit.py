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
    job_benefit = JobBenefit(user=None, name="Name")

    with pytest.raises(ValidationError):
        job_benefit.full_clean()

    # User is not provided
    job_benefit = JobBenefit(name="Name")

    with pytest.raises(ValidationError):
        job_benefit.full_clean()

    # User is not created in database
    job_benefit = JobBenefit(user=User(email="email@gmail.com"), name="Name")

    with pytest.raises(ValidationError):
        job_benefit.full_clean()


@pytest.mark.django_db
def test_job_benefit_require_name(user):

    # Name is None
    job_benefit = JobBenefit(user=user, name=None)

    with pytest.raises(ValidationError):
        job_benefit.full_clean()

    # Name is not provided
    job_benefit = JobBenefit(user=user)

    with pytest.raises(ValidationError):
        job_benefit.full_clean()


@pytest.mark.django_db
def test_job_benefit_require_non_empty_name(user):

    job_benefit = JobBenefit(user=user, name="")

    with pytest.raises(ValidationError):
        job_benefit.full_clean()


#   ----------------------------------- ****** -----------------------------------

# Constraint Tests:

@pytest.mark.django_db
def test_job_benefit_name_and_description_is_lower_unique_for_user(user):

    job_benefit1 = JobBenefit.objects.create(user=user, name="Insurance")

    assert job_benefit1.name == "Insurance"
    assert job_benefit1.description == ""

    with transaction.atomic():
        with pytest.raises(IntegrityError):
            JobBenefit.objects.create(user=user, name="iNsuraNCE")

    job_benefit2 = JobBenefit.objects.create(
        user=user, name="Insurance", description="Good Insurance"
    )

    assert job_benefit2.name == "Insurance"
    assert job_benefit2.description == "Good Insurance"

    with transaction.atomic():
        with pytest.raises(IntegrityError):
            JobBenefit.objects.create(
                user=user, name="Insurance", description="Good INSURANCE"
            )


#   ----------------------------------- ****** -----------------------------------


# Valid Creation:

@pytest.mark.django_db
def test_job_benefit_valid_optional_description(user, other_user):

    # Description is None
    job_benefit = JobBenefit(user=user, name="Insurance", description=None)

    job_benefit.full_clean()
    job_benefit.save()

    assert job_benefit.name == "Insurance"
    assert job_benefit.description == ""

    # Description is not provided
    job_benefit = JobBenefit(user=other_user, name="Insurance")

    job_benefit.full_clean()
    job_benefit.save()

    assert job_benefit.name == "Insurance"
    assert job_benefit.description == ""


@pytest.mark.django_db
def test_job_benefit_valid_with_description(user):

    job_benefit = JobBenefit(
        user=user, name="Insurance", description="Good Insurance"
    )

    job_benefit.full_clean()
    job_benefit.save()

    assert job_benefit.name == "Insurance"
    assert job_benefit.description == "Good Insurance"


@pytest.mark.django_db
def test_job_benefit_with_same_name_and_description_is_valid_for_another_user(
        user, other_user
):

    job_benefit1 = JobBenefit(
        user=user, name="Insurance", description="Good Insurance"
    )

    job_benefit1.full_clean()
    job_benefit1.save()

    assert job_benefit1.name == "Insurance"
    assert job_benefit1.description == "Good Insurance"

    job_benefit2 = JobBenefit(
        user=other_user, name="Insurance", description="Good Insurance"
    )

    job_benefit2.full_clean()
    job_benefit2.save()

    assert job_benefit2.name == "Insurance"
    assert job_benefit2.description == "Good Insurance"


#   ----------------------------------- ****** -----------------------------------
