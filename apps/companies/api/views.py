from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

# Serializers
from apps.companies.api.serializers import (

    # Company Serializers:
    CompanySerializer,

    # Company Note Serializers:
    CompanyNoteSerializer,

    # Company Email Serializers:
    CompanyEmailSerializer,

    # Job Benefit Serializers:
    JobBenefitSerializer,

    # Job Task Serializers:
    JobTaskSerializer,

    # Job Requirement Serializers:
    JobRequirementSerializer,

    # Job Position Serializers:
    JobPositionSerializer,
)

# Selectors
from apps.companies.selectors.company_email_selector import CompanyEmailSelector
from apps.companies.selectors.company_note_selector import CompanyNoteSelector
from apps.companies.selectors.company_selector import CompanySelector
from apps.companies.selectors.job_benefit_selector import JobBenefitSelector
from apps.companies.selectors.job_position_selector import JobPositionSelector
from apps.companies.selectors.job_requirement_selector import JobRequirementSelector
from apps.companies.selectors.job_task_selector import JobTaskSelector

# Services
from apps.companies.services.company_service import CompanyService
from apps.companies.services.company_note_service import CompanyNoteService
from apps.companies.services.company_email_service import CompanyEmailService
from apps.companies.services.job_benefit_service import JobBenefitService
from apps.companies.services.job_position_service import JobPositionService
from apps.companies.services.job_requirement_service import JobRequirementService
from apps.companies.services.job_task_service import JobTaskService

# Contexts
from apps.companies.services.contexts.company_context import (
    CompanyContext,
    CompanyChildContext
)


# ViewSets

class CompanyViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    # URL Path:
    # companies/{id}

    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "id"

    def get_queryset(self):

        return CompanySelector.list(
            user=self.request.user,
            filters=self._get_queryset_filters(),
        )

    def _get_queryset_filters(self) -> CompanySelector.QueryFilter:

        return CompanySelector.QueryFilter(
            workspace_id=self.request.query_params.get("workspace_id"),
        )


class NestedCompanyViewSet(ModelViewSet):

    # URL Path:
    # workspaces/{workspace_id}/companies/{id}

    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer

    lookup_url_kwarg = "id"

    def get_queryset(self):

        return CompanySelector.list(
            user=self.request.user,
            filters=self._get_queryset_filters()
        )

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = CompanyService.create(
            user=self.request.user,
            context=self._get_context(None),
            validated_data=serializer.validated_data,
        )

        return Response(self.get_serializer(instance).data)

    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = CompanyService.update(
            user=self.request.user,
            context=self._get_context(self.kwargs["id"]),
            validated_data=serializer.validated_data,
        )

        return Response(self.get_serializer(instance).data)

    def partial_update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        instance = CompanyService.update(
            user=self.request.user,
            context=self._get_context(self.kwargs["id"]),
            validated_data=serializer.validated_data,
        )

        return Response(self.get_serializer(instance).data)

    def destroy(self, request, *args, **kwargs):

        CompanyService.remove(
            user=self.request.user,
            context=self._get_context(self.kwargs["id"]),
        )

        return Response(status=status.HTTP_200_OK)

    def _get_context(self, company_id: int | None) -> CompanyContext:

        return CompanyContext(
            workspace_id=self.kwargs["workspace_id"],
            id=company_id
        )

    def _get_queryset_filters(self):

        return CompanySelector.QueryFilter(
            workspace_id=self.kwargs["workspace_id"],
        )


class CompanyNoteViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    # URL Path:
    # company-notes/{id}

    serializer_class = CompanyNoteSerializer
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "id"

    def get_queryset(self):

        return CompanyNoteSelector.list(
            user=self.request.user,
            filters=self._get_queryset_filters()
        )

    def _get_queryset_filters(self) -> CompanyNoteSelector.QueryFilter:

        return CompanyNoteSelector.QueryFilter(
            workspace_id=self.request.query_params.get("workspace_id"),
            company_id=self.request.query_params.get("company_id"),
        )


