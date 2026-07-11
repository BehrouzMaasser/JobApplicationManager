import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import EmploymentType


pytestmark = pytest.mark.django_db


@pytest.fixture
def name1() -> str:
    return "Name1"


# ---------------------------------------------------------------------------
# M-01: Persistence Schema
# ---------------------------------------------------------------------------


class TestEmploymentTypeSchema:

    def test_employment_type_requires_name(self):
        employment_type = EmploymentType(
            name=None,
        )

        with pytest.raises(ValidationError):
            employment_type.full_clean()

    def test_employment_type_name_cannot_be_empty(self):
        employment_type = EmploymentType(
            name="",
        )

        with pytest.raises(ValidationError):
            employment_type.full_clean()

    def test_valid_employment_type_creation(
        self,
        name1,
    ):
        employment_type = EmploymentType(
            name=name1,
        )

        employment_type.full_clean()
        employment_type.save()

        assert employment_type.id is not None
        assert employment_type.name == name1


class TestEmploymentTypeConstraints:

    def test_name_must_be_globally_unique(
        self,
        name1,
    ):
        EmploymentType.objects.create(
            name=name1,
        )

        with pytest.raises(IntegrityError):
            EmploymentType.objects.create(
                name=name1,
            )

    def test_name_is_case_insensitively_unique(
        self,
    ):
        EmploymentType.objects.create(
            name="Full Time",
        )

        with pytest.raises(IntegrityError):
            EmploymentType.objects.create(
                name="full time",
            )

    def test_full_clean_reports_duplicate_employment_type_name(
        self,
        name1,
    ):
        EmploymentType.objects.create(
            name=name1,
        )

        with pytest.raises(ValidationError) as exc:
            EmploymentType(
                name=name1,
            ).full_clean()

        assert (
            exc.value.error_dict["__all__"][0].code
            == "duplicate_employment_type_name"
        )


# ---------------------------------------------------------------------------
# Model Convenience Behavior
# ---------------------------------------------------------------------------


class TestEmploymentTypeProperties:

    def test_string_representation(
        self,
        name1,
    ):
        employment_type = EmploymentType(
            name=name1,
        )

        assert str(employment_type) == name1
