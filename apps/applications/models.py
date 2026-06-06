from django.conf import settings
from django.core.exceptions import ValidationError

from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone

from apps.companies.models import JobPosition, CompanyEmail
from apps.documents.models import Document
from apps.workspaces.models import Workspace


# Create your models here.


class ApplicationStatus(models.Model):

    label = models.CharField(max_length=20, default="Pending")
    order = models.PositiveSmallIntegerField(unique=True, default=1)
    is_final = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        ordering = ("order", )
        verbose_name_plural = "Application Statuses"
        constraints = [
            models.UniqueConstraint(
                Lower("label"), name="globally_unique_application_status"
            )
        ]

    def __str__(self):

        return self.label


class JobApplication(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_applications"
    )

    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name="job_applications"
    )

    job_position = models.ForeignKey(
        JobPosition,
        on_delete=models.CASCADE,
        related_name="job_applications"
    )

    status = models.ForeignKey(
        ApplicationStatus, on_delete=models.PROTECT, db_index=True
    )

    date_applied = models.DateTimeField(null=True, blank=True, db_index=True)

    emails = models.ManyToManyField(
        CompanyEmail, related_name="job_applications", blank=True
    )

    documents = models.ManyToManyField(
        Document, related_name="job_applications",  blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=["owner", "workspace", "job_position"],
                name="unique_job_application_for_each_job_position_in_the_same_"
                     "workspace_for_the_user"
            )
        ]
        ordering = ("-date_applied", "owner", "workspace", "job_position")
        indexes = [
            models.Index(fields=["owner"]),
            models.Index(fields=["owner", "workspace"]),
            models.Index(fields=["owner", "workspace", "job_position"]),
        ]

    def __str__(self):

        return (f"{self.job_position.company.name} - {self.job_position} - "
                f"{self.status}")

    def clean(self):

        # Making sure the fields to validate are created
        if not all([self.owner_id, self.workspace_id, self.job_position_id]):
            return
        if self.owner != self.workspace.owner:
            raise ValidationError(
                {
                    "workspace": "Owner of the application should be the owner of "
                                 "the workspace!"
                }
            )
        if self.workspace != self.job_position.company.workspace:
            raise ValidationError(
                {
                    "job_position": "Workspace of the application should be the same"
                                    " workspace of the company's job position!"
                }
            )

        if self._validate_date_applied() and self.job_position.date_posted:
            if self.date_applied < self.job_position.date_posted:
                raise ValidationError(
                    {
                        "date_applied": "Date applied to the job position should be"
                                        " after the job position's release date!"
                    }
                )

    def _validate_date_applied(self):

        if not self.date_applied:
            return False

        if self.date_applied and self.date_applied > timezone.now():
            raise ValidationError(
                {"date_applied": "Date applied should not be in the future!"}
            )

        return True

    def save(self, *args, **kwargs):

        if not self.date_applied:
            self.date_applied = None

        super().save(*args, **kwargs)


class JobApplicationNote(models.Model):

    job_application = models.ForeignKey(
        JobApplication,
        on_delete=models.CASCADE,
        related_name="job_application_notes"
    )

    title = models.CharField(max_length=60)
    content = models.TextField()

    class Meta:

        constraints = [
            models.UniqueConstraint(
                Lower("title"), "job_application",
                name="unique_job_application_note_per_job_application"
            )
        ]
        ordering = ("job_application", "title")

    def __str__(self):

        return f"{self.job_application} - {self.title}"
