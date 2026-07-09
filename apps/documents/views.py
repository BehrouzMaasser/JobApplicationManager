# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.core.mixins.app_context_mixin import AppContextMixin
from apps.core.mixins.document_file_response_mixin import DocumentFileResponseMixin
from apps.core.mixins.documents_form_mixin import DocumentFormMixin

# Django
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

# Generic Views
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

# Contexts
from apps.core.contexts.extra_context import ExtraContext
from apps.core.mixins.view_exception_handler import ViewExceptionHandlerMixin

# Models
from apps.documents.models import DocumentType, Document

# Selectors
from apps.documents.selectors.document_type_selector import DocumentTypeSelector
from apps.documents.selectors.document_selector import DocumentSelector

# Services
from apps.documents.services.document_type_service import DocumentTypeService
from apps.documents.services.document_service import DocumentService


class DocumentTypeListView(ViewExceptionHandlerMixin, LoginRequiredMixin, ListView):

    model = DocumentType
    template_name = "documents/document_type/list.html"
    context_object_name = "document_types"

    def get_queryset(self):

        return DocumentTypeSelector.list(user=self.request.user)


class DocumentTypeCreateView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, CreateView
):

    model = DocumentType
    template_name = "create_page.html"
    fields = ["name", "description"]

    def form_valid(self, form):

        DocumentTypeService.create(
            user=self.request.user,
            validated_data=form.cleaned_data
        )

        return redirect(self.get_success_url())

    def form_invalid(self, form):

        return super().form_invalid(form)

    def get_success_url(self):

        return reverse_lazy("document-type-list-web")

    def build_extra_context(self):

        return ExtraContext(
            app_kind="document type",
            page_title="Create Document Type",
        )


class DocumentTypeDetailView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, DetailView
):

    model = DocumentType
    template_name = "documents/document_type/detail.html"
    context_object_name = "document_type"

    def get_object(self, queryset=None):

        return DocumentTypeSelector.get(
            user=self.request.user, document_type_id=self.kwargs["pk"]
        )


class DocumentTypeUpdateView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, UpdateView
):

    model = DocumentType
    template_name = "edit_page.html"
    fields = ["name", "description"]

    def get_object(self, queryset=None):

        return DocumentTypeSelector.get(
            user=self.request.user, document_type_id=self.kwargs["pk"]
        )

    def form_valid(self, form):

        DocumentTypeService.update(
            user=self.request.user,
            document_type_id=self.kwargs["pk"],
            validated_data=form.cleaned_data
        )

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "document-type-detail-web",
            kwargs={"pk": self.kwargs["pk"]}
        )

    def form_invalid(self, form):

        return super().form_invalid(form)

    def build_extra_context(self):

        return ExtraContext(
            app_kind="document type",
            page_title="Update Document Type",
        )


class DocumentTypeDeleteView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, DeleteView
):

    model = DocumentType
    template_name = "delete_confirm.html"

    def get_object(self, queryset=None):

        return DocumentTypeSelector.get(
            user=self.request.user, document_type_id=self.kwargs["pk"]
        )

    def post(self, request, *args, **kwargs):

        DocumentTypeService.remove(
            user=self.request.user,
            document_type_id=self.kwargs["pk"],
        )

        return redirect(reverse_lazy("document-type-list-web"))

    def build_extra_context(self):

        return ExtraContext(
            app_kind="document type",
            page_title="Delete Document Type",
        )


class DocumentListView(ViewExceptionHandlerMixin, LoginRequiredMixin, ListView):

    model = Document
    template_name = "documents/document/list.html"
    context_object_name = "documents"

    def get_queryset(self):

        return DocumentSelector.list(user=self.request.user)


class DocumentCreateView(
    ViewExceptionHandlerMixin,
    LoginRequiredMixin,
    AppContextMixin,
    DocumentFormMixin,
    CreateView
):

    model = Document
    template_name = "create_page.html"
    fields = ["name", "document_type", "file"]

    def form_valid(self, form):

        DocumentService.create(
            user=self.request.user,
            validated_data=form.cleaned_data
        )

        return redirect(self.get_success_url())

    def form_invalid(self, form):

        return super().form_invalid(form)

    def get_success_url(self):

        return reverse_lazy("document-list-web")

    def build_extra_context(self):

        return ExtraContext(
            app_kind="document",
            page_title="Create Document",
        )


class DocumentDetailView(ViewExceptionHandlerMixin, LoginRequiredMixin, DetailView):

    model = Document
    template_name = "documents/document/detail.html"
    context_object_name = "document"

    def get_object(self, queryset=None):

        return DocumentSelector.get(
            user=self.request.user, document_id=self.kwargs["pk"]
        )


class DocumentUpdateView(
    ViewExceptionHandlerMixin,
    LoginRequiredMixin,
    AppContextMixin,
    DocumentFormMixin,
    UpdateView
):

    model = Document
    template_name = "edit_page.html"
    fields = ["name", "document_type", "file"]

    def get_object(self, queryset=None):

        return DocumentSelector.get(
            user=self.request.user, document_id=self.kwargs["pk"]
        )

    def form_valid(self, form):

        DocumentService.update(
            user=self.request.user,
            document_id=self.kwargs["pk"],
            validated_data=form.cleaned_data
        )

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "document-detail-web",
            kwargs={"pk": self.kwargs["pk"]}
        )

    def form_invalid(self, form):

        return super().form_invalid(form)

    def build_extra_context(self):

        return ExtraContext(
            app_kind="document",
            page_title="Update Document",
        )


class DocumentDeleteView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, DeleteView
):

    model = Document
    template_name = "delete_confirm.html"

    def get_object(self, queryset=None):

        return DocumentSelector.get(
            user=self.request.user, document_id=self.kwargs["pk"]
        )

    def post(self, request, *args, **kwargs):

        DocumentService.remove(
            user=self.request.user,
            document_id=self.kwargs["pk"],
        )

        return redirect(reverse_lazy("document-list-web"))

    def build_extra_context(self):

        return ExtraContext(
            app_kind="document",
            page_title="Delete Document",
        )


class BaseDocumentFileView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, DocumentFileResponseMixin, View
):

    def get_document(self):

        return DocumentSelector.get(
            user=self.request.user, document_id=self.kwargs["pk"]
        )

    def get(self, request, *args, **kwargs):

        return self.get_response()


class DownloadDocumentView(BaseDocumentFileView):

    as_attachment = True


class OpenDocumentView(BaseDocumentFileView):

    as_attachment = False
