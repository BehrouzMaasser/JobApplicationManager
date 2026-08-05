import pytest

from unittest.mock import ANY, Mock, patch

from django.http import HttpResponse
from django.test import RequestFactory

from apps.companies.views import (
    CompanyEmailListView,
    CompanyEmailCreateView,
    CompanyEmailDetailView,
    CompanyEmailUpdateView,
    CompanyEmailDeleteView,
)

from apps.core.common.contexts.contexts import CompanyChildContext

pytestmark = pytest.mark.django_db


class TestCompanyEmailListView:

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

        assert (
            kwargs["filters"].company_id
            == str(co_email1_co1_ws1_user1.company.pk)
        )

        assert result is queryset

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

        assert (
            context.workspace_id
            == co1_ws1_user1.workspace.workspace_id
        )

        assert context.company_id == co1_ws1_user1.pk


class TestCompanyEmailCreateView:

    @patch.object(
        CompanyEmailCreateView,
        "execute_service",
    )
    def test_form_valid_executes_service_and_redirects_on_success(
        self,
        mock_execute_service,
        user1,
        co1_ws1_user1,
    ):
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
            "workspace_id": (
                co1_ws1_user1.workspace.workspace_id
            ),
            "company_id": co1_ws1_user1.pk,
        }

        mock_execute_service.return_value = None

        with patch.object(
            view,
            "get_success_url",
            return_value="/success/",
        ):

            response = view.form_valid(form)

        mock_execute_service.assert_called_once_with(
            form=form,
            operation=ANY,
        )

        operation = (
            mock_execute_service
            .call_args
            .kwargs["operation"]
        )

        with patch(
            "apps.companies.views.CompanyEmailService.create"
        ) as mock_create:

            operation()

            mock_create.assert_called_once_with(
                user=user1,
                context=CompanyChildContext(
                    workspace_id=(
                        co1_ws1_user1.workspace.workspace_id
                    ),
                    company_id=co1_ws1_user1.pk,
                ),
                validated_data=form.cleaned_data,
            )

        assert response.status_code == 302

    def test_get_success_url(
        self,
        co1_ws1_user1,
    ):
        view = CompanyEmailCreateView()

        view.kwargs = {
            "company_id": co1_ws1_user1.pk,
        }

        url = view.get_success_url()

        assert str(co1_ws1_user1.pk) in url

    def test_build_app_context(
        self,
        co1_ws1_user1,
    ):
        view = CompanyEmailCreateView()

        view.kwargs = {
            "workspace_id": (
                co1_ws1_user1.workspace.workspace_id
            ),
            "company_id": co1_ws1_user1.pk,
        }

        context = view.build_app_context()

        assert (
            context.workspace_id
            == co1_ws1_user1.workspace.workspace_id
        )

        assert context.company_id == co1_ws1_user1.pk

    def test_build_extra_context(self):

        view = CompanyEmailCreateView()

        context = view.build_extra_context()

        assert context.app_kind == "company email"
        assert context.page_title == "Create Company Email"


class TestCompanyEmailDetailView:

    @patch(
        "apps.companies.views.CompanyEmailSelector.get"
    )
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        co_email1_co1_ws1_user1,
    ):
        mock_get.return_value = (
            co_email1_co1_ws1_user1
        )

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
            obj_id=(
                co_email1_co1_ws1_user1.pk
            ),
        )

        assert result is co_email1_co1_ws1_user1

    def test_build_app_context(
        self,
        co_email1_co1_ws1_user1,
    ):
        request = RequestFactory().get("/")

        view = CompanyEmailDetailView()
        view.request = request
        view.object = co_email1_co1_ws1_user1

        context = view.build_app_context()

        assert (
            context.workspace_id
            == (
                co_email1_co1_ws1_user1
                .company
                .workspace
                .workspace_id
            )
        )

        assert (
            context.company_id
            == co_email1_co1_ws1_user1.company.pk
        )

        assert (
            context.email_id
            == co_email1_co1_ws1_user1.pk
        )

        assert context.applications_list_url is None
        assert context.companies_list_url is None
        assert context.positions_list_url is None
        assert context.company_emails_list_url is None
        assert context.company_notes_list_url is None


