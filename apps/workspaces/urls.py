from django.urls import path
from .views import (
    WorkspaceListView,
    WorkspaceCreateView,
    WorkspaceDetailView,
    WorkspaceUpdateView,
    WorkspaceDeleteView
)

urlpatterns = [
    path("", WorkspaceListView.as_view(), name="workspace-list-web"),
    path("create/", WorkspaceCreateView.as_view(), name="workspace-create"),
    path("<int:pk>/", WorkspaceDetailView.as_view(), name="workspace-detail-web"),
    path("<int:pk>/edit/", WorkspaceUpdateView.as_view(), name="workspace-edit"),
    path("<int:pk>/delete/", WorkspaceDeleteView.as_view(), name="workspace-delete"),
]