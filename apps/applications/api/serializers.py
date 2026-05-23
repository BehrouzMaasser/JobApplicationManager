from rest_framework import serializers

from apps.applications.models import (
    JobApplication,
    JobApplicationNote,
)

from apps.companies.models import CompanyEmail
from apps.documents.models import Document


class JobApplicationSerializer(serializers.ModelSerializer):

    emails = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CompanyEmail.objects.all(),
        required=True,
        allow_null=False,
        allow_empty=False,
    )

    documents = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Document.objects.all(),
        required=False,
        allow_null=False,
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


class JobApplicationNoteSerializer(serializers.ModelSerializer):

    title = serializers.CharField(
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
