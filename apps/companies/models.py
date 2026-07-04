"""
Database models for the companies application.

This module defines companies and their related entities, including notes,
emails, employment types, job sites, benefits, tasks, requirements, and
job positions.
"""

from django.conf import settings
from django.core.exceptions import ValidationError

from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone

from apps.workspaces.models import Workspace


class Company(models.Model):
    """Represents a company belonging to a workspace."""

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="companies"
    )

    name = models.CharField(max_length=60)
    website = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Model metadata."""
        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                "workspace",
                name="unique_company_name_per_workspace",
                violation_error_message="A company with this name already exists in"
                                        " the workspace.",
                violation_error_code="duplicate_company_name"
            )
        ]
        ordering = ("name", "created_at", "updated_at", "workspace")
        verbose_name_plural = "companies"
        indexes = [
            models.Index(fields=["workspace", "name"]),
        ]

    def __str__(self):
        """Return the company name."""

        return self.name

    def save(self, *args, **kwargs):
        """Normalize optional fields before saving."""

        if self.website == "":
            self.website = None

        super().save(*args, **kwargs)


class CompanyNote(models.Model):
    """Represents a note associated with a company."""

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="company_notes"
    )

    title = models.CharField(max_length=40)
    content = models.TextField()

    class Meta:
        """Model metadata."""

        constraints = [
            models.UniqueConstraint(
                Lower("title"),
                "company",
                name="unique_note_title_per_company",
                violation_error_message="A company note with this title already "
                                        "exists in the company.",
                violation_error_code="duplicate_company_note_title"
            )
        ]
        indexes = [
            models.Index(fields=["company"]),
            models.Index(fields=["company", "title"]),
        ]
        ordering = ("company", "title")

    def __str__(self):
        """Return the note title."""

        return self.title


class CompanyEmail(models.Model):
    """Represents an email address associated with a company."""

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="company_emails"
    )

    title = models.CharField(max_length=60)
    email = models.EmailField()

    class Meta:
        """Model metadata."""

        constraints = [
            models.UniqueConstraint(
                Lower("email"),
                Lower("title"),
                "company",
                name="unique_company_email_and_title_per_company",
                violation_error_message="A company email with this email address "
                                        "and title already exists in the company.",
                violation_error_code="duplicate_company_email"
            )
        ]
        indexes = [
            models.Index(fields=["company"]),
            models.Index(fields=["company", "title"]),
            models.Index(fields=["company", "email"]),
        ]
        ordering = ("company", "title")

    def __str__(self):
        """Return the email title."""

        return self.title

    def save(self, *args, **kwargs):
        """Normalize optional fields before saving."""

        if self.email:
            self.email = self.email.lower()

        super().save(*args, **kwargs)


class EmploymentType(models.Model):
    """Represents a type of employment."""

    name = models.CharField(max_length=15)

    class Meta:
        """Model metadata."""

        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="globally_unique_employment_type",
                violation_error_message="An employment type with this name already "
                                        "exists.",
                violation_error_code="duplicate_employment_type_name"
            )
        ]
        ordering = ("name", )

    def __str__(self):
        """Return the employment type name."""

        return self.name


class JobSite(models.Model):
    """Represents a job site classification."""

    name = models.CharField(max_length=15)

    class Meta:
        """Model metadata."""

        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                name="globally_unique_job_site",
                violation_error_message="A job site with this name already exists.",
                violation_error_code="duplicate_job_site_name"
            )
        ]

        ordering = ("name", )

    def __str__(self):
        """Return the job site name."""

        return self.name


class JobBenefit(models.Model):
    """Represents a reusable job benefit defined by a user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_benefits"
    )

    name = models.CharField(max_length=25)
    description = models.TextField(max_length=60, blank=True, default="")

    class Meta:
        """Model metadata."""

        constraints = [
            models.UniqueConstraint(
                Lower("name"),
                Lower("description"),
                "user",
                name="unique_job_benefit_per_user",
                violation_error_message="A job benefit with this name and "
                                        "description already exists.",
                violation_error_code="duplicate_job_benefit"
            )
        ]
        ordering = ("user", "name")

    def __str__(self):
        """Return the job benefit name."""

        return self.name

    def save(self, *args, **kwargs):
        """Normalize optional fields before saving."""

        if self.description is None:
            self.description = ""

        super().save(*args, **kwargs)


