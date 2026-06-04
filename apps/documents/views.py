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


class DocumentTypeCreateView(LoginRequiredMixin, CreateView):

    model = DocumentType
    template_name = "documents/document_type/create.html"
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


class DocumentTypeDetailView(LoginRequiredMixin, DetailView):

    model = DocumentType
    template_name = "documents/document_type/detail.html"
    context_object_name = "document_type"

    def get_queryset(self):

        return DocumentTypeSelector.list(user=self.request.user)


class DocumentTypeUpdateView(LoginRequiredMixin, UpdateView):

    model = DocumentType
    template_name = "documents/document_type/edit.html"
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


class DocumentTypeDeleteView(LoginRequiredMixin, DeleteView):

    model = DocumentType
    template_name = "documents/document_type/delete.html"

    def get_queryset(self):

        return DocumentTypeSelector.list(user=self.request.user)

    def post(self, request, *args, **kwargs):

        DocumentTypeService.remove(
            user=self.request.user,
            document_type_id=self.kwargs["pk"],
        )

        return redirect("document-type-list-web")


class DocumentListView(LoginRequiredMixin, ListView):

    model = Document
    template_name = "documents/document/list.html"
    context_object_name = "documents"

    def get_queryset(self):

        return DocumentSelector.list(user=self.request.user)


class DocumentCreateView(LoginRequiredMixin, CreateView):

    model = Document
    template_name = "documents/document/create.html"
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


class DocumentDetailView(LoginRequiredMixin, DetailView):

    model = Document
    template_name = "documents/document/detail.html"
    context_object_name = "document"

    def get_queryset(self):

        return DocumentSelector.list(user=self.request.user)


class DocumentUpdateView(LoginRequiredMixin, UpdateView):

    model = Document
    template_name = "documents/document_type/edit.html"
    fields = ["name", "description"]

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


class DocumentDeleteView(LoginRequiredMixin, DeleteView):

    model = Document
    template_name = "documents/document/delete.html"

    def get_queryset(self):

        return DocumentSelector.list(user=self.request.user)

    def post(self, request, *args, **kwargs):

        DocumentService.remove(
            user=self.request.user,
            document_id=self.kwargs["pk"],
        )

        return redirect("document-list-web")


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
