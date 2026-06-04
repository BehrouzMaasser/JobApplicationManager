from django.urls import path

from apps.documents.views import (
    DocumentTypeListView, DocumentTypeCreateView, DocumentTypeDetailView, DocumentTypeDeleteView, DocumentTypeUpdateView

)

urlpatterns = [
    path("document_types/", DocumentTypeListView.as_view(), name="document-type-list-web"),
    path("document_types/create/", DocumentTypeCreateView.as_view(), name="document-type-create-web"),
    path("document_types/<int:pk>/", DocumentTypeDetailView.as_view(), name="document-type-detail-web"),
    path("document_types/<int:pk>/edit/", DocumentTypeUpdateView.as_view(), name="document-type-edit-web"),
    path("document_types/<int:pk>/delete/", DocumentTypeDeleteView.as_view(),name="document-type-delete-web"),
]
