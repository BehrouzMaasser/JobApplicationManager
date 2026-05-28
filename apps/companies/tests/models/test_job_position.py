import datetime

import pytest

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.companies.models import JobPosition


#   ----------------------------------- ****** -----------------------------------

# Invalid Creation:

@pytest.mark.django_db
def test_job_position_requires_company():

    # Company is None
    with pytest.raises(ValidationError):
        JobPosition(
            company=None,
            title="Job Position",
            description="Description",
        ).full_clean()

    # Company is not provided
    with pytest.raises(ValidationError):
        JobPosition(
            title="Job Position",
            description="Description",
        ).full_clean()


@pytest.mark.django_db
def test_job_position_requires_title(co1_ws1_user1):

    # Title is None
    with pytest.raises(ValidationError):
        JobPosition(
            title=None,
            company=co1_ws1_user1,
            description="Description",
        ).full_clean()

    # Title is not provided
    with pytest.raises(ValidationError):
        JobPosition(
            company=co1_ws1_user1,
            description="Description",
        ).full_clean()


@pytest.mark.django_db
def test_job_position_requires_non_empty_title(co1_ws1_user1):

    with pytest.raises(ValidationError):
        JobPosition(
            title="",
            company=co1_ws1_user1,
            description="Something"
        ).full_clean()


@pytest.mark.django_db
def test_job_position_requires_description(co1_ws1_user1):

    # Description is None
    with pytest.raises(ValidationError):
        JobPosition(
            title="Title",
            company=co1_ws1_user1,
            description=None
        ).full_clean()

    # Description is not Provided
    with pytest.raises(ValidationError):
        JobPosition(
            title="Title",
            company=co1_ws1_user1,
        ).full_clean()


@pytest.mark.django_db
def test_job_position_requires_non_empty_description(co1_ws1_user1):

    with pytest.raises(ValidationError):
        JobPosition(
            title="Title", company=co1_ws1_user1, description=""
        ).full_clean()


@pytest.mark.django_db
def test_date_posted_with_empty_value_raise_error(co1_ws1_user1):

    # Date Posted is Empty string
    job_position = JobPosition(
        title="Title",
        company=co1_ws1_user1,
        description="Description",
        date_posted="",
    )

    with transaction.atomic():
        job_position.full_clean()
        with pytest.raises(ValidationError):
            job_position.save()


@pytest.mark.django_db
def test_min_salary_with_empty_value_raise_error(co1_ws1_user1):

    # Min-Salary is Empty string
    job_position = JobPosition(
        title="Title",
        company=co1_ws1_user1,
        description="Description",
        min_salary="",
    )

    with transaction.atomic():
        job_position.full_clean()
        with pytest.raises(ValueError):
            job_position.save()


@pytest.mark.django_db
def test_max_salary_with_empty_value_raise_error(co1_ws1_user1):

    # Max-Salary is Empty string
    job_position = JobPosition(
        title="Title",
        company=co1_ws1_user1,
        description="Description",
        max_salary="",
    )

    with transaction.atomic():
        job_position.full_clean()
        with pytest.raises(ValueError):
            job_position.save()


@pytest.mark.django_db
def test_invalid_date_posted_in_future(co1_ws1_user1):

    future = timezone.now() + datetime.timedelta(days=1)

    with pytest.raises(ValidationError):
        JobPosition(
            title="Title",
            company=co1_ws1_user1,
            description="Description",
            date_posted=future
        ).full_clean()


@pytest.mark.django_db
def test_invalid_min_and_max_salary(co1_ws1_user1):

    with pytest.raises(ValidationError):
        JobPosition(
            title="Title",
            company=co1_ws1_user1,
            description="Description",
            min_salary=10,
            max_salary=9
        ).full_clean()


@pytest.mark.django_db
def test_invalid_job_position_ad_url(co1_ws1_user1):

    # URL missing HTTPS://
    with pytest.raises(ValidationError):
        JobPosition(
            title="Title",
            company=co1_ws1_user1,
            description="Description",
            job_position_ad_url="www.google.com"
        ).full_clean()


