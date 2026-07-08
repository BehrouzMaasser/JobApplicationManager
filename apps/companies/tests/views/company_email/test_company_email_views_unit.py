import pytest

from unittest.mock import Mock, patch

from django.http import HttpResponse
from django.test import RequestFactory

from apps.companies.views import (
    CompanyEmailListView,
    CompanyEmailCreateView,
    CompanyEmailDetailView,
    CompanyEmailUpdateView,
    CompanyEmailDeleteView,
)

from apps.companies.services.contexts.company_context import CompanyChildContext

pytestmark = pytest.mark.django_db


class TestCompanyEmailListView:

    # ------------------------
    # Queryset
    # ------------------------

    @patch("apps.companies.views.CompanyEmailSelector.list")
    def test_get_queryset_calls_selector(
        self,
        mock_list,
        user1,
        co_email1_co1_ws1_user1,
    ):
        queryset = Mock()

        mock_list.return_value = queryset

        request = RequestFactory().get(
            "/",
            {
                "company_id": co_email1_co1_ws1_user1.company.pk,
            },
        )
        request.user = user1

        view = CompanyEmailListView()
        view.request = request

        result = view.get_queryset()

        mock_list.assert_called_once()

        kwargs = mock_list.call_args.kwargs

        assert kwargs["user"] == user1
        assert (kwargs["filters"].company_id ==
                str(co_email1_co1_ws1_user1.company.pk))

        assert result is queryset

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
        self,
        user1,
        co1_ws1_user1,
    ):
        request = RequestFactory().get(
            "/",
            {
                "workspace_id": co1_ws1_user1.workspace.workspace_id,
                "company_id": co1_ws1_user1.pk,
            },
        )
        request.user = user1

        view = CompanyEmailListView()
        view.request = request

        context = view.build_app_context()

        assert context.workspace_id == co1_ws1_user1.workspace.workspace_id
        assert context.company_id == co1_ws1_user1.pk


class TestCompanyEmailCreateView:

    # ------------------------
    # Form
    # ------------------------

    @patch("apps.companies.views.redirect")
    @patch("apps.companies.views.CompanyEmailService.create")
    def test_form_valid_calls_service(
        self,
        mock_create,
        mock_redirect,
        user1,
        co1_ws1_user1,
    ):
        response = HttpResponse()
        mock_redirect.return_value = response

        form = Mock()
        form.cleaned_data = {
            "title": "T1",
            "email": "email1@gmail.com",
        }

        request = RequestFactory().post("/")
        request.user = user1

        view = CompanyEmailCreateView()
        view.request = request
        view.kwargs = {
            "workspace_id": co1_ws1_user1.workspace.workspace_id,
            "company_id": co1_ws1_user1.pk,
        }

        result = view.form_valid(form)

        mock_create.assert_called_once()

        kwargs = mock_create.call_args.kwargs

        assert kwargs["user"] == user1
        assert kwargs["validated_data"] == form.cleaned_data

        assert isinstance(kwargs["context"], CompanyChildContext)
        assert kwargs["context"].workspace_id == co1_ws1_user1.workspace.workspace_id
        assert kwargs["context"].company_id == co1_ws1_user1.pk
        assert kwargs["context"].id is None

        mock_redirect.assert_called_once()

        assert result is response

    # ------------------------
    # Success URL
    # ------------------------

    def test_get_success_url(self, co1_ws1_user1):

        view = CompanyEmailCreateView()
        view.kwargs = {
            "company_id": co1_ws1_user1.pk,
        }

        url = view.get_success_url()

        assert str(co1_ws1_user1.pk) in url

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(self, co1_ws1_user1):

        view = CompanyEmailCreateView()
        view.kwargs = {
            "workspace_id": co1_ws1_user1.workspace.workspace_id,
            "company_id": co1_ws1_user1.pk,
        }

        context = view.build_app_context()

        assert context.workspace_id == co1_ws1_user1.workspace.workspace_id
        assert context.company_id == co1_ws1_user1.pk

    # ------------------------
    # Extra Context
    # ------------------------

    def test_build_extra_context(self):

        view = CompanyEmailCreateView()

        context = view.build_extra_context()

        assert context.app_kind == "company email"
        assert context.page_title == "Create Company Email"


class TestCompanyEmailDetailView:

    # ------------------------
    # Object
    # ------------------------

    @patch("apps.companies.views.CompanyEmailSelector.get")
    def test_get_object_calls_selector(
            self,
            mock_get,
            user1,
            co_email1_co1_ws1_user1,
    ):
        mock_get.return_value = co_email1_co1_ws1_user1

        request = RequestFactory().get("/")
        request.user = user1

        view = CompanyEmailDetailView()
        view.request = request
        view.kwargs = {
            "pk": co_email1_co1_ws1_user1.pk,
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            company_email_id=co_email1_co1_ws1_user1.pk,
        )

        assert result is co_email1_co1_ws1_user1

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
            self,
            co_email1_co1_ws1_user1,
    ):
        request = RequestFactory().get("/")

        view = CompanyEmailDetailView()
        view.request = request
        view.object = co_email1_co1_ws1_user1

        context = view.build_app_context()

        assert context.workspace_id == (
            co_email1_co1_ws1_user1.company.workspace.workspace_id
        )

        assert context.company_id == co_email1_co1_ws1_user1.company.pk
        assert context.email_id == co_email1_co1_ws1_user1.pk

        assert context.applications_list_url is None
        assert context.companies_list_url is None
        assert context.positions_list_url is None
        assert context.company_emails_list_url is None
        assert context.company_notes_list_url is None


