import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import CompanyNote


pytestmark = pytest.mark.django_db


@pytest.fixture
def content1() -> str:
    return "Content 1"


# ---------------------------------------------------------------------------
# M-01: Persistence Schema
# ---------------------------------------------------------------------------


class TestCompanyNoteSchema:

    def test_company_note_requires_company(
        self,
        content1,
    ):
        note = CompanyNote(
            company=None,
            title="Title",
            content=content1,
        )

        with pytest.raises(ValidationError):
            note.full_clean()

    def test_company_note_requires_title(
        self,
        co1_ws1_user1,
        content1,
    ):
        note = CompanyNote(
            company=co1_ws1_user1,
            title=None,
            content=content1,
        )

        with pytest.raises(ValidationError):
            note.full_clean()

    def test_company_note_title_cannot_be_empty(
        self,
        co1_ws1_user1,
        content1,
    ):
        note = CompanyNote(
            company=co1_ws1_user1,
            title="",
            content=content1,
        )

        with pytest.raises(ValidationError):
            note.full_clean()

    def test_company_note_requires_content(
        self,
        co1_ws1_user1,
    ):
        note = CompanyNote(
            company=co1_ws1_user1,
            title="Title",
            content=None,
        )

        with pytest.raises(ValidationError):
            note.full_clean()

    def test_company_note_content_cannot_be_empty(
        self,
        co1_ws1_user1,
    ):
        note = CompanyNote(
            company=co1_ws1_user1,
            title="Title",
            content="",
        )

        with pytest.raises(ValidationError):
            note.full_clean()

    def test_valid_company_note_creation(
        self,
        co1_ws1_user1,
        content1,
    ):
        note = CompanyNote(
            company=co1_ws1_user1,
            title="Note 1",
            content=content1,
        )

        note.full_clean()
        note.save()

        assert note.id is not None
        assert note.company == co1_ws1_user1
        assert note.title == "Note 1"
        assert note.content == content1


class TestCompanyNoteConstraints:

    def test_title_must_be_unique_within_company(
        self,
        co1_ws1_user1,
        content1,
    ):
        CompanyNote.objects.create(
            company=co1_ws1_user1,
            title="Note 1",
            content=content1,
        )

        with pytest.raises(IntegrityError):
            CompanyNote.objects.create(
                company=co1_ws1_user1,
                title="Note 1",
                content=content1,
            )

    def test_title_is_case_insensitively_unique_within_company(
        self,
        co1_ws1_user1,
        content1,
    ):
        CompanyNote.objects.create(
            company=co1_ws1_user1,
            title="Note 1",
            content=content1,
        )

        with pytest.raises(IntegrityError):
            CompanyNote.objects.create(
                company=co1_ws1_user1,
                title="note 1",
                content=content1,
            )

    def test_full_clean_reports_duplicate_company_note_title(
        self,
        co1_ws1_user1,
        content1,
    ):
        CompanyNote.objects.create(
            company=co1_ws1_user1,
            title="Note 1",
            content=content1,
        )

        with pytest.raises(ValidationError) as exc:
            CompanyNote(
                company=co1_ws1_user1,
                title="Note 1",
                content=content1,
            ).full_clean()

        assert (
            exc.value.error_dict["__all__"][0].code
            == "duplicate_company_note_title"
        )

    def test_same_title_is_allowed_in_different_companies(
        self,
        co1_ws1_user1,
        co1_ws2_user1,
        content1,
    ):
        note1 = CompanyNote.objects.create(
            company=co1_ws1_user1,
            title="Note 1",
            content=content1,
        )

        note2 = CompanyNote.objects.create(
            company=co1_ws2_user1,
            title="Note 1",
            content=content1,
        )

        assert note1.title == note2.title


# ---------------------------------------------------------------------------
# Model Convenience Behavior
# ---------------------------------------------------------------------------


class TestCompanyNoteProperties:

    def test_string_representation(
        self,
        co1_ws1_user1,
        content1,
    ):
        note = CompanyNote(
            company=co1_ws1_user1,
            title="Note 1",
            content=content1,
        )

        assert str(note) == "Note 1"
