import uuid
from unittest.mock import ANY, Mock, patch

import pytest
from django.http import HttpResponse, Http404
from django.test import RequestFactory
from django.urls import reverse

from apps.core.common.contexts.contexts import (
    EmptyContext,
    WorkspaceContext,
)
from apps.core.view_contexts.app_context import AppContext
from apps.core.view_contexts.extra_context import ExtraContext
from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    BusinessRuleViolationError,
)
from apps.workspaces.views import (
    WorkspaceCreateView,
    WorkspaceDeleteView,
    WorkspaceDetailView,
    WorkspaceListView,
    WorkspaceUpdateView,
)


class TestWorkspaceListView:

    @patch("apps.workspaces.views.WorkspaceSelector.list")
    def test_get_queryset_delegates_to_selector(
        self,
        mock_list,
        user1,
    ):
        queryset = Mock()
        mock_list.return_value = queryset

        request = RequestFactory().get("/")
        request.user = user1

        view = WorkspaceListView()
        view.request = request

        result = view.get_queryset()

        mock_list.assert_called_once_with(
            user=user1,
        )

        assert result is queryset

    @patch("apps.workspaces.views.WorkspaceSelector.list")
    def test_dispatch_translates_selector_exceptions_to_404(
        self,
        mock_list,
        user1,
    ):
        # When the selector raises a ResourceNotFoundError during dispatch,
        # the ViewExceptionHandlerMixin should translate it to Http404.
        mock_list.side_effect = ResourceNotFoundError("not found")

        request = RequestFactory().get("/")
        request.user = user1

        view = WorkspaceListView()
        view.request = request

        with pytest.raises(Http404):
            view.dispatch(request)


class TestWorkspaceCreateView:

    @patch.object(WorkspaceCreateView, "execute_service")
    @patch("apps.workspaces.views.redirect")
    def test_form_valid_executes_service_and_redirects_on_success(
        self,
        mock_redirect,
        mock_execute_service,
        user1,
    ):
        response = HttpResponse()
        mock_redirect.return_value = response

        form = Mock()
        form.cleaned_data = {
            "name": "Backend Workspace",
        }

        request = RequestFactory().post("/")
        request.user = user1

        view = WorkspaceCreateView()
        view.request = request
        view.success_url = "/success/"

        mock_execute_service.return_value = None

        result = view.form_valid(form)

        mock_execute_service.assert_called_once_with(
            form=form,
            operation=ANY,
        )

        operation = mock_execute_service.call_args.kwargs["operation"]

        with patch(
            "apps.workspaces.views.WorkspaceService.create"
        ) as mock_create:

            operation()

            mock_create.assert_called_once_with(
                user=user1,
                context=EmptyContext(),
                validated_data=form.cleaned_data,
            )

        mock_redirect.assert_called_once_with("/success/")

        assert result is response

    @patch.object(WorkspaceCreateView, "execute_service")
    def test_form_valid_returns_form_invalid_response_when_service_fails(
        self,
        mock_execute_service,
        user1,
    ):
        error_response = HttpResponse(status=200)
        mock_execute_service.return_value = error_response

        form = Mock()

        request = RequestFactory().post("/")
        request.user = user1

        view = WorkspaceCreateView()
        view.request = request

        result = view.form_valid(form)

        mock_execute_service.assert_called_once_with(
            form=form,
            operation=ANY,
        )

        assert result is error_response

    def test_build_extra_context(self):

        context = WorkspaceCreateView().build_extra_context()

        assert isinstance(context, ExtraContext)
        assert context.app_kind == "workspace"
        assert context.page_title == "Create Workspace"

    @patch("apps.workspaces.views.WorkspaceService.create")
    def test_form_valid_service_raises_business_rule_adds_form_errors(
        self,
        mock_create,
        user1,
    ):
        # Simulate the service raising a business rule error and ensure the
        # ServiceFormErrorMixin adds errors to the form and form_valid returns
        # the form_invalid response (status 200).
        err = BusinessRuleViolationError()
        # add expected attributes used by ServiceFormErrorMixin.add_service_errors_to_form
        err.fields = ["name"]
        err.messages = ["invalid workspace name"]
        mock_create.side_effect = err

        form = Mock()
        form.cleaned_data = {"name": "Bad Name"}

        request = RequestFactory().post("/")
        request.user = user1

        view = WorkspaceCreateView()
        view.request = request
        view.object = Mock()

        result = view.form_valid(form)

        # The mixin should add the service errors to the form
        form.add_error.assert_called_with("name", "invalid workspace name")

        # form_valid should return a form_invalid response (status 200)
        assert hasattr(result, "status_code")
        assert result.status_code == 200


