import pytest

from unittest.mock import Mock, patch

from django.http import HttpResponse, Http404
from django.test import RequestFactory

from apps.companies.views import (
    CompanyListView,
    CompanyCreateView,
    CompanyDetailView,
    CompanyUpdateView,
    CompanyDeleteView,
)

from apps.core.common.contexts.contexts import CompanyContext
from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    BusinessRuleViolationError,
)


pytestmark = pytest.mark.django_db


class TestCompanyListView:

    # ------------------------
    # Queryset
    # ------------------------

    @patch("apps.companies.views.CompanySelector.list")
    def test_get_queryset_calls_selector(
        self,
        mock_list,
        user1,
        workspace1_user1,
    ):
        queryset = Mock()

        mock_list.return_value = queryset

        request = RequestFactory().get(
            "/",
            {
                "workspace_id": workspace1_user1.workspace_id,
            },
        )
        request.user = user1

        view = CompanyListView()
        view.request = request

        result = view.get_queryset()

        mock_list.assert_called_once()

        kwargs = mock_list.call_args.kwargs

        assert kwargs["user"] == user1
        assert (
            kwargs["filters"].workspace_id
            == str(workspace1_user1.workspace_id)
        )

        assert result is queryset

    @patch("apps.companies.views.CompanySelector.list")
    def test_dispatch_translates_selector_exceptions_to_404(
        self,
        mock_list,
        user1,
    ):
        mock_list.side_effect = ResourceNotFoundError("not found")

        request = RequestFactory().get(
            "/",
            {
                "workspace_id": "workspace-id",
            },
        )
        request.user = user1

        view = CompanyListView()
        view.request = request

        with pytest.raises(Http404):
            view.dispatch(request)

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
        self,
        user1,
        workspace1_user1,
    ):
        request = RequestFactory().get(
            "/",
            {
                "workspace_id": workspace1_user1.workspace_id,
            },
        )
        request.user = user1

        view = CompanyListView()
        view.request = request

        context = view.build_app_context()

        assert (
            context.workspace_id
            == str(workspace1_user1.workspace_id)
        )


class TestCompanyCreateView:

    # ------------------------
    # Form
    # ------------------------

    @patch.object(
        CompanyCreateView,
        "execute_service",
    )
    def test_form_valid_executes_service_and_redirects_on_success(
        self,
        mock_execute_service,
        user1,
        workspace1_user1,
    ):
        form = Mock()

        form.cleaned_data = {
            "name": "ACME",
            "website": "https://acme.com",
        }

        mock_execute_service.return_value = None

        request = RequestFactory().post("/")
        request.user = user1

        view = CompanyCreateView()

        view.request = request
        view.kwargs = {
            "workspace_id": workspace1_user1.workspace_id,
        }

        with patch.object(
            view,
            "get_success_url",
            return_value="/success/",
        ):

            result = view.form_valid(form)

        mock_execute_service.assert_called_once()

        operation = (
            mock_execute_service
            .call_args
            .kwargs["operation"]
        )

        with patch(
            "apps.companies.views.CompanyService.create"
        ) as mock_create:

            operation()

            mock_create.assert_called_once_with(
                user=user1,
                context=CompanyContext(
                    workspace_id=workspace1_user1.workspace_id,
                ),
                validated_data=form.cleaned_data,
            )

        assert result.status_code == 302
        assert result.url == "/success/"

    @patch("apps.companies.views.CompanyService.create")
    def test_form_valid_service_raises_business_rule_adds_form_errors(
        self,
        mock_create,
        user1,
    ):
        # Simulate the service raising a business rule error and ensure the
        # ServiceFormErrorMixin adds errors to the form and form_valid returns
        # the form_invalid response (status 200).
        err = BusinessRuleViolationError()
        err.fields = ["name"]
        err.messages = ["invalid name"]
        mock_create.side_effect = err

        form = Mock()
        form.cleaned_data = {"name": "Bad Company", "website": ""}

        request = RequestFactory().post("/")
        request.user = user1

        view = CompanyCreateView()
        view.request = request
        view.kwargs = {"workspace_id": "workspace-id"}
        view.object = Mock()

        result = view.form_valid(form)

        form.add_error.assert_called_with("name", "invalid name")
        assert hasattr(result, "status_code")
        assert result.status_code == 200

    # ------------------------
    # Success URL
    # ------------------------

    def test_get_success_url(
        self,
        workspace1_user1,
    ):
        view = CompanyCreateView()

        view.kwargs = {
            "workspace_id": workspace1_user1.workspace_id,
        }

        url = view.get_success_url()

        assert (
            str(workspace1_user1.workspace_id)
            in url
        )

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
        self,
        workspace1_user1,
    ):
        view = CompanyCreateView()

        view.kwargs = {
            "workspace_id": workspace1_user1.workspace_id,
        }

        context = view.build_app_context()

        assert (
            context.workspace_id
            == workspace1_user1.workspace_id
        )

    # ------------------------
    # Extra Context
    # ------------------------

    def test_build_extra_context(self):

        view = CompanyCreateView()

        context = view.build_extra_context()

        assert context.app_kind == "company"
        assert context.page_title == "Create Company"


