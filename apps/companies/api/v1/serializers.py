from rest_framework import serializers

# Models
from apps.companies.models import (
    Company,
    CompanyNote,
    CompanyEmail,
    JobBenefit,
    JobTask,
    JobRequirement,
    JobPosition,
    EmploymentType,
    JobSite
)


# Serializers
class CompanySerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
    )

    website = serializers.URLField(
        required=False,
        allow_null=True,
        allow_blank=False,
    )

    class Meta:

        model = Company

        fields = [
            "id",
            "workspace",
            "name",
            "website",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "workspace",
            "created_at",
            "updated_at",
        ]


class CompanyNoteSerializer(serializers.ModelSerializer):

    title = serializers.CharField(
        max_length=40,
        required=True,
        allow_null=False,
        allow_blank=False,
    )

    content = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
    )

    class Meta:

        model = CompanyNote

        fields = [
            "id",
            "company",
            "title",
            "content",
        ]

        read_only_fields = [
            "id",
            "company",
        ]


class CompanyEmailSerializer(serializers.ModelSerializer):

    title = serializers.CharField(
        max_length=60,
        required=True,
        allow_null=False,
        allow_blank=False,
    )

    email = serializers.EmailField(
        required=True,
        allow_null=False,
        allow_blank=False,
    )

    class Meta:

        model = CompanyEmail

        fields = [
            "id",
            "company",
            "title",
            "email",
        ]

        read_only_fields = [
            "id",
            "company",
        ]


class JobBenefitSerializer(serializers.ModelSerializer):

    name = serializers.CharField(
        max_length=25,
        required=True,
        allow_null=False,
        allow_blank=False,
    )

    description = serializers.CharField(
        max_length=60,
        required=False,
        allow_null=False,
        allow_blank=False,
    )

    class Meta:

        model = JobBenefit

        fields = [
            "id",
            "name",
            "description",
        ]

        read_only_fields = [
            "id",
        ]


class JobTaskSerializer(serializers.ModelSerializer):

    title = serializers.CharField(
        max_length=25,
        required=True,
        allow_null=False,
        allow_blank=False,
    )

    description = serializers.CharField(
        max_length=60,
        required=False,
        allow_null=False,
        allow_blank=False,
    )

    class Meta:

        model = JobTask

        fields = [
            "id",
            "title",
            "description",
        ]

        read_only_fields = [
            "id",
        ]


class JobRequirementSerializer(serializers.ModelSerializer):

    title = serializers.CharField(
        max_length=50,
        required=True,
        allow_null=False,
        allow_blank=False,
    )

    description = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False,
    )

    class Meta:

        model = JobRequirement

        fields = [
            "id",
            "title",
            "description",
        ]

        read_only_fields = [
            "id",
        ]


class JobPositionSerializer(serializers.ModelSerializer):

    # For Many-To-Many relations
    employment_types = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=EmploymentType.objects.all(),
        required=True,
        allow_null=False,
        allow_empty=False
    )

    job_sites = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=JobSite.objects.all(),
        required=True,
        allow_null=False,
        allow_empty=False
    )

    tasks = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=JobTask.objects.all(),
        required=True,
        allow_null=False,
        allow_empty=False
    )

    requirements = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=JobRequirement.objects.all(),
        required=True,
        allow_null=False,
        allow_empty=False
    )

    benefits = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=JobBenefit.objects.all(),
        required=False,
        allow_null=False,
        allow_empty=True
    )

    class Meta:

        model = JobPosition

        fields = [
            "id",
            "company",
            "employment_types",
            "job_sites",
            "title",
            "date_posted",
            "description",
            "tasks",
            "requirements",
            "benefits",
            "min_salary",
            "max_salary",
            "job_position_ad_url",
            "job_location_url",
            "job_portal_url",
            "portal_username",
            "portal_password",
            "created_at",
            "updated_at",
        ]

        extra_kwargs = {
            "id": {
                "read_only": True
            },
            "company": {
                "read_only": True
            },
            "created_at": {
                "read_only": True
            },
            "updated_at": {
                "read_only": True
            },
            "title": {
                "required": True, "allow_null": False, "allow_blank": False
            },
            "date_posted": {
                "required": False, "allow_null": True,
            },
            "description": {
                "required": True, "allow_null": False, "allow_blank": False
            },
            "min_salary": {
                "required": False, "allow_null": True,
            },
            "max_salary": {
                "required": False, "allow_null": True,
            },
            "job_position_ad_url": {
                "required": False, "allow_null": True, "allow_blank": False
            },
            "job_location_url": {
                "required": False, "allow_null": True, "allow_blank": False
            },
            "job_portal_url": {
                "required": False, "allow_null": True, "allow_blank": False
            },
            "portal_username": {
                "required": False, "allow_null": True, "allow_blank": False
            },
            "portal_password": {
                "required": False, "allow_null": True, "allow_blank": False
            },
        }
