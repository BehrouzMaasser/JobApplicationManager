import pytest

from apps.core.common.services.base_service import BaseService
from apps.testing.models import DummyItem
from apps.testing.selectors import DummyItemSelector


class DummyCreateService(BaseService):

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
    def _resolve_create_dependencies(cls, user, context):
        cls.calls.append("_resolve_create_dependencies")
        return {"owner": user}

    @classmethod
    def _build_instance(cls, **kwargs):
        cls.calls.append("_build_instance")
        return super()._build_instance(**kwargs)

    @classmethod
    def _create_validate(cls, **kwargs):
        cls.calls.append("_create_validate")

    @classmethod
    def _create_pre_save(cls, **kwargs):
        cls.calls.append("_create_pre_save")

    @classmethod
    def _save(cls, instance):
        cls.calls.append("_save")

    @classmethod
    def _create_post_save(cls, instance, validated_data):
        cls.calls.append("_create_post_save")

    @classmethod
    def _validate_resolved_instance(cls, **kwargs):
        pass


@pytest.mark.django_db
def test_create_executes_create_workflow_in_contract_order(user1):

    DummyCreateService.calls = []

    DummyCreateService.create(
        user=user1,
        context=None,
        validated_data={
            "name": "Workspace",
        },
    )

    assert DummyCreateService.calls == [
        "_resolve_create_dependencies",
        "_build_instance",
        "_create_validate",
        "_create_pre_save",
        "_save",
        "_create_post_save",
    ]


@pytest.mark.django_db
def test_create_merges_resolved_dependencies(user1):

    captured = {}

    class Service(DummyCreateService):

        @classmethod
        def _build_instance(cls, **kwargs):
            captured.update(kwargs)
            return DummyItem(**kwargs)

    Service.create(
        user=user1,
        context=None,
        validated_data={
            "name": "Example",
        },
    )

    assert captured["owner"] == user1
    assert captured["name"] == "Example"


@pytest.mark.django_db
def test_create_returns_created_instance(user1):

    class Service(DummyCreateService):

        @classmethod
        def _save(cls, instance):
            instance.save()

    instance = Service.create(
        user=user1,
        context=None,
        validated_data={
            "name": "Example",
        },
    )

    assert isinstance(instance, DummyItem)
    assert instance.pk is not None
    assert instance.owner == user1
    assert instance.name == "Example"


@pytest.mark.django_db
def test_create_calls_build_instance_only_once(user1):

    count = 0

    class Service(DummyCreateService):

        @classmethod
        def _build_instance(cls, **kwargs):
            nonlocal count
            count += 1
            return super()._build_instance(**kwargs)

    Service.create(
        user=user1,
        context=None,
        validated_data={
            "name": "Example",
        },
    )

    assert count == 1
