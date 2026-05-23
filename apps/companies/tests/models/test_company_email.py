import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from apps.companies.models import CompanyEmail


#   ----------------------------------- ****** -----------------------------------

# Invalid Creation:

@pytest.mark.django_db
def test_company_email_requires_company():

    # Company is None
    c_email = CompanyEmail(company=None, title="HR 1", email="email@gmail.com")

    with pytest.raises(ValidationError):
        c_email.full_clean()

    # Company is not provided
    c_email = CompanyEmail(title="HR 1", email="email@gmail.com")

    with pytest.raises(ValidationError):
        c_email.full_clean()


@pytest.mark.django_db
def test_company_email_requires_title(co1_ws1_user1):

    # Title is None
    c_email = CompanyEmail(
        title=None,
        company=co1_ws1_user1,
        email="email@gmail.com"
    )

    with pytest.raises(ValidationError):
        c_email.full_clean()

    # Title is not provided
    c_email = CompanyEmail(
        company=co1_ws1_user1,
        email="email@gmail.com"
    )

    with pytest.raises(ValidationError):
        c_email.full_clean()


@pytest.mark.django_db
def test_company_email_requires_non_empty_title(co1_ws1_user1):

    c_email = CompanyEmail(title="", company=co1_ws1_user1, email="email@gmail.com")

    with pytest.raises(ValidationError):
        c_email.full_clean()


@pytest.mark.django_db
def test_company_email_requires_email(co1_ws1_user1):

    # Email is None
    c_email = CompanyEmail(title="HR 1", company=co1_ws1_user1, email=None)

    with pytest.raises(ValidationError):
        c_email.full_clean()

    # Email is not provided
    c_email = CompanyEmail(title="HR 1", company=co1_ws1_user1)

    with pytest.raises(ValidationError):
        c_email.full_clean()


@pytest.mark.django_db
def test_company_email_requires_non_empty_email(co1_ws1_user1):

    c_email = CompanyEmail(title="Title", company=co1_ws1_user1, email="")

    with pytest.raises(ValidationError):
        c_email.full_clean()


#   ----------------------------------- ****** -----------------------------------

# Constraint Check:

@pytest.mark.django_db
def test_lower_case_title_and_email_is_unique_per_company(co1_ws1_user1):

    CompanyEmail.objects.create(
        title="Title",
        company=co1_ws1_user1,
        email="email@gmail.com"
    )

    with transaction.atomic():
        with pytest.raises(IntegrityError):
            CompanyEmail.objects.create(
                title="tiTLE",
                company=co1_ws1_user1,
                email="email@gmail.com"
            )

    with transaction.atomic():
        with pytest.raises(IntegrityError):
            CompanyEmail.objects.create(
                title="title",
                company=co1_ws1_user1,
                email="EMAIL@gmail.com"
            )

    with transaction.atomic():
        with pytest.raises(IntegrityError):
            CompanyEmail.objects.create(
                title="tiTLE",
                company=co1_ws1_user1,
                email="EMAIl@gmail.com"
            )


#   ----------------------------------- ****** -----------------------------------


# Valid Creation:
@pytest.mark.django_db
def test_valid_company_email(co1_ws1_user1):

    c_email = CompanyEmail(
        title="HR 1", company=co1_ws1_user1, email="email@gmail.com"
    )

    c_email.full_clean()
    c_email.save()

    assert c_email.company == co1_ws1_user1
    assert c_email.title == "HR 1"
    assert c_email.email == "email@gmail.com"


@pytest.mark.django_db
def test_same_title_in_same_company(co1_ws1_user1):

    c_email_1 = CompanyEmail(
        title="Title", company=co1_ws1_user1, email="email@gmail.com"
    )

    c_email_1.full_clean()
    c_email_1.save()

    c_email_2 = CompanyEmail(
        title="Title", company=co1_ws1_user1, email="email2@gmail.com"
    )

    c_email_2.full_clean()
    c_email_2.save()

    assert c_email_1.title == c_email_2.title

    assert c_email_1.email != c_email_2.email


@pytest.mark.django_db
def test_same_email_with_different_title_in_same_company(co1_ws1_user1):

    c_email_1 = CompanyEmail(
        title="HR 1", company=co1_ws1_user1, email="email@gmail.com"
    )

    c_email_1.full_clean()
    c_email_1.save()

    c_email_2 = CompanyEmail(
        title="HR 2", company=co1_ws1_user1, email="email@gmail.com"
    )

    c_email_2.full_clean()
    c_email_2.save()

    assert c_email_1.title != c_email_2.title
    assert c_email_1.email == c_email_2.email

    assert c_email_1.email == c_email_2.email


@pytest.mark.django_db
def test_same_title_and_email_in_different_company(
        co1_ws1_user1, co1_ws2_user1, co2_ws1_user1, co1_ws1_user2
):

    c_email_1 = CompanyEmail(
        title="HR 1", company=co1_ws1_user1, email="email@gmail.com"
    )

    c_email_1.full_clean()
    c_email_1.save()

    c_email_2 = CompanyEmail(
        title="HR 1", company=co2_ws1_user1, email="email@gmail.com"
    )

    c_email_2.full_clean()
    c_email_2.save()

    c_email_3 = CompanyEmail(
        title="HR 1", company=co1_ws2_user1, email="email@gmail.com"
    )

    c_email_2.full_clean()
    c_email_2.save()

    c_email_4 = CompanyEmail(
        title="HR 1", company=co1_ws1_user2, email="email@gmail.com"
    )

    c_email_2.full_clean()
    c_email_2.save()

    assert c_email_1.title == c_email_2.title
    assert c_email_1.title == c_email_3.title
    assert c_email_1.title == c_email_4.title

    assert c_email_1.email == c_email_2.email
    assert c_email_1.email == c_email_3.email
    assert c_email_1.email == c_email_4.email

#   ----------------------------------- ****** -----------------------------------
