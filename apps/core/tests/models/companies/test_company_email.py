import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import CompanyEmail


pytestmark = pytest.mark.django_db


@pytest.fixture
def email_address1() -> str:
    return "email1@gmail.com"


# ---------------------------------------------------------------------------
# M-01: Persistence Schema
# ---------------------------------------------------------------------------


class TestCompanyEmailSchema:

    def test_company_email_requires_company(
        self,
        email_address1,
    ):
        email = CompanyEmail(
            company=None,
            title="Title",
            email=email_address1,
        )

        with pytest.raises(ValidationError):
            email.full_clean()

    def test_company_email_requires_title(
        self,
        co1_ws1_user1,
        email_address1,
    ):
        email = CompanyEmail(
            company=co1_ws1_user1,
            title=None,
            email=email_address1,
        )

        with pytest.raises(ValidationError):
            email.full_clean()

    def test_company_email_title_cannot_be_empty(
        self,
        co1_ws1_user1,
        email_address1,
    ):
        email = CompanyEmail(
            company=co1_ws1_user1,
            title="",
            email=email_address1,
        )

        with pytest.raises(ValidationError):
            email.full_clean()

    def test_company_email_requires_email(
        self,
        co1_ws1_user1,
    ):
        email = CompanyEmail(
            company=co1_ws1_user1,
            title="Title",
            email=None,
        )

        with pytest.raises(ValidationError):
            email.full_clean()

    def test_company_email_cannot_be_empty(
        self,
        co1_ws1_user1,
    ):
        email = CompanyEmail(
            company=co1_ws1_user1,
            title="Title",
            email="",
        )

        with pytest.raises(ValidationError):
            email.full_clean()

    def test_valid_company_email_creation(
        self,
        co1_ws1_user1,
        email_address1,
    ):
        email = CompanyEmail(
            company=co1_ws1_user1,
            title="Work",
            email=email_address1,
        )

        email.full_clean()
        email.save()

        assert email.id is not None
        assert email.company == co1_ws1_user1
        assert email.title == "Work"
        assert email.email == email_address1


class TestCompanyEmailConstraints:

    def test_email_and_title_must_be_unique_within_company(
        self,
        co1_ws1_user1,
        email_address1,
    ):
        CompanyEmail.objects.create(
            company=co1_ws1_user1,
            title="Work",
            email=email_address1,
        )

        with pytest.raises(IntegrityError):
            CompanyEmail.objects.create(
                company=co1_ws1_user1,
                title="Work",
                email=email_address1,
            )

    def test_email_and_title_are_case_insensitively_unique_within_company(
        self,
        co1_ws1_user1,
    ):
        CompanyEmail.objects.create(
            company=co1_ws1_user1,
            title="Work",
            email="User@Example.com",
        )

        with pytest.raises(IntegrityError):
            CompanyEmail.objects.create(
                company=co1_ws1_user1,
                title="work",
                email="user@example.com",
            )

    def test_full_clean_reports_duplicate_company_email(
        self,
        co1_ws1_user1,
        email_address1,
    ):
        CompanyEmail.objects.create(
            company=co1_ws1_user1,
            title="Work",
            email=email_address1,
        )

        with pytest.raises(ValidationError) as exc:
            CompanyEmail(
                company=co1_ws1_user1,
                title="Work",
                email=email_address1,
            ).full_clean()

        assert (
            exc.value.error_dict["__all__"][0].code
            == "duplicate_company_email"
        )

    def test_same_email_and_title_are_allowed_in_different_companies(
        self,
        co1_ws1_user1,
        co1_ws2_user1,
        email_address1,
    ):
        email1 = CompanyEmail.objects.create(
            company=co1_ws1_user1,
            title="Work",
            email=email_address1,
        )

        email2 = CompanyEmail.objects.create(
            company=co1_ws2_user1,
            title="Work",
            email=email_address1,
        )

        assert email1.title == email2.title
        assert email1.email == email2.email


# ---------------------------------------------------------------------------
# M-03: Persistence Normalization
# ---------------------------------------------------------------------------


class TestCompanyEmailNormalization:

    def test_email_is_normalized_to_lowercase(
        self,
        co1_ws1_user1,
    ):
        email = CompanyEmail.objects.create(
            company=co1_ws1_user1,
            title="Work",
            email="John.Doe@Example.COM",
        )

        assert email.email == "john.doe@example.com"

    def test_lowercase_email_is_preserved(
        self,
        co1_ws1_user1,
        email_address1,
    ):
        email = CompanyEmail.objects.create(
            company=co1_ws1_user1,
            title="Work",
            email=email_address1,
        )

        assert email.email == email_address1


# ---------------------------------------------------------------------------
# Model Convenience Behavior
# ---------------------------------------------------------------------------


class TestCompanyEmailProperties:

    def test_string_representation(
        self,
        co1_ws1_user1,
        email_address1,
    ):
        email = CompanyEmail(
            company=co1_ws1_user1,
            title="Work",
            email=email_address1,
        )

        assert str(email) == "Work"
