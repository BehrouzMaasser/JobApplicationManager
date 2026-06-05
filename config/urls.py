"""
URL configuration for JobAppTracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("accounts/", include("apps.accounts.urls")),
    path("documents/", include("apps.documents.urls")),
    path("workspaces/", include("apps.workspaces.urls")),
    path("workspaces/<uuid:workspace_id>/companies/", include("apps.companies.urls")),
    path("applications/", include("apps.applications.urls")),
    path("workspaces/<uuid:workspace_id>/companies/<int:company_id>/job_positions/<int:job_position_id>/applications/", include("apps.applications.context_urls")),
    path('admin/', admin.site.urls),
    path("api/v1/", include("config.api.v1.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
