from django.urls import path
from .views import (
    CompanyListView,
    CompanyCreateView,
    CompanyDetailView,
    CompanyUpdateView,
    CompanyDeleteView,
    CompanyEmailListView,
    CompanyEmailCreateView,
    CompanyEmailDetailView,
    CompanyEmailUpdateView,
    CompanyEmailDeleteView
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
]
