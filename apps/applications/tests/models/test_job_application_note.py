import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.applications.models import JobApplicationNote


#   ----------------------------------- ****** -----------------------------------

# Invalid Creation:

@pytest.mark.django_db
def test_job_application_note_requires_job_application():

    job_application_note = JobApplicationNote(
        job_application=None,
        title="Title",
        content="Content",
    )

    with pytest.raises(ValidationError):
        job_application_note.full_clean()

    job_application_note = JobApplicationNote(
        title="Title",
        content="Content",
    )

    with pytest.raises(ValidationError):
        job_application_note.full_clean()


@pytest.mark.django_db
def test_job_application_note_requires_title(job_application1):

    job_application_note = JobApplicationNote(
        job_application=job_application1,
        title=None,
        content="Content",
    )

    with pytest.raises(ValidationError):
        job_application_note.full_clean()

    job_application_note = JobApplicationNote(
        job_application=job_application1,
        content="Content",
    )

    with pytest.raises(ValidationError):
        job_application_note.full_clean()


@pytest.mark.django_db
def test_job_application_note_requires_non_empty_title(job_application1):

    job_application_note = JobApplicationNote(
        job_application=job_application1,
        title="",
        content="Content",
    )

    with pytest.raises(ValidationError):
        job_application_note.full_clean()

    # None Empty Title
    JobApplicationNote(
        job_application=job_application1,
        title="Title",
        content="Content",
    ).full_clean()


@pytest.mark.django_db
def test_job_application_note_requires_content(job_application1):

    job_application_note = JobApplicationNote(
        job_application=job_application1,
        title="Title",
        content=None,
    )

    with pytest.raises(ValidationError):
        job_application_note.full_clean()

    job_application_note = JobApplicationNote(
        job_application=job_application1,
        title="Title",
    )

    with pytest.raises(ValidationError):
        job_application_note.full_clean()


@pytest.mark.django_db
def test_job_application_note_requires_non_empty_content(job_application1):

    job_application_note = JobApplicationNote(
        job_application=job_application1,
        title="Title",
        content="",
    )

    with pytest.raises(ValidationError):
        job_application_note.full_clean()

    # None Empty Content
    JobApplicationNote(
        job_application=job_application1,
        title="Title",
        content="Content",
    ).full_clean()


# Constraint Check:

@pytest.mark.django_db
def test_job_application_note_lower_title_is_unique_for_each_job_application(
        job_application1
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
            content="CONtENT",
        )

#   ----------------------------------- ****** -----------------------------------


# Valid Creation:

@pytest.mark.django_db
def test_valid_job_application_note(job_application1):

    job_application_note = JobApplicationNote(
        job_application=job_application1,
        title="Title",
        content="Content",
    )

    job_application_note.full_clean()
    job_application_note.save()

    assert job_application_note.job_application == job_application1
    assert job_application_note.title == "Title"
    assert job_application_note.content == "Content"


@pytest.mark.django_db
def test_same_title_different_job_application(
        job_application1, job_application2
):

    job_application_note1 = JobApplicationNote(
        job_application=job_application1,
        title="Title",
        content="Content",
    )

    job_application_note1.full_clean()
    job_application_note1.save()

    assert job_application_note1.job_application == job_application1
    assert job_application_note1.title == "Title"
    assert job_application_note1.content == "Content"

    job_application_note2 = JobApplicationNote(
        job_application=job_application2,
        title="Title",
        content="Content",
    )

    job_application_note2.full_clean()
    job_application_note2.save()

    assert job_application_note2.job_application == job_application2
    assert job_application_note2.title == "Title"
    assert job_application_note2.content == "Content"

    assert job_application_note1.title == job_application_note2.title
    assert job_application_note1.content == job_application_note2.content


#   ----------------------------------- ****** -----------------------------------