@pytest.mark.django_db
def test_invalid_job_location_url(co1_ws1_user1):

    # URL missing HTTPS://
    with pytest.raises(ValidationError):
        JobPosition(
            title="Title",
            company=co1_ws1_user1,
            description="Description",
            job_location_url="www.google.com"
        ).full_clean()


@pytest.mark.django_db
def test_invalid_job_portal_url(co1_ws1_user1):

    # URL missing HTTPS://
    with pytest.raises(ValidationError):
        JobPosition(
            title="Title",
            company=co1_ws1_user1,
            description="Description",
            job_portal_url="www.google.com"
        ).full_clean()


#   ----------------------------------- ****** -----------------------------------


# Valid Creation:
@pytest.mark.django_db
def test_valid_minimal_job_position(co1_ws1_user1):

    # No Many-To-Many Fields are allowed upon creation
    job_position = JobPosition(
        title="Title",
        company=co1_ws1_user1,
        description="Description"
    )

    job_position.full_clean()
    job_position.save()

    assert job_position.id is not None
    assert job_position.title == "Title"
    assert job_position.description == "Description"
    assert job_position.company.id == co1_ws1_user1.id


@pytest.mark.django_db
def test_valid_job_position_with_date_posted(co1_ws1_user1):

    now = timezone.now()

    job_position = JobPosition(
        title="Title",
        company=co1_ws1_user1,
        description="Description",
        date_posted=now
    )

    job_position.full_clean()
    job_position.save()

    assert job_position.date_posted == now


@pytest.mark.django_db
def test_valid_job_position_with_min_salary(co1_ws1_user1):

    job_position = JobPosition(
        title="Title",
        company=co1_ws1_user1,
        description="Description",
        min_salary=10
    )

    job_position.full_clean()
    job_position.save()

    assert job_position.min_salary == 10


@pytest.mark.django_db
def test_valid_job_position_with_max_salary(co1_ws1_user1):

    job_position = JobPosition(
        title="Title",
        company=co1_ws1_user1,
        description="Description",
        max_salary=10
    )

    job_position.full_clean()
    job_position.save()

    assert job_position.max_salary == 10


@pytest.mark.django_db
def test_valid_job_position_with_min_and_max_salary(co1_ws1_user1):

    # Same max and min
    job_position = JobPosition(
        title="Title",
        company=co1_ws1_user1,
        description="Description",
        min_salary=10,
        max_salary=10
    )

    job_position.full_clean()
    job_position.save()

    assert job_position.min_salary == 10
    assert job_position.max_salary == 10

    job_position = JobPosition(
        title="Title",
        company=co1_ws1_user1,
        description="Description",
        min_salary=10,
        max_salary=12
    )

    job_position.full_clean()
    job_position.save()

    assert job_position.min_salary == 10
    assert job_position.max_salary == 12


@pytest.mark.django_db
def test_valid_job_position_with_job_position_ad_url(co1_ws1_user1):

    job_position = JobPosition(
        title="Title",
        company=co1_ws1_user1,
        description="Description",
        job_position_ad_url="https://www.google.com"
    )

    job_position.full_clean()
    job_position.save()

    assert job_position.job_position_ad_url == "https://www.google.com"


@pytest.mark.django_db
def test_valid_job_position_with_job_location_url(co1_ws1_user1):

    job_position = JobPosition(
        title="Title",
        company=co1_ws1_user1,
        description="Description",
        job_location_url="https://www.google.com"
    )

    job_position.full_clean()
    job_position.save()

    assert job_position.job_location_url == "https://www.google.com"


@pytest.mark.django_db
def test_valid_job_position_with_job_portal_url(co1_ws1_user1):

    job_position = JobPosition(
        title="Title",
        company=co1_ws1_user1,
        description="Description",
        job_portal_url="https://www.google.com"
    )

    job_position.full_clean()
    job_position.save()

    assert job_position.job_portal_url == "https://www.google.com"


