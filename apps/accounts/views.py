from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic import ListView, CreateView, DetailView, UpdateView, \
    DeleteView

from apps.companies.models import JobBenefit
from apps.companies.selectors.job_benefit_selector import JobBenefitSelector
from apps.companies.services.job_benefit_service import JobBenefitService
from apps.core.mixins.app_context_mixin import AppContextMixin

User = get_user_model()


class SignupView(View):

    template_name = "accounts/signup.html"

    def get(self, request):

        if request.user.is_authenticated:

            return redirect("dashboard")

        return render(request, self.template_name)

    def post(self, request):

        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")

            return render(request, self.template_name)

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")

            return render(request, self.template_name)

        user = User.objects.create_user(
            email=email,
            password=password
        )

        login(request, user)

        return redirect("workspace-list-web")


class LoginView(View):

    template_name = "accounts/login.html"

    def get(self, request):

        if request.user.is_authenticated:

            return redirect("workspace-list-web")

        return render(request, self.template_name)

    def post(self, request):

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            email=email,
            password=password
        )

        if user:
            login(request, user)

            return redirect("workspace-list-web")

        messages.error(request, "Invalid credentials.")

        return render(request, self.template_name)


class LogoutView(View):

    def post(self, request):

        logout(request)

        return redirect("login")


@login_required
def dashboard_view(request):

    return render(request, "accounts/dashboard.html")


class JobBenefitListView(LoginRequiredMixin, ListView):

    model = JobBenefit
    template_name = "accounts/job_benefit/list.html"
    context_object_name = "job_benefits"

    def get_queryset(self):

        return JobBenefitSelector.list(user=self.request.user)


class JobBenefitCreateView(LoginRequiredMixin, CreateView):

    model = JobBenefit
    template_name = "accounts/job_benefit/create.html"
    fields = ["name", "description"]
    success_url = reverse_lazy("job-benefit-list-web")

    def form_valid(self, form):
        JobBenefitService.create(
            user=self.request.user,
            validated_data=form.cleaned_data
        )

        return redirect(self.success_url)

    def form_invalid(self, form):

        return super().form_invalid(form)


class JobBenefitDetailView(LoginRequiredMixin,  DetailView):

    model = JobBenefit
    template_name = "accounts/job_benefit/detail.html"
    context_object_name = "job_benefit"

    def get_queryset(self):

        return JobBenefitSelector.list(user=self.request.user)


class JobBenefitUpdateView(LoginRequiredMixin, UpdateView):

    model = JobBenefit
    template_name = "accounts/job_benefit/edit.html"
    fields = ["name", "description"]
    context_object_name = "job_benefit"

    def get_queryset(self):

        return JobBenefitSelector.list(user=self.request.user)

    def form_valid(self, form):

        JobBenefitService.update(
            user=self.request.user,
            job_benefit_id=self.kwargs["pk"],
            validated_data=form.cleaned_data
        )

        return redirect("job-benefit-detail-web", pk=self.kwargs["pk"])

    def form_invalid(self, form):

        return super().form_invalid(form)


class JobBenefitDeleteView(LoginRequiredMixin, DeleteView):

    model = JobBenefit
    template_name = "accounts/job_benefit/delete.html"

    def get_queryset(self):

        return JobBenefitSelector.list(user=self.request.user)

    def post(self, request, *args, **kwargs):

        JobBenefitService.remove(
            user=self.request.user,
            job_benefit_id=self.kwargs["pk"],
        )

        return redirect("job-benefit-list-web")
