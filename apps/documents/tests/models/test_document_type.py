import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.documents.models import DocumentType


@pytest.mark.django_db
def test_document_type_requires_owner():

    doc_type = DocumentType(owner=None, name='Document Type')

    with pytest.raises(ValidationError):
        doc_type.full_clean()


@pytest.mark.django_db
def test_document_type_requires_name(user):

    doc_type = DocumentType(owner=user, name=None)

    with pytest.raises(ValidationError):
        doc_type.full_clean()


@pytest.mark.django_db
def test_document_type_requires_non_empty_name(user):

    doc_type = DocumentType(owner=user, name="")

    with pytest.raises(ValidationError):
        doc_type.full_clean()


@pytest.mark.django_db
def test_document_type_lower_name_is_unique_per_user(user):

    DocumentType.objects.create(owner=user, name='Document Type1')

    with pytest.raises(IntegrityError):
        DocumentType.objects.create(owner=user, name='document type1')


@pytest.mark.django_db
def test_valid_document_type(user):

    doc_type = DocumentType(owner=user, name='Document Type')

    doc_type.full_clean()
    doc_type.save()

    assert doc_type.name == 'Document Type'
    assert doc_type.owner == user
    assert doc_type.description is None


@pytest.mark.django_db
def test_same_name_different_user(user, other_user):

    doc_type1 = DocumentType.objects.create(owner=user, name='Document Type')
    doc_type2 = DocumentType.objects.create(owner=other_user, name='Document Type')

    assert doc_type1.name == doc_type2.name
    assert doc_type1.owner != doc_type2.owner


@pytest.mark.django_db
def test_description_is_optional(user):

    # Description has value
    doc_type1 = DocumentType(
        owner=user,
        name='Document Type',
        description='Some Description'
    )
    doc_type1.full_clean()

    # Description is empty string
    doc_type2 = DocumentType(
        owner=user,
        name='Document Type',
        description=''
    )
    doc_type2.full_clean()

    # Description is None
    doc_type3 = DocumentType(
        owner=user,
        name='Document Type',
    )
    doc_type3.full_clean()