class TestWorkspaceDetailView:

    @patch("apps.workspaces.views.WorkspaceSelector.get")
    def test_get_object_delegates_to_selector(
        self,
        mock_get,
        user1,
    ):
        workspace = Mock()
        mock_get.return_value = workspace

        request = RequestFactory().get("/")
        request.user = user1

        view = WorkspaceDetailView()
        view.request = request
        view.kwargs = {
            "workspace_id": "workspace-id",
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            obj_id="workspace-id",
        )

        assert result is workspace

    @patch("apps.workspaces.views.WorkspaceSelector.get")
    def test_dispatch_translates_selector_get_exceptions_to_404(
        self,
        mock_get,
        user1,
    ):
        mock_get.side_effect = ResourceNotFoundError("missing")

        request = RequestFactory().get("/")
        request.user = user1

        view = WorkspaceDetailView()
        view.request = request
        view.kwargs = {
            "workspace_id": "workspace-id",
        }

        with pytest.raises(Http404):
            view.dispatch(request)

    @patch("apps.workspaces.views.company_list_url")
    def test_build_app_context(
        self,
        mock_company_list_url,
    ):
        mock_company_list_url.return_value = "/companies/"

        view = WorkspaceDetailView()
        view.kwargs = {
            "workspace_id": "workspace-id",
        }

        context = view.build_app_context()

        mock_company_list_url.assert_called_once_with(
            workspace_id="workspace-id",
        )

        assert isinstance(context, AppContext)
        assert context.companies_list_url == "/companies/"


