from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from apps.applications.api.views import (
    JobApplicationNestedViewSet,
    JobApplicationNoteNestedViewSet
)

from apps.companies.api.views import (
    NestedCompanyViewSet,
    NestedCompanyNoteViewSet,
    NestedCompanyEmailViewSet,
    NestedJobPositionViewSet
)

from .routers import urlpatterns as router_urls


# App Urls Flat Access:
urlpatterns = [
    path("", include(router_urls)),
]


# Authentication:
urlpatterns += [
    path("auth/", TokenObtainPairView.as_view()),
    path("auth/refresh/", TokenRefreshView.as_view()),
]

# Nested Company URL Path Config
company_list = NestedCompanyViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

company_detail = NestedCompanyViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns += [
    path(
        "workspaces/<uuid:workspace_id>/companies/",
        company_list,
        name="companies-list",
    ),
    path(
        "workspaces/<uuid:workspace_id>/companies/<int:id>/",
        company_detail,
        name="companies-detail",
    ),
]

# Nested Company Note URL Path Config
company_note_list = NestedCompanyNoteViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

company_note_detail = NestedCompanyNoteViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns += [
    path(
        "workspaces/<uuid:workspace_id>/companies/<int:company_id>/company-notes/",
        company_note_list,
        name="company-notes-list",
    ),
    path(
        "workspaces/<uuid:workspace_id>/companies/<int:company_id>/company-notes/<int:id>/",
        company_note_detail,
        name="company-notes-detail",
    ),
]

# Nested Company Email URL Path Config
company_email_list = NestedCompanyEmailViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

company_email_detail = NestedCompanyEmailViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns += [
    path(
        "workspaces/<uuid:workspace_id>/companies/<int:company_id>/company-emails/",
        company_email_list,
        name="company-emails-list",
    ),
    path(
        "workspaces/<uuid:workspace_id>/companies/<int:company_id>/company-emails/<int:id>/",
        company_email_detail,
        name="company-emails-detail",
    ),
]


# Nested Job Position URL Path Config
job_position_list = NestedJobPositionViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

job_position_detail = NestedJobPositionViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns += [
    path(
        "workspaces/<uuid:workspace_id>/companies/<int:company_id>/job-positions/",
        job_position_list,
        name="job-positions-list",
    ),
    path(
        "workspaces/<uuid:workspace_id>/companies/<int:company_id>/job-positions/<int:id>/",
        job_position_detail,
        name="job-positions-detail",
    ),
]


# Nested Job Application URL Path Config
job_application_list = JobApplicationNestedViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

job_application_detail = JobApplicationNestedViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns += [
    path(
        "workspaces/<uuid:workspace_id>/companies/<int:company_id>/job-positions/<int:job_position_id>/job-applications/",
        job_application_list,
        name="job-application-list",
    ),
    path(
        "workspaces/<uuid:workspace_id>/companies/<int:company_id>/job-positions/<int:job_position_id>/job-applications/<int:id>/",
        job_application_detail,
        name="job-application-detail",
    ),
]

# Nested Job Application Note URL Path Config
job_application_note_list = JobApplicationNoteNestedViewSet.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

job_application_note_detail = JobApplicationNoteNestedViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns += [
    path(
        "workspaces/<uuid:workspace_id>/companies/<int:company_id>/job-positions/<int:job_position_id>/job-applications/<int:job_application_id>/job-application-notes/",
        job_application_note_list,
        name="job-application-notes-list",
    ),
    path(
        "workspaces/<uuid:workspace_id>/companies/<int:company_id>/job-positions/<int:job_position_id>/job-applications/<int:job_application_id>/job-application-notes/<int:id>/",
        job_application_note_detail,
        name="job-application-notes-detail",
    ),
]
