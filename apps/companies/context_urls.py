from django.urls import path
from .views import (
    CompanyCreateView,
    CompanyEmailCreateView, CompanyNoteCreateView, JobPositionCreateView
)

urlpatterns = [
    path("create/", CompanyCreateView.as_view(), name="company-create-web"),
    path("<int:company_id>/emails/create/", CompanyEmailCreateView.as_view(), name="company-email-create-web"),
    path("<int:company_id>/notes/create/", CompanyNoteCreateView.as_view(), name="company-note-create-web"),
    path("<int:company_id>/job_positions/create/", JobPositionCreateView.as_view(), name="job-position-create-web"),
]
