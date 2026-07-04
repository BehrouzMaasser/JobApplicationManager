import pytest

from apps.companies.api.v1.serializers import CompanyNoteSerializer


@pytest.mark.django_db
class TestCompanyNoteSerializer:

    def test_valid_data(self, co_note1_co1_ws1_user1_valid_data):

        serializer = CompanyNoteSerializer(data=co_note1_co1_ws1_user1_valid_data)

        assert serializer.is_valid(), serializer.errors

    def test_title_required(self, co_note1_co1_ws1_user1_valid_data):

        payload = co_note1_co1_ws1_user1_valid_data.copy()
        payload.pop("title")

        serializer = CompanyNoteSerializer(data=payload)

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_content_required(self, co_note1_co1_ws1_user1_valid_data):

        payload = co_note1_co1_ws1_user1_valid_data.copy()
        payload.pop("content")

        serializer = CompanyNoteSerializer(data=payload)

        assert not serializer.is_valid()
        assert "content" in serializer.errors

    def test_blank_fields_not_allowed(self, co_note1_co1_ws1_user1_valid_data):

        payload = co_note1_co1_ws1_user1_valid_data.copy()
        payload["title"] = ""
        payload["content"] = ""

        serializer = CompanyNoteSerializer(data=payload)

        assert not serializer.is_valid()
        assert "title" in serializer.errors
        assert "content" in serializer.errors

    def test_null_fields_not_allowed(self, co_note1_co1_ws1_user1_valid_data):

        payload = co_note1_co1_ws1_user1_valid_data.copy()
        payload["title"] = None
        payload["content"] = None

        serializer = CompanyNoteSerializer(data=payload)

        assert not serializer.is_valid()
        assert "title" in serializer.errors
        assert "content" in serializer.errors

    def test_read_only_fields_cannot_be_set_on_create(
            self, co_note1_co1_ws1_user1_valid_data
    ):

        payload = co_note1_co1_ws1_user1_valid_data.copy()
        payload["company"] = 999
        payload["id"] = 123

        serializer = CompanyNoteSerializer(data=payload)

        assert serializer.is_valid(), serializer.errors
        validated = serializer.validated_data

        assert "company" not in validated
