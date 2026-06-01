from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from django.urls import reverse_lazy, reverse

from .models import Workspace
from .services.workspace_service import WorkspaceService


class WorkspaceListView(LoginRequiredMixin, ListView):

    model = Workspace
    template_name = "workspaces/list.html"
    context_object_name = "workspaces"

    def get_queryset(self):

        return Workspace.objects.filter(owner=self.request.user)


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


class WorkspaceDetailView(LoginRequiredMixin, DetailView):

    model = Workspace
    template_name = "workspaces/detail.html"
    context_object_name = "workspace"

    def get_queryset(self):

        return Workspace.objects.filter(owner=self.request.user)


class WorkspaceUpdateView(LoginRequiredMixin, UpdateView):

    model = Workspace
    template_name = "workspaces/edit.html"
    fields = ["name"]

    def get_queryset(self):

        return Workspace.objects.filter(owner=self.request.user)

    def form_valid(self, form):

        WorkspaceService.update(
            user=self.request.user,
            workspace_id=self.get_object().workspace_id,
            validated_data=form.cleaned_data
        )

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "workspace-detail-web",
            kwargs={"pk": self.object.pk}
        )

    def form_invalid(self, form):

        return super().form_invalid(form)


class WorkspaceDeleteView(LoginRequiredMixin, DeleteView):

    model = Workspace
    template_name = "workspaces/delete.html"
    success_url = reverse_lazy("workspace-list-web")

    def get_queryset(self):

        return Workspace.objects.filter(owner=self.request.user)

    def post(self, request, *args, **kwargs):

        WorkspaceService.remove(
            user=self.request.user,
            workspace_id=self.get_object().workspace_id
        )

        return redirect(self.success_url)
