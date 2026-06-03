from django.urls import path

from .views import (
    SignupView,
    LoginView,
    LogoutView,
    dashboard_view,
    JobBenefitListView,
    JobBenefitDetailView,
    JobBenefitUpdateView,
    JobBenefitCreateView,
    JobBenefitDeleteView
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
]
