import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.applications.models import JobApplicationNote


pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------
# M-01: Persistence Schema
# ---------------------------------------------------------------------------


class TestJobApplicationNoteSchema:

    def test_job_application_note_requires_job_application(self):
        note = JobApplicationNote(
            job_application=None,
            title="Title",
            content="Content",
        )

        with pytest.raises(ValidationError):
            note.full_clean()

    def test_job_application_note_requires_title(
        self,
        job_application1,
    ):
        note = JobApplicationNote(
            job_application=job_application1,
            title=None,
            content="Content",
        )

        with pytest.raises(ValidationError):
            note.full_clean()

    def test_job_application_note_title_cannot_be_blank(
        self,
        job_application1,
    ):
        note = JobApplicationNote(
            job_application=job_application1,
            title="",
            content="Content",
        )

        with pytest.raises(ValidationError):
            note.full_clean()

    def test_job_application_note_requires_content(
        self,
        job_application1,
    ):
        note = JobApplicationNote(
            job_application=job_application1,
            title="Title",
            content=None,
        )

        with pytest.raises(ValidationError):
            note.full_clean()

    def test_job_application_note_content_cannot_be_blank(
        self,
        job_application1,
    ):
        note = JobApplicationNote(
            job_application=job_application1,
            title="Title",
            content="",
        )

        with pytest.raises(ValidationError):
            note.full_clean()

    def test_valid_job_application_note_creation(
        self,
        job_application1,
    ):
        note = JobApplicationNote(
            job_application=job_application1,
            title="Title",
            content="Content",
        )

        note.full_clean()
        note.save()

        assert note.id is not None
        assert note.job_application == job_application1
        assert note.title == "Title"
        assert note.content == "Content"

    def test_notes_are_ordered_by_job_application_then_title(
        self,
        job_application1,
    ):
        note1 = JobApplicationNote.objects.create(
            job_application=job_application1,
            title="B title",
            content="Content",
        )

        note2 = JobApplicationNote.objects.create(
            job_application=job_application1,
            title="A title",
            content="Content",
        )

        notes = list(JobApplicationNote.objects.all())

        assert notes == [
            note2,
            note1,
        ]


class TestJobApplicationNoteConstraints:

    def test_note_title_is_case_insensitive_unique_per_application(
        self,
        job_application1,
    ):
        JobApplicationNote.objects.create(
            job_application=job_application1,
            title="Title",
            content="Content",
        )

        with pytest.raises(IntegrityError):
            JobApplicationNote.objects.create(
                job_application=job_application1,
                title="tITLe",
                content="Different Content",
            )

    def test_same_title_is_allowed_for_different_applications(
        self,
        job_application1,
        job_application2,
    ):
        note1 = JobApplicationNote.objects.create(
            job_application=job_application1,
            title="Title",
            content="Content",
        )

        note2 = JobApplicationNote.objects.create(
            job_application=job_application2,
            title="Title",
            content="Content",
        )

        assert note1.id != note2.id
        assert note1.title == note2.title
        assert note1.content == note2.content


# ---------------------------------------------------------------------------
# Model Convenience Behavior
# ---------------------------------------------------------------------------


class TestJobApplicationNoteProperties:

    def test_string_representation(
        self,
        job_application1,
    ):
        note = JobApplicationNote(
            job_application=job_application1,
            title="Interview",
            content="Content",
        )

        assert str(note) == (
            f"{job_application1} - Interview"
        )
