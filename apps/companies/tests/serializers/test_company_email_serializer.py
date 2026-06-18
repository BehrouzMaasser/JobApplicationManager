import pytest

from apps.companies.api.v1.serializers import CompanyEmailSerializer


@pytest.mark.django_db
class TestCompanyEmailSerializer:

    def test_valid_data(self, co_email1_co1_ws1_user1_valid_data):

        serializer = CompanyEmailSerializer(data=co_email1_co1_ws1_user1_valid_data)

        assert serializer.is_valid()

    def test_invalid_email(self, co_email1_co1_ws1_user1_valid_data):

        co_email1_co1_ws1_user1_valid_data["email"] = "invalid-email"

        serializer = CompanyEmailSerializer(data=co_email1_co1_ws1_user1_valid_data)

        assert not serializer.is_valid()
        assert "email" in serializer.errors
