from django.contrib import admin

from apps.applications.forms import JobApplicationForm, JobApplicationNoteForm

from apps.applications.models import (
    ApplicationStatus,
    JobApplication,
    JobApplicationNote
)


# Register your models here.


@admin.register(ApplicationStatus)
class ApplicationStatusAdmin(admin.ModelAdmin):
    list_display = ("label", "order", "is_final", "created_at")


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = (
        "owner", "workspace", "job_position", "status", "date_applied",
        "created_at", "updated_at"
    )
    form = JobApplicationForm


@admin.register(JobApplicationNote)
class JobApplicationNoteAdmin(admin.ModelAdmin):
    list_display = ("job_application", "title", "content")
    form = JobApplicationNoteForm
