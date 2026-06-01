from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages


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

        return redirect("workspace-list")


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
