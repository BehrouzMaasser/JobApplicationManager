from apps.documents.api.v1.serializers import DocumentTypeSerializer


class TestDocumentTypeSerializer:

    def test_valid_data(self):

        data = {
            "name": "Resume",
            "description": "CV and related documents",
        }

        serializer = DocumentTypeSerializer(data=data)

        assert serializer.is_valid(), serializer.errors

    def test_valid_without_description(self):

        data = {
            "name": "Resume",
        }

        serializer = DocumentTypeSerializer(data=data)

        assert serializer.is_valid(), serializer.errors

    def test_accepts_null_description(self):

        data = {
            "name": "Resume",
            "description": None,
        }

        serializer = DocumentTypeSerializer(data=data)

        assert serializer.is_valid(), serializer.errors

    def test_requires_name(self):

        serializer = DocumentTypeSerializer(data={})

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_rejects_blank_name(self):

        data = {
            "name": "",
        }

        serializer = DocumentTypeSerializer(data=data)

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_rejects_null_name(self):

        data = {
            "name": None,
        }

        serializer = DocumentTypeSerializer(data=data)

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_rejects_name_too_long(self):

        data = {
            "name": "a" * 41,
        }

        serializer = DocumentTypeSerializer(data=data)

        assert not serializer.is_valid()
        assert "name" in serializer.errors

    def test_rejects_blank_description(self):

        data = {
            "name": "Resume",
            "description": "",
        }

        serializer = DocumentTypeSerializer(data=data)

        assert not serializer.is_valid()
        assert "description" in serializer.errors

    def test_read_only_fields_are_ignored(self):

        data = {
            "name": "Resume",
            "owner": 999,
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-01T00:00:00Z",
        }

        serializer = DocumentTypeSerializer(data=data)

        assert serializer.is_valid(), serializer.errors

        assert set(serializer.validated_data.keys()) == {"name"}
