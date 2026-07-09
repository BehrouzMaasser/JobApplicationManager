"""
REST API serializers for the Applications domain.
"""

from rest_framework import serializers

from apps.applications.models import (
    JobApplication,
    JobApplicationNote,
)

from apps.companies.models import CompanyEmail
from apps.documents.models import Document


# Serializers

# =========================================================
# Job Application
# =========================================================

class JobApplicationSerializer(serializers.ModelSerializer):
    """
    Serialize job application data for API requests and responses.
    """

    emails = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CompanyEmail.objects.all(),
        required=False,
        allow_empty=True,
    )

    documents = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Document.objects.all(),
        required=False,
        allow_empty=True,
    )

    date_applied = serializers.DateTimeField(
        required=False,
        allow_null=True,
    )

    class Meta:

        model = JobApplication

        fields = [
            "id",
            "owner",
            "workspace",
            "job_position",
            "status",
            "date_applied",
            "created_at",
            "updated_at",
            "documents",
            "emails",
        ]

        read_only_fields = [
            "id",
            "owner",
            "workspace",
            "job_position",
            "created_at",
            "updated_at",
        ]


# =========================================================
# Job Application Note
# =========================================================

class JobApplicationNoteSerializer(serializers.ModelSerializer):
    """
    Serialize job application note data for API requests and responses.
    """

    title = serializers.CharField(
        max_length=60,
        required=True,
        allow_blank=False,
        allow_null=False,
    )

    content = serializers.CharField(
        required=True,
        allow_blank=False,
        allow_null=False,
    )

    class Meta:

        model = JobApplicationNote

        fields = [
            "id",
            "job_application",
            "title",
            "content",
        ]

        read_only_fields = [
            "id",
            "job_application",
        ]
