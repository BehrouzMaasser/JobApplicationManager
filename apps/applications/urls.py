from django.urls import path
from .views import (
    JobApplicationListView, JobApplicationDetailView, JobApplicationUpdateView,
    JobApplicationDeleteView,
)


urlpatterns = [
    path("", JobApplicationListView.as_view(), name="job-application-list-web"),
    path("<int:pk>/", JobApplicationDetailView.as_view(), name="job-application-detail-web"),
    path("<int:pk>/edit/", JobApplicationUpdateView.as_view(), name="job-application-edit-web"),
    path("<int:pk>/delete/", JobApplicationDeleteView.as_view(), name="job-application-delete-web"),
]
