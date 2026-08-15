import uuid
from unittest.mock import ANY, Mock, patch

import pytest
from django.http import HttpResponse, Http404
from django.core.exceptions import ValidationError
from django.test import RequestFactory
from django.urls import reverse

from apps.core.common.contexts.contexts import EmptyContext, JobTaskContext
from apps.core.exceptions.exceptions import (
    ResourceNotFoundError,
    BusinessRuleViolationError,
)
from apps.accounts.views import (
    JobTaskListView,
    JobTaskCreateView,
    JobTaskDetailView,
    JobTaskUpdateView,
    JobTaskDeleteView,
)


class TestJobTaskListView:

    @patch("apps.accounts.views.JobTaskSelector.list")
    def test_get_queryset_delegates_to_selector(
        self,
        mock_list,
        user1,
    ):
        queryset = Mock()
        mock_list.return_value = queryset

        request = RequestFactory().get("/")
        request.user = user1

        view = JobTaskListView()
        view.request = request

        result = view.get_queryset()

        mock_list.assert_called_once_with(
            user=user1,
        )

        assert result is queryset

    @patch("apps.accounts.views.JobTaskSelector.list")
    def test_dispatch_translates_selector_exceptions_to_404(
        self,
        mock_list,
        user1,
    ):
        mock_list.side_effect = ResourceNotFoundError("not found")

        request = RequestFactory().get("/")
        request.user = user1

        view = JobTaskListView()
        view.request = request

        with pytest.raises(Http404):
            view.dispatch(request)


class TestJobTaskCreateView:

    @patch.object(JobTaskCreateView, "execute_service")
    @patch("apps.accounts.views.redirect")
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
            "title": "New Task",
            "description": "Some Description",
        }

        request = RequestFactory().post("/")
        request.user = user1

        view = JobTaskCreateView()
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
            "apps.accounts.views.JobTaskService.create"
        ) as mock_create:

            operation()

            mock_create.assert_called_once_with(
                user=user1,
                context=EmptyContext(),
                validated_data=form.cleaned_data,
            )

        mock_redirect.assert_called_once_with("/success/")

        assert result is response

    @patch.object(JobTaskCreateView, "execute_service")
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

        view = JobTaskCreateView()
        view.request = request

        result = view.form_valid(form)

        mock_execute_service.assert_called_once_with(
            form=form,
            operation=ANY,
        )

        assert result is error_response

    @patch("apps.accounts.views.JobTaskService.create")
    def test_form_valid_service_raises_business_rule_adds_form_errors(
        self,
        mock_create,
        user1,
    ):
        err = BusinessRuleViolationError()
        err.fields = ["title"]
        err.messages = ["invalid title"]
        mock_create.side_effect = err

        form = Mock()
        form.cleaned_data = {"title": "Bad"}

        request = RequestFactory().post("/")
        request.user = user1

        view = JobTaskCreateView()
        view.request = request
        view.object = Mock()

        result = view.form_valid(form)

        form.add_error.assert_called_with("title", "invalid title")

        assert hasattr(result, "status_code")
        assert result.status_code == 200


class TestJobTaskDetailView:

    @patch("apps.accounts.views.JobTaskSelector.list")
    def test_get_queryset_delegates_to_selector(
        self,
        mock_list,
        user1,
    ):
        queryset = Mock()
        mock_list.return_value = queryset

        request = RequestFactory().get("/")
        request.user = user1

        view = JobTaskDetailView()
        view.request = request

        result = view.get_queryset()

        mock_list.assert_called_once_with(user=user1)
        assert result is queryset


class TestJobTaskUpdateView:

    @patch("apps.accounts.views.JobTaskSelector.list")
    def test_get_queryset_delegates_to_selector(
        self,
        mock_list,
        user1,
    ):
        queryset = Mock()
        mock_list.return_value = queryset

        request = RequestFactory().get("/")
        request.user = user1

        view = JobTaskUpdateView()
        view.request = request

        result = view.get_queryset()

        mock_list.assert_called_once_with(user=user1)
        assert result is queryset

    @patch.object(JobTaskUpdateView, "execute_service")
    @patch("apps.accounts.views.redirect")
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
            "title": "Updated Task",
            "description": "Updated",
        }

        request = RequestFactory().post("/")
        request.user = user1

        view = JobTaskUpdateView()
        view.request = request
        view.kwargs = {"pk": "task-id"}

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
            "apps.accounts.views.JobTaskService.update"
        ) as mock_update:

            operation()

            mock_update.assert_called_once_with(
                user=user1,
                context=JobTaskContext(id="task-id"),
                validated_data=form.cleaned_data,
            )

        mock_redirect.assert_called_once_with("/success/")

        assert result is response

    @patch.object(JobTaskUpdateView, "execute_service")
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

        view = JobTaskUpdateView()
        view.request = request
        view.kwargs = {"pk": "task-id"}

        result = view.form_valid(form)

        mock_execute_service.assert_called_once_with(
            form=form,
            operation=ANY,
        )

        assert result is error_response

    def test_get_success_url(self):

        view = JobTaskUpdateView()
        view.kwargs = {"pk": 1}

        assert view.get_success_url() == reverse(
            "job-task-detail-web",
            kwargs={
                "pk": 1,
            },
        )

    @patch("apps.accounts.views.JobTaskService.update")
    def test_form_valid_service_raises_business_rule_adds_form_errors(
        self,
        mock_update,
        user1,
    ):
        err = BusinessRuleViolationError()
        err.fields = ["title"]
        err.messages = ["cannot use this title"]
        mock_update.side_effect = err

        form = Mock()
        form.cleaned_data = {"title": "Bad Update"}

        request = RequestFactory().post("/")
        request.user = user1

        view = JobTaskUpdateView()
        view.request = request
        view.kwargs = {"pk": "task-id"}
        view.object = Mock()

        result = view.form_valid(form)

        form.add_error.assert_called_with("title", "cannot use this title")
        assert hasattr(result, "status_code")
        assert result.status_code == 200


class TestJobTaskDeleteView:

    @patch("apps.accounts.views.JobTaskSelector.list")
    def test_get_queryset_delegates_to_selector(
        self,
        mock_list,
        user1,
    ):
        queryset = Mock()
        mock_list.return_value = queryset

        request = RequestFactory().get("/")
        request.user = user1

        view = JobTaskDeleteView()
        view.request = request

        result = view.get_queryset()

        mock_list.assert_called_once_with(user=user1)
        assert result is queryset

    @patch("apps.accounts.views.redirect")
    @patch("apps.accounts.views.JobTaskService.remove")
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

        view = JobTaskDeleteView()
        view.request = request
        view.kwargs = {"pk": "task-id"}
        view.success_url = "/success/"

        result = view.post(request)

        mock_remove.assert_called_once_with(
            user=user1,
            context=JobTaskContext(id="task-id"),
        )

        mock_redirect.assert_called_once_with("/success/")

        assert result is response

    @patch("apps.accounts.views.JobTaskService.remove")
    def test_post_service_raises_resource_not_found_translates_to_404(
        self,
        mock_remove,
        user1,
    ):
        mock_remove.side_effect = ResourceNotFoundError("not found")

        request = RequestFactory().post("/")
        request.user = user1

        view = JobTaskDeleteView()
        view.request = request
        view.kwargs = {"pk": "task-id"}
        view.success_url = "/success/"

        with pytest.raises(Http404):
            view.dispatch(request)
