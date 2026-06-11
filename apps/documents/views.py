from mimetypes import guess_type

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from apps.core.contexts.extra_context import ExtraContext
from apps.core.mixins.app_context_mixin import AppContextMixin
from apps.core.mixins.documents_form_mixin import DocumentFormMixin
# Models
from apps.documents.models import DocumentType, Document
from apps.documents.selectors.document_selector import DocumentSelector

# Selectors
from apps.documents.selectors.document_type_selector import DocumentTypeSelector
from apps.documents.services.document_service import DocumentService

# Services
from apps.documents.services.document_type_service import DocumentTypeService


class DocumentTypeListView(LoginRequiredMixin, ListView):

    model = DocumentType
    template_name = "documents/document_type/list.html"
    context_object_name = "document_types"

    def get_queryset(self):

        return DocumentTypeSelector.list(user=self.request.user)


class DocumentTypeCreateView(LoginRequiredMixin, AppContextMixin, CreateView):

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


class DocumentTypeDetailView(LoginRequiredMixin, DetailView):

    model = DocumentType
    template_name = "documents/document_type/detail.html"
    context_object_name = "document_type"

    def get_queryset(self):

        return DocumentTypeSelector.list(user=self.request.user)


class DocumentTypeUpdateView(LoginRequiredMixin, AppContextMixin, UpdateView):

    model = DocumentType
    template_name = "edit_page.html"
    fields = ["name", "description"]

    def get_queryset(self):

        return DocumentTypeSelector.list(user=self.request.user)

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


class DocumentTypeDeleteView(LoginRequiredMixin, AppContextMixin, DeleteView):

    model = DocumentType
    template_name = "delete_confirm.html"

    def get_queryset(self):

        return DocumentTypeSelector.list(user=self.request.user)

    def post(self, request, *args, **kwargs):

        DocumentTypeService.remove(
            user=self.request.user,
            document_type_id=self.kwargs["pk"],
        )

        return redirect("document-type-list-web")

    def build_extra_context(self):

        return ExtraContext(
            app_kind="document type",
            page_title="Delete Document Type",
        )


class DocumentListView(LoginRequiredMixin, ListView):

    model = Document
    template_name = "documents/document/list.html"
    context_object_name = "documents"

    def get_queryset(self):

        return DocumentSelector.list(user=self.request.user)


class DocumentCreateView(
    LoginRequiredMixin, AppContextMixin, DocumentFormMixin, CreateView
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


class DocumentDetailView(LoginRequiredMixin, DetailView):

    model = Document
    template_name = "documents/document/detail.html"
    context_object_name = "document"

    def get_queryset(self):

        return DocumentSelector.list(user=self.request.user)


class DocumentUpdateView(
    LoginRequiredMixin, AppContextMixin, DocumentFormMixin, UpdateView
):

    model = Document
    template_name = "edit_page.html"
    fields = ["name", "document_type", "file"]

    def get_queryset(self):

        return DocumentSelector.list(user=self.request.user)

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


class DocumentDeleteView(LoginRequiredMixin, AppContextMixin, DeleteView):

    model = Document
    template_name = "delete_confirm.html"

    def get_queryset(self):

        return DocumentSelector.list(user=self.request.user)

    def post(self, request, *args, **kwargs):

        DocumentService.remove(
            user=self.request.user,
            document_id=self.kwargs["pk"],
        )

        return redirect("document-list-web")

    def build_extra_context(self):

        return ExtraContext(
            app_kind="document",
            page_title="Delete Document",
        )


class BaseDocumentFileView(LoginRequiredMixin, View):

    as_attachment = False

    def get(self, request, *args, **kwargs):

        document = get_object_or_404(
            Document, owner=request.user, pk=self.kwargs["pk"]
        )

        content_type, _ = guess_type(document.file.name)

        return FileResponse(
            document.file.open("rb"),
            as_attachment=self.as_attachment,
            filename=slugify(document.name),
            content_type=content_type,
        )


class DownloadDocumentView(BaseDocumentFileView):

    as_attachment = True


class OpenDocumentView(BaseDocumentFileView):

    as_attachment = False
