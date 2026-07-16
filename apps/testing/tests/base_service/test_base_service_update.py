import pytest

from apps.core.common.services.base_service import BaseService
from apps.testing.models import DummyItem
from apps.testing.selectors import DummyItemSelector


class DummyUpdateService(BaseService):

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

    calls = []

    @classmethod
    def _resolve_instance(cls, *, user, context):
        cls.calls.append("_resolve_instance")
        return context

    @classmethod
    def _update_validate(cls, **kwargs):
        cls.calls.append("_update_validate")

    @classmethod
    def _pre_save(cls, **kwargs):
        cls.calls.append("_pre_save")

    @classmethod
    def _apply_scalar_updates(cls, **kwargs):
        cls.calls.append("_apply_scalar_updates")

    @classmethod
    def _save(cls, instance):
        cls.calls.append("_save")

    @classmethod
    def _update_post_save(cls, instance, validated_data):
        cls.calls.append("_update_post_save")

    @classmethod
    def _validate_resolved_instance(cls, **kwargs):
        pass


@pytest.mark.django_db
def test_update_executes_hooks_in_contract_order(item1):

    DummyUpdateService.calls = []

    DummyUpdateService.update(
        user=item1.owner,
        context=item1,
        validated_data={
            "name": "Updated",
        },
    )

    assert DummyUpdateService.calls == [
        "_resolve_instance",
        "_update_validate",
        "_pre_save",
        "_apply_scalar_updates",
        "_save",
        "_update_post_save",
    ]


@pytest.mark.django_db
def test_update_calls_resolve_instance_once(item1):

    calls = 0

    class Service(DummyUpdateService):

        @classmethod
        def _resolve_instance(cls, *, user, context):
            nonlocal calls
            calls += 1
            return context

    Service.update(
        user=item1.owner,
        context=item1,
        validated_data={},
    )

    assert calls == 1


@pytest.mark.django_db
def test_update_passes_resolved_instance_to_scalar_updates(item1):

    received = None

    class Service(DummyUpdateService):

        @classmethod
        def _apply_scalar_updates(cls, *, instance, validated_data):
            nonlocal received
            received = instance

    Service.update(
        user=item1.owner,
        context=item1,
        validated_data={},
    )

    assert received is item1


@pytest.mark.django_db
def test_update_validation_occurs_before_scalar_updates(item1):

    order = []

    class Service(DummyUpdateService):

        @classmethod
        def _update_validate(cls, **kwargs):
            order.append("validate")

        @classmethod
        def _apply_scalar_updates(cls, **kwargs):
            order.append("update")

    Service.update(
        user=item1.owner,
        context=item1,
        validated_data={},
    )

    assert order == [
        "validate",
        "update",
    ]


@pytest.mark.django_db
def test_update_returns_updated_instance(item1):

    class Service(DummyUpdateService):

        @classmethod
        def _save(cls, instance):
            instance.save()

    result = Service.update(
        user=item1.owner,
        context=item1,
        validated_data={},
    )

    assert result is item1


@pytest.mark.django_db
def test_update_validate_receives_unmodified_instance(item1):

    original_name = item1.name

    class Service(DummyUpdateService):

        @classmethod
        def _update_validate(cls, *, instance, validated_data, **kwargs):
            assert instance.name == original_name

        @classmethod
        def _apply_scalar_updates(cls, *, instance, validated_data):
            instance.name = validated_data["name"]

        @classmethod
        def _save(cls, instance):
            pass

    Service.update(
        user=item1.owner,
        context=item1,
        validated_data={
            "name": "New Name",
        },
    )
