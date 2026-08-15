import pytest

from apps.companies.api.v1.serializers import CompanyEmailSerializer


@pytest.mark.django_db
class TestCompanyEmailSerializer:

    def test_valid_data(self, co_email1_co1_ws1_user1_api_v1_valid_data):

        serializer = CompanyEmailSerializer(
            data=co_email1_co1_ws1_user1_api_v1_valid_data
        )

        assert serializer.is_valid(), serializer.errors

    def test_invalid_email(self, co_email1_co1_ws1_user1_api_v1_valid_data):

        payload = co_email1_co1_ws1_user1_api_v1_valid_data.copy()
        payload["email"] = "invalid-email"

        serializer = CompanyEmailSerializer(data=payload)

        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_email_is_required(self, co_email1_co1_ws1_user1_api_v1_valid_data):

        payload = co_email1_co1_ws1_user1_api_v1_valid_data.copy()
        payload.pop("email")

        serializer = CompanyEmailSerializer(data=payload)

        assert not serializer.is_valid()
        assert "email" in serializer.errors

    def test_title_is_required(self, co_email1_co1_ws1_user1_api_v1_valid_data):

        payload = co_email1_co1_ws1_user1_api_v1_valid_data.copy()
        payload.pop("title")

        serializer = CompanyEmailSerializer(data=payload)

        assert not serializer.is_valid()
        assert "title" in serializer.errors

    def test_blank_fields_are_not_allowed(
            self,
            co_email1_co1_ws1_user1_api_v1_valid_data
    ):

        payload = co_email1_co1_ws1_user1_api_v1_valid_data.copy()
        payload["title"] = ""
        payload["email"] = ""

        serializer = CompanyEmailSerializer(data=payload)

        assert not serializer.is_valid()
        assert "title" in serializer.errors
        assert "email" in serializer.errors

    def test_read_only_fields_cannot_be_set_on_create(
            self, co_email1_co1_ws1_user1_api_v1_valid_data
    ):

        payload = co_email1_co1_ws1_user1_api_v1_valid_data.copy()
        payload["company"] = 999
        payload["id"] = 123

        serializer = CompanyEmailSerializer(data=payload)

        assert serializer.is_valid(), serializer.errors
        validated = serializer.validated_data

        assert "company" not in validated
