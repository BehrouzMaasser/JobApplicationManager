import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import EmploymentType


pytestmark = pytest.mark.django_db

#   ----------------------------------- ****** -----------------------------------


@pytest.fixture
def name1() -> str:
    
    return "Name1"


class TestEmploymentTypeValidation:

    def test_employment_type_requires_name(self):
        with pytest.raises(ValidationError):
            EmploymentType(name=None).full_clean()

    def test_employment_type_requires_non_empty_name(self):
        with pytest.raises(ValidationError):
            EmploymentType(name="").full_clean()

#   ----------------------------------- ****** -----------------------------------


class TestEmploymentTypeConstraint:

    def test_name_is_unique(self, name1):
        EmploymentType.objects.create(name=name1)

        with pytest.raises(IntegrityError):
            EmploymentType.objects.create(name=name1)

    def test_same_name_raise_error_when_call_full_clean(self, name1):
        EmploymentType.objects.create(name=name1)

        with pytest.raises(ValidationError) as e:
            EmploymentType(name=name1).full_clean()

            assert (e.error_dict["__all__"][0].code ==
                    "duplicate_employment_type_name")

#   ----------------------------------- ****** -----------------------------------


class TestEmploymentTypeCreation:

    def test_valid_employment_type_creation(self, name1):
        employment_type = EmploymentType.objects.create(name=name1)

        assert employment_type.name == name1

    def test_ordering(self):
        emp_type1 = EmploymentType.objects.create(name="C")
        emp_type2 = EmploymentType.objects.create(name="A")
        emp_type3 = EmploymentType.objects.create(name="B")

        correct_name_order = [
            emp_type2,
            emp_type3,
            emp_type1,
        ]

        emp_types = EmploymentType.objects.all()

        for emp_types_correct_order, emp_types_given in (
                zip(correct_name_order, emp_types)):
            assert emp_types_correct_order == emp_types_given

#   ----------------------------------- ****** -----------------------------------


class TestEmploymentTypeRepresentation:

    def test_employment_type_string_representation(self, name1):
        employment_type = EmploymentType.objects.create(name=name1)

        assert str(employment_type) == employment_type.name


#   ----------------------------------- ****** -----------------------------------
