from django.urls import path
from .views import JobApplicationCreateView



urlpatterns = [
    path("create/", JobApplicationCreateView.as_view(), name="job-application-create-web"),
]
