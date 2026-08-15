"""
Reusable Django REST Framework ViewSet base classes.

These classes provide a thin HTTP layer for applications that separate
read operations into selectors and write operations into services.

Responsibilities:
    - Dispatch read requests to selector classes.
    - Dispatch write requests to service classes.
    - Validate request payloads using DRF serializers.
    - Handle common CRUD response generation.

Subclasses are expected to provide the required selector, service,
serializer, and lookup configuration for each resource.
"""

from abc import ABC, abstractmethod
from typing import Any

from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated


from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer


class BaseReadOnlyViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
    ABC,
):
    """
    Base ViewSet for read-only resources backed by selector classes.

    Provides standard ``list`` and ``retrieve`` endpoints while delegating all
    read operations to the configured selector.

    Subclasses must configure:

        - ``selector_class``
        - ``lookup_url_kwarg``

    and implement ``get_queryset()``.
    """

    READ_ACTIONS = ("list", "retrieve")
    WRITE_ACTIONS = ("create", "update", "partial_update")

    permission_classes = [IsAuthenticated]

    selector_class: type | None = None

    lookup_url_kwarg: str | None = None

    @property
    def selector(self):
        """
        Return the configured selector class.

        Raises:
            ImproperlyConfigured:
                If ``selector_class`` has not been defined.
        """

        return self._require_attr("selector_class")

    @property
    def lookup_url(self) -> str | ImproperlyConfigured:
        """
        Return the URL keyword argument used to identify a resource.

        Raises:
            ImproperlyConfigured:
                If ``lookup_url_kwarg`` has not been defined.
        """

        return self._require_attr("lookup_url_kwarg")

    def get_object(self):
        """
        Retrieve a single resource using the configured selector.

        The lookup value is extracted from the request URL and passed to the
        selector together with the authenticated user.

        Object-level permissions are evaluated before the resource is returned.

        Returns:
            The selected domain object.
        """

        obj = self.selector.get(
            user=self.request.user,
            obj_id=self.kwargs[self.lookup_url],
        )

        self.check_object_permissions(self.request, obj)

        return obj

    @abstractmethod
    def get_queryset(self) -> QuerySet[Any]:
        """
        Return the queryset backing the list endpoint.

        Subclasses are responsible for delegating the query to the appropriate
        selector and applying any required filtering.
        """
        ...

    def _require_attr(self, name) -> Any | ImproperlyConfigured:
        """
        Return the value of a required class attribute.

        Args:
            name:
                Name of the attribute to retrieve.

        Raises:
            ImproperlyConfigured:
                If the requested attribute has not been configured.

        Returns:
            The configured attribute value.
        """

        value = getattr(self, name)
        if value is None:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} must define {name}."
            )
        return value


