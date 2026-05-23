from django.contrib import admin

from .models import (
    Company,
    CompanyNote,
    CompanyEmail,
    EmploymentType,
    JobPosition,
    JobSite,
    JobBenefit,
    JobTask,
    JobRequirement
)


# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "workspace", "website", "created_at", "updated_at")
    search_fields = ("name", "workspace__name")
    list_filter = ("created_at", "updated_at", "workspace__name")


@admin.register(CompanyNote)
class CompanyNoteAdmin(admin.ModelAdmin):
    list_display = ("company", "title", "content")


@admin.register(CompanyEmail)
class CompanyEmailAdmin(admin.ModelAdmin):
    list_display = ("company", "title", "email")


@admin.register(EmploymentType)
class EmploymentTypeAdmin(admin.ModelAdmin):
    list_display = ("name", )


@admin.register(JobPosition)
class JobPositionAdmin(admin.ModelAdmin):
    list_display = (
        "company", "title", "date_posted", "description", "min_salary",
        "max_salary", "created_at", "updated_at"
    )


@admin.register(JobSite)
class JJobSiteAdmin(admin.ModelAdmin):
    list_display = ("name", )


@admin.register(JobBenefit)
class JobBenefitAdmin(admin.ModelAdmin):
    list_display = ("name", )


@admin.register(JobTask)
class JobTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


@admin.register(JobRequirement)
class JobRequirementsAdmin(admin.ModelAdmin):
    list_display = ("title", "description")
