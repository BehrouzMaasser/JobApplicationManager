import datetime

import pytest

from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.companies.models import JobPosition


pytestmark = pytest.mark.django_db


@pytest.fixture
def title1() -> str:
    return "Title 1"


@pytest.fixture
def description1() -> str:
    return "Description 1"


@pytest.fixture
def salary1() -> int:
    return 10


@pytest.fixture
def salary2() -> int:
    return 12


@pytest.fixture
def url1() -> str:
    return "https://someurl.com"


@pytest.fixture
def username1() -> str:
    return "username1"


@pytest.fixture
def password1() -> str:
    return "password1"


# ---------------------------------------------------------------------------
# M-01: Persistence Schema
# ---------------------------------------------------------------------------


class TestJobPositionSchema:

    def test_job_position_requires_company(
        self,
        title1,
        description1,
    ):
        job_position = JobPosition(
            company=None,
            title=title1,
            description=description1,
        )

        with pytest.raises(ValidationError):
            job_position.full_clean()

    def test_job_position_requires_title(
        self,
        co1_ws1_user1,
        description1,
    ):
        job_position = JobPosition(
            company=co1_ws1_user1,
            title=None,
            description=description1,
        )

        with pytest.raises(ValidationError):
            job_position.full_clean()

    def test_job_position_title_cannot_be_empty(
        self,
        co1_ws1_user1,
        description1,
    ):
        job_position = JobPosition(
            company=co1_ws1_user1,
            title="",
            description=description1,
        )

        with pytest.raises(ValidationError):
            job_position.full_clean()

    def test_job_position_requires_description(
        self,
        co1_ws1_user1,
        title1,
    ):
        job_position = JobPosition(
            company=co1_ws1_user1,
            title=title1,
            description=None,
        )

        with pytest.raises(ValidationError):
            job_position.full_clean()

    def test_job_position_description_cannot_be_empty(
        self,
        co1_ws1_user1,
        title1,
    ):
        job_position = JobPosition(
            company=co1_ws1_user1,
            title=title1,
            description="",
        )

        with pytest.raises(ValidationError):
            job_position.full_clean()

    def test_valid_job_position_creation(
        self,
        co1_ws1_user1,
        title1,
        description1,
        salary1,
        salary2,
        url1,
        username1,
        password1,
    ):
        job_position = JobPosition(
            company=co1_ws1_user1,
            title=title1,
            description=description1,
            date_posted=timezone.now(),
            min_salary=salary1,
            max_salary=salary2,
            job_position_ad_url=url1,
            job_location_url=url1,
            job_portal_url=url1,
            portal_username=username1,
            portal_password=password1,
        )

        job_position.full_clean()
        job_position.save()

        assert job_position.id is not None
        assert job_position.company == co1_ws1_user1
        assert job_position.title == title1
        assert job_position.description == description1
        assert job_position.min_salary == salary1
        assert job_position.max_salary == salary2


# ---------------------------------------------------------------------------
# M-02: Domain Invariants
# ---------------------------------------------------------------------------


class TestJobPositionValidation:

    def test_date_posted_cannot_be_in_future(
        self,
        co1_ws1_user1,
        title1,
        description1,
    ):
        job_position = JobPosition(
            company=co1_ws1_user1,
            title=title1,
            description=description1,
            date_posted=(
                timezone.now()
                + datetime.timedelta(days=1)
            ),
        )

        with pytest.raises(ValidationError):
            job_position.full_clean()

    def test_min_salary_cannot_exceed_max_salary(
        self,
        co1_ws1_user1,
        title1,
        description1,
    ):
        job_position = JobPosition(
            company=co1_ws1_user1,
            title=title1,
            description=description1,
            min_salary=100,
            max_salary=50,
        )

        with pytest.raises(ValidationError):
            job_position.full_clean()

    def test_min_salary_equal_to_max_salary_is_valid(
        self,
        co1_ws1_user1,
        title1,
        description1,
    ):
        job_position = JobPosition(
            company=co1_ws1_user1,
            title=title1,
            description=description1,
            min_salary=100,
            max_salary=100,
        )

        job_position.full_clean()


# ---------------------------------------------------------------------------
# M-03: Persistence Normalization
# ---------------------------------------------------------------------------


class TestJobPositionNormalization:

    def test_empty_optional_text_fields_are_normalized_to_none(
        self,
        co1_ws1_user1,
        title1,
        description1,
    ):
        job_position = JobPosition.objects.create(
            company=co1_ws1_user1,
            title=title1,
            description=description1,
            job_position_ad_url="",
            job_location_url="",
            job_portal_url="",
            portal_username="",
            portal_password="",
        )

        assert job_position.job_position_ad_url is None
        assert job_position.job_location_url is None
        assert job_position.job_portal_url is None
        assert job_position.portal_username is None
        assert job_position.portal_password is None

    def test_optional_fields_are_none_by_default(
        self,
        co1_ws1_user1,
        title1,
        description1,
    ):
        job_position = JobPosition.objects.create(
            company=co1_ws1_user1,
            title=title1,
            description=description1,
        )

        assert job_position.job_position_ad_url is None
        assert job_position.job_location_url is None
        assert job_position.job_portal_url is None
        assert job_position.portal_username is None
        assert job_position.portal_password is None


# ---------------------------------------------------------------------------
# Model Convenience Behavior
# ---------------------------------------------------------------------------


class TestJobPositionProperties:

    def test_string_representation(
        self,
        co1_ws1_user1,
        title1,
    ):
        job_position = JobPosition(
            company=co1_ws1_user1,
            title=title1,
        )

        assert str(job_position) == title1
