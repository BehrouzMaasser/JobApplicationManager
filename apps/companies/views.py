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

# Models
from .models import Company, CompanyEmail

# Selectors
from .selectors.company_email_selector import CompanyEmailSelector
from .selectors.company_selector import CompanySelector

# Services
from .services.company_email_service import CompanyEmailService
from .services.company_service import CompanyService
from .services.contexts.company_context import CompanyContext, CompanyChildContext

# View Contexts and Mixins
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


class CompanyEmailListView(LoginRequiredMixin, AppContextMixin, ListView):

    model = CompanyEmail
    template_name = "companies/email/list.html"
    context_object_name = "emails"

    def get_queryset(self):

        return CompanyEmailSelector.list(
            user=self.request.user,
            filters=CompanyEmailSelector.QueryFilter(
                workspace_id=self.kwargs["workspace_id"],
                company_id=self.kwargs["company_id"]
            )
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
        )


class CompanyEmailCreateView(LoginRequiredMixin, AppContextMixin, CreateView):

    model = CompanyEmail
    template_name = "companies/email/create.html"
    fields = ["title", "email"]

    def form_valid(self, form):

        CompanyEmailService.create(
            user=self.request.user,
            context=CompanyChildContext(
                workspace_id=self.kwargs["workspace_id"],
                company_id=self.kwargs["company_id"],
                id=None
            ),
            validated_data=form.cleaned_data
        )

        return redirect(self.get_success_url())

    def form_invalid(self, form):

        return super().form_invalid(form)

    def get_success_url(self):

        return reverse_lazy(
            "company-detail-web",
            kwargs={
                "workspace_id": self.kwargs["workspace_id"],
                "pk": self.kwargs["company_id"]
            }
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
        )


class CompanyEmailDetailView(LoginRequiredMixin, AppContextMixin, DetailView):

    model = CompanyEmail
    template_name = "companies/email/detail.html"
    context_object_name = "email"

    @property
    def email(self):

        return self.get_object()

    def get_queryset(self):

        return CompanyEmailSelector.list(
            user=self.request.user,
            filters=CompanyEmailSelector.QueryFilter(
                workspace_id=self.kwargs["workspace_id"],
                company_id=self.kwargs["company_id"]
            )
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            email_id=self.kwargs["pk"],
        )


class CompanyEmailUpdateView(LoginRequiredMixin, AppContextMixin, UpdateView):

    model = CompanyEmail
    template_name = "companies/email/edit.html"
    fields = ["title", "email"]

    @property
    def email(self):

        return self.get_object()

    def get_queryset(self):

        return CompanyEmailSelector.list(
            user=self.request.user,
            filters=CompanyEmailSelector.QueryFilter(
                workspace_id=self.kwargs["workspace_id"],
                company_id=self.kwargs["company_id"]
            )
        )

    def form_valid(self, form):

        CompanyEmailService.update(
            user=self.request.user,
            context=CompanyChildContext(
                workspace_id=self.email.company.workspace.workspace_id,
                company_id=self.email.company.pk,
                id=self.email.pk,
            ),
            validated_data=form.cleaned_data
        )

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "company-detail-web",
            kwargs={
                "pk": self.kwargs["company_id"],
                "workspace_id": self.kwargs["workspace_id"],
            }
        )

    def form_invalid(self, form):

        return super().form_invalid(form)

    def build_app_context(self):

        return AppContext(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            email_id=self.kwargs["pk"],
        )


class CompanyEmailDeleteView(LoginRequiredMixin, AppContextMixin, DeleteView):

    model = CompanyEmail
    template_name = "companies/email/delete.html"

    @property
    def email(self):

        return self.get_object()

    def get_queryset(self):

        return CompanyEmailSelector.list(
            user=self.request.user,
            filters=CompanyEmailSelector.QueryFilter(
                workspace_id=self.kwargs["workspace_id"],
                company_id=self.kwargs["company_id"]
            )
        )

    def post(self, request, *args, **kwargs):

        CompanyEmailService.remove(
            user=self.request.user,
            context=CompanyChildContext(
                workspace_id=self.email.company.workspace.workspace_id,
                company_id=self.email.company.pk,
                id=self.email.pk,
            )
        )

        return redirect(
            "company-detail-web",
            workspace_id=self.kwargs["workspace_id"],
            pk=self.kwargs["company_id"],
        )

    def build_app_context(self):

        return AppContext(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            email_id=self.kwargs["pk"],
        )