class NestedCompanyNoteViewSet(ModelViewSet):

    # URL Path:
    # workspaces/workspace_id/companies/company_id/company-notes/{id}

    permission_classes = [IsAuthenticated]
    serializer_class = CompanyNoteSerializer

    lookup_url_kwarg = "id"

    def get_queryset(self):

        return CompanyNoteSelector.list(
            user=self.request.user,
            filters=self._get_queryset_filters()
        )

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = CompanyNoteService.create(
            user=self.request.user,
            context=self._get_context(None),
            validated_data=serializer.validated_data,
        )

        return Response(self.get_serializer(instance).data)

    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = CompanyNoteService.update(
            user=self.request.user,
            context=self._get_context(self.kwargs["id"]),
            validated_data=serializer.validated_data,
        )

        return Response(self.get_serializer(instance).data)

    def partial_update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        instance = CompanyNoteService.update(
            user=self.request.user,
            context=self._get_context(self.kwargs["id"]),
            validated_data=serializer.validated_data,
        )

        return Response(self.get_serializer(instance).data)

    def destroy(self, request, *args, **kwargs):

        CompanyNoteService.remove(
            user=self.request.user,
            context=self._get_context(self.kwargs["id"]),
        )

        return Response(status=status.HTTP_200_OK)

    def _get_context(self, company_note_id: int | None) -> CompanyChildContext:

        return CompanyChildContext(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            id=company_note_id
        )

    def _get_queryset_filters(self) -> CompanyNoteSelector.QueryFilter:

        return CompanyNoteSelector.QueryFilter(
            workspace_id=self.request.query_params.get("workspace_id"),
            company_id=self.request.query_params.get("company_id"),
        )


class CompanyEmailViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    # URL Path:
    # company-emails/{id}

    serializer_class = CompanyEmailSerializer
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "id"

    def get_queryset(self):

        return CompanyEmailSelector.list(
            user=self.request.user,
            filters=self._get_queryset_filters()
        )

    def _get_queryset_filters(self) -> CompanyEmailSelector.QueryFilter:

        return CompanyEmailSelector.QueryFilter(
            workspace_id=self.request.query_params.get("workspace_id"),
            company_id=self.request.query_params.get("company_id"),
        )


class NestedCompanyEmailViewSet(ModelViewSet):

    # URL Path:
    # workspaces/workspace_id/companies/company_id/company-emails/{id}

    permission_classes = [IsAuthenticated]
    serializer_class = CompanyEmailSerializer

    lookup_url_kwarg = "id"

    def get_queryset(self):

        return CompanyEmailSelector.list(
            user=self.request.user,
            filters=self._get_queryset_filters()
        )

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = CompanyEmailService.create(
            user=self.request.user,
            context=self._get_context(None),
            validated_data=serializer.validated_data,
        )

        return Response(CompanyEmailSerializer(instance).data)

    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = CompanyEmailService.update(
            user=self.request.user,
            context=self._get_context(self.kwargs["id"]),
            validated_data=serializer.validated_data,
        )

        return Response(CompanyEmailSerializer(instance).data)

    def partial_update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        instance = CompanyEmailService.update(
            user=self.request.user,
            context=self._get_context(self.kwargs["id"]),
            validated_data=serializer.validated_data,
        )

        return Response(CompanyEmailSerializer(instance).data)

    def destroy(self, request, *args, **kwargs):

        CompanyEmailService.remove(
            user=request.user,
            context=self._get_context(self.kwargs["id"]),
        )

        return Response(status=status.HTTP_200_OK)

    def _get_context(self, company_note_id: int | None) -> CompanyChildContext:

        return CompanyChildContext(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            id=company_note_id
        )

    def _get_queryset_filters(self) -> CompanyEmailSelector.QueryFilter:

        return CompanyEmailSelector.QueryFilter(
            workspace_id=self.request.query_params.get("workspace_id"),
            company_id=self.request.query_params.get("company_id"),
        )


class JobBenefitViewSet(ModelViewSet):

    # URL Path:
    # job-benefits/{id}

    permission_classes = [IsAuthenticated]
    serializer_class = JobBenefitSerializer

    lookup_url_kwarg = "id"

    def get_queryset(self):

        return JobBenefitSelector.list()

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = JobBenefitService.create(
            user=self.request.user,
            validated_data=serializer.validated_data,
        )

        return Response(self.get_serializer(instance).data)

    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = JobBenefitService.update(
            user=self.request.user,
            job_benefit_id=self.kwargs["id"],
            validated_data=serializer.validated_data,
        )

        return Response(self.get_serializer(instance).data)

    def partial_update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        instance = JobBenefitService.update(
            user=self.request.user,
            job_benefit_id=self.kwargs["id"],
            validated_data=serializer.validated_data,
        )

        return Response(self.get_serializer(instance).data)

    def destroy(self, request, *args, **kwargs):

        JobBenefitService.remove(user=request.user, job_benefit_id=self.kwargs["id"])

        return Response(status=status.HTTP_200_OK)


