from django.urls import path
from .views import (
    CompanyListView, CompanyDetailView, CompanyUpdateView,
    CompanyDeleteView,
    CompanyEmailListView, CompanyEmailDetailView,
    CompanyEmailUpdateView, CompanyEmailDeleteView,
    CompanyNoteDetailView, CompanyNoteUpdateView,
    CompanyNoteDeleteView, CompanyNoteListView, JobPositionListView,
    JobPositionDetailView, JobPositionUpdateView,
    JobPositionDeleteView
)

urlpatterns = [
    path("", CompanyListView.as_view(), name="company-list-web"),
    path("<int:pk>/", CompanyDetailView.as_view(), name="company-detail-web"),
    path("<int:pk>/edit/", CompanyUpdateView.as_view(), name="company-edit-web"),
    path("<int:pk>/delete/", CompanyDeleteView.as_view(), name="company-delete-web"),
    path("emails/", CompanyEmailListView.as_view(), name="company-email-list-web"),
    path("emails/<int:pk>/", CompanyEmailDetailView.as_view(), name="company-email-detail-web"),
    path("emails/<int:pk>/edit/", CompanyEmailUpdateView.as_view(), name="company-email-edit-web"),
    path("emails/<int:pk>/delete/", CompanyEmailDeleteView.as_view(), name="company-email-delete-web"),
    path("notes/", CompanyNoteListView.as_view(), name="company-note-list-web"),
    path("notes/<int:pk>/", CompanyNoteDetailView.as_view(), name="company-note-detail-web"),
    path("notes/<int:pk>/edit/", CompanyNoteUpdateView.as_view(), name="company-note-edit-web"),
    path("notes/<int:pk>/delete/", CompanyNoteDeleteView.as_view(), name="company-note-delete-web"),
    path("job_positions/", JobPositionListView.as_view(), name="job-position-list-web"),
    path("job_positions/<int:pk>/", JobPositionDetailView.as_view(), name="job-position-detail-web"),
    path("job_positions/<int:pk>/edit/", JobPositionUpdateView.as_view(), name="job-position-edit-web"),
    path("job_positions/<int:pk>/delete/", JobPositionDeleteView.as_view(), name="job-position-delete-web"),
]
