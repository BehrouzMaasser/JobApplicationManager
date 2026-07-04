import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import JobTask


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


class TestJobTaskValidation:
    
    def test_job_task_required_user(self, title1):
        with pytest.raises(ValidationError):
            JobTask(user=None, title=title1).full_clean()

    def test_job_task_requires_title(self, user1):
        with pytest.raises(ValidationError):
            JobTask(user=user1, title=None).full_clean()

    def test_job_task_requires_non_empty_title(self, user1):
        with pytest.raises(ValidationError):
            JobTask(user=user1, title="").full_clean()

#   ----------------------------------- ****** -----------------------------------


class TestJobTaskConstraint:

    def test_title_and_description_is_unique_for_each_user(
            self, user1, title1, description1
    ):
        JobTask.objects.create(user=user1, title=title1, description=description1)

        with pytest.raises(IntegrityError):
            JobTask.objects.create(
                user=user1, title=title1, description=description1
            )

    def test_same_title_and_description_raise_error_when_call_full_clean(
            self, user1, title1, description1
    ):
        JobTask.objects.create(user=user1, title=title1, description=description1)

        with pytest.raises(ValidationError) as e:
            JobTask(user=user1, title=title1, description=description1).full_clean()

            assert e.error_dict["__all__"][0].code == "duplicate_job_task"

#   ----------------------------------- ****** -----------------------------------


class TestJobTaskCreation:

    def test_valid_job_task_creation(self, user1, title1, description1):
        job_task = JobTask.objects.create(
            user=user1, title=title1, description=description1
        )

        assert job_task.user == user1
        assert job_task.title == title1
        assert job_task.description == description1

    def test_description_is_optional(self, user1, title1, default_description):
        job_task = JobTask.objects.create(user=user1, title=title1)

        assert job_task.user == user1
        assert job_task.title == title1
        assert job_task.description == default_description

    def test_same_title_and_description_is_valid_for_different_users(
            self, user1, user2, title1, description1
    ):
        job_task1 = JobTask.objects.create(
            user=user1, title=title1, description=description1
        )

        job_task2 = JobTask.objects.create(
            user=user2, title=title1, description=description1
        )

        assert job_task1.user != job_task2.user
        assert job_task1.title == job_task2.title
        assert job_task1.description == job_task2.description

    def test_ordering(self, user1, description1):
        benefit1 = JobTask.objects.create(
            user=user1, title="C", description=description1
        )
        benefit2 = JobTask.objects.create(
            user=user1, title="A", description=description1
        )
        benefit3 = JobTask.objects.create(
            user=user1, title="B", description=description1
        )

        correct_title_order = [
            benefit2,
            benefit3,
            benefit1,
        ]

        benefits = JobTask.objects.all()

        for benefits_correct_order, benefits_given in (
                zip(correct_title_order, benefits)):
            assert benefits_correct_order == benefits_given

#   ----------------------------------- ****** -----------------------------------


class TestJobTaskRepresentation:

    def test_job_task_string_representation(self, user1, title1, description1):
        job_task = JobTask.objects.create(
            user=user1, title=title1, description=description1
        )

        assert str(job_task) == job_task.title

#   ----------------------------------- ****** -----------------------------------
