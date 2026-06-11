from django.conf import settings
from django.core.exceptions import ValidationError

from django.db import models
from django.db.models.functions import Lower
from django.utils import timezone

from apps.workspaces.models import Workspace


# Create your models here.


class Company(models.Model):

    workspace = models.ForeignKey(
        Workspace, on_delete=models.CASCADE, related_name="companies"
    )

    name = models.CharField(max_length=60)
    website = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("name"), "workspace", name="unique_company_name_per_workspace"
            )
        ]
        ordering = ("name", "created_at", "updated_at", "workspace")
        verbose_name_plural = "companies"
        indexes = [
            models.Index(fields=["workspace", "name"]),
        ]

    def __str__(self):

        return self.name

    def save(self, *args, **kwargs):

        if self.website == "":
            self.website = None

        super().save(*args, **kwargs)


class CompanyNote(models.Model):

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_notes"
    )

    title = models.CharField(max_length=40)
    content = models.TextField()

    class Meta:

        constraints = [
            models.UniqueConstraint(
                Lower("title"), "company", name="unique_note_title_per_company"
            )
        ]
        indexes = [
            models.Index(fields=["company"]),
            models.Index(fields=["company", "title"]),
        ]
        ordering = ("company", "title")

    def __str__(self):

        return self.title


class CompanyEmail(models.Model):

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="company_emails")

    title = models.CharField(max_length=60)
    email = models.EmailField()

    class Meta:

        constraints = [
            models.UniqueConstraint(
                Lower("email"), Lower("title"), "company",
                name="unique_company_email_and_title_per_company"
            )
        ]
        indexes = [
            models.Index(fields=["company"]),
            models.Index(fields=["company", "title"]),
            models.Index(fields=["company", "email"]),
        ]
        ordering = ("company", "title")

    def __str__(self):

        return self.title

    def save(self, *args, **kwargs):

        if self.email:
            self.email = self.email.lower()

        super().save(*args, **kwargs)


class EmploymentType(models.Model):

    name = models.CharField(max_length=15)

    class Meta:

        constraints = [
            models.UniqueConstraint(
                Lower("name"), name="globally_unique_employment_type"
            )
        ]

    def __str__(self):
        return self.name


class JobSite(models.Model):

    name = models.CharField(max_length=15)

    class Meta:

        constraints = [
            models.UniqueConstraint(
                Lower("name"), name="globally_unique_job_site"
            )
        ]

    def __str__(self):
        return self.name


class JobBenefit(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_benefits"
    )

    name = models.CharField(max_length=25)
    description = models.TextField(max_length=60, blank=True, default="")

    class Meta:

        constraints = [
            models.UniqueConstraint(
                Lower("name"), Lower("description"), "user",
                name="unique_job_benefit_per_user"
            )
        ]
        ordering = ("user", "name")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        if self.description is None:
            self.description = ""

        super().save(*args, **kwargs)


class JobTask(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_tasks"
    )

    title = models.CharField(max_length=25)
    description = models.TextField(max_length=60, blank=True, default="")

    class Meta:

        constraints = [
            models.UniqueConstraint(
                Lower("title"), Lower("description"), "user",
                name="unique_job_task_per_user"
            )
        ]
        indexes = [
            models.Index(fields=["title"]),
        ]
        ordering = ("user", "title")

    def __str__(self):

        return self.title

    def save(self, *args, **kwargs):

        if self.description is None:
            self.description = ""

        super().save(*args, **kwargs)


class JobRequirement(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_requirements"
    )

    title = models.CharField(max_length=50)
    description = models.TextField(max_length=60, blank=True, default="")

    class Meta:

        constraints = [
            models.UniqueConstraint(
                Lower("description"), Lower("title"), "user",
                name="unique_job_requirement_per_user"
            )
        ]
        ordering = ("user", "title")

    def __str__(self):

        return self.title

    def save(self, *args, **kwargs):

        if self.description is None:
            self.description = ""

        super().save(*args, **kwargs)


class JobPosition(models.Model):

    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="job_positions")

    employment_types = models.ManyToManyField(
        EmploymentType,  related_name="job_positions"
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

        ordering = ["company", "title"]
        indexes = [
            models.Index(fields=["company"]),
            models.Index(fields=["company", "title"]),
        ]

    def clean(self):

        if self.min_salary and self.max_salary:
            if self.min_salary > self.max_salary:
                raise ValidationError(
                    {"min_salary": "Min salary cannot exceed max salary."}
                )

        if self.date_posted:
            if self.date_posted > timezone.now():
                raise ValidationError(
                    {"date_posted": "Date post cannot be in the future."}
                )

    def __str__(self):

        return self.title

    def save(self, *args, **kwargs):

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
