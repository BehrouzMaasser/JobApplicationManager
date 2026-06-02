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
from .services.company_service import CompanyService
from .services.contexts.company_context import CompanyContext


class CompanyListView(LoginRequiredMixin, ListView):

    model = Company
    template_name = "companies/company/list.html"
    context_object_name = "companies"

    def get_queryset(self):

        return Company.objects.filter(
            workspace__owner=self.request.user,
            workspace__workspace_id=self.kwargs["workspace_id"]
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["workspace_id"] = self.kwargs["workspace_id"]

        return context


class CompanyCreateView(LoginRequiredMixin, CreateView):

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
            kwargs={"workspace_id": self.kwargs["workspace_id"]}
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["workspace_id"] = self.kwargs["workspace_id"]

        return context


class CompanyDetailView(LoginRequiredMixin, DetailView):

    model = Company
    template_name = "companies/company/detail.html"
    context_object_name = "company"

    def get_queryset(self):

        return Company.objects.filter(workspace__owner=self.request.user)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["workspace_id"] = self.get_object().workspace.workspace_id

        return context


class CompanyUpdateView(LoginRequiredMixin, UpdateView):

    model = Company
    template_name = "companies/company/edit.html"
    fields = ["name", "website"]

    def get_queryset(self):

        return Company.objects.filter(workspace__owner=self.request.user)

    def form_valid(self, form):

        company = self.get_object()

        CompanyService.update(
            user=self.request.user,
            context=CompanyContext(
                workspace_id=company.workspace.workspace_id,
                id=company.id,
            ),
            validated_data=form.cleaned_data
        )

        return redirect(self.get_success_url())

    def get_success_url(self):

        return reverse(
            "company-detail-web",
            kwargs={"pk": self.object.pk}
        )

    def form_invalid(self, form):

        return super().form_invalid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["workspace_id"] = self.get_object().workspace.workspace_id

        return context


class CompanyDeleteView(LoginRequiredMixin, DeleteView):

    model = Company
    template_name = "companies/company/delete.html"

    def get_queryset(self):

        return Company.objects.filter(workspace__owner=self.request.user)

    def post(self, request, *args, **kwargs):

        company = self.get_object()

        CompanyService.remove(
            user=self.request.user,
            context=CompanyContext(
                workspace_id=company.workspace.workspace_id,
                id=company.id,
            )
        )

        return redirect(
            "company-list-web",
            workspace_id=company.workspace.workspace_id
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["workspace_id"] = self.get_object().workspace.workspace_id

        return context
