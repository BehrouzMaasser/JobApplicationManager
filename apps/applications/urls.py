from django.urls import path
from .views import (
    # Job Applications
    JobApplicationListView, JobApplicationDetailView, JobApplicationUpdateView,
    JobApplicationDeleteView,

    # Job Application Notes
    JobApplicationNoteListView, JobApplicationNoteUpdateView,
    JobApplicationNoteDeleteView, JobApplicationNoteCreateView,
    JobApplicationNoteDetailView,
)


urlpatterns = [
    # Job Application
    path("", JobApplicationListView.as_view(), name="job-application-list-web"),
    path("<int:pk>/", JobApplicationDetailView.as_view(), name="job-application-detail-web"),
    path("<int:pk>/edit/", JobApplicationUpdateView.as_view(), name="job-application-edit-web"),
    path("<int:pk>/delete/", JobApplicationDeleteView.as_view(), name="job-application-delete-web"),

    # Job Application Note
    path("job_application_notes/", JobApplicationNoteListView.as_view(), name="job-application-note-list-web"),
    path("<int:job_application_id>/job_application_notes/create/", JobApplicationNoteCreateView.as_view(), name="job-application-note-create-web"),
    path("job_application_notes/<int:pk>/", JobApplicationNoteDetailView.as_view(), name="job-application-note-detail-web"),
    path("job_application_notes/<int:pk>/edit/", JobApplicationNoteUpdateView.as_view(), name="job-application-note-edit-web"),
    path("job_application_notes/<int:pk>/delete/", JobApplicationNoteDeleteView.as_view(), name="job-application-note-delete-web"),
]
