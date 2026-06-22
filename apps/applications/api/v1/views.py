from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Serializers
from apps.applications.api.v1.serializers import (
    JobApplicationSerializer,
    JobApplicationNoteSerializer,
)

# Selectors
from apps.applications.selectors.application_note_selector import (

    JobApplicationNoteSelector,
)

from apps.applications.selectors.application_selector import JobApplicationSelector

# Contexts
from apps.applications.services.contexts.application_context import (
    JobApplicationContext,
    JobApplicationChildContext
)

# Services
from apps.applications.services.application_note_service import (
    JobApplicationNoteService,
)

from apps.applications.services.application_service import JobApplicationService


# ViewSets

class JobApplicationViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    # URL Path:
    # job-applications/{id}

    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "id"

    def get_object(self, queryset=None):

        return JobApplicationSelector.get(
            user=self.request.user, application_id=self.kwargs["id"]
        )

    def get_queryset(self):

        return JobApplicationSelector.list(
            user=self.request.user,
            filters=self._get_queryset_filters(),
        )

    def _get_queryset_filters(self):

        return JobApplicationSelector.QueryFilter(
            workspace_id=self.request.query_params.get('workspace_id'),
            company_id=self.request.query_params.get('company_id'),
            job_position_id=self.request.query_params.get('job_position_id'),
            status_id=self.request.query_params.get('status_id'),
            date_applied=self.request.query_params.get('date_applied'),
        )


class JobApplicationNestedViewSet(viewsets.ModelViewSet):

    # URL Path:
    # workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/job-applications/{id}

    permission_classes = [IsAuthenticated]
    serializer_class = JobApplicationSerializer

    lookup_url_kwarg = "id"

    def get_object(self, queryset=None):

        return JobApplicationSelector.get(
            user=self.request.user, application_id=self.kwargs["id"]
        )

    def get_queryset(self):

        return JobApplicationSelector.list(
            user=self.request.user,
            filters=self._get_queryset_filters(),
        )

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = JobApplicationService.create(
            user=self.request.user,
            context=self._get_context(None),
            validated_data=serializer.validated_data)

        return Response(self.get_serializer(instance).data)

    def update(self, request, *args, **kwargs):

        serializer = self._validated_serializer()

        instance = JobApplicationService.update(
            user=self.request.user,
            context=self._get_context(self.kwargs['id']),
            validated_data=serializer.validated_data)

        return Response(self.get_serializer(instance).data)

    def partial_update(self, request, *args, **kwargs):

        serializer = self._validated_serializer(partial=True)

        instance = JobApplicationService.update(
            user=self.request.user,
            context=self._get_context(self.kwargs['id']),
            validated_data=serializer.validated_data)

        return Response(self.get_serializer(instance).data)

    def destroy(self, request, *args, **kwargs):

        JobApplicationService.remove(
            user=self.request.user,
            context=self._get_context(self.kwargs['id']),
        )

        return Response(status=status.HTTP_200_OK)

    def _get_context(self, job_application_id: int | None):

        return JobApplicationContext(
            id=job_application_id,
            workspace_id=self.kwargs['workspace_id'],
            company_id=self.kwargs['company_id'],
            job_position_id=self.kwargs['job_position_id'],
        )

    def _get_queryset_filters(self):
        return JobApplicationSelector.QueryFilter(
            workspace_id=self.kwargs['workspace_id'],
            company_id=self.kwargs['company_id'],
            job_position_id=self.kwargs['job_position_id'],
        )

    def _validated_serializer(self, partial=False):
        serializer = self.get_serializer(
            data=self.request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        return serializer


class JobApplicationNoteViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):

    # URL Path:
    # job-application-notes/{id}

    serializer_class = JobApplicationNoteSerializer
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "id"

    def get_object(self, queryset=None):

        return JobApplicationNoteSelector.get(
            user=self.request.user, application_note_id=self.kwargs["id"]
        )

    def get_queryset(self):

        return JobApplicationNoteSelector.list(
            user=self.request.user,
            filters=self._get_queryset_filters(),
        )

    def _get_queryset_filters(self):

        return JobApplicationNoteSelector.QueryFilter(
            workspace_id=self.request.query_params.get('workspace_id'),
            company_id=self.request.query_params.get('company_id'),
            job_position_id=self.request.query_params.get('job_position_id'),
            job_application_id=self.request.query_params.get('job_application_id'),
        )


class JobApplicationNoteNestedViewSet(viewsets.ModelViewSet):

    # URL Path:
    # workspaces/{workspace_id}/companies/{company_id}/job-positions/{job_position_id}/job-applications/{job_application_id}/job-application-notes/{id}

    permission_classes = [IsAuthenticated]
    serializer_class = JobApplicationNoteSerializer

    lookup_url_kwarg = "id"

    def get_object(self, queryset=None):

        return JobApplicationNoteSelector.get(
            user=self.request.user, application_note_id=self.kwargs["id"]
        )

    def get_queryset(self):

        return JobApplicationNoteSelector.list(
            user=self.request.user,
            filters=self._get_queryset_filters(),
        )

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = JobApplicationNoteService.create(
            user=self.request.user,
            context=self._get_context(None),
            validated_data=serializer.validated_data
        )

        return Response(self.get_serializer(instance).data)

    def update(self, request, *args, **kwargs):

        serializer = self._validated_serializer()

        instance = JobApplicationNoteService.update(
            user=self.request.user,
            context=self._get_context(self.kwargs['id']),
            validated_data=serializer.validated_data)

        return Response(self.get_serializer(instance).data)

    def partial_update(self, request, *args, **kwargs):

        serializer = self._validated_serializer(partial=True)

        instance = JobApplicationNoteService.update(
            user=self.request.user,
            context=self._get_context(self.kwargs['id']),
            validated_data=serializer.validated_data)

        return Response(self.get_serializer(instance).data)

    def destroy(self, request, *args, **kwargs):

        JobApplicationNoteService.remove(
            user=self.request.user,
            context=self._get_context(self.kwargs['id']),
        )

        return Response(status=status.HTTP_200_OK)

    def _get_context(self, job_application_note_id: int | None):

        return JobApplicationChildContext(
            id=job_application_note_id,
            workspace_id=self.kwargs['workspace_id'],
            company_id=self.kwargs['company_id'],
            job_position_id=self.kwargs['job_position_id'],
            job_application_id=self.kwargs["job_application_id"],
        )

    def _get_queryset_filters(self):
        return JobApplicationNoteSelector.QueryFilter(
            workspace_id=self.kwargs['workspace_id'],
            company_id=self.kwargs['company_id'],
            job_position_id=self.kwargs['job_position_id'],
            job_application_id=self.kwargs['job_application_id'],
        )

    def _validated_serializer(self, partial=False):
        serializer = self.get_serializer(
            data=self.request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        return serializer
