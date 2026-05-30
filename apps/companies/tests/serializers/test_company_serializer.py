import pytest

from apps.companies.api.serializers import CompanySerializer


@pytest.mark.django_db
class TestCompanySerializer:

    def test_valid_data(self, co1_ws1_user1_valid_data):

        serializer = CompanySerializer(data=co1_ws1_user1_valid_data)

        assert serializer.is_valid()

    def test_name_required(self, co1_ws1_user1_valid_data):

        co1_ws1_user1_valid_data.pop("name")

        serializer = CompanySerializer(data=co1_ws1_user1_valid_data)

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_name_cannot_be_blank(self):

        data = {
            "name": "",
        }

        serializer = CompanySerializer(data=data)

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_invalid_website(self, co1_ws1_user1_valid_data):

        co1_ws1_user1_valid_data["website"] = "invalid-website"

        serializer = CompanySerializer(data=co1_ws1_user1_valid_data)

        assert not serializer.is_valid()
        assert "website" in serializer.errors