class TestCompanyDetailView:

    # ------------------------
    # Object
    # ------------------------

    @patch("apps.companies.views.CompanySelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        co1_ws1_user1,
    ):
        mock_get.return_value = co1_ws1_user1

        request = RequestFactory().get("/")

        request.user = user1

        view = CompanyDetailView()

        view.request = request
        view.kwargs = {
            "pk": co1_ws1_user1.pk,
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            obj_id=co1_ws1_user1.pk,
        )

        assert result is co1_ws1_user1

    @patch("apps.companies.views.CompanySelector.get")
    def test_dispatch_translates_selector_get_exceptions_to_404(
        self,
        mock_get,
        user1,
    ):
        mock_get.side_effect = ResourceNotFoundError("missing")

        request = RequestFactory().get("/")
        request.user = user1

        view = CompanyDetailView()
        view.request = request
        view.kwargs = {
            "pk": "123",
        }

        with pytest.raises(Http404):
            view.dispatch(request)

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
        self,
        co1_ws1_user1,
    ):
        request = RequestFactory().get("/")

        view = CompanyDetailView()

        view.request = request
        view.object = co1_ws1_user1

        context = view.build_app_context()

        assert (
            context.workspace_id
            == co1_ws1_user1.workspace.workspace_id
        )

        assert (
            context.company_id
            == co1_ws1_user1.pk
        )

        assert context.applications_list_url is not None
        assert context.companies_list_url is not None
        assert context.positions_list_url is not None
        assert context.company_emails_list_url is not None
        assert context.company_notes_list_url is not None


class TestCompanyUpdateView:

    # ------------------------
    # Object
    # ------------------------

    @patch("apps.companies.views.CompanySelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        co1_ws1_user1,
    ):
        mock_get.return_value = co1_ws1_user1

        request = RequestFactory().get("/")

        request.user = user1

        view = CompanyUpdateView()

        view.request = request
        view.kwargs = {
            "pk": co1_ws1_user1.pk,
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            obj_id=co1_ws1_user1.pk,
        )

        assert result is co1_ws1_user1

    # ------------------------
    # Form
    # ------------------------

    @patch.object(
        CompanyUpdateView,
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
            "name": "Updated Company",
            "website": "https://updated.com",
        }

        mock_execute_service.return_value = None

        request = RequestFactory().post("/")

        request.user = user1

        view = CompanyUpdateView()

        view.request = request
        view.object = co1_ws1_user1
        view.kwargs = {
            "pk": co1_ws1_user1.pk,
        }

        with patch.object(
            view,
            "get_success_url",
            return_value="/success/",
        ):

            result = view.form_valid(form)

        mock_execute_service.assert_called_once()

        operation = (
            mock_execute_service
            .call_args
            .kwargs["operation"]
        )

        with patch(
            "apps.companies.views.CompanyService.update"
        ) as mock_update:

            operation()

            mock_update.assert_called_once_with(
                user=user1,
                context=CompanyContext(
                    workspace_id=(
                        co1_ws1_user1
                        .workspace
                        .workspace_id
                    ),
                    id=co1_ws1_user1.pk,
                ),
                validated_data=form.cleaned_data,
            )

        assert result.status_code == 302
        assert result.url == "/success/"

    @patch("apps.companies.views.CompanyService.update")
    def test_form_valid_service_raises_business_rule_adds_form_errors(
        self,
        mock_update,
        user1,
        co1_ws1_user1
    ):
        err = BusinessRuleViolationError()
        err.fields = ["name"]
        err.messages = ["cannot use this name"]
        mock_update.side_effect = err

        form = Mock()
        form.cleaned_data = {"name": "Bad Update", "website": ""}

        request = RequestFactory().post("/")
        request.user = user1

        view = CompanyUpdateView()
        view.request = request
        view.object = None
        view.kwargs = {"pk": "123"}
        view.object = co1_ws1_user1

        result = view.form_valid(form)

        form.add_error.assert_called_with("name", "cannot use this name")
        assert hasattr(result, "status_code")
        assert result.status_code == 200

    # ------------------------
    # Success URL
    # ------------------------

    def test_get_success_url(
        self,
        co1_ws1_user1,
    ):
        view = CompanyUpdateView()

        view.kwargs = {
            "pk": co1_ws1_user1.pk,
        }

        url = view.get_success_url()

        assert str(co1_ws1_user1.pk) in url

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
        self,
        co1_ws1_user1,
    ):
        view = CompanyUpdateView()

        view.object = co1_ws1_user1

        context = view.build_app_context()

        assert (
            context.workspace_id
            == co1_ws1_user1.workspace.workspace_id
        )

        assert (
            context.company_id
            == co1_ws1_user1.pk
        )

    # ------------------------
    # Extra Context
    # ------------------------

    def test_build_extra_context(self):

        view = CompanyUpdateView()

        context = view.build_extra_context()

        assert context.app_kind == "company"
        assert context.page_title == "Update Company"


