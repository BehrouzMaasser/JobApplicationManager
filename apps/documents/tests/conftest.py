from django.core.files.uploadedfile import SimpleUploadedFile

from apps.applications.tests.conftest import *

from apps.documents.models import DocumentType, Document


class FakeFile:

    def __init__(self, content, chunk_size: int, name: str = "Doc"):

        self.content = content
        self.chunk_size = chunk_size
        self._name = name
        self._committed = True

    @property
    def name(self):
        return self._name

    def chunks(self):

        for i in range(0, len(self.content), self.chunk_size):
            yield self.content[i:i + self.chunk_size]


@pytest.fixture
def api_upload_file1():

    return SimpleUploadedFile(
        "test1.txt", b"test1", content_type="text/plain"
    )


@pytest.fixture
def api_upload_file2():

    return SimpleUploadedFile(
        "test2.txt", b"test2", content_type="text/plain"
    )


@pytest.fixture
def doc_type1_user1_valid_data():

    return {"name": "Document Type 1", "description": "Description 1"}


@pytest.fixture
def document_type_user1(user):

    return DocumentType.objects.create(
        owner=user,
        name="Doc Type 1",
    )


@pytest.fixture
def document_type2_user1(user):

    return DocumentType.objects.create(
        owner=user,
        name="Doc Type 2",
    )


@pytest.fixture
def document_type_user2(other_user):

    return DocumentType.objects.create(
        owner=other_user,
        name="Doc Type 1",
    )


@pytest.fixture
def doc1_user1_valid_data(document_type_user1, fake_file1):

    return {
        "name": "Document 1",
        "document_type": document_type_user1,
        "file": fake_file1
    }


@pytest.fixture
def doc1_user1_api_valid_data(document_type_user1, api_upload_file1):

    return {
        "name": "Document 1",
        "document_type": document_type_user1.id,
        "file": api_upload_file1
    }


@pytest.fixture
def doc1_user1_api_updated_valid_data(document_type2_user1, api_upload_file2):

    return {
        "name": "Document 1 Edited",
        "document_type": document_type2_user1.id,
        "file": api_upload_file2
    }


@pytest.fixture
def doc1_user1(document_type_user1, fake_file1):

    return Document.objects.create(
        name="Document 1",
        owner=document_type_user1.owner,
        document_type=document_type_user1,
        file=fake_file1,
    )


@pytest.fixture
def doc2_user1(document_type2_user1, fake_file1):

    return Document.objects.create(
        name="Document 2",
        owner=document_type2_user1.owner,
        document_type=document_type2_user1,
        file=fake_file1,
    )


@pytest.fixture
def doc1_user2(document_type_user2, fake_file1):

    return Document.objects.create(
        name="Document 1",
        owner=document_type_user2.owner,
        document_type=document_type_user2,
        file=fake_file1,
    )


@pytest.fixture
def fake_file1():

    return FakeFile("Some File".encode("utf-8"), 1)


@pytest.fixture
def fake_file2():

    return FakeFile("Some File 222".encode("utf-8"), 1)