class JobTask(models.Model):
    """Represents a reusable task associated with job positions."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_tasks"
    )

    title = models.CharField(max_length=25)
    description = models.TextField(max_length=60, blank=True, default="")

    class Meta:
        """Model metadata."""

        constraints = [
            models.UniqueConstraint(
                Lower("title"),
                Lower("description"),
                "user",
                name="unique_job_task_per_user",
                violation_error_message="A job task with this title and description "
                                        "already exists.",
                violation_error_code="duplicate_job_task"
            )
        ]
        indexes = [
            models.Index(fields=["title"]),
        ]
        ordering = ("user", "title")

    def __str__(self):
        """Return the job task name."""

        return self.title

    def save(self, *args, **kwargs):
        """Normalize optional fields before saving."""

        if self.description is None:
            self.description = ""

        super().save(*args, **kwargs)


class JobRequirement(models.Model):
    """Represents a reusable job requirement defined by a user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_requirements"
    )

    title = models.CharField(max_length=50)
    description = models.TextField(max_length=60, blank=True, default="")

    class Meta:
        """Model metadata."""

        constraints = [
            models.UniqueConstraint(
                Lower("description"),
                Lower("title"),
                "user",
                name="unique_job_requirement_per_user",
                violation_error_message="A job requirement with this title and "
                                        "description already exists.",
                violation_error_code="duplicate_job_requirement"
            )
        ]
        ordering = ("user", "title")

    def __str__(self):
        """Return the job requirement title."""

        return self.title

    def save(self, *args, **kwargs):
        """Normalize optional fields before saving."""

        if self.description is None:
            self.description = ""

        super().save(*args, **kwargs)


class JobPosition(models.Model):
    """Represents an advertised job position at a company."""

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="job_positions"
    )

    employment_types = models.ManyToManyField(
        EmploymentType,
        related_name="job_positions"
    )

    job_sites = models.ManyToManyField(JobSite, related_name="job_positions")

    title = models.CharField(max_length=150)
    date_posted = models.DateTimeField(null=True, blank=True)
    description = models.TextField()

    tasks = models.ManyToManyField(JobTask, related_name="job_positions")

    requirements = models.ManyToManyField(
        JobRequirement, related_name="job_positions"
    )

    benefits = models.ManyToManyField(
        JobBenefit, related_name="job_positions", blank=True
    )

    min_salary = models.PositiveIntegerField(null=True, blank=True)
    max_salary = models.PositiveIntegerField(null=True, blank=True)
    job_position_ad_url = models.URLField(blank=True, null=True)
    job_location_url = models.URLField(blank=True, null=True)
    job_portal_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # The data below should be protected(implementation later)
    portal_username = models.CharField(max_length=150, null=True, blank=True)
    portal_password = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        """Model metadata."""

        indexes = [
            models.Index(fields=["company"]),
            models.Index(fields=["company", "title"]),
        ]
        ordering = ("company", "title")

    def clean(self):

        if not (self.min_salary is None or self.max_salary is None):
            if self.min_salary > self.max_salary:
                raise ValidationError(
                    {"min_salary": "Min salary cannot exceed max salary."}
                )

        if self.date_posted is not None:
            if self.date_posted > timezone.now():
                raise ValidationError(
                    {"date_posted": "Date post cannot be in the future."}
                )

    def __str__(self):
        """Return the job position title."""

        return self.title

    def save(self, *args, **kwargs):
        """Normalize optional fields before saving."""

        if self.job_position_ad_url == "":
            self.job_position_ad_url = None

        if self.job_location_url == "":
            self.job_location_url = None

        if self.job_portal_url == "":
            self.job_portal_url = None

        if self.portal_username == "":
            self.portal_username = None

        if self.portal_password == "":
            self.portal_password = None

        super().save(*args, **kwargs)