class TestCompanyDeleteView:

    # ------------------------
    # Object
    # ------------------------

    @patch("apps.companies.views.CompanySelector.get")
    def test_get_object_calls_selector(
        self,
        mock_get,
        user1,
        co1_ws1_user1,
    ):
        mock_get.return_value = co1_ws1_user1

        request = RequestFactory().get("/")

        request.user = user1

        view = CompanyDeleteView()

        view.request = request
        view.kwargs = {
            "pk": co1_ws1_user1.pk,
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            obj_id=co1_ws1_user1.pk,
        )

        assert result is co1_ws1_user1

    # ------------------------
    # Delete
    # ------------------------

    @patch("apps.companies.views.redirect")
    @patch("apps.companies.views.CompanyService.remove")
    def test_post_calls_remove_service(
        self,
        mock_remove,
        mock_redirect,
        user1,
        co1_ws1_user1,
    ):
        response = HttpResponse()

        mock_redirect.return_value = response

        request = RequestFactory().post("/")

        request.user = user1

        view = CompanyDeleteView()

        view.request = request
        view.kwargs = {
            "pk": co1_ws1_user1.pk,
        }

        result = view.post(
            request,
            pk=co1_ws1_user1.pk,
        )

        mock_remove.assert_called_once_with(
            user=user1,
            context=CompanyContext(
                workspace_id=(
                    co1_ws1_user1
                    .workspace
                    .workspace_id
                ),
                id=co1_ws1_user1.pk,
            ),
        )

        mock_redirect.assert_called_once()

        assert result is response

    @patch("apps.companies.views.CompanyService.remove")
    def test_post_service_raises_resource_not_found_translates_to_404(
        self,
        mock_remove,
        user1,
    ):
        mock_remove.side_effect = ResourceNotFoundError("not found")

        request = RequestFactory().post("/")
        request.user = user1

        view = CompanyDeleteView()
        view.request = request
        view.kwargs = {"pk": "123"}

        with pytest.raises(Http404):
            view.dispatch(request)

    # ------------------------
    # App Context
    # ------------------------

    def test_build_app_context(
        self,
        co1_ws1_user1,
    ):
        view = CompanyDeleteView()

        view.object = co1_ws1_user1

        context = view.build_app_context()

        assert (
            context.workspace_id
            == co1_ws1_user1.workspace.workspace_id
        )

        assert (
            context.company_id
            == co1_ws1_user1.pk
        )

    # ------------------------
    # Extra Context
    # ------------------------

    def test_build_extra_context(self):

        view = CompanyDeleteView()

        context = view.build_extra_context()

        assert context.app_kind == "company"
        assert context.page_title == "Delete Company"
