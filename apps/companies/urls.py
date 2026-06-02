from django.urls import path
from .views import (
    CompanyListView,
    CompanyCreateView,
    CompanyDetailView,
    CompanyUpdateView,
    CompanyDeleteView
)

urlpatterns = [
    path("<uuid:workspace_id>/", CompanyListView.as_view(), name="company-list-web"),
    path("<uuid:workspace_id>/create/", CompanyCreateView.as_view(), name="company-create"),
    path("<int:pk>/", CompanyDetailView.as_view(), name="company-detail-web"),
    path("<int:pk>/edit/", CompanyUpdateView.as_view(), name="company-edit"),
    path("<int:pk>/delete/", CompanyDeleteView.as_view(), name="company-delete"),
]
