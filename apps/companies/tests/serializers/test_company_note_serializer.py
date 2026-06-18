import pytest

from apps.companies.api.v1.serializers import CompanyNoteSerializer


@pytest.mark.django_db
class TestCompanyNoteSerializer:

    def test_valid_data(self, co_note1_co1_ws1_user1_valid_data):

        serializer = CompanyNoteSerializer(data=co_note1_co1_ws1_user1_valid_data)

        assert serializer.is_valid()

    def test_title_required(self, co_note1_co1_ws1_user1_valid_data):

        co_note1_co1_ws1_user1_valid_data.pop("title")

        serializer = CompanyNoteSerializer(data=co_note1_co1_ws1_user1_valid_data)

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_content_required(self, co_note1_co1_ws1_user1_valid_data):

        co_note1_co1_ws1_user1_valid_data.pop("content")

        serializer = CompanyNoteSerializer(data=co_note1_co1_ws1_user1_valid_data)

        assert not serializer.is_valid()
        assert "content" in serializer.errors
