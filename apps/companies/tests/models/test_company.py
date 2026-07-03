import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import Company


pytestmark = pytest.mark.django_db

#   ----------------------------------- ****** -----------------------------------


class TestCompanyValidation:

    def test_company_requires_company(self):
        with pytest.raises(ValidationError):
            Company(name="Test", workspace=None).full_clean()

    def test_company_requires_name(self, workspace1_user1):
        with pytest.raises(ValidationError):
            Company(name=None, workspace=workspace1_user1).full_clean()

    def test_company_requires_non_empty_name(self, workspace1_user1):
        with pytest.raises(ValidationError):
            Company(name="", workspace=workspace1_user1).full_clean()


class TestCompanyConstraint:

    def test_company_name_is_unique_per_company(self, workspace1_user1):
        Company.objects.create(name="Test 1", workspace=workspace1_user1)

        with pytest.raises(IntegrityError):
            Company.objects.create(name="Test 1", workspace=workspace1_user1)

    def test_same_company_name_raise_error_when_call_full_clean(
            self, workspace1_user1
    ):
        Company.objects.create(name="Test 1", workspace=workspace1_user1)

        with pytest.raises(ValidationError) as e:
            Company(name="Test 1", workspace=workspace1_user1).full_clean()

            assert e.error_dict["__all__"][0].code == "duplicate_company_name"


#   ----------------------------------- ****** -----------------------------------


class TestCompanyCreation:

    def test_valid_company_creation(self, workspace1_user1):
        company = Company.objects.create(
            name="Company 1",
            workspace=workspace1_user1,
            website="https://www.google.com"
        )

        assert company.workspace == workspace1_user1
        assert company.name == "Company 1"
        assert company.website == "https://www.google.com"
        assert company.created_at is not None
        assert company.updated_at is not None

    def test_website_is_optional(self, workspace1_user1):
        company = Company.objects.create(
            name="Company 1",
            workspace=workspace1_user1,
            website=None
        )

        assert company.workspace == workspace1_user1
        assert company.name == "Company 1"
        assert company.website is None
        assert company.created_at is not None
        assert company.updated_at is not None

    def test_ordering(self, workspace1_user1):
        company1 = Company.objects.create(name="A", workspace=workspace1_user1)
        company2 = Company.objects.create(name="C", workspace=workspace1_user1)
        company3 = Company.objects.create(name="B", workspace=workspace1_user1)
        company4 = Company.objects.create(
            name="Company 2", workspace=workspace1_user1
        )
        company5 = Company.objects.create(
            name="Company 1", workspace=workspace1_user1
        )

        correct_name_order = [
            company1, company3, company2, company5, company4
        ]

        companies = Company.objects.all()

        for co_correct_order, ws_given in zip(correct_name_order, companies):
            assert co_correct_order == ws_given

    def test_other_users_with_same_company_name_is_valid(
            self, workspace1_user1, workspace1_user2
    ):

        company1 = Company.objects.create(
            name="Company 1", workspace=workspace1_user1
        )
        company2 = Company.objects.create(
            name="Company 1", workspace=workspace1_user2
        )

        assert company1.name == "Company 1"
        assert company1.name == company2.name

    def test_different_workspaces_with_same_company_name_is_valid(
            self, workspace1_user1, workspace2_user1
    ):

        company1 = Company.objects.create(
            name="Company 1", workspace=workspace1_user1
        )
        company2 = Company.objects.create(
            name="Company 1", workspace=workspace2_user1
        )

        assert company1.name == "Company 1"
        assert company1.name == company2.name


class TestCompanyRepresentation:

    def test_company_string_representation(self, workspace1_user1):
        company = Company.objects.create(
            name="Company 1", workspace=workspace1_user1
        )

        assert str(company) == company.name

#   ----------------------------------- ****** -----------------------------------
