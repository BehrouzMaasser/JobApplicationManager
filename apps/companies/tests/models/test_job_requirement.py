import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import JobRequirement


pytestmark = pytest.mark.django_db

#   ----------------------------------- ****** -----------------------------------


@pytest.fixture
def default_description() -> str:

    return ""


@pytest.fixture
def title1() -> str:
    
    return "Title1"


@pytest.fixture
def description1() -> str:

    return "Description1"


class TestJobRequirementValidation:
    
    def test_job_requirement_required_user(self, title1):
        with pytest.raises(ValidationError):
            JobRequirement(user=None, title=title1).full_clean()

    def test_job_requirement_requires_title(self, user1):
        with pytest.raises(ValidationError):
            JobRequirement(user=user1, title=None).full_clean()

    def test_job_requirement_requires_non_empty_title(self, user1):
        with pytest.raises(ValidationError):
            JobRequirement(user=user1, title="").full_clean()

#   ----------------------------------- ****** -----------------------------------


class TestJobRequirementConstraint:

    def test_title_and_description_is_unique_for_each_user(
            self, user1, title1, description1
    ):
        JobRequirement.objects.create(
            user=user1, title=title1, description=description1
        )

        with pytest.raises(IntegrityError):
            JobRequirement.objects.create(
                user=user1, title=title1, description=description1
            )

    def test_same_title_and_description_raise_error_when_call_full_clean(
            self, user1, title1, description1
    ):
        JobRequirement.objects.create(
            user=user1, title=title1, description=description1
        )

        with pytest.raises(ValidationError) as e:
            JobRequirement(
                user=user1, title=title1, description=description1
            ).full_clean()

            assert e.error_dict["__all__"][0].code == "duplicate_job_requirement"

#   ----------------------------------- ****** -----------------------------------


class TestJobRequirementCreation:

    def test_valid_job_requirement_creation(self, user1, title1, description1):
        job_requirement = JobRequirement.objects.create(
            user=user1, title=title1, description=description1
        )

        assert job_requirement.user == user1
        assert job_requirement.title == title1
        assert job_requirement.description == description1

    def test_description_is_optional(self, user1, title1, default_description):
        job_requirement = JobRequirement.objects.create(user=user1, title=title1)

        assert job_requirement.user == user1
        assert job_requirement.title == title1
        assert job_requirement.description == default_description

    def test_same_title_and_description_is_valid_for_different_users(
            self, user1, user2, title1, description1
    ):
        job_requirement1 = JobRequirement.objects.create(
            user=user1, title=title1, description=description1
        )

        job_requirement2 = JobRequirement.objects.create(
            user=user2, title=title1, description=description1
        )

        assert job_requirement1.user != job_requirement2.user
        assert job_requirement1.title == job_requirement2.title
        assert job_requirement1.description == job_requirement2.description

    def test_ordering(self, user1, description1):
        requirement1 = JobRequirement.objects.create(
            user=user1, title="C", description=description1
        )
        requirement2 = JobRequirement.objects.create(
            user=user1, title="A", description=description1
        )
        requirement3 = JobRequirement.objects.create(
            user=user1, title="B", description=description1
        )

        correct_name_order = [
            requirement2,
            requirement3,
            requirement1,
        ]

        requirements = JobRequirement.objects.all()

        for requirements_correct_order, requirements_given in (
                zip(correct_name_order, requirements)):
            assert requirements_correct_order == requirements_given

#   ----------------------------------- ****** -----------------------------------


class TestJobRequirementRepresentation:

    def test_job_requirement_string_representation(
            self, user1, title1, description1
    ):
        job_requirement = JobRequirement.objects.create(
            user=user1, title=title1, description=description1
        )

        assert str(job_requirement) == job_requirement.title

#   ----------------------------------- ****** -----------------------------------
