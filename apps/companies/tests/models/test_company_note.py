import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import CompanyNote


#   ----------------------------------- ****** -----------------------------------

# Invalid Creation:

@pytest.mark.django_db
def test_company_note_requires_company():

    # Company is None
    c_note = CompanyNote(company=None, title="Co.1 Bad", content="Content")

    with pytest.raises(ValidationError):
        c_note.full_clean()

    c_note = CompanyNote(title="Co.1 Bad", content="Content")

    # Company is not provided
    with pytest.raises(ValidationError):
        c_note.full_clean()


@pytest.mark.django_db
def test_company_note_requires_title(co1_ws1_user1):

    # Title is None
    c_note = CompanyNote(title=None, company=co1_ws1_user1, content="Content")

    with pytest.raises(ValidationError):
        c_note.full_clean()

    # Title is not provided
    c_note = CompanyNote(company=co1_ws1_user1, content="Content")

    with pytest.raises(ValidationError):
        c_note.full_clean()


@pytest.mark.django_db
def test_company_note_requires_non_empty_title(co1_ws1_user1):

    c_note = CompanyNote(title="", company=co1_ws1_user1, content="Content")

    with pytest.raises(ValidationError):
        c_note.full_clean()


@pytest.mark.django_db
def test_company_note_requires_content(co1_ws1_user1):

    # Content is None
    c_note = CompanyNote(title="Title", company=co1_ws1_user1, content=None)

    with pytest.raises(ValidationError):
        c_note.full_clean()

    # Content is not Provided
    c_note = CompanyNote(title="Title", company=co1_ws1_user1)

    with pytest.raises(ValidationError):
        c_note.full_clean()


@pytest.mark.django_db
def test_company_note_requires_non_empty_content(co1_ws1_user1):

    c_note = CompanyNote(title="Title", company=co1_ws1_user1, content="")

    with pytest.raises(ValidationError):
        c_note.full_clean()

#   ----------------------------------- ****** -----------------------------------


# Constraint Check:

@pytest.mark.django_db
def test_lower_case_title_is_unique_per_company(co1_ws1_user1):

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

    assert c_note.company == co1_ws1_user1
    assert c_note.title == "Title"
    assert c_note.content == "something"


@pytest.mark.django_db
def test_same_title_in_different_company_in_same_workspace(
        co1_ws1_user1, co2_ws1_user1
):

    c_note_1 = CompanyNote(
        title="Title", company=co1_ws1_user1, content="Content1"
    )
    
    c_note_1.full_clean()
    c_note_1.save()
    
    c_note_2 = CompanyNote(
        title="Title", company=co2_ws1_user1, content="Content1"
    )
    
    c_note_2.full_clean()
    c_note_2.save()

    assert c_note_1.title == c_note_2.title


@pytest.mark.django_db
def test_same_title_in_different_companies(
        co1_ws1_user1, co2_ws1_user1, co1_ws2_user1, co1_ws1_user2
):

    c_note_1 = CompanyNote(
        title="Title", company=co1_ws1_user1, content="Content"
    )

    c_note_1.full_clean()
    c_note_1.save()

    c_note_2 = CompanyNote(
        title="Title", company=co2_ws1_user1, content="Content"
    )

    c_note_2.full_clean()
    c_note_2.save()

    c_note_3 = CompanyNote(
        title="Title", company=co1_ws2_user1, content="Content"
    )

    c_note_3.full_clean()
    c_note_3.save()

    c_note_4 = CompanyNote(
        title="Title", company=co1_ws1_user2, content="Content"
    )

    c_note_4.full_clean()
    c_note_4.save()

    assert c_note_1.title == c_note_2.title
    assert c_note_1.title == c_note_3.title


#   ----------------------------------- ****** -----------------------------------

# Constraint Check:

@pytest.mark.django_db
def test_same_title_in_same_company_raise_error(
        co1_ws1_user1
):

    CompanyNote.objects.create(
        company=co1_ws1_user1, title="Title", content="Content1"
    )

    with pytest.raises(IntegrityError):
        CompanyNote.objects.create(
            company=co1_ws1_user1, title="TITLE", content="Content2"
        )


#   ----------------------------------- ****** -----------------------------------