@pytest.mark.django_db
def test_same_title_in_different_company_is_allowed(
        co1_ws1_user1, co2_ws1_user1, co1_ws2_user1, co1_ws1_user2
):

    job_position_1 = JobPosition(
        title="Title", company=co1_ws1_user1, description="Description"
    )

    job_position_1.full_clean()
    job_position_1.save()

    job_position_2 = JobPosition(
        title="Title", company=co2_ws1_user1, description="Description"
    )

    job_position_2.full_clean()
    job_position_2.save()

    job_position_3 = JobPosition(
        title="Title", company=co1_ws2_user1, description="Description"
    )

    job_position_3.full_clean()
    job_position_3.save()

    job_position_4 = JobPosition(
        title="Title", company=co1_ws1_user2, description="Description"
    )

    job_position_4.full_clean()
    job_position_4.save()

    assert job_position_1.title == job_position_2.title
    assert job_position_1.title == job_position_3.title
    assert job_position_1.title == job_position_4.title

    assert job_position_1.company != job_position_2.company
    assert job_position_1.company != job_position_3.company
    assert job_position_1.company != job_position_4.company


@pytest.mark.django_db
def test_same_job_position_in_same_company_is_allowed(co1_ws1_user1):

    job_position_1 = JobPosition.objects.create(
        title="Title", company=co1_ws1_user1, description="Description"
    )

    job_position_2 = JobPosition.objects.create(
        title="Title", company=co1_ws1_user1, description="Description"
    )

    assert job_position_1.title == job_position_2.title
    assert job_position_1.description == job_position_2.description
    assert job_position_1.company.id == job_position_2.company.id


@pytest.mark.django_db
def test_optional_non_m2m_fields_with_none_do_not_raise_error(co1_ws1_user1):

    # Date Posted is None
    job_position = JobPosition(
        title="Title",
        company=co1_ws1_user1,
        description="Description",
    )

    job_position.full_clean()
    job_position.save()

    assert job_position.id is not None


@pytest.mark.django_db
def test_job_position_ad_url_with_empty_string_sets_it_to_none(co1_ws1_user1):

    # Job Position Ad URL is Empty string
    job_position = JobPosition(
        title="Title",
        company=co1_ws1_user1,
        description="Description",
        job_position_ad_url="",
    )

    job_position.full_clean()
    job_position.save()

    assert job_position.job_position_ad_url is None


@pytest.mark.django_db
def test_job_location_url_with_empty_string_sets_it_to_none(co1_ws1_user1):

    # Job Location URL is Empty string
    job_position = JobPosition(
        title="Title",
        company=co1_ws1_user1,
        description="Description",
        job_location_url="",
    )

    job_position.full_clean()
    job_position.save()

    assert job_position.job_location_url is None


@pytest.mark.django_db
def test_job_portal_url_with_empty_string_sets_it_to_none(co1_ws1_user1):

    # Job Portal URL is Empty string
    job_position = JobPosition(
        title="Title",
        company=co1_ws1_user1,
        description="Description",
        job_portal_url="",
    )

    job_position.full_clean()
    job_position.save()

    assert job_position.job_portal_url is None


@pytest.mark.django_db
def test_portal_username_with_empty_string_sets_it_to_none(co1_ws1_user1):

    # Portal Username is Empty string
    job_position = JobPosition(
        title="Title",
        company=co1_ws1_user1,
        description="Description",
        portal_username="",
    )

    job_position.full_clean()
    job_position.save()

    assert job_position.portal_username is None


@pytest.mark.django_db
def test_portal_password_with_empty_string_sets_it_to_none(co1_ws1_user1):

    # Portal Password is Empty string
    job_position = JobPosition(
        title="Title",
        company=co1_ws1_user1,
        description="Description",
        portal_password="",
    )

    job_position.full_clean()
    job_position.save()

    assert job_position.portal_password is None

#   ----------------------------------- ****** -----------------------------------
