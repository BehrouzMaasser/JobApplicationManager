import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import JobRequirement


pytestmark = pytest.mark.django_db


@pytest.fixture
def default_description() -> str:
    return ""


@pytest.fixture
def title1() -> str:
    return "Title1"


@pytest.fixture
def description1() -> str:
    return "Description1"


# ---------------------------------------------------------------------------
# M-01: Persistence Schema
# ---------------------------------------------------------------------------


class TestJobRequirementSchema:

    def test_job_requirement_requires_user(
        self,
        title1,
    ):
        job_requirement = JobRequirement(
            user=None,
            title=title1,
        )

        with pytest.raises(ValidationError):
            job_requirement.full_clean()

    def test_job_requirement_requires_title(
        self,
        user1,
    ):
        job_requirement = JobRequirement(
            user=user1,
            title=None,
        )

        with pytest.raises(ValidationError):
            job_requirement.full_clean()

    def test_job_requirement_title_cannot_be_empty(
        self,
        user1,
    ):
        job_requirement = JobRequirement(
            user=user1,
            title="",
        )

        with pytest.raises(ValidationError):
            job_requirement.full_clean()

    def test_valid_job_requirement_creation(
        self,
        user1,
        title1,
        description1,
    ):
        job_requirement = JobRequirement(
            user=user1,
            title=title1,
            description=description1,
        )

        job_requirement.full_clean()
        job_requirement.save()

        assert job_requirement.id is not None
        assert job_requirement.user == user1
        assert job_requirement.title == title1
        assert job_requirement.description == description1

    def test_description_is_optional(
        self,
        user1,
        title1,
        default_description,
    ):
        job_requirement = JobRequirement(
            user=user1,
            title=title1,
        )

        job_requirement.full_clean()
        job_requirement.save()

        assert job_requirement.description == default_description


class TestJobRequirementConstraints:

    def test_title_and_description_must_be_unique_per_user(
        self,
        user1,
        title1,
        description1,
    ):
        JobRequirement.objects.create(
            user=user1,
            title=title1,
            description=description1,
        )

        with pytest.raises(IntegrityError):
            JobRequirement.objects.create(
                user=user1,
                title=title1,
                description=description1,
            )

    def test_title_and_description_are_case_insensitively_unique_per_user(
        self,
        user1,
    ):
        JobRequirement.objects.create(
            user=user1,
            title="Bachelor Degree",
            description="Computer Science",
        )

        with pytest.raises(IntegrityError):
            JobRequirement.objects.create(
                user=user1,
                title="bachelor degree",
                description="computer science",
            )

    def test_full_clean_reports_duplicate_job_requirement(
        self,
        user1,
        title1,
        description1,
    ):
        JobRequirement.objects.create(
            user=user1,
            title=title1,
            description=description1,
        )

        with pytest.raises(ValidationError) as exc:
            JobRequirement(
                user=user1,
                title=title1,
                description=description1,
            ).full_clean()

        assert (
            exc.value.error_dict["__all__"][0].code
            == "duplicate_job_requirement"
        )

    def test_same_title_and_description_are_allowed_for_different_users(
        self,
        user1,
        user2,
        title1,
        description1,
    ):
        requirement1 = JobRequirement.objects.create(
            user=user1,
            title=title1,
            description=description1,
        )

        requirement2 = JobRequirement.objects.create(
            user=user2,
            title=title1,
            description=description1,
        )

        assert requirement1.title == requirement2.title
        assert requirement1.description == requirement2.description


# ---------------------------------------------------------------------------
# M-03: Persistence Normalization
# ---------------------------------------------------------------------------


class TestJobRequirementNormalization:

    def test_none_description_is_normalized_to_empty_string(
        self,
        user1,
        title1,
    ):
        job_requirement = JobRequirement.objects.create(
            user=user1,
            title=title1,
            description=None,
        )

        assert job_requirement.description == ""

    def test_empty_description_is_preserved(
        self,
        user1,
        title1,
    ):
        job_requirement = JobRequirement.objects.create(
            user=user1,
            title=title1,
            description="",
        )

        assert job_requirement.description == ""

    def test_description_is_preserved(
        self,
        user1,
        title1,
        description1,
    ):
        job_requirement = JobRequirement.objects.create(
            user=user1,
            title=title1,
            description=description1,
        )

        assert job_requirement.description == description1


# ---------------------------------------------------------------------------
# Model Convenience Behavior
# ---------------------------------------------------------------------------


class TestJobRequirementProperties:

    def test_string_representation(
        self,
        user1,
        title1,
    ):
        job_requirement = JobRequirement(
            user=user1,
            title=title1,
        )

        assert str(job_requirement) == title1
