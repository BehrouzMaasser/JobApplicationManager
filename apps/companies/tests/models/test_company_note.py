import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import CompanyNote


#   ----------------------------------- ****** -----------------------------------

# Invalid Creation:

@pytest.mark.django_db
def test_company_note_requires_company():

    # Company is None
    with pytest.raises(ValidationError):
        CompanyNote(company=None, title="Co.1 Bad", content="Content").full_clean()

    # Company is not provided
    with pytest.raises(ValidationError):
        CompanyNote(title="Co.1 Bad", content="Content").full_clean()


@pytest.mark.django_db
def test_company_note_requires_title(co1_ws1_user1):

    # Title is None

    with pytest.raises(ValidationError):
        CompanyNote(
            title=None, company=co1_ws1_user1, content="Content"
        ).full_clean()

    # Title is not provided
    with pytest.raises(ValidationError):
        CompanyNote(company=co1_ws1_user1, content="Content").full_clean()


@pytest.mark.django_db
def test_company_note_requires_non_empty_title(co1_ws1_user1):

    with pytest.raises(ValidationError):
        CompanyNote(title="", company=co1_ws1_user1, content="Content").full_clean()


@pytest.mark.django_db
def test_company_note_requires_content(co1_ws1_user1):

    # Content is None
    with pytest.raises(ValidationError):
        CompanyNote(title="Title", company=co1_ws1_user1, content=None).full_clean()

    # Content is not Provided
    with pytest.raises(ValidationError):
        CompanyNote(title="Title", company=co1_ws1_user1).full_clean()


@pytest.mark.django_db
def test_company_note_requires_non_empty_content(co1_ws1_user1):

    with pytest.raises(ValidationError):
        CompanyNote(title="Title", company=co1_ws1_user1, content="").full_clean()

#   ----------------------------------- ****** -----------------------------------


# Constraint Check:

@pytest.mark.django_db
def test_lower_case_title_should_be_unique_per_company(co1_ws1_user1):

    CompanyNote.objects.create(
        title="Title",
        company=co1_ws1_user1,
        content="Content"
    )

    with pytest.raises(IntegrityError):
        CompanyNote.objects.create(
            title="tiTLE",
            company=co1_ws1_user1,
            content="Another Content"
        )


#   ----------------------------------- ****** -----------------------------------


# Valid Creation:
@pytest.mark.django_db
def test_valid_company_note(co1_ws1_user1):

    c_note = CompanyNote(
        title="Title",
        company=co1_ws1_user1,
        content="something"
    )
    
    c_note.full_clean()
    c_note.save()

    assert c_note.id is not None
    assert c_note.company == co1_ws1_user1
    assert c_note.title == "Title"
    assert c_note.content == "something"


@pytest.mark.django_db
def test_same_title_in_different_company_in_same_workspace_is_allowed(
        co1_ws1_user1, co2_ws1_user1
):

    c_note_1 = CompanyNote.objects.create(
        title="Title", company=co1_ws1_user1, content="Content1"
    )
    
    c_note_2 = CompanyNote.objects.create(
        title="Title", company=co2_ws1_user1, content="Content1"
    )
    
    assert c_note_1.title == c_note_2.title


@pytest.mark.django_db
def test_same_title_in_different_companies_is_allowed(
        co1_ws1_user1, co2_ws1_user1, co1_ws2_user1, co1_ws1_user2
):

    c_note_1 = CompanyNote.objects.create(
        title="Title", company=co1_ws1_user1, content="Content"
    )

    c_note_2 = CompanyNote.objects.create(
        title="Title", company=co2_ws1_user1, content="Content"
    )

    c_note_3 = CompanyNote.objects.create(
        title="Title", company=co1_ws2_user1, content="Content"
    )

    c_note_4 = CompanyNote.objects.create(
        title="Title", company=co1_ws1_user2, content="Content"
    )

    assert c_note_1.title == c_note_2.title
    assert c_note_1.title == c_note_3.title
    assert c_note_1.title == c_note_4.title

#   ----------------------------------- ****** -----------------------------------
