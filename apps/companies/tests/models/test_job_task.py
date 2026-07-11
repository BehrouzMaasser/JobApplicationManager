import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import JobTask


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


class TestJobTaskSchema:

    def test_job_task_requires_user(
        self,
        title1,
    ):
        job_task = JobTask(
            user=None,
            title=title1,
        )

        with pytest.raises(ValidationError):
            job_task.full_clean()

    def test_job_task_requires_title(
        self,
        user1,
    ):
        job_task = JobTask(
            user=user1,
            title=None,
        )

        with pytest.raises(ValidationError):
            job_task.full_clean()

    def test_job_task_title_cannot_be_empty(
        self,
        user1,
    ):
        job_task = JobTask(
            user=user1,
            title="",
        )

        with pytest.raises(ValidationError):
            job_task.full_clean()

    def test_valid_job_task_creation(
        self,
        user1,
        title1,
        description1,
    ):
        job_task = JobTask(
            user=user1,
            title=title1,
            description=description1,
        )

        job_task.full_clean()
        job_task.save()

        assert job_task.id is not None
        assert job_task.user == user1
        assert job_task.title == title1
        assert job_task.description == description1

    def test_description_is_optional(
        self,
        user1,
        title1,
        default_description,
    ):
        job_task = JobTask(
            user=user1,
            title=title1,
        )

        job_task.full_clean()
        job_task.save()

        assert job_task.description == default_description


class TestJobTaskConstraints:

    def test_title_and_description_must_be_unique_per_user(
        self,
        user1,
        title1,
        description1,
    ):
        JobTask.objects.create(
            user=user1,
            title=title1,
            description=description1,
        )

        with pytest.raises(IntegrityError):
            JobTask.objects.create(
                user=user1,
                title=title1,
                description=description1,
            )

    def test_title_and_description_are_case_insensitively_unique_per_user(
        self,
        user1,
    ):
        JobTask.objects.create(
            user=user1,
            title="Backend Development",
            description="Build REST APIs",
        )

        with pytest.raises(IntegrityError):
            JobTask.objects.create(
                user=user1,
                title="backend development",
                description="build rest apis",
            )

    def test_full_clean_reports_duplicate_job_task(
        self,
        user1,
        title1,
        description1,
    ):
        JobTask.objects.create(
            user=user1,
            title=title1,
            description=description1,
        )

        with pytest.raises(ValidationError) as exc:
            JobTask(
                user=user1,
                title=title1,
                description=description1,
            ).full_clean()

        assert (
            exc.value.error_dict["__all__"][0].code
            == "duplicate_job_task"
        )

    def test_same_title_and_description_are_allowed_for_different_users(
        self,
        user1,
        user2,
        title1,
        description1,
    ):
        task1 = JobTask.objects.create(
            user=user1,
            title=title1,
            description=description1,
        )

        task2 = JobTask.objects.create(
            user=user2,
            title=title1,
            description=description1,
        )

        assert task1.title == task2.title
        assert task1.description == task2.description


# ---------------------------------------------------------------------------
# M-03: Persistence Normalization
# ---------------------------------------------------------------------------


class TestJobTaskNormalization:

    def test_none_description_is_normalized_to_empty_string(
        self,
        user1,
        title1,
    ):
        job_task = JobTask.objects.create(
            user=user1,
            title=title1,
            description=None,
        )

        assert job_task.description == ""

    def test_empty_description_is_preserved(
        self,
        user1,
        title1,
    ):
        job_task = JobTask.objects.create(
            user=user1,
            title=title1,
            description="",
        )

        assert job_task.description == ""

    def test_description_is_preserved(
        self,
        user1,
        title1,
        description1,
    ):
        job_task = JobTask.objects.create(
            user=user1,
            title=title1,
            description=description1,
        )

        assert job_task.description == description1


# ---------------------------------------------------------------------------
# Model Convenience Behavior
# ---------------------------------------------------------------------------


class TestJobTaskProperties:

    def test_string_representation(
        self,
        user1,
        title1,
    ):
        job_task = JobTask(
            user=user1,
            title=title1,
        )

        assert str(job_task) == title1
