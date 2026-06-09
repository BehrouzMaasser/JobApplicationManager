from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from django.urls import reverse_lazy, reverse

# Models
from .models import Workspace

# Selectors
from .selectors.workspace_selector import WorkspaceSelector

# Services
from .services.workspace_service import WorkspaceService
from ..companies.views import company_list_url
from ..core.contexts.app_context import AppContext
from ..core.mixins.app_context_mixin import AppContextMixin


class WorkspaceListView(LoginRequiredMixin, ListView):

    model = Workspace
    template_name = "workspaces/list.html"
    context_object_name = "workspaces"

    def get_queryset(self):

        return WorkspaceSelector.list(user=self.request.user)


class WorkspaceCreateView(LoginRequiredMixin, CreateView):

    model = Workspace
    template_name = "workspaces/create.html"
    fields = ["name"]
    success_url = reverse_lazy("workspace-list-web")

    def form_valid(self, form):

        WorkspaceService.create(
            user=self.request.user,
            validated_data=form.cleaned_data
        )

        return redirect(self.success_url)

    def form_invalid(self, form):

        return super().form_invalid(form)


class WorkspaceDetailView(LoginRequiredMixin, AppContextMixin, DetailView):

    model = Workspace
    template_name = "workspaces/detail.html"
    context_object_name = "workspace"

    def get_object(self, queryset=None):

        return get_object_or_404(
            Workspace,
            owner=self.request.user,
            workspace_id=self.kwargs["workspace_id"]
        )

    def build_app_context(self):

        return AppContext(
            companies_list_url=company_list_url(
                workspace_id=self.kwargs["workspace_id"]
            )
        )


class WorkspaceUpdateView(LoginRequiredMixin, UpdateView):

    model = Workspace
    template_name = "workspaces/edit.html"
    fields = ["name"]

    def get_object(self, queryset=None):

        return get_object_or_404(
            Workspace,
            owner=self.request.user,
            workspace_id=self.kwargs["workspace_id"]
        )

    def form_valid(self, form):

        WorkspaceService.update(
            user=self.request.user,
            workspace_id=self.kwargs["workspace_id"],
            validated_data=form.cleaned_data
        )

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "workspace-detail-web",
            kwargs={"workspace_id": self.kwargs["workspace_id"]}
        )

    def form_invalid(self, form):

        return super().form_invalid(form)


class WorkspaceDeleteView(LoginRequiredMixin, DeleteView):

    model = Workspace
    template_name = "workspaces/delete.html"
    success_url = reverse_lazy("workspace-list-web")

    def get_object(self, queryset=None):

        return get_object_or_404(
            Workspace,
            owner=self.request.user,
            workspace_id=self.kwargs["workspace_id"]
        )

    def post(self, request, *args, **kwargs):

        WorkspaceService.remove(
            user=self.request.user,
            workspace_id=self.kwargs["workspace_id"]
        )

        return redirect(self.success_url)
