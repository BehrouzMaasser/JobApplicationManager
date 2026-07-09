"""
Database models for the applications application.

This module defines job application statuses, job applications, and
application notes.
"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone

from apps.companies.models import (
    CompanyEmail,
    JobPosition,
)
from apps.documents.models import Document
from apps.workspaces.models import Workspace


# =========================================================
# Application Status
# =========================================================

class ApplicationStatus(models.Model):
    """
    Represents the current status of a job application.
    """

    label = models.CharField(max_length=20, default="Pending")
    order = models.PositiveSmallIntegerField(unique=True, default=1)
    is_final = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Model metadata."""

        ordering = ("order",)
        verbose_name_plural = "Application Statuses"

        constraints = [
            models.UniqueConstraint(
                Lower("label"),
                name="globally_unique_application_status",
                violation_error_code="duplicate_label",
                violation_error_message="Application status with this label already"
                                        " exists.",
            )
        ]

    def __str__(self):
        """Return the application status label."""

        return self.label


# =========================================================
# Job Application
# =========================================================

class JobApplication(models.Model):
    """
    Represents a user's application for a job position.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_applications",
    )

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="job_applications",
    )

    job_position = models.ForeignKey(
        JobPosition,
        on_delete=models.CASCADE,
        related_name="job_applications",
    )

    status = models.ForeignKey(
        ApplicationStatus,
        on_delete=models.PROTECT,
        db_index=True,
    )

    date_applied = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
    )

    emails = models.ManyToManyField(
        CompanyEmail,
        related_name="job_applications",
        blank=True,
    )

    documents = models.ManyToManyField(
        Document,
        related_name="job_applications",
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Model metadata."""

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "owner",
                    "workspace",
                    "job_position",
                ],
                name="unique_job_application_for_each_job_position_in_the_same_"
                "workspace_for_the_user",
                violation_error_code="duplicate_job_application",
                violation_error_message="Job application for job position already"
                                        " exists.",
            )
        ]

        ordering = (
            "-date_applied",
            "owner",
            "workspace",
            "job_position",
        )

        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["owner", "workspace"]),
            models.Index(fields=["owner", "workspace", "job_position"]),
        ]

    def __str__(self):
        """Return a human-readable representation of the application."""

        return (
            f"{self.job_position.company.name} - "
            f"{self.job_position} - "
            f"{self.status}"
        )

    def clean(self):
        """
        Validate ownership, workspace relationships, and application dates.
        """

        if not all(
            [
                self.owner_id,
                self.workspace_id,
                self.job_position_id,
            ]
        ):
            return

        if self.owner != self.workspace.owner:
            raise ValidationError(
                {
                    "workspace": (
                        "Owner of the application should be the owner of "
                        "the workspace!"
                    )
                }
            )

        if self.workspace != self.job_position.company.workspace:
            raise ValidationError(
                {
                    "job_position": (
                        "Workspace of the application should be the same "
                        "workspace of the company's job position!"
                    )
                }
            )

        if self._validate_date_applied() and self.job_position.date_posted:
            if self.date_applied < self.job_position.date_posted:
                raise ValidationError(
                    {
                        "date_applied": (
                            "Date applied to the job position should be "
                            "after the job position's release date!"
                        )
                    }
                )

    def _validate_date_applied(self):
        """
        Validate the application date.

        Returns:
            True if a date is present and valid, otherwise False.

        Raises:
            ValidationError:
                If the application date is in the future.
        """

        if not self.date_applied:
            return False

        if self.date_applied > timezone.now():
            raise ValidationError(
                {
                    "date_applied": (
                        "Date applied should not be in the future!"
                    )
                }
            )

        return True

    def save(self, *args, **kwargs):
        """Normalize optional fields before saving."""

        if not self.date_applied:
            self.date_applied = None

        super().save(*args, **kwargs)


# =========================================================
# Job Application Note
# =========================================================

class JobApplicationNote(models.Model):
    """
    Represents a note associated with a job application.
    """

    job_application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name="job_application_notes",
    )

    title = models.CharField(max_length=60)
    content = models.TextField()

    class Meta:
        """Model metadata."""

        constraints = [
            models.UniqueConstraint(
                Lower("title"),
                "job_application",
                name="unique_job_application_note_per_job_application",
                violation_error_code="duplicate_job_application_note",
                violation_error_message="Job application note with this title "
                                        "already exists.",
            )
        ]

        ordering = ("job_application", "title")

    def __str__(self):
        """Return a human-readable representation of the application note."""

        return f"{self.job_application} - {self.title}"
