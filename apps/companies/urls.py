from django.urls import path
from .views import (
    CompanyListView, CompanyCreateView, CompanyDetailView, CompanyUpdateView,
    CompanyDeleteView,
    CompanyEmailListView, CompanyEmailCreateView, CompanyEmailDetailView,
    CompanyEmailUpdateView, CompanyEmailDeleteView,
    CompanyNoteCreateView, CompanyNoteDetailView, CompanyNoteUpdateView,
    CompanyNoteDeleteView, CompanyNoteListView, JobPositionListView,
    JobPositionCreateView, JobPositionDetailView, JobPositionUpdateView,
    JobPositionDeleteView
)

urlpatterns = [
    path("", CompanyListView.as_view(), name="company-list-web"),
    path("create/", CompanyCreateView.as_view(), name="company-create-web"),
    path("<int:pk>/", CompanyDetailView.as_view(), name="company-detail-web"),
    path("<int:pk>/edit/", CompanyUpdateView.as_view(), name="company-edit-web"),
    path("<int:pk>/delete/", CompanyDeleteView.as_view(), name="company-delete-web"),
    path("<int:company_id>/emails/", CompanyEmailListView.as_view(), name="company-email-list-web"),
    path("<int:company_id>/emails/create/", CompanyEmailCreateView.as_view(), name="company-email-create-web"),
    path("<int:company_id>/emails/<int:pk>/", CompanyEmailDetailView.as_view(), name="company-email-detail-web"),
    path("<int:company_id>/emails/<int:pk>/edit/", CompanyEmailUpdateView.as_view(), name="company-email-edit-web"),
    path("<int:company_id>/emails/<int:pk>/delete/", CompanyEmailDeleteView.as_view(), name="company-email-delete-web"),
    path("<int:company_id>/notes/", CompanyNoteListView.as_view(), name="company-note-list-web"),
    path("<int:company_id>/notes/create/", CompanyNoteCreateView.as_view(), name="company-note-create-web"),
    path("<int:company_id>/notes/<int:pk>/", CompanyNoteDetailView.as_view(), name="company-note-detail-web"),
    path("<int:company_id>/notes/<int:pk>/edit/", CompanyNoteUpdateView.as_view(), name="company-note-edit-web"),
    path("<int:company_id>/notes/<int:pk>/delete/", CompanyNoteDeleteView.as_view(), name="company-note-delete-web"),
    path("<int:company_id>/job_positions/", JobPositionListView.as_view(), name="job-position-list-web"),
    path("<int:company_id>/job_positions/create/", JobPositionCreateView.as_view(), name="job-position-create-web"),
    path("<int:company_id>/job_positions/<int:pk>/", JobPositionDetailView.as_view(), name="job-position-detail-web"),
    path("<int:company_id>/job_positions/<int:pk>/edit/", JobPositionUpdateView.as_view(), name="job-position-edit-web"),
    path("<int:company_id>/job_positions/<int:pk>/delete/", JobPositionDeleteView.as_view(), name="job-position-delete-web"),
]
