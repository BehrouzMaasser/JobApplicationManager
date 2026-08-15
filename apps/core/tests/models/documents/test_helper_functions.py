import pytest

from django.core.exceptions import ValidationError

from apps.documents.models import document_upload_path

# ---------------------------------------------------------------------------
# document_upload_path helper tests
# ---------------------------------------------------------------------------


class TestDocumentUploadPath:

    def test_filename_without_exactly_one_extension_raises_error(
        self,
        doc1_user1,
    ):
        with pytest.raises(ValidationError):
            document_upload_path(
                doc1_user1,
                "My Document 1.txt.pdf",
            )

        with pytest.raises(ValidationError):
            document_upload_path(
                doc1_user1,
                "My Document 1 txt",
            )

    def test_invalid_filename_returns_expected_error_key(
        self,
        doc1_user1,
    ):
        with pytest.raises(ValidationError) as exc:
            document_upload_path(
                doc1_user1,
                "My Document 1.txt.pdf",
            )

        assert "file_name" in exc.value.message_dict

    def test_upload_path_has_expected_structure(
        self,
        doc1_user1,
    ):
        doc1_user1.document_type.owner.documents_directory = (
            "some-directory"
        )

        path = document_upload_path(
            doc1_user1,
            "My Document 1.txt",
        )

        assert path.startswith(
            "docs/some-directory/doc-type-1"
        )

        assert path.endswith(".txt")

        assert "Document 1" not in path
        assert "My Document 1" not in path

    def test_upload_path_generates_unique_file_names(
        self,
        doc1_user1,
    ):
        path1 = document_upload_path(
            doc1_user1,
            "document.txt",
        )

        path2 = document_upload_path(
            doc1_user1,
            "document.txt",
        )

        assert path1 != path2

    def test_upload_path_preserves_file_extension(
        self,
        doc1_user1,
    ):
        path = document_upload_path(
            doc1_user1,
            "document.PDF",
        )

        assert path.endswith(".PDF")
