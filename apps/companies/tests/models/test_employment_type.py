import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import EmploymentType


#   ----------------------------------- ****** -----------------------------------

# Invalid Creation:

@pytest.mark.django_db
def test_employment_type_require_name():

    # Name is None
    employment_type = EmploymentType(name=None)

    with pytest.raises(ValidationError):
        employment_type.full_clean()

    # Name is not provided
    employment_type = EmploymentType()

    with pytest.raises(ValidationError):
        employment_type.full_clean()


@pytest.mark.django_db
def test_employment_type_require_non_empty_name():

    employment_type = EmploymentType(name="")

    with pytest.raises(ValidationError):
        employment_type.full_clean()


#   ----------------------------------- ****** -----------------------------------

# Constraint Tests:

@pytest.mark.django_db
def test_employment_type_name_is_lower_unique():

    EmploymentType.objects.create(name="Full-Time")

    with pytest.raises(IntegrityError):
        EmploymentType.objects.create(name="fULL-time")


#   ----------------------------------- ****** -----------------------------------


# Valid Creation:

@pytest.mark.django_db
def test_employment_type_valid():

    employment_type = EmploymentType(name="Full-Time")

    employment_type.full_clean()
    employment_type.save()

    assert employment_type.name == "Full-Time"


#   ----------------------------------- ****** -----------------------------------