class TestWorkspaceUpdateView:

    @patch("apps.workspaces.views.WorkspaceSelector.get")
    def test_get_object_delegates_to_selector(
        self,
        mock_get,
        user1,
    ):
        workspace = Mock()
        mock_get.return_value = workspace

        request = RequestFactory().get("/")
        request.user = user1

        view = WorkspaceUpdateView()
        view.request = request
        view.kwargs = {
            "workspace_id": "workspace-id",
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            obj_id="workspace-id",
        )

        assert result is workspace

    @patch.object(WorkspaceUpdateView, "execute_service")
    @patch("apps.workspaces.views.redirect")
    def test_form_valid_executes_service_and_redirects_on_success(
        self,
        mock_redirect,
        mock_execute_service,
        user1,
    ):
        response = HttpResponse()
        mock_redirect.return_value = response

        form = Mock()
        form.cleaned_data = {
            "name": "Updated Workspace",
        }

        request = RequestFactory().post("/")
        request.user = user1

        view = WorkspaceUpdateView()
        view.request = request
        view.kwargs = {
            "workspace_id": "workspace-id",
        }

        mock_execute_service.return_value = None

        with patch.object(
            view,
            "get_success_url",
            return_value="/success/",
        ):
            result = view.form_valid(form)

        mock_execute_service.assert_called_once_with(
            form=form,
            operation=ANY,
        )

        operation = mock_execute_service.call_args.kwargs["operation"]

        with patch(
            "apps.workspaces.views.WorkspaceService.update"
        ) as mock_update:

            operation()

            mock_update.assert_called_once_with(
                user=user1,
                context=WorkspaceContext(
                    id="workspace-id",
                ),
                validated_data=form.cleaned_data,
            )

        mock_redirect.assert_called_once_with("/success/")

        assert result is response

    @patch.object(WorkspaceUpdateView, "execute_service")
    def test_form_valid_returns_form_invalid_response_when_service_fails(
        self,
        mock_execute_service,
        user1,
    ):
        error_response = HttpResponse(status=200)
        mock_execute_service.return_value = error_response

        form = Mock()

        request = RequestFactory().post("/")
        request.user = user1

        view = WorkspaceUpdateView()
        view.request = request
        view.kwargs = {
            "workspace_id": "workspace-id",
        }

        result = view.form_valid(form)

        mock_execute_service.assert_called_once_with(
            form=form,
            operation=ANY,
        )

        assert result is error_response

    def test_get_success_url(self):

        workspace_id = uuid.uuid4()

        view = WorkspaceUpdateView()
        view.kwargs = {
            "workspace_id": workspace_id,
        }

        assert view.get_success_url() == reverse(
            "workspace-detail-web",
            kwargs={
                "workspace_id": workspace_id,
            },
        )

    def test_build_extra_context(self):

        context = WorkspaceUpdateView().build_extra_context()

        assert isinstance(context, ExtraContext)
        assert context.app_kind == "workspace"
        assert context.page_title == "Update Workspace"

    @patch("apps.workspaces.views.WorkspaceService.update")
    def test_form_valid_service_raises_business_rule_adds_form_errors(
        self,
        mock_update,
        user1,
    ):
        err = BusinessRuleViolationError()
        err.fields = ["name"]
        err.messages = ["cannot use this name"]
        mock_update.side_effect = err

        form = Mock()
        form.cleaned_data = {"name": "Bad Update"}

        request = RequestFactory().post("/")
        request.user = user1

        view = WorkspaceUpdateView()
        view.request = request
        view.kwargs = {"workspace_id": "workspace-id"}
        view.object = Mock()

        result = view.form_valid(form)

        form.add_error.assert_called_with("name", "cannot use this name")
        assert hasattr(result, "status_code")
        assert result.status_code == 200


class TestWorkspaceDeleteView:

    @patch("apps.workspaces.views.WorkspaceSelector.get")
    def test_get_object_delegates_to_selector(
        self,
        mock_get,
        user1,
    ):
        workspace = Mock()
        mock_get.return_value = workspace

        request = RequestFactory().get("/")
        request.user = user1

        view = WorkspaceDeleteView()
        view.request = request
        view.kwargs = {
            "workspace_id": "workspace-id",
        }

        result = view.get_object()

        mock_get.assert_called_once_with(
            user=user1,
            obj_id="workspace-id",
        )

        assert result is workspace

    @patch("apps.workspaces.views.redirect")
    @patch("apps.workspaces.views.WorkspaceService.remove")
    def test_post_calls_service_and_redirects(
        self,
        mock_remove,
        mock_redirect,
        user1,
    ):
        response = HttpResponse()
        mock_redirect.return_value = response

        request = RequestFactory().post("/")
        request.user = user1

        view = WorkspaceDeleteView()
        view.request = request
        view.kwargs = {
            "workspace_id": "workspace-id",
        }
        view.success_url = "/success/"

        result = view.post(request)

        mock_remove.assert_called_once_with(
            user=user1,
            context=WorkspaceContext(
                id="workspace-id",
            ),
        )

        mock_redirect.assert_called_once_with("/success/")

        assert result is response

    @patch("apps.workspaces.views.WorkspaceService.remove")
    def test_post_service_raises_resource_not_found_translates_to_404(
        self,
        mock_remove,
        user1,
    ):
        mock_remove.side_effect = ResourceNotFoundError("not found")

        request = RequestFactory().post("/")
        request.user = user1

        view = WorkspaceDeleteView()
        view.request = request
        view.kwargs = {"workspace_id": "workspace-id"}
        view.success_url = "/success/"

        with pytest.raises(Http404):
            view.dispatch(request)

    def test_build_extra_context(self):

        context = WorkspaceDeleteView().build_extra_context()

        assert isinstance(context, ExtraContext)
        assert context.app_kind == "workspace"
        assert context.page_title == "Delete Workspace"
