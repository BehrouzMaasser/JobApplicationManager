"""
Base class for write services.

Services coordinate write use-cases, enforce business rules, delegate
model validation, and persist aggregate changes.

Concrete services should implement only domain-specific behavior while
reusing the generic write workflow provided by this base class.
"""

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from django.core.exceptions import ValidationError
from django.db import models, transaction

# Models
from apps.accounts.models import User
from apps.core.common.contexts.contexts import BaseContext
from apps.core.common.selectors.base_selector import BaseSelector

# Exceptions
from apps.core.exceptions.exceptions import (
    AppError,
    BusinessRuleViolationError,
    DomainInvariantViolationError,
    InfrastructureViolationError,
)

DjangoModel = TypeVar("DjangoModel", bound=models.Model)


class BaseService(ABC, Generic[DjangoModel]):
    """
    Base implementation of the service contract.

    A service encapsulates a write use-case of a single aggregate root.
    It coordinates business validation, delegates model validation to
    ``Model.full_clean()``, persists changes, and translates unexpected
    infrastructure failures into domain-level exceptions.
    """

    _REQUIRED_CONFIG = (
        "MODEL",
        "SELECTOR",
        "CREATE_FIELDS",
        "SCALAR_UPDATABLE_FIELDS",
        "M2M_UPDATABLE_FIELDS",
        "REQUIRED_M2M_FIELDS",
        "NON_EMPTY_M2M_FIELDS",
        "M2M_OWNER_FIELD_MAP",
    )

    #
    # Service configuration
    #

    MODEL: type[DjangoModel] = None
    SELECTOR: type[BaseSelector] = None

    CREATE_FIELDS: tuple[str, ...] = None
    SCALAR_UPDATABLE_FIELDS: tuple[str, ...] = None
    M2M_UPDATABLE_FIELDS: tuple[str, ...] = None
    REQUIRED_M2M_FIELDS: tuple[str, ...] = None
    NON_EMPTY_M2M_FIELDS: tuple[str, ...] = None
    M2M_OWNER_FIELD_MAP: dict[str, str] = None

    def __init_subclass__(cls):
        super().__init_subclass__()
        cls._validate_configuration()

    #
    # Public API
    #

    @classmethod
    @transaction.atomic
    def create(
        cls,
        user: User,
        context: BaseContext,
        validated_data: dict[str, Any],
    ) -> DjangoModel:
        """
        Create and persist a new aggregate instance.
        """

        try:
            model_data = {**validated_data}

            create_dependencies = cls._resolve_create_dependencies(
                user=user,
                context=context,
            )

            if create_dependencies:
                model_data.update(create_dependencies)

            instance = cls._build_instance(**model_data)

            cls._create_validate(
                user=user,
                instance=instance,
                validated_data=validated_data,
            )

            cls._create_pre_save(
                user=user,
                validated_data=validated_data,
            )

            cls._save(instance)

            cls._create_post_save(
                instance=instance,
                validated_data=validated_data,
            )

            return instance

        except (AppError, ValidationError):
            raise

        except Exception as exc:
            raise InfrastructureViolationError(
                f"Unexpected error while creating {cls.MODEL.__name__}."
            ) from exc

    @classmethod
    @transaction.atomic
    def update(
        cls,
        user: User,
        context: BaseContext,
        validated_data: dict[str, Any],
    ) -> DjangoModel:
        """
        Update and persist an existing aggregate instance.
        """

        try:
            instance = cls._resolve_instance(
                user=user,
                context=context,
            )

            cls._update_validate(
                user=user,
                instance=instance,
                validated_data=validated_data,
            )

            cls._update_pre_save(
                user=user,
                validated_data=validated_data,
            )

            cls._apply_scalar_updates(
                instance=instance,
                validated_data=validated_data,
            )

            cls._save(instance)

            cls._update_post_save(
                instance=instance,
                validated_data=validated_data,
            )

            return instance

        except (AppError, ValidationError):
            raise

        except Exception as exc:
            raise InfrastructureViolationError(
                f"Unexpected error while updating {cls.MODEL.__name__}."
            ) from exc

    @classmethod
    @transaction.atomic
    def remove(
        cls,
        *,
        user: User,
        context: BaseContext,
    ) -> None:
        """
        Delete an existing aggregate instance.
        """

        try:
            instance = cls._resolve_instance(
                user=user,
                context=context,
            )

            instance.delete()

        except (AppError, ValidationError):
            raise

        except Exception as exc:
            raise InfrastructureViolationError(
                f"Unexpected error while removing {cls.MODEL.__name__}."
            ) from exc

    #
    # Workflow hooks
    #

    @classmethod
    def _resolve_create_dependencies(
        cls,
        user: User,
        context: BaseContext,
    ) -> dict[str, Any]:
        """
        Resolve additional model fields required during creation.

        The returned mapping is merged into the arguments passed to
        `_build_instance()`.

        The default implementation returns an empty dictionary.
        """

        return {}

    @classmethod
    def _resolve_instance(
        cls,
        *,
        user: User,
        context: BaseContext,
    ) -> DjangoModel:
        """
        Resolve the aggregate being modified.

        The resolved instance is validated against the supplied context
        before being returned.
        """

        instance = cls.SELECTOR.get(
            user=user,
            obj_id=context.id,
        )

        cls._validate_resolved_instance(
            instance=instance,
            context=context,
        )

        return instance

    @classmethod
    @abstractmethod
    def _validate_resolved_instance(
        cls,
        *,
        instance: DjangoModel,
        context: BaseContext,
    ) -> None:
        """
        Validate that the resolved aggregate matches the supplied context.

        Override this hook to enforce aggregate hierarchy constraints and
        other domain invariants.

        The default implementation performs no validation.
        """
        ...

    @classmethod
    def _create_validate(
        cls,
        *,
        user: User,
        instance: DjangoModel,
        validated_data: dict[str, Any],
    ) -> None:
        """
        Execute business validations specific to the create operation.

        `instance` exists only in memory and has not yet been validated or
        persisted.
        """

        pass

    @classmethod
    def _update_validate(
        cls,
        *,
        user: User,
        instance: DjangoModel,
        validated_data: dict[str, Any],
    ) -> None:
        """
        Execute business validations specific to the update operation.

        `instance` is the persisted model before any scalar updates have
        been applied.
        """

        pass

    @classmethod
    def _create_pre_save(
        cls,
        *,
        user: User,
        validated_data: dict[str, Any],
    ) -> None:
        """
        Execute common pre-save validations for create operations.

        The default implementation validates ownership and required
        many-to-many fields.
        """

        cls._validate_m2m_ownership(
            user=user,
            validated_data=validated_data,
        )

        cls._validate_required_m2m_fields_exist(
            validated_data=validated_data,
        )

    @classmethod
    def _update_pre_save(
        cls,
        *,
        user: User,
        validated_data: dict[str, Any],
    ) -> None:
        """
        Execute common pre-save validations for update operations.

        The default implementation validates ownership of supplied
        many-to-many relations.
        """

        cls._validate_m2m_ownership(
            user=user,
            validated_data=validated_data,
        )

    @classmethod
    def _create_post_save(
        cls,
        instance: DjangoModel,
        validated_data: dict[str, Any],
    ) -> None:
        """
        Execute common post-save operations for newly created instances.

        `instance` has already been validated and persisted.
        """

        cls._add_m2m_fields(
            instance=instance,
            validated_data=validated_data,
        )

        cls._m2m_non_empty_validation(instance)

    @classmethod
    def _update_post_save(
        cls,
        instance: DjangoModel,
        validated_data: dict[str, Any],
    ) -> None:
        """
        Execute common post-save operations for updated instances.

        `instance` has already been validated and persisted.
        """

        cls._apply_m2m_updates(
            instance=instance,
            validated_data=validated_data,
        )

        cls._m2m_non_empty_validation(instance)

        #
        # Validation helpers
        #

    @classmethod
    def _m2m_non_empty_validation(
            cls,
            instance: DjangoModel,
    ) -> None:
        """
        Validate that configured many-to-many relations are not empty.

        `instance` must already be persisted because many-to-many
        relationships are queried through the database.

        Raises:
            BusinessRuleViolationError:
                If any configured relation is empty.
        """

        empty_required_fields = []

        for field in cls.NON_EMPTY_M2M_FIELDS:
            if not getattr(instance, field).exists():
                empty_required_fields.append(field)

        if empty_required_fields:
            raise BusinessRuleViolationError(
                fields=empty_required_fields,
                messages=[
                    "Should not be empty"
                    for _ in empty_required_fields
                ],
            )

    @classmethod
    def _validate_required_m2m_fields_exist(
            cls,
            *,
            validated_data: dict[str, Any],
    ) -> None:
        """
        Validate that all configured required many-to-many fields were
        supplied during creation.

        This validates field presence only. Non-empty validation occurs
        after persistence.
        """

        missing = [
            field
            for field in cls.REQUIRED_M2M_FIELDS
            if field not in validated_data
        ]

        if missing:
            raise BusinessRuleViolationError(
                fields=missing,
                messages=[
                    "This field is required."
                    for _ in missing
                ],
            )

    @classmethod
    def _validate_m2m_ownership(
            cls,
            *,
            user: User,
            validated_data: dict[str, Any],
    ) -> None:
        """
        Validate ownership of supplied many-to-many related objects.

        Only fields present in `validated_data` are validated.

        Related objects that do not expose the configured ownership
        attribute are ignored because ownership cannot be determined.
        """

        invalid_fields_with_ids: dict[str, list[Any]] = {}

        for field_name, owner_field in cls.M2M_OWNER_FIELD_MAP.items():

            if field_name not in validated_data:
                continue

            for related_object in validated_data[field_name]:

                try:
                    if getattr(related_object, owner_field) != user:
                        invalid_fields_with_ids.setdefault(
                            field_name,
                            [],
                        ).append(related_object.pk)

                except AttributeError:
                    continue

        if invalid_fields_with_ids:
            raise DomainInvariantViolationError(
                message="; ".join(
                    (
                        f"Current user does not own "
                        f"{field}: {ids}"
                    )
                    for field, ids in invalid_fields_with_ids.items()
                )
            )

    #
    # Field helpers
    #

    @classmethod
    def _apply_scalar_updates(
            cls,
            *,
            instance: DjangoModel,
            validated_data: dict[str, Any],
    ) -> None:
        """
        Apply scalar field updates in memory.

        Validation and persistence occur later through `_save()`.
        """

        for field in cls.SCALAR_UPDATABLE_FIELDS:

            if field in validated_data:
                setattr(
                    instance,
                    field,
                    validated_data[field],
                )

    @classmethod
    def _add_m2m_fields(
            cls,
            *,
            instance: DjangoModel,
            validated_data: dict[str, Any],
    ) -> None:
        """
        Add many-to-many relations to a newly created instance.

        `instance` must already be persisted because many-to-many
        relationships require a primary key.
        """

        for field in cls.M2M_UPDATABLE_FIELDS:

            if field in validated_data:
                getattr(
                    instance,
                    field,
                ).add(*validated_data[field])

    @classmethod
    def _apply_m2m_updates(
            cls,
            *,
            instance: DjangoModel,
            validated_data: dict[str, Any],
    ) -> None:
        """
        Synchronize many-to-many relations of an existing instance.

        Relations are replaced only for fields supplied in
        `validated_data`.
        """

        for field in cls.M2M_UPDATABLE_FIELDS:

            if field in validated_data:
                getattr(
                    instance,
                    field,
                ).set(validated_data[field])

    #
    # Persistence helpers
    #

    @classmethod
    def _save(
            cls,
            instance: DjangoModel,
    ) -> None:
        """
        Validate and persist the supplied model instance.

        `Model.full_clean()` is executed before saving.

        After this method returns successfully, `instance` is guaranteed
        to be synchronized with the database.
        """

        instance.full_clean()
        instance.save()

    #
    # Factory helper
    #

    @classmethod
    def _build_instance(
            cls,
            **kwargs,
    ) -> DjangoModel:
        """
        Construct a new model instance from the configured create fields.

        The returned instance exists only in memory and has not yet been
        validated or persisted.
        """

        return cls.MODEL(
            **{
                field: kwargs.get(field)
                for field in cls.CREATE_FIELDS
            }
        )

    #
    # Configuration validation
    #

    @classmethod
    def _validate_configuration(cls) -> None:
        """
        Validate the concrete service configuration.

        This method is executed automatically when a subclass is created.
        It verifies that all required configuration attributes exist and
        are internally consistent.
        """

        if cls is BaseService:
            return

        #
        # Required attributes
        #

        for attr in cls._REQUIRED_CONFIG:
            if getattr(cls, attr, None) is None:
                raise TypeError(
                    f"{cls.__name__} must define {attr}"
                )

        #
        # Required types
        #

        if not issubclass(cls.MODEL, models.Model):
            raise TypeError(
                f"{cls.__name__}.MODEL must inherit from "
                "django.db.models.Model"
            )

        if not issubclass(cls.SELECTOR, BaseSelector):
            raise TypeError(
                f"{cls.__name__}.SELECTOR must inherit from BaseSelector"
            )

        #
        # Tuple configuration
        #

        cls._validate_tuple_of_strings(
            "CREATE_FIELDS",
            cls.CREATE_FIELDS,
        )

        cls._validate_tuple_of_strings(
            "SCALAR_UPDATABLE_FIELDS",
            cls.SCALAR_UPDATABLE_FIELDS,
        )

        cls._validate_tuple_of_strings(
            "M2M_UPDATABLE_FIELDS",
            cls.M2M_UPDATABLE_FIELDS,
        )

        cls._validate_tuple_of_strings(
            "REQUIRED_M2M_FIELDS",
            cls.REQUIRED_M2M_FIELDS,
        )

        cls._validate_tuple_of_strings(
            "NON_EMPTY_M2M_FIELDS",
            cls.NON_EMPTY_M2M_FIELDS,
        )

        cls._validate_owner_field_map()

        #
        # Cross-configuration validation
        #

        overlap = (
            set(cls.SCALAR_UPDATABLE_FIELDS)
            & set(cls.M2M_UPDATABLE_FIELDS)
        )

        if overlap:
            raise TypeError(
                "Fields cannot be both scalar and many-to-many: "
                f"{sorted(overlap)}"
            )

        cls._validate_model_fields()

    @classmethod
    def _validate_model_fields(cls) -> None:
        """
        Validate that every configured field exists on the configured
        model.
        """

        model_fields = {
            field.name
            for field in cls.MODEL._meta.get_fields()
            if hasattr(field, "name")
        }

        configured_fields = (
            set(cls.CREATE_FIELDS)
            | set(cls.SCALAR_UPDATABLE_FIELDS)
            | set(cls.M2M_UPDATABLE_FIELDS)
            | set(cls.REQUIRED_M2M_FIELDS)
            | set(cls.NON_EMPTY_M2M_FIELDS)
            | set(cls.M2M_OWNER_FIELD_MAP.keys())
        )

        unknown = configured_fields - model_fields

        if unknown:
            raise TypeError(
                f"{cls.__name__} references unknown model field(s): "
                f"{sorted(unknown)}"
            )

    @classmethod
    def _validate_tuple_of_strings(
        cls,
        name: str,
        value: tuple[str, ...],
    ) -> None:
        """
        Validate that a configuration value is a tuple of unique field
        names.
        """

        if not isinstance(value, tuple):
            raise TypeError(
                f"{name} must be an instance of tuple"
            )

        if len(value) != len(set(value)):
            raise TypeError(
                f"{name} must not contain duplicate field names"
            )

        for field in value:

            if not isinstance(field, str):
                raise TypeError(
                    f"{name} must contain only field names (str), "
                    f"got {type(field).__name__}"
                )

    @classmethod
    def _validate_owner_field_map(cls) -> None:
        """
        Validate the `M2M_OWNER_FIELD_MAP` configuration.
        """

        value = cls.M2M_OWNER_FIELD_MAP

        if not isinstance(value, dict):
            raise TypeError(
                "M2M_OWNER_FIELD_MAP must be an instance of dict"
            )

        for field, owner in value.items():

            if not isinstance(field, str):
                raise TypeError(
                    "M2M_OWNER_FIELD_MAP keys must be field names (str)"
                )

            if not isinstance(owner, str):
                raise TypeError(
                    "M2M_OWNER_FIELD_MAP values must be attribute "
                    "paths (str)"
                )
