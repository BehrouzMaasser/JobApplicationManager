from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

# Models
from apps.documents.models import DocumentType

# Selectors
from apps.documents.selectors.document_type_selector import DocumentTypeSelector

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
