import datetime

import pytest

from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.companies.models import JobPosition


pytestmark = pytest.mark.django_db

#   ----------------------------------- ****** -----------------------------------


@pytest.fixture
def default_min_salary() -> None:

    return None


@pytest.fixture
def default_max_salary() -> None:

    return None


@pytest.fixture
def default_date_posted() -> None:

    return None


@pytest.fixture
def default_job_position_ad_url() -> None:

    return None


@pytest.fixture
def default_job_location_url() -> None:

    return None


@pytest.fixture
def default_job_portal_url() -> None:

    return None


@pytest.fixture
def default_portal_username() -> None:

    return None


@pytest.fixture
def default_portal_password() -> None:

    return None


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


class TestJobPositionValidation:

    def test_job_position_requires_company(self, title1, description1):
        with pytest.raises(ValidationError):
            JobPosition(
                title=title1, description=description1, company=None
            ).full_clean()

    def test_job_position_requires_title(self, co1_ws1_user1, description1):
        with pytest.raises(ValidationError):
            JobPosition(
                title=None, company=co1_ws1_user1, description=description1
            ).full_clean()

    def test_job_position_requires_description(self, co1_ws1_user1, title1):
        with pytest.raises(ValidationError):
            JobPosition(
                title=title1, company=co1_ws1_user1, description=None
            ).full_clean()

    def test_job_position_requires_non_empty_description(
            self, co1_ws1_user1, title1
    ):
        with pytest.raises(ValidationError):
            JobPosition(
                title=title1, company=co1_ws1_user1, description=""
            ).full_clean()

    def test_job_position_requires_non_empty_title(
            self, co1_ws1_user1, description1
    ):
        with pytest.raises(ValidationError):
            JobPosition(
                title="", company=co1_ws1_user1, description=description1
            ).full_clean()

    def test_invalid_date_posted_in_future(
            self, co1_ws1_user1, title1, description1
    ):

        future = timezone.now() + datetime.timedelta(days=1)

        with pytest.raises(ValidationError):
            JobPosition(
                title=title1,
                company=co1_ws1_user1,
                description=description1,
                date_posted=future
            ).full_clean()

    def test_min_salary_more_than_max_salary_raise_error(
            self, co1_ws1_user1, title1, description1
    ):
        with pytest.raises(ValidationError):
            JobPosition(
                title=title1,
                company=co1_ws1_user1,
                description=description1,
                min_salary=10,
                max_salary=9
            ).full_clean()

#   ----------------------------------- ****** -----------------------------------


class TestJobPositionCreation:

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

        time_now = timezone.now()

        job_position = JobPosition.objects.create(
            title=title1,
            company=co1_ws1_user1,
            description=description1,
            date_posted=time_now,
            job_position_ad_url=url1,
            job_location_url=url1,
            min_salary=salary1,
            max_salary=salary2,
            job_portal_url=url1,
            portal_username=username1,
            portal_password=password1,
        )

        assert job_position.company == co1_ws1_user1
        assert job_position.title == title1
        assert job_position.description == description1
        assert job_position.date_posted == time_now
        assert job_position.job_position_ad_url == url1
        assert job_position.job_location_url == url1
        assert job_position.min_salary == salary1
        assert job_position.max_salary == salary2
        assert job_position.job_portal_url == url1
        assert job_position.portal_username == username1
        assert job_position.portal_password == password1

    def test_optional_fields_are_optional_and_they_set_to_none_if_not_given(
            self,
            co1_ws1_user1,
            title1,
            description1,
            default_job_position_ad_url,
            default_job_location_url,
            default_min_salary,
            default_max_salary,
            default_job_portal_url,
            default_portal_username,
            default_portal_password,
            default_date_posted
    ):

        job_position = JobPosition.objects.create(
            title=title1,
            company=co1_ws1_user1,
            description=description1,
        )

        assert job_position.company == co1_ws1_user1
        assert job_position.title == title1
        assert job_position.description == description1
        assert job_position.date_posted == default_date_posted
        assert job_position.job_position_ad_url == default_job_position_ad_url
        assert job_position.job_location_url == default_job_location_url
        assert job_position.min_salary == default_min_salary
        assert job_position.max_salary == default_max_salary
        assert job_position.job_portal_url == default_job_portal_url
        assert job_position.portal_username == default_portal_username
        assert job_position.portal_password == default_portal_password

    def test_ordering(self, co1_ws1_user1, description1):
        job_position1 = JobPosition.objects.create(
            title="A", company=co1_ws1_user1, description=description1
        )
        job_position2 = JobPosition.objects.create(
            title="C", company=co1_ws1_user1, description=description1
        )
        job_position3 = JobPosition.objects.create(
            title="B", company=co1_ws1_user1, description=description1
        )
        job_position4 = JobPosition.objects.create(
            title="C-description 2", company=co1_ws1_user1, description=description1
        )
        job_position5 = JobPosition.objects.create(
            title="C-description 1", company=co1_ws1_user1, description=description1
        )

        correct_name_order = [
            job_position1,
            job_position3,
            job_position2,
            job_position5,
            job_position4
        ]

        job_positions = JobPosition.objects.all()

        for positions_correct_order, positions_given in (
                zip(correct_name_order, job_positions)):
            assert positions_correct_order == positions_given


class TestJobPositionRepresentation:

    def test_job_position_string_representation(
            self, co1_ws1_user1, title1, description1
    ):
        job_position = JobPosition.objects.create(
            title=title1, company=co1_ws1_user1, description=description1
        )

        assert str(job_position) == job_position.title

#   ----------------------------------- ****** -----------------------------------
