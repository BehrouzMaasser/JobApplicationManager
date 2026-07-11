import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import JobBenefit


pytestmark = pytest.mark.django_db


@pytest.fixture
def default_description() -> str:
    return ""


@pytest.fixture
def name1() -> str:
    return "Name1"


@pytest.fixture
def description1() -> str:
    return "Description1"


# ---------------------------------------------------------------------------
# M-01: Persistence Schema
# ---------------------------------------------------------------------------


class TestJobBenefitSchema:

    def test_job_benefit_requires_user(
        self,
        name1,
    ):
        job_benefit = JobBenefit(
            user=None,
            name=name1,
        )

        with pytest.raises(ValidationError):
            job_benefit.full_clean()

    def test_job_benefit_requires_name(
        self,
        user1,
    ):
        job_benefit = JobBenefit(
            user=user1,
            name=None,
        )

        with pytest.raises(ValidationError):
            job_benefit.full_clean()

    def test_job_benefit_name_cannot_be_empty(
        self,
        user1,
    ):
        job_benefit = JobBenefit(
            user=user1,
            name="",
        )

        with pytest.raises(ValidationError):
            job_benefit.full_clean()

    def test_valid_job_benefit_creation(
        self,
        user1,
        name1,
        description1,
    ):
        job_benefit = JobBenefit(
            user=user1,
            name=name1,
            description=description1,
        )

        job_benefit.full_clean()
        job_benefit.save()

        assert job_benefit.id is not None
        assert job_benefit.user == user1
        assert job_benefit.name == name1
        assert job_benefit.description == description1

    def test_description_is_optional(
        self,
        user1,
        name1,
        default_description,
    ):
        job_benefit = JobBenefit(
            user=user1,
            name=name1,
        )

        job_benefit.full_clean()
        job_benefit.save()

        assert job_benefit.description == default_description


class TestJobBenefitConstraints:

    def test_name_and_description_must_be_unique_per_user(
        self,
        user1,
        name1,
        description1,
    ):
        JobBenefit.objects.create(
            user=user1,
            name=name1,
            description=description1,
        )

        with pytest.raises(IntegrityError):
            JobBenefit.objects.create(
                user=user1,
                name=name1,
                description=description1,
            )

    def test_name_and_description_are_case_insensitively_unique_per_user(
        self,
        user1,
    ):
        JobBenefit.objects.create(
            user=user1,
            name="Health Insurance",
            description="Private Plan",
        )

        with pytest.raises(IntegrityError):
            JobBenefit.objects.create(
                user=user1,
                name="health insurance",
                description="private plan",
            )

    def test_full_clean_reports_duplicate_job_benefit(
        self,
        user1,
        name1,
        description1,
    ):
        JobBenefit.objects.create(
            user=user1,
            name=name1,
            description=description1,
        )

        with pytest.raises(ValidationError) as exc:
            JobBenefit(
                user=user1,
                name=name1,
                description=description1,
            ).full_clean()

        assert (
            exc.value.error_dict["__all__"][0].code
            == "duplicate_job_benefit"
        )

    def test_same_name_and_description_are_allowed_for_different_users(
        self,
        user1,
        user2,
        name1,
        description1,
    ):
        benefit1 = JobBenefit.objects.create(
            user=user1,
            name=name1,
            description=description1,
        )

        benefit2 = JobBenefit.objects.create(
            user=user2,
            name=name1,
            description=description1,
        )

        assert benefit1.name == benefit2.name
        assert benefit1.description == benefit2.description


# ---------------------------------------------------------------------------
# M-03: Persistence Normalization
# ---------------------------------------------------------------------------


class TestJobBenefitNormalization:

    def test_none_description_is_normalized_to_empty_string(
        self,
        user1,
        name1,
    ):
        job_benefit = JobBenefit.objects.create(
            user=user1,
            name=name1,
            description=None,
        )

        assert job_benefit.description == ""

    def test_empty_description_is_preserved(
        self,
        user1,
        name1,
    ):
        job_benefit = JobBenefit.objects.create(
            user=user1,
            name=name1,
            description="",
        )

        assert job_benefit.description == ""

    def test_description_is_preserved(
        self,
        user1,
        name1,
        description1,
    ):
        job_benefit = JobBenefit.objects.create(
            user=user1,
            name=name1,
            description=description1,
        )

        assert job_benefit.description == description1


# ---------------------------------------------------------------------------
# Model Convenience Behavior
# ---------------------------------------------------------------------------


class TestJobBenefitProperties:

    def test_string_representation(
        self,
        user1,
        name1,
    ):
        job_benefit = JobBenefit(
            user=user1,
            name=name1,
        )

        assert str(job_benefit) == name1
