from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

# Serializers
from apps.workspaces.api.serializers import (
    DisplayWorkspaceSerializer,
    WorkspaceSerializer,
)

# Selectors
from apps.workspaces.selectors.workspace_selector import WorkspaceSelector

# Services
from apps.workspaces.services.workspace_service import WorkspaceService


# ViewSets

class WorkspaceViewSet(ModelViewSet):

    # URL Path:
    # workspaces/{id}

    permission_classes = [IsAuthenticated]

    lookup_field = 'workspace_id'
    lookup_url_kwarg = 'id'

    def get_queryset(self):

        return WorkspaceSelector.list(user=self.request.user)

    def get_serializer_class(self):

        if self.action in ['create', 'update', 'partial_update']:
            return WorkspaceSerializer

        return DisplayWorkspaceSerializer

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = WorkspaceService.create(
            user=request.user, validated_data=serializer.validated_data
        )

        return Response(DisplayWorkspaceSerializer(instance).data)

    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = WorkspaceService.update(
            user=request.user,
            workspace_id=self.kwargs['id'],
            validated_data=serializer.validated_data
        )

        return Response(DisplayWorkspaceSerializer(instance).data)

    def destroy(self, request, *args, **kwargs):

        WorkspaceService.remove(
            user=request.user,
            workspace_id=self.kwargs['id'],
        )

        return Response(status=status.HTTP_200_OK)
