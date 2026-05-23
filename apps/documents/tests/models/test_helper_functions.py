import hashlib
import pytest

from django.core.exceptions import ValidationError

from apps.documents.models import document_upload_path, calculate_file_hash

from apps.documents.tests.conftest import FakeFile


# Invalid file name

@pytest.mark.django_db
def test_document_upload_path_with_invalid_file_extension(doc1_user1):

    doc1_user1.document_type.owner.documents_directory = "some-directory"

    with pytest.raises(ValidationError):
        document_upload_path(doc1_user1, "My Document 1.txt.pdf")


# Valid file name

@pytest.mark.django_db
def test_document_upload_path_structure(doc1_user1):

    doc1_user1.document_type.owner.documents_directory = "some-directory"
    path = document_upload_path(doc1_user1, "My Document 1.txt")

    assert path.startswith("documents/docs/some-directory/doc-type-1")
    assert path.endswith(".txt")
    assert "Document 1" not in path
    assert "My Document 1" not in path


@pytest.mark.django_db
def test_calculate_file_hash_correctness_with_encoded_string():

    s1 = "some text in here"
    f1 = FakeFile(s1.encode('utf-8'), 5)
    hash1_result = calculate_file_hash(f1)

    s2 = ""
    f2 = FakeFile(s2.encode('utf-8'), 5)
    hash2_result = calculate_file_hash(f2)

    assert hash1_result == hashlib.sha256(f1.content).hexdigest()
    assert hash2_result == hashlib.sha256(f2.content).hexdigest()


@pytest.mark.django_db
def test_calculate_file_hash_correctness_with_same_results_over_multiple_runs():

    s1 = "some text in here"
    f1 = FakeFile(s1.encode('utf-8'), 5)
    expected_result = hashlib.sha256(f1.content).hexdigest()

    for _ in range(1000):
        assert expected_result == calculate_file_hash(f1)
