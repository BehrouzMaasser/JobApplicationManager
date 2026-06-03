from django.urls import path
from .views import (
    CompanyListView,
    CompanyCreateView,
    CompanyDetailView,
    CompanyUpdateView,
    CompanyDeleteView
)

urlpatterns = [
    path("", CompanyListView.as_view(), name="company-list-web"),
    path("create/", CompanyCreateView.as_view(), name="company-create-web"),
    path("<int:pk>/", CompanyDetailView.as_view(), name="company-detail-web"),
    path("<int:pk>/edit/", CompanyUpdateView.as_view(), name="company-edit-web"),
    path("<int:pk>/delete/", CompanyDeleteView.as_view(), name="company-delete-web"),
]
