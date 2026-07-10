import pytest

from django.core.exceptions import ValidationError

from apps.documents.models import Document

from apps.documents.tests.conftest import FakeFile


@pytest.mark.django_db
def test_document_requires_owner(document_type_user1):

    doc = Document(
        owner=None,
        name="Document 1",
        document_type=document_type_user1,
        file=FakeFile("Some File".encode("utf-8"), 1),
    )

    with pytest.raises(ValidationError):
        doc.full_clean()


@pytest.mark.django_db
def test_document_requires_name(user1, document_type_user1):

    doc = Document(
        owner=user1,
        name=None,
        document_type=document_type_user1,
        file=FakeFile("Some File".encode("utf-8"), 1),
    )

    with pytest.raises(ValidationError):
        doc.full_clean()


@pytest.mark.django_db
def test_document_requires_non_empty_name(user1, document_type_user1):

    doc = Document(
        owner=user1,
        name="",
        document_type=document_type_user1,
        file=FakeFile("Some File".encode("utf-8"), 1),
    )

    with pytest.raises(ValidationError):
        doc.full_clean()


@pytest.mark.django_db
def test_document_owner_should_be_the_owner_of_the_document_type(
        user1, document_type_user2
):

    doc = Document(
        owner=user1,
        name="Document 1",
        document_type=document_type_user2,
        file=FakeFile("Some File".encode("utf-8"), 1),
    )

    with pytest.raises(ValidationError):
        doc.full_clean()


@pytest.mark.django_db
def test_valid_document(document_type_user1):

    doc = Document(
        owner=document_type_user1.owner,
        name="Document 1",
        document_type=document_type_user1,
        file=FakeFile("Some File".encode("utf-8"), 1),
    )
    doc.full_clean()
    doc.save()

    assert doc.id is not None
    assert doc.name == 'Document 1'
    assert doc.owner == document_type_user1.owner
    assert doc.document_type == document_type_user1
    assert doc.file_hash is not None


@pytest.mark.django_db
def test_same_document_name_different_user_is_allowed(
        document_type_user1, document_type_user2
):

    doc1 = Document(
        owner=document_type_user1.owner,
        name="Document 1",
        document_type=document_type_user1,
        file=FakeFile("Some File".encode("utf-8"), 1),
    )
    doc1.full_clean()
    doc1.save()

    doc2 = Document(
        owner=document_type_user2.owner,
        name="Document 1",
        document_type=document_type_user2,
        file=FakeFile("Some File".encode("utf-8"), 1),
    )
    doc2.full_clean()
    doc2.save()

    assert doc1.id is not None
    assert doc2.id is not None

    assert doc1.name == doc2.name
    assert doc1.owner != doc2.owner


@pytest.mark.django_db
def test_duplicate_file_will_use_the_existing_file_hash_instead_of_saving_a_copy(
        document_type_user1
):

    doc1 = Document(
        owner=document_type_user1.owner,
        name="Document 1",
        document_type=document_type_user1,
        file=FakeFile("Some File".encode("utf-8"), 1),
    )
    doc1.full_clean()
    doc1.save()

    doc2 = Document(
        owner=document_type_user1.owner,
        name="Document 2",
        document_type=document_type_user1,
        file=FakeFile("Some File".encode("utf-8"), 1),
    )
    doc2.full_clean()
    doc2.save()

    assert doc1.name != doc2.name
    assert doc1.file_hash == doc2.file_hash
