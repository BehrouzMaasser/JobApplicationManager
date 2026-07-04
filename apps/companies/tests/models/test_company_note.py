import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import CompanyNote


pytestmark = pytest.mark.django_db

#   ----------------------------------- ****** -----------------------------------


@pytest.fixture
def content1() -> str:

    return "Content 1"


class TestCompanyNoteValidation:

    def test_company_note_requires_company(self, content1):
        with pytest.raises(ValidationError):
            CompanyNote(
                title="Test", content=content1, company=None
            ).full_clean()

    def test_company_note_requires_title(self, co1_ws1_user1, content1):
        with pytest.raises(ValidationError):
            CompanyNote(
                title=None, company=co1_ws1_user1, content=content1
            ).full_clean()

    def test_company_note_requires_content(self, co1_ws1_user1):
        with pytest.raises(ValidationError):
            CompanyNote(
                title="Test", company=co1_ws1_user1, content=None
            ).full_clean()

    def test_company_note_requires_non_empty_content(self, co1_ws1_user1):
        with pytest.raises(ValidationError):
            CompanyNote(
                title="Title", company=co1_ws1_user1, content=""
            ).full_clean()

    def test_company_note_requires_non_empty_title(
            self, co1_ws1_user1, content1
    ):
        with pytest.raises(ValidationError):
            CompanyNote(
                title="", company=co1_ws1_user1, content=content1
            ).full_clean()


#   ----------------------------------- ****** -----------------------------------


class TestCompanyNoteConstraint:

    def test_title_is_unique_per_company(self, co1_ws1_user1, content1):
        CompanyNote.objects.create(
            title="Test 1", company=co1_ws1_user1, content=content1
        )

        with pytest.raises(IntegrityError):
            CompanyNote.objects.create(
                title="Test 1", company=co1_ws1_user1, content=content1
            )

    def test_same_title_and_company_raise_error_when_call_full_clean(
            self,
            co1_ws1_user1,
            content1
    ):
        CompanyNote.objects.create(
            title="Test 1", company=co1_ws1_user1, content=content1
        )

        with pytest.raises(ValidationError) as e:
            CompanyNote(
                title="Test 1", company=co1_ws1_user1, content=content1
            ).full_clean()

            assert e.error_dict["__all__"][0].code == "duplicate_company_note_title"

#   ----------------------------------- ****** -----------------------------------


class TestCompanyNoteCreation:

    def test_valid_company_note_creation(self, co1_ws1_user1, content1):
        company_email = CompanyNote.objects.create(
            title="Title 1",
            company=co1_ws1_user1,
            content=content1,
        )

        assert company_email.company == co1_ws1_user1
        assert company_email.title == "Title 1"
        assert company_email.content == content1

    def test_ordering(self, co1_ws1_user1, content1):
        note1 = CompanyNote.objects.create(
            title="A", company=co1_ws1_user1, content=content1
        )
        note2 = CompanyNote.objects.create(
            title="C", company=co1_ws1_user1, content=content1
        )
        note3 = CompanyNote.objects.create(
            title="B", company=co1_ws1_user1, content=content1
        )
        note4 = CompanyNote.objects.create(
            title="C-Note 2", company=co1_ws1_user1, content=content1
        )
        note5 = CompanyNote.objects.create(
            title="C-Note 1", company=co1_ws1_user1, content=content1
        )

        correct_title_order = [
            note1,
            note3,
            note2,
            note5,
            note4
        ]

        notes = CompanyNote.objects.all()

        for notes_correct_order, notes_given in zip(correct_title_order, notes):
            assert notes_correct_order == notes_given

    def test_other_users_with_same_title_is_valid(
            self, co1_ws1_user1, co1_ws1_user2, content1
    ):

        note1 = CompanyNote.objects.create(
            title="Note 1", company=co1_ws1_user1, content=content1
        )
        note2 = CompanyNote.objects.create(
            title="Note 1", company=co1_ws1_user2, content=content1
        )

        assert note1.title == "Note 1"
        assert note1.title == note2.title

        assert note1.content == content1
        assert note1.content == note2.content

    def test_different_companies_with_same_title_is_valid(
            self, co1_ws1_user1, co1_ws2_user1, content1
    ):

        note1 = CompanyNote.objects.create(
            title="Note 1", company=co1_ws1_user1, content=content1
        )
        note2 = CompanyNote.objects.create(
            title="Note 1", company=co1_ws2_user1, content=content1
        )

        assert note1.title == "Note 1"
        assert note1.title == note2.title

#   ----------------------------------- ****** -----------------------------------


class TestCompanyNoteRepresentation:

    def test_company_note_string_representation(self, co1_ws1_user1, content1):
        note = CompanyNote.objects.create(
            title="Note 1", company=co1_ws1_user1, content=content1
        )

        assert str(note) == note.title

#   ----------------------------------- ****** -----------------------------------