class BaseServiceViewSet(BaseReadOnlyViewSet, ABC):
    """
    Base ViewSet for resources that support write operations through services.

    Extends ``BaseReadOnlyViewSet`` by providing common implementations of
    ``create()``, ``update()``, ``partial_update()`` and ``destroy()``.

    Business logic is delegated to the configured service class, while request
    validation and response serialization are handled using separate write and
    read serializers.

    Subclasses must configure:

        - ``selector_class``
        - ``selector_lookup_field``
        - ``lookup_url_kwarg``
        - ``service_class``
        - ``read_serializer_class``
        - ``write_serializer_class``

    and implement:

        - ``get_queryset()``
        - ``service_create()``
        - ``service_update()``
        - ``service_destroy()``
    """

    service_class: type | None = None

    read_serializer_class: type[Serializer] | None = None
    write_serializer_class: type[Serializer] | None = None

    @property
    def service(self):
        """
        Return the configured service class.

        Raises:
            ImproperlyConfigured:
                If ``service_class`` has not been defined.
        """

        return self._require_attr("service_class")

    @property
    def read_serializer(self) -> type[Serializer] | ImproperlyConfigured:
        """
        Return the serializer class used for response serialization.

        Raises:
            ImproperlyConfigured:
                If ``read_serializer_class`` has not been defined.
        """

        return self._require_attr("read_serializer_class")

    @property
    def write_serializer(self) -> type[Serializer] | ImproperlyConfigured:
        """
        Return the serializer class used for request validation.

        Raises:
            ImproperlyConfigured:
                If ``write_serializer_class`` has not been defined.
        """

        return self._require_attr("write_serializer_class")

    def get_serializer_class(self) -> type[Serializer] | ImproperlyConfigured:
        """
        Return the serializer class for the current action.

        Read actions use the configured read serializer, while write actions use
        the configured write serializer.

        Raises:
            ImproperlyConfigured:
                If the current action is unsupported.
            AssertionError:
                If the read_serializer_class or write_serializer_class has not been
                 defined.
        """

        assert self.read_serializer_class or self.write_serializer_class

        if self.action in self.READ_ACTIONS:
            return self.read_serializer
        if self.action in self.WRITE_ACTIONS:
            return self.write_serializer

        raise ImproperlyConfigured(f"Unsupported action: {self.action}.")

    @abstractmethod
    def service_create(self, validated_data: dict[str, Any]):
        """
        Create a new resource.

        Implemented by subclasses to invoke the appropriate service method.
        """
        ...

    @abstractmethod
    def service_destroy(self):
        """
        Delete an existing resource.

        Implemented by subclasses to invoke the appropriate service method.
        """
        ...

    @abstractmethod
    def service_update(self, validated_data: dict[str, Any]):
        """
        Update an existing resource.

        Implemented by subclasses to invoke the appropriate service method.
        """
        ...

    def create(self, request, *args, **kwargs) -> Response:
        """
        Create a new resource.

        Validates the incoming payload, delegates creation to the configured
        service, and returns the created resource serialized with the read
        serializer.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.service_create(
            validated_data=serializer.validated_data,
        )

        return Response(
            self.read_serializer(
                instance=instance, context=self.get_serializer_context()
            ).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs) -> Response:
        """
        Replace an existing resource.
        """

        return self._update(request, partial=False)

    def partial_update(self, request, *args, **kwargs) -> Response:
        """
        Partially update an existing resource.
        """

        return self._update(request, partial=True)

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Delete an existing resource.
        """

        self.service_destroy()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def _update(self, request, *, partial) -> Response:
        """
        Validate and execute an update operation.

        Args:
            request:
                Incoming HTTP request.

            partial:
                Whether the update should allow partial input.

        Returns:
            A response containing the updated resource.
        """

        serializer = self.get_serializer(data=request.data, partial=partial)

        serializer.is_valid(raise_exception=True)

        instance = self.service_update(validated_data=serializer.validated_data)

        return Response(
            self.read_serializer(
                instance=instance, context=self.get_serializer_context()
            ).data
        )


class BaseContextServiceViewSet(BaseServiceViewSet, ABC):
    """
    Base ViewSet for services operating on explicit context objects.

    Provides implementations of create, update and destroy operations for
    services that accept context objects instead of primitive lookup values.

    Subclasses must configure:

        - ``selector_class``
        - ``selector_lookup_field``
        - ``lookup_url_kwarg``
        - ``service_class``
        - ``read_serializer_class``
        - ``write_serializer_class``

    and implement:

        - ``get_queryset()``
        - ``get_create_context()``
        - ``get_update_context()``
    """

    @abstractmethod
    def get_create_context(self):
        """
        Return the context required for resource creation.
        """
        ...

    @abstractmethod
    def get_update_context(self):
        """
        Return the context required for update and delete operations.
        """
        ...

    def service_create(self, validated_data: dict[str, Any]):
        """
        Delegate resource creation to the configured service using a creation
        context.
        """

        return self.service.create(
            user=self.request.user,
            context=self.get_create_context(),
            validated_data=validated_data,
        )

    def service_update(self, validated_data: dict[str, Any]):
        """
        Delegate resource updates to the configured service using an update
        context.
        """

        return self.service.update(
            user=self.request.user,
            context=self.get_update_context(),
            validated_data=validated_data,
        )

    def service_destroy(self):
        """
        Delegate resource deletion to the configured service using an update
        context.
        """

        self.service.remove(
            user=self.request.user,
            context=self.get_update_context(),
        )