class JobTaskViewSet(ModelViewSet):

    # URL Path:
    # job-tasks/{id}

    permission_classes = [IsAuthenticated]
    serializer_class = JobTaskSerializer

    lookup_url_kwarg = "id"

    def get_queryset(self):

        return JobTaskSelector.list()

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = JobTaskService.create(
            user=self.request.user,
            validated_data=serializer.validated_data,
        )

        return Response(self.get_serializer(instance).data)

    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = JobTaskService.update(
            user=self.request.user,
            job_task_id=self.kwargs["id"],
            validated_data=serializer.validated_data,
        )

        return Response(self.get_serializer(instance).data)

    def partial_update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        instance = JobTaskService.update(
            user=self.request.user,
            job_task_id=self.kwargs["id"],
            validated_data=serializer.validated_data,
        )

        return Response(self.get_serializer(instance).data)

    def destroy(self, request, *args, **kwargs):

        JobTaskService.remove(user=request.user, job_task_id=self.kwargs["id"])

        return Response(status=status.HTTP_200_OK)


class JobRequirementViewSet(ModelViewSet):

    # URL Path:
    # job-requirements/{id}

    permission_classes = [IsAuthenticated]
    serializer_class = JobRequirementSerializer

    lookup_url_kwarg = "id"

    def get_queryset(self):

        return JobRequirementSelector.list()

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = JobRequirementService.create(
            user=self.request.user,
            validated_data=serializer.validated_data,
        )

        return Response(self.get_serializer(instance).data)

    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = JobRequirementService.update(
            user=self.request.user,
            job_requirement_id=self.kwargs["id"],
            validated_data=serializer.validated_data,
        )

        return Response(self.get_serializer(instance).data)

    def partial_update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        instance = JobRequirementService.update(
            user=self.request.user,
            job_requirement_id=self.kwargs["id"],
            validated_data=serializer.validated_data,
        )

        return Response(self.get_serializer(instance).data)

    def destroy(self, request, *args, **kwargs):

        JobRequirementService.remove(
            user=request.user, job_requirement_id=self.kwargs["id"]
        )

        return Response(status=status.HTTP_200_OK)


class JobPositionViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):

    # URL Path:
    # job-positions/{id}

    serializer_class = JobPositionSerializer
    permission_classes = [IsAuthenticated]

    lookup_url_kwarg = "id"

    def get_queryset(self):

        filters = JobPositionSelector.QueryFilter(
            workspace_id=self.request.query_params.get("workspace_id"),
            company_id=self.request.query_params.get("company_id"),
        )

        return JobPositionSelector.list(
            user=self.request.user,
            filters=filters
        )


class NestedJobPositionViewSet(ModelViewSet):

    # URL Path:
    # workspaces/workspace_id/companies/company_id/job-positions/{id}

    permission_classes = [IsAuthenticated]
    serializer_class = JobPositionSerializer

    lookup_url_kwarg = "id"

    def get_queryset(self):

        return JobPositionSelector.list(
            user=self.request.user,
            filters=self._get_queryset_filters()
        )

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = JobPositionService.create(
            user=self.request.user,
            context=self._get_context(None),
            validated_data=serializer.validated_data,
        )

        return Response(self.get_serializer(instance).data)

    def update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        context = self._get_context(self.kwargs["id"])

        instance = JobPositionService.update(
            user=request.user,
            context=context,
            validated_data=serializer.validated_data,
        )

        return Response(self.get_serializer(instance).data)

    def partial_update(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        context = self._get_context(self.kwargs["id"])

        instance = JobPositionService.update(
            user=request.user,
            context=context,
            validated_data=serializer.validated_data,
        )

        return Response(self.get_serializer(instance).data)

    def destroy(self, request, *args, **kwargs):

        JobPositionService.remove(
            user=request.user,
            context=self._get_context(self.kwargs["id"]),
        )

        return Response(status=status.HTTP_200_OK)

    def _get_context(self, job_position_id: int | None) -> CompanyChildContext:

        return CompanyChildContext(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            id=job_position_id
        )

    def _get_queryset_filters(self):

        return JobPositionSelector.QueryFilter(
            workspace_id=self.kwargs["workspace_id"],
            company_id=self.kwargs["company_id"],
            id=self.kwargs.get("id"),
        )
