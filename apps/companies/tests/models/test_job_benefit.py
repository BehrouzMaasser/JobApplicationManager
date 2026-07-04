import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import JobBenefit


pytestmark = pytest.mark.django_db

#   ----------------------------------- ****** -----------------------------------


@pytest.fixture
def default_description() -> str:

    return ""


@pytest.fixture
def name1() -> str:
    
    return "Name1"


@pytest.fixture
def description1() -> str:

    return "Description1"


class TestJobBenefitValidation:
    
    def test_job_benefit_required_user(self, name1):
        with pytest.raises(ValidationError):
            JobBenefit(user=None, name=name1).full_clean()

    def test_job_benefit_requires_name(self, user1):
        with pytest.raises(ValidationError):
            JobBenefit(user=user1, name=None).full_clean()

    def test_job_benefit_requires_non_empty_name(self, user1):
        with pytest.raises(ValidationError):
            JobBenefit(user=user1, name="").full_clean()

#   ----------------------------------- ****** -----------------------------------


class TestJobBenefitConstraint:

    def test_name_and_description_is_unique_for_each_user(
            self, user1, name1, description1
    ):
        JobBenefit.objects.create(user=user1, name=name1, description=description1)

        with pytest.raises(IntegrityError):
            JobBenefit.objects.create(
                user=user1, name=name1, description=description1
            )

    def test_same_name_and_description_raise_error_when_call_full_clean(
            self, user1, name1, description1
    ):
        JobBenefit.objects.create(user=user1, name=name1, description=description1)

        with pytest.raises(ValidationError) as e:
            JobBenefit(user=user1, name=name1, description=description1).full_clean()

            assert e.error_dict["__all__"][0].code == "duplicate_job_benefit"

#   ----------------------------------- ****** -----------------------------------


class TestJobBenefitCreation:

    def test_valid_job_benefit_creation(self, user1, name1, description1):
        job_benefit = JobBenefit.objects.create(
            user=user1, name=name1, description=description1
        )

        assert job_benefit.user == user1
        assert job_benefit.name == name1
        assert job_benefit.description == description1

    def test_description_is_optional(self, user1, name1, default_description):
        job_benefit = JobBenefit.objects.create(user=user1, name=name1)

        assert job_benefit.user == user1
        assert job_benefit.name == name1
        assert job_benefit.description == default_description

    def test_same_name_and_description_is_valid_for_different_users(
            self, user1, user2, name1, description1
    ):
        job_benefit1 = JobBenefit.objects.create(
            user=user1, name=name1, description=description1
        )

        job_benefit2 = JobBenefit.objects.create(
            user=user2, name=name1, description=description1
        )

        assert job_benefit1.user != job_benefit2.user
        assert job_benefit1.name == job_benefit2.name
        assert job_benefit1.description == job_benefit2.description

    def test_ordering(self, user1, description1):
        benefit1 = JobBenefit.objects.create(
            user=user1, name="C", description=description1
        )
        benefit2 = JobBenefit.objects.create(
            user=user1, name="A", description=description1
        )
        benefit3 = JobBenefit.objects.create(
            user=user1, name="B", description=description1
        )

        correct_name_order = [
            benefit2,
            benefit3,
            benefit1,
        ]

        benefits = JobBenefit.objects.all()

        for benefits_correct_order, benefits_given in (
                zip(correct_name_order, benefits)):
            assert benefits_correct_order == benefits_given

#   ----------------------------------- ****** -----------------------------------


class TestJobBenefitRepresentation:

    def test_job_benefit_string_representation(self, user1, name1, description1):
        job_benefit = JobBenefit.objects.create(
            user=user1, name=name1, description=description1
        )

        assert str(job_benefit) == job_benefit.name

#   ----------------------------------- ****** -----------------------------------
