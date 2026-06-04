from django.urls import path

from apps.documents.views import (
    # Document Type Views
    DocumentTypeListView,
    DocumentTypeCreateView,
    DocumentTypeDetailView,
    DocumentTypeDeleteView,
    DocumentTypeUpdateView,

    # Document Views
    DocumentListView,
    DocumentCreateView,
    DocumentDetailView,
    DocumentUpdateView,
    DocumentDeleteView,
    DownloadDocumentView,
    OpenDocumentView,

)

urlpatterns = [
    path("documents/<int:pk>/download/", DownloadDocumentView.as_view(), name="document-download-web"),
    path("documents/<int:pk>/open/", OpenDocumentView.as_view(), name="document-open-web"),
    path("document_types/", DocumentTypeListView.as_view(), name="document-type-list-web"),
    path("document_types/create/", DocumentTypeCreateView.as_view(), name="document-type-create-web"),
    path("document_types/<int:pk>/", DocumentTypeDetailView.as_view(), name="document-type-detail-web"),
    path("document_types/<int:pk>/edit/", DocumentTypeUpdateView.as_view(), name="document-type-edit-web"),
    path("document_types/<int:pk>/delete/", DocumentTypeDeleteView.as_view(),name="document-type-delete-web"),
    path("documents/", DocumentListView.as_view(), name="document-list-web"),
    path("documents/create/", DocumentCreateView.as_view(), name="document-create-web"),
    path("documents/<int:pk>/", DocumentDetailView.as_view(), name="document-detail-web"),
    path("documents/<int:pk>/edit/", DocumentUpdateView.as_view(), name="document-edit-web"),
    path("documents/<int:pk>/delete/", DocumentDeleteView.as_view(),name="document-delete-web"),
]
