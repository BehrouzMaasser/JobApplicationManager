import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import Company


pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------
# M-01: Persistence Schema
# ---------------------------------------------------------------------------


class TestCompanySchema:

    def test_company_requires_workspace(self):
        company = Company(
            workspace=None,
            name="Test Company",
        )

        with pytest.raises(ValidationError):
            company.full_clean()

    def test_company_requires_name(
        self,
        workspace1_user1,
    ):
        company = Company(
            workspace=workspace1_user1,
            name=None,
        )

        with pytest.raises(ValidationError):
            company.full_clean()

    def test_company_name_cannot_be_empty(
        self,
        workspace1_user1,
    ):
        company = Company(
            workspace=workspace1_user1,
            name="",
        )

        with pytest.raises(ValidationError):
            company.full_clean()

    def test_valid_company_creation(
        self,
        workspace1_user1,
    ):
        company = Company(
            workspace=workspace1_user1,
            name="Company 1",
            website="https://www.google.com",
        )

        company.full_clean()
        company.save()

        assert company.id is not None
        assert company.workspace == workspace1_user1
        assert company.name == "Company 1"
        assert company.website == "https://www.google.com"

    def test_website_is_optional(
        self,
        workspace1_user1,
    ):
        company = Company(
            workspace=workspace1_user1,
            name="Company 1",
            website=None,
        )

        company.full_clean()
        company.save()

        assert company.website is None


class TestCompanyConstraints:

    def test_company_name_must_be_unique_within_workspace(
        self,
        workspace1_user1,
    ):
        Company.objects.create(
            workspace=workspace1_user1,
            name="Company 1",
        )

        with pytest.raises(IntegrityError):
            Company.objects.create(
                workspace=workspace1_user1,
                name="Company 1",
            )

    def test_company_name_is_case_insensitively_unique_within_workspace(
        self,
        workspace1_user1,
    ):
        Company.objects.create(
            workspace=workspace1_user1,
            name="Company 1",
        )

        with pytest.raises(IntegrityError):
            Company.objects.create(
                workspace=workspace1_user1,
                name="company 1",
            )

    def test_full_clean_reports_duplicate_company_name(
        self,
        workspace1_user1,
    ):
        Company.objects.create(
            workspace=workspace1_user1,
            name="Company 1",
        )

        with pytest.raises(ValidationError) as exc:
            Company(
                workspace=workspace1_user1,
                name="Company 1",
            ).full_clean()

        assert (
            exc.value.error_dict["__all__"][0].code
            == "duplicate_company_name"
        )

    def test_same_company_name_is_allowed_in_different_workspaces(
        self,
        workspace1_user1,
        workspace2_user1,
    ):
        company1 = Company.objects.create(
            workspace=workspace1_user1,
            name="Company 1",
        )

        company2 = Company.objects.create(
            workspace=workspace2_user1,
            name="Company 1",
        )

        assert company1.name == company2.name


# ---------------------------------------------------------------------------
# M-03: Persistence Normalization
# ---------------------------------------------------------------------------


class TestCompanyNormalization:

    def test_empty_website_is_normalized_to_none(
        self,
        workspace1_user1,
    ):
        company = Company.objects.create(
            workspace=workspace1_user1,
            name="Company 1",
            website="",
        )

        assert company.website is None

    def test_none_website_remains_none(
        self,
        workspace1_user1,
    ):
        company = Company.objects.create(
            workspace=workspace1_user1,
            name="Company 1",
            website=None,
        )

        assert company.website is None

    def test_valid_website_is_preserved(
        self,
        workspace1_user1,
    ):
        company = Company.objects.create(
            workspace=workspace1_user1,
            name="Company 1",
            website="https://www.google.com",
        )

        assert company.website == "https://www.google.com"


# ---------------------------------------------------------------------------
# Model Convenience Behavior
# ---------------------------------------------------------------------------


class TestCompanyProperties:

    def test_string_representation(
        self,
        workspace1_user1,
    ):
        company = Company(
            workspace=workspace1_user1,
            name="Company 1",
        )

        assert str(company) == "Company 1"
