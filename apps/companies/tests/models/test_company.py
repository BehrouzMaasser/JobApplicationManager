import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import Company


#   ----------------------------------- ****** -----------------------------------

# Invalid Creation:

@pytest.mark.django_db
def test_company_requires_workspace():

    # Workspace is None
    with pytest.raises(ValidationError):
        Company(name="Test", workspace=None).full_clean()

    # Workspace is not provided
    with pytest.raises(ValidationError):
        Company(name="Test").full_clean()


@pytest.mark.django_db
def test_company_requires_name(workspace_user1):

    # Name is None
    with pytest.raises(ValidationError):
        Company(name=None, workspace=workspace_user1).full_clean()

    # Name is not provided
    with pytest.raises(ValidationError):
        Company(workspace=workspace_user1).full_clean()


@pytest.mark.django_db
def test_company_requires_non_empty_name(workspace_user1):

    with pytest.raises(ValidationError):
        Company(name="", workspace=workspace_user1).full_clean()


#   ----------------------------------- ****** -----------------------------------

# Constraint Check:

@pytest.mark.django_db
def test_company_lower_case_name_is_unique_per_workspace(workspace_user1):

    Company.objects.create(name="Company 1", workspace=workspace_user1)

    with pytest.raises(IntegrityError):
        Company.objects.create(name="COMPanY 1", workspace=workspace_user1)


#   ----------------------------------- ****** -----------------------------------


# Valid Creation:
@pytest.mark.django_db
def test_valid_company(workspace_user1):

    company = Company(
        name="Company 1",
        website="https://www.google.com",
        workspace=workspace_user1
    )

    company.full_clean()
    company.save()

    assert company.id is not None
    assert company.workspace == workspace_user1
    assert company.name == "Company 1"
    assert company.website == "https://www.google.com"


@pytest.mark.django_db
def test_valid_company_with_optional_website(workspace_user1):

    # Website not provided
    company_1 = Company(
        name="Company 1",
        workspace=workspace_user1,
    )

    company_1.full_clean()
    company_1.save()

    assert company_1.website is None

    # Website is provided and it is None
    company_2 = Company(
        name="Company 2",
        workspace=workspace_user1,
        website=None
    )

    company_2.full_clean()
    company_2.save()

    assert company_2.website is None

    # Website is provided and it is empty string
    company_3 = Company(
        name="Company 3",
        workspace=workspace_user1,
        website=""
    )

    company_3.full_clean()
    company_3.save()

    # Empty string website is stored as None
    assert company_3.website is None


@pytest.mark.django_db
def test_same_company_name_in_different_workspaces_is_allowed(
        workspace_user1,
        other_workspace_user1,
        workspace_user2
):

    company1_ws1_user1 = Company(name="Company 1", workspace=workspace_user1)

    company1_ws1_user1.full_clean()
    company1_ws1_user1.save()

    company1_ws2_user1 = Company(name="Company 1", workspace=other_workspace_user1)

    company1_ws2_user1.full_clean()
    company1_ws2_user1.save()

    company1_ws1_user2 = Company(name="Company 1", workspace=workspace_user2)

    company1_ws1_user2.full_clean()
    company1_ws1_user2.save()

    assert company1_ws1_user1.workspace != company1_ws2_user1.workspace
    assert company1_ws1_user1.workspace != company1_ws1_user2.workspace

    assert company1_ws1_user1.name == company1_ws2_user1.name
    assert company1_ws1_user1.name == company1_ws1_user2.name

    assert company1_ws1_user1.workspace.owner == company1_ws2_user1.workspace.owner
    assert company1_ws1_user1.workspace.owner != company1_ws1_user2.workspace.owner

#   ----------------------------------- ****** -----------------------------------