class TestCompanyEmailUpdateView:

    @patch(
        "apps.companies.views.CompanyEmailSelector.get"
    )
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        co_email1_co1_ws1_user1,
    ):
        mock_get.return_value = (
            co_email1_co1_ws1_user1
        )

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
            obj_id=(
                co_email1_co1_ws1_user1.pk
            ),
        )

        assert result is co_email1_co1_ws1_user1

    @patch.object(
        CompanyEmailUpdateView,
        "execute_service",
    )
    def test_form_valid_executes_service_and_redirects_on_success(
        self,
        mock_execute_service,
        user1,
        co_email1_co1_ws1_user1,
    ):
        form = Mock()

        form.cleaned_data = {
            "title": "Updated",
            "email": "updated@gmail.com",
        }

        request = RequestFactory().post("/")
        request.user = user1

        view = CompanyEmailUpdateView()
        view.request = request
        view.object = co_email1_co1_ws1_user1
        view.kwargs = {
            "pk": co_email1_co1_ws1_user1.pk,
        }

        mock_execute_service.return_value = None

        with patch.object(
            view,
            "get_success_url",
            return_value="/success/",
        ):

            response = view.form_valid(form)

        mock_execute_service.assert_called_once_with(
            form=form,
            operation=ANY,
        )

        operation = (
            mock_execute_service
            .call_args
            .kwargs["operation"]
        )

        with patch(
            "apps.companies.views.CompanyEmailService.update"
        ) as mock_update:

            operation()

            mock_update.assert_called_once_with(
                user=user1,
                context=CompanyChildContext(
                    workspace_id=(
                        co_email1_co1_ws1_user1
                        .company
                        .workspace
                        .workspace_id
                    ),
                    company_id=(
                        co_email1_co1_ws1_user1
                        .company
                        .pk
                    ),
                    id=(
                        co_email1_co1_ws1_user1.pk
                    ),
                ),
                validated_data=form.cleaned_data,
            )

        assert response.status_code == 302

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

        assert (
            str(co_email1_co1_ws1_user1.pk)
            in url
        )

    def test_build_app_context(
        self,
        co_email1_co1_ws1_user1,
    ):
        view = CompanyEmailUpdateView()

        view.object = co_email1_co1_ws1_user1

        context = view.build_app_context()

        assert (
            context.workspace_id
            == (
                co_email1_co1_ws1_user1
                .company
                .workspace
                .workspace_id
            )
        )

        assert (
            context.company_id
            == co_email1_co1_ws1_user1.company.pk
        )

        assert (
            context.email_id
            == co_email1_co1_ws1_user1.pk
        )

    def test_build_extra_context(self):

        view = CompanyEmailUpdateView()

        context = view.build_extra_context()

        assert context.app_kind == "company email"
        assert context.page_title == "Update Company Email"


class TestCompanyEmailDeleteView:

    @patch(
        "apps.companies.views.CompanyEmailSelector.get"
    )
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        co_email1_co1_ws1_user1,
    ):
        mock_get.return_value = (
            co_email1_co1_ws1_user1
        )

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
            obj_id=(
                co_email1_co1_ws1_user1.pk
            ),
        )

        assert result is co_email1_co1_ws1_user1

    @patch("apps.companies.views.redirect")
    @patch("apps.companies.views.CompanyEmailService.remove")
    def test_post_calls_remove_service_and_redirects(
            self,
            mock_remove,
            mock_redirect,
            user1,
            co_email1_co1_ws1_user1,
    ):
        response = HttpResponse()

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

        mock_remove.assert_called_once_with(
            user=user1,
            context=CompanyChildContext(
                workspace_id=(
                    co_email1_co1_ws1_user1
                    .company
                    .workspace
                    .workspace_id
                ),
                company_id=(
                    co_email1_co1_ws1_user1
                    .company
                    .pk
                ),
                id=(
                    co_email1_co1_ws1_user1.pk
                ),
            ),
        )

        mock_redirect.assert_called_once()

        assert result is response

    def test_build_app_context(
        self,
        co_email1_co1_ws1_user1,
    ):
        view = CompanyEmailDeleteView()

        view.object = co_email1_co1_ws1_user1

        context = view.build_app_context()

        assert (
            context.workspace_id
            == (
                co_email1_co1_ws1_user1
                .company
                .workspace
                .workspace_id
            )
        )

        assert (
            context.company_id
            == co_email1_co1_ws1_user1.company.pk
        )

        assert (
            context.email_id
            == co_email1_co1_ws1_user1.pk
        )

    def test_build_extra_context(self):

        view = CompanyEmailDeleteView()

        context = view.build_extra_context()

        assert context.app_kind == "company email"
        assert context.page_title == "Delete Company Email"
