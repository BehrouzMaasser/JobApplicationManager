from django.urls import path

from .views import (
    SignupView,
    LoginView,
    LogoutView,
    dashboard_view,
    JobBenefitListView, JobBenefitDetailView, JobBenefitUpdateView, JobBenefitCreateView, JobBenefitDeleteView,
    JobTaskListView, JobTaskCreateView, JobTaskDetailView, JobTaskUpdateView, JobTaskDeleteView
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("job_benefits/", JobBenefitListView.as_view(), name="job-benefit-list-web"),
    path("job_benefits/create/", JobBenefitCreateView.as_view(), name="job-benefit-create-web"),
    path("job_benefits/<int:pk>/", JobBenefitDetailView.as_view(), name="job-benefit-detail-web"),
    path("job_benefits/<int:pk>/edit/", JobBenefitUpdateView.as_view(), name="job-benefit-edit-web"),
    path("job_benefits/<int:pk>/delete/", JobBenefitDeleteView.as_view(), name="job-benefit-delete-web"),
    path("job_tasks/", JobTaskListView.as_view(), name="job-task-list-web"),
    path("job_tasks/create/", JobTaskCreateView.as_view(), name="job-task-create-web"),
    path("job_tasks/<int:pk>/", JobTaskDetailView.as_view(), name="job-task-detail-web"),
    path("job_tasks/<int:pk>/edit/", JobTaskUpdateView.as_view(), name="job-task-edit-web"),
    path("job_tasks/<int:pk>/delete/", JobTaskDeleteView.as_view(), name="job-task-delete-web"),
]
