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

from .models import Company
from .selectors.company_selector import CompanySelector
from .services.company_service import CompanyService
from .services.contexts.company_context import CompanyContext
from ..core.contexts.app_context import AppContext
from ..core.mixins.app_context_mixin import AppContextMixin


class CompanyListView(LoginRequiredMixin, AppContextMixin, ListView):

    model = Company
    template_name = "companies/company/list.html"
    context_object_name = "companies"

    def get_queryset(self):

        return CompanySelector.list(
            user=self.request.user,
            filters=CompanySelector.QueryFilter(
                workspace_id=self.kwargs["workspace_id"]
            )
        )


class CompanyCreateView(LoginRequiredMixin, AppContextMixin, CreateView):

    model = Company
    template_name = "companies/company/create.html"
    fields = ["name", "website"]

    def form_valid(self, form):

        CompanyService.create(
            user=self.request.user,
            context=CompanyContext(
                workspace_id=self.kwargs["workspace_id"],
                id=None
            ),
            validated_data=form.cleaned_data
        )

        return redirect(self.get_success_url())

    def form_invalid(self, form):

        return super().form_invalid(form)

    def get_success_url(self):

        return reverse_lazy(
            "company-list-web",
            kwargs={
                "workspace_id": self.kwargs["workspace_id"]
            }
        )


class CompanyDetailView(LoginRequiredMixin, AppContextMixin, DetailView):

    model = Company
    template_name = "companies/company/detail.html"
    context_object_name = "company"

    @property
    def company(self):

        return self.get_object()

    def get_queryset(self):

        return CompanySelector.list(
            user=self.request.user,
            filters=CompanySelector.QueryFilter(
                workspace_id=self.kwargs["workspace_id"]
            )
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.company.workspace.workspace_id,
            company_id=self.company.pk,
        )


class CompanyUpdateView(LoginRequiredMixin, AppContextMixin, UpdateView):

    model = Company
    template_name = "companies/company/edit.html"
    fields = ["name", "website"]

    @property
    def company(self):

        return self.get_object()

    def get_queryset(self):

        return CompanySelector.list(
            user=self.request.user,
            filters=CompanySelector.QueryFilter(
                workspace_id=self.kwargs["workspace_id"]
            )
        )

    def form_valid(self, form):

        CompanyService.update(
            user=self.request.user,
            context=CompanyContext(
                workspace_id=self.company.workspace.workspace_id,
                id=self.company.pk,
            ),
            validated_data=form.cleaned_data
        )

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "company-detail-web",
            kwargs={
                "pk": self.company.pk,
                "workspace_id": self.company.workspace.workspace_id,
            }
        )

    def form_invalid(self, form):

        return super().form_invalid(form)

    def build_app_context(self):

        return AppContext(
            workspace_id=self.company.workspace.workspace_id,
            company_id=self.company.pk,
        )


class CompanyDeleteView(LoginRequiredMixin, AppContextMixin, DeleteView):

    model = Company
    template_name = "companies/company/delete.html"

    @property
    def company(self):

        return self.get_object()

    def get_queryset(self):

        return CompanySelector.list(
            user=self.request.user,
            filters=CompanySelector.QueryFilter(
                workspace_id=self.kwargs["workspace_id"]
            )
        )

    def post(self, request, *args, **kwargs):

        CompanyService.remove(
            user=self.request.user,
            context=CompanyContext(
                workspace_id=self.company.workspace.workspace_id,
                id=self.company.pk,
            )
        )

        return redirect(
            "company-list-web",
            workspace_id=self.kwargs["workspace_id"]
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.company.workspace.workspace_id,
            company_id=self.company.pk,
        )
