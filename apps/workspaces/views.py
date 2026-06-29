# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin
from ..core.mixins.app_context_mixin import AppContextMixin

# Django
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse

# Generic Views
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

# Models
from .models import Workspace

# Selectors
from .selectors.workspace_selector import WorkspaceSelector

# Services
from .services.workspace_service import WorkspaceService

# Contexts
from ..core.contexts.app_context import AppContext
from ..core.contexts.extra_context import ExtraContext

# View Helpers
from ..companies.views import company_list_url
from ..core.mixins.view_exception_handler import ViewExceptionHandlerMixin


class WorkspaceListView(ViewExceptionHandlerMixin, LoginRequiredMixin, ListView):

    model = Workspace
    template_name = "workspaces/list.html"
    context_object_name = "workspaces"

    def get_queryset(self):

        return WorkspaceSelector.list(user=self.request.user)


class WorkspaceCreateView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, CreateView
):

    model = Workspace
    template_name = "create_page.html"
    fields = ["name"]
    success_url = reverse_lazy("workspace-list-web")

    def form_valid(self, form):

        WorkspaceService.create(
            user=self.request.user,
            validated_data=form.cleaned_data
        )

        return redirect(self.success_url)

    def build_extra_context(self):

        return ExtraContext(
            app_kind="workspace",
            page_title="Create Workspace",
        )


class WorkspaceDetailView(
    ViewExceptionHandlerMixin, LoginRequiredMixin, AppContextMixin, DetailView
):

    model = Workspace
    template_name = "workspaces/detail.html"
    context_object_name = "workspace"

    def get_object(self, queryset=None):

        return WorkspaceSelector.get(
            user=self.request.user,
            workspace_id=self.kwargs["workspace_id"]
        )

    def build_app_context(self):

        return AppContext(
            companies_list_url=company_list_url(
                workspace_id=self.kwargs["workspace_id"]
            )
        )


class WorkspaceUpdateView(ViewExceptionHandlerMixin, LoginRequiredMixin, UpdateView):

    model = Workspace
    template_name = "edit_page.html"
    fields = ["name"]

    def get_object(self, queryset=None):

        return WorkspaceSelector.get(
            user=self.request.user,
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

    def build_extra_context(self):

        return ExtraContext(
            app_kind="workspace",
            page_title="Update Workspace",
        )


class WorkspaceDeleteView(ViewExceptionHandlerMixin, LoginRequiredMixin, DeleteView):

    model = Workspace
    template_name = "delete_confirm.html"
    success_url = reverse_lazy("workspace-list-web")

    def get_object(self, queryset=None):

        return WorkspaceSelector.get(
            user=self.request.user,
            workspace_id=self.kwargs["workspace_id"]
        )

    def post(self, request, *args, **kwargs):

        WorkspaceService.remove(
            user=self.request.user,
            workspace_id=self.kwargs["workspace_id"]
        )

        return redirect(self.success_url)

    def build_extra_context(self):

        return ExtraContext(
            app_kind="workspace",
            page_title="Delete Workspace",
        )
