import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import CompanyEmail


pytestmark = pytest.mark.django_db

#   ----------------------------------- ****** -----------------------------------


@pytest.fixture
def email_address1() -> str:

    return "email1@gmail.com"


class TestCompanyEmailValidation:

    def test_company_email_requires_company(self, email_address1):
        with pytest.raises(ValidationError):
            CompanyEmail(
                title="Test", email=email_address1, company=None
            ).full_clean()

    def test_company_email_requires_title(self, co1_ws1_user1, email_address1):
        with pytest.raises(ValidationError):
            CompanyEmail(
                title=None, company=co1_ws1_user1, email=email_address1
            ).full_clean()

    def test_company_email_requires_email(self, co1_ws1_user1):
        with pytest.raises(ValidationError):
            CompanyEmail(
                title="Test", company=co1_ws1_user1, email=None
            ).full_clean()

    def test_company_email_requires_non_empty_email(self, co1_ws1_user1):
        with pytest.raises(ValidationError):
            CompanyEmail(
                title="Title", company=co1_ws1_user1, email=""
            ).full_clean()

    def test_company_email_requires_non_empty_title(
            self, co1_ws1_user1, email_address1
    ):
        with pytest.raises(ValidationError):
            CompanyEmail(
                title="", company=co1_ws1_user1, email=email_address1
            ).full_clean()


class TestCompanyEmailConstraint:

    def test_email_title_and_address_is_unique_per_company(
            self, co1_ws1_user1, email_address1
    ):
        CompanyEmail.objects.create(
            title="Test 1", company=co1_ws1_user1, email=email_address1
        )

        with pytest.raises(IntegrityError):
            CompanyEmail.objects.create(
                title="Test 1", company=co1_ws1_user1, email=email_address1
            )

    def test_same_email_title_and_address_raise_error_when_call_full_clean(
            self, co1_ws1_user1, email_address1
    ):
        CompanyEmail.objects.create(
            title="Test 1", company=co1_ws1_user1, email=email_address1
        )

        with pytest.raises(ValidationError) as e:
            CompanyEmail(
                title="Test 1", company=co1_ws1_user1, email=email_address1
            ).full_clean()

            assert e.error_dict["__all__"][0].code == "duplicate_company_email"

#   ----------------------------------- ****** -----------------------------------


class TestCompanyEmailCreation:

    def test_valid_company_email_creation(self, co1_ws1_user1, email_address1):
        company_email = CompanyEmail.objects.create(
            title="Title 1",
            company=co1_ws1_user1,
            email=email_address1
        )

        assert company_email.company == co1_ws1_user1
        assert company_email.title == "Title 1"
        assert company_email.email == email_address1

    def test_ordering(self, co1_ws1_user1, email_address1):
        company_email1 = CompanyEmail.objects.create(
            title="A", company=co1_ws1_user1, email=email_address1
        )
        company_email2 = CompanyEmail.objects.create(
            title="C", company=co1_ws1_user1, email=email_address1
        )
        company_email3 = CompanyEmail.objects.create(
            title="B", company=co1_ws1_user1, email=email_address1
        )
        company_email4 = CompanyEmail.objects.create(
            title="C-Email 2", company=co1_ws1_user1, email=email_address1
        )
        company_email5 = CompanyEmail.objects.create(
            title="C-Email 1", company=co1_ws1_user1, email=email_address1
        )

        correct_name_order = [
            company_email1,
            company_email3,
            company_email2,
            company_email5,
            company_email4
        ]

        company_emails = CompanyEmail.objects.all()

        for ems_correct_order, ems_given in zip(correct_name_order, company_emails):
            assert ems_correct_order == ems_given

    def test_other_users_with_same_email_title_and_address_is_valid(
            self, co1_ws1_user1, co1_ws1_user2, email_address1
    ):

        email1 = CompanyEmail.objects.create(
            title="Email 1", company=co1_ws1_user1, email=email_address1
        )
        email2 = CompanyEmail.objects.create(
            title="Email 1", company=co1_ws1_user2, email=email_address1
        )

        assert email1.title == "Email 1"
        assert email1.title == email2.title

        assert email1.email == email_address1
        assert email1.email == email2.email

    def test_different_companies_with_same_email_title_and_address_is_valid(
            self, co1_ws1_user1, co1_ws2_user1, email_address1
    ):

        email1 = CompanyEmail.objects.create(
            title="Email 1", company=co1_ws1_user1, email=email_address1
        )
        email2 = CompanyEmail.objects.create(
            title="Email 1", company=co1_ws2_user1, email=email_address1
        )

        assert email1.title == "Email 1"
        assert email1.title == email2.title


class TestCompanyRepresentation:

    def test_company_string_representation(self, co1_ws1_user1, email_address1):
        email = CompanyEmail.objects.create(
            title="Email 1", company=co1_ws1_user1, email=email_address1
        )

        assert str(email) == email.title

#   ----------------------------------- ****** -----------------------------------
