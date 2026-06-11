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
    path("create/", WorkspaceCreateView.as_view(), name="workspace-create-web"),
    path("<uuid:workspace_id>/", WorkspaceDetailView.as_view(), name="workspace-detail-web"),
    path("<uuid:workspace_id>/edit/", WorkspaceUpdateView.as_view(), name="workspace-edit-web"),
    path("<uuid:workspace_id>/delete/", WorkspaceDeleteView.as_view(), name="workspace-delete-web"),
]
