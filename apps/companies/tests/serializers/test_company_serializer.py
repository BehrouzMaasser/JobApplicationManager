import pytest

from apps.companies.api.v1.serializers import CompanySerializer


@pytest.mark.django_db
class TestCompanySerializer:

    def test_valid_data(self, co1_ws1_user1_valid_data):

        serializer = CompanySerializer(data=co1_ws1_user1_valid_data)

        assert serializer.is_valid(), serializer.errors

    def test_name_required(self, co1_ws1_user1_valid_data):

        payload = co1_ws1_user1_valid_data.copy()
        payload.pop("name")

        serializer = CompanySerializer(data=payload)

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_name_cannot_be_blank(self, co1_ws1_user1_valid_data):

        payload = co1_ws1_user1_valid_data.copy()
        payload["name"] = ""

        serializer = CompanySerializer(data=payload)

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_website_must_be_valid_url(self, co1_ws1_user1_valid_data):

        payload = co1_ws1_user1_valid_data.copy()
        payload["website"] = "invalid-website"

        serializer = CompanySerializer(data=payload)

        assert not serializer.is_valid()
        assert "website" in serializer.errors

    def test_website_can_be_null(self, co1_ws1_user1_valid_data):

        payload = co1_ws1_user1_valid_data.copy()
        payload["website"] = None

        serializer = CompanySerializer(data=payload)

        assert serializer.is_valid(), serializer.errors

    def test_website_is_optional(self, co1_ws1_user1_valid_data):

        payload = co1_ws1_user1_valid_data.copy()
        payload.pop("website", None)

        serializer = CompanySerializer(data=payload)

        assert serializer.is_valid(), serializer.errors

    def test_read_only_fields_are_ignored_on_input(self, co1_ws1_user1_valid_data):

        payload = co1_ws1_user1_valid_data.copy()

        payload["id"] = 999
        payload["workspace"] = 123
        payload["created_at"] = "2000-01-01T00:00:00Z"
        payload["updated_at"] = "2000-01-01T00:00:00Z"

        serializer = CompanySerializer(data=payload)

        assert serializer.is_valid(), serializer.errors
        validated = serializer.validated_data

        assert "workspace" not in validated
        assert "id" not in validated
        assert "created_at" not in validated
        assert "updated_at" not in validated