class TestCompanyEmailUpdateView:

    # ------------------------
    # Object
    # ------------------------

    @patch("apps.companies.views.CompanyEmailSelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        co_email1_co1_ws1_user1,
    ):
        mock_get.return_value = co_email1_co1_ws1_user1

        request = RequestFactory().get("/")
        request.user = user1

        view = CompanyEmailUpdateView()
        view.request = request
        view.kwargs = {
            "pk": co_email1_co1_ws1_user1.pk,
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            company_email_id=co_email1_co1_ws1_user1.pk,
        )

        assert result is co_email1_co1_ws1_user1

    # ------------------------
    # Form
    # ------------------------

    @patch("apps.companies.views.redirect")
    @patch("apps.companies.views.CompanyEmailService.update")
    def test_form_valid_calls_service(
        self,
        mock_update,
        mock_redirect,
        user1,
        co_email1_co1_ws1_user1,
    ):
        response = HttpResponse()
        mock_redirect.return_value = response

        form = Mock()
        form.cleaned_data = {
            "title": "Updated",
            "email": "email1@gmail.com",
        }

        request = RequestFactory().post("/")
        request.user = user1

        view = CompanyEmailUpdateView()
        view.request = request
        view.object = co_email1_co1_ws1_user1
        view.kwargs = {
            "pk": co_email1_co1_ws1_user1.pk,
        }

        result = view.form_valid(form)

        mock_update.assert_called_once()

        kwargs = mock_update.call_args.kwargs

        assert kwargs["user"] == user1
        assert kwargs["validated_data"] == form.cleaned_data

        assert kwargs["context"].workspace_id == (
            co_email1_co1_ws1_user1.company.workspace.workspace_id
        )

        assert kwargs["context"].company_id == co_email1_co1_ws1_user1.company.pk
        assert kwargs["context"].id == co_email1_co1_ws1_user1.pk

        mock_redirect.assert_called_once()

        assert result is response

    # ------------------------
    # Success URL
    # ------------------------

    def test_get_success_url(
        self,
        co_email1_co1_ws1_user1,
    ):
        view = CompanyEmailUpdateView()
        view.object = co_email1_co1_ws1_user1

        view.kwargs = {
            "pk": co_email1_co1_ws1_user1.pk,
        }

        url = view.get_success_url()

        assert str(co_email1_co1_ws1_user1.pk) in url

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
        self,
        co_email1_co1_ws1_user1,
    ):
        view = CompanyEmailUpdateView()
        view.object = co_email1_co1_ws1_user1

        context = view.build_app_context()

        assert context.workspace_id == (
            co_email1_co1_ws1_user1.company.workspace.workspace_id
        )

        assert context.company_id == co_email1_co1_ws1_user1.company.pk
        assert context.email_id == co_email1_co1_ws1_user1.pk

    # ------------------------
    # Extra Context
    # ------------------------

    def test_build_extra_context(self):

        view = CompanyEmailUpdateView()

        context = view.build_extra_context()

        assert context.app_kind == "company email"
        assert context.page_title == "Update Company Email"


class TestCompanyEmailDeleteView:

    # ------------------------
    # Object
    # ------------------------

    @patch("apps.companies.views.CompanyEmailSelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        co_email1_co1_ws1_user1,
    ):
        mock_get.return_value = co_email1_co1_ws1_user1

        request = RequestFactory().get("/")
        request.user = user1

        view = CompanyEmailDeleteView()

        view.request = request
        view.kwargs = {
            "pk": co_email1_co1_ws1_user1.pk,
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            company_email_id=co_email1_co1_ws1_user1.pk,
        )

        assert result is co_email1_co1_ws1_user1

    # ------------------------
    # Delete
    # ------------------------

    @patch("apps.companies.views.redirect")
    @patch("apps.companies.views.CompanyEmailService.remove")
    @patch("apps.companies.views.CompanyEmailSelector.get")
    def test_post_calls_remove_service(
        self,
        mock_get,
        mock_remove,
        mock_redirect,
        user1,
        co_email1_co1_ws1_user1,
    ):
        response = HttpResponse()

        mock_get.return_value = co_email1_co1_ws1_user1
        mock_redirect.return_value = response

        request = RequestFactory().post("/")
        request.user = user1

        view = CompanyEmailDeleteView()

        view.request = request
        view.kwargs = {
            "pk": co_email1_co1_ws1_user1.pk,
        }

        result = view.post(
            request,
            pk=co_email1_co1_ws1_user1.pk,
        )

        mock_remove.assert_called_once()

        kwargs = mock_remove.call_args.kwargs

        assert kwargs["user"] == user1

        assert kwargs["context"].workspace_id == (
            co_email1_co1_ws1_user1.company.workspace.workspace_id
        )

        assert kwargs["context"].company_id == co_email1_co1_ws1_user1.company.pk
        assert kwargs["context"].id == co_email1_co1_ws1_user1.pk

        mock_redirect.assert_called_once()

        assert result is response

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
        self,
        co_email1_co1_ws1_user1,
    ):
        view = CompanyEmailDeleteView()
        view.object = co_email1_co1_ws1_user1

        context = view.build_app_context()

        assert context.workspace_id == (
            co_email1_co1_ws1_user1.company.workspace.workspace_id
        )

        assert context.company_id == co_email1_co1_ws1_user1.company.pk
        assert context.email_id == co_email1_co1_ws1_user1.pk

    # ------------------------
    # Extra Context
    # ------------------------

    def test_build_extra_context(self):

        view = CompanyEmailDeleteView()

        context = view.build_extra_context()

        assert context.app_kind == "company email"
        assert context.page_title == "Delete Company Email"
