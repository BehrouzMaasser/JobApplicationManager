import pytest


from apps.core.common.services.base_service import BaseService
from apps.core.exceptions.exceptions import (
    BusinessRuleViolationError,
    InfrastructureViolationError,
    ResourceNotFoundError,
)

from apps.testing.models import DummyItem
from apps.testing.selectors import DummyItemSelector


class ExceptionTestService(BaseService):

    MODEL = DummyItem
    SELECTOR = DummyItemSelector

    CREATE_FIELDS = (
        "owner",
        "name",
    )

    SCALAR_UPDATABLE_FIELDS = (
        "name",
    )

    M2M_UPDATABLE_FIELDS = ()

    REQUIRED_M2M_FIELDS = ()

    NON_EMPTY_M2M_FIELDS = ()

    M2M_OWNER_FIELD_MAP = {}

    @classmethod
    def _validate_resolved_instance(cls, **kwargs):
        pass


# ---------------------------------------------------------------------------
# create()
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_create_propagates_app_errors(user1):

    expected = BusinessRuleViolationError(
        messages=["Invalid"],
        fields=["name"],
    )

    class Service(ExceptionTestService):

        @classmethod
        def _resolve_create_dependencies(cls, user, context):
            raise expected

    with pytest.raises(BusinessRuleViolationError) as exc:

        Service.create(
            user=user1,
            context=None,
            validated_data={
                "name": "Invalid",
            },
        )

    assert exc.value is expected


@pytest.mark.django_db
def test_create_wraps_unexpected_errors(user1):

    class Service(ExceptionTestService):

        @classmethod
        def _resolve_create_dependencies(cls, user, context):
            raise ValueError("something broke")

    with pytest.raises(
            InfrastructureViolationError
    ) as exc:

        Service.create(
            user=user1,
            context=None,
            validated_data={
                "name": "Broken",
            },
        )

    assert isinstance(exc.value.__cause__, ValueError)


@pytest.mark.django_db
def test_create_preserves_original_exception(user1):

    original = ValueError("database exploded")

    class Service(ExceptionTestService):

        @classmethod
        def _resolve_create_dependencies(cls, user, context):
            raise original

    with pytest.raises(
            InfrastructureViolationError
    ) as exc:

        Service.create(
            user=user1,
            context=None,
            validated_data={
                "name": "Broken",
            },
        )

    assert exc.value.__cause__ is original


@pytest.mark.django_db
def test_create_rolls_back_when_post_save_fails(user1):

    class Service(ExceptionTestService):

        @classmethod
        def _resolve_create_dependencies(cls, user, context):
            raise {"owner": user}

        @classmethod
        def _create_post_save(cls, instance, validated_data):
            raise RuntimeError("post save failure")

    with pytest.raises(
            InfrastructureViolationError
    ):

        Service.create(
            user=user1,
            context=None,
            validated_data={
                "name": "Should rollback",
            },
        )

    assert not DummyItem.objects.filter(
        name="Should rollback"
    ).exists()


@pytest.mark.django_db
def test_create_does_not_wrap_app_errors(user1):

    class Service(ExceptionTestService):

        @classmethod
        def _create_validate(
                cls,
                *,
                user,
                instance,
                validated_data
        ):

            raise BusinessRuleViolationError(
                messages=["invalid"],
                fields=["name"],
            )

    with pytest.raises(
            BusinessRuleViolationError
    ):

        Service.create(
            user=user1,
            context=None,
            validated_data={
                "name": "Invalid",
            },
        )


# ---------------------------------------------------------------------------
# update()
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_update_propagates_selector_errors():

    expected = ResourceNotFoundError(
        resource="DummyItem"
    )

    class Service(ExceptionTestService):

        @classmethod
        def _resolve_instance(
                cls,
                *,
                user,
                context
        ):

            raise expected

    with pytest.raises(
            ResourceNotFoundError
    ) as exc:

        Service.update(
            user=None,
            context=None,
            validated_data={
                "name": "Updated",
            },
        )

    assert exc.value is expected


@pytest.mark.django_db
def test_update_wraps_unexpected_errors(item1):

    class Service(ExceptionTestService):

        @classmethod
        def _update_validate(
                cls,
                *,
                user,
                instance,
                validated_data
        ):

            raise ValueError("update failed")

        @classmethod
        def _resolve_instance(
                cls,
                *,
                user,
                context
        ):

            return item1

    with pytest.raises(
            InfrastructureViolationError
    ) as exc:

        Service.update(
            user=item1.owner,
            context=None,
            validated_data={
                "name": "Updated",
            },
        )

    assert isinstance(exc.value.__cause__, ValueError)


# ---------------------------------------------------------------------------
# remove()
# ---------------------------------------------------------------------------


@pytest.mark.django_db
def test_remove_wraps_unexpected_errors(item1):

    class Service(ExceptionTestService):

        @classmethod
        def _resolve_instance(
                cls,
                *,
                user,
                context
        ):

            raise RuntimeError("delete failed")

    with pytest.raises(
            InfrastructureViolationError
    ) as exc:

        Service.remove(
            user=item1.owner,
            context=None,
        )

    assert isinstance(exc.value.__cause__, RuntimeError)


@pytest.mark.django_db
def test_remove_propagates_app_errors():

    expected = ResourceNotFoundError(
        resource="DummyItem"
    )

    class Service(ExceptionTestService):

        @classmethod
        def _resolve_instance(
                cls,
                *,
                user,
                context
        ):

            raise expected

    with pytest.raises(
            ResourceNotFoundError
    ) as exc:

        Service.remove(
            user=None,
            context=None,
        )

    assert exc.value is expected
