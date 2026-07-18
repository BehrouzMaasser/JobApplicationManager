import pytest

from apps.core.common.services.base_service import BaseService
from apps.core.exceptions.exceptions import (
    BusinessRuleViolationError,
    DomainInvariantViolationError,
)

from apps.testing.models import DummyItem
from apps.testing.selectors import DummyItemSelector


class DummyHelperService(BaseService):

    MODEL = DummyItem
    SELECTOR = DummyItemSelector

    CREATE_FIELDS = (
        "owner",
        "name",
    )

    SCALAR_UPDATABLE_FIELDS = (
        "name",
    )

    M2M_UPDATABLE_FIELDS = (
        "tags",
    )

    REQUIRED_M2M_FIELDS = (
        "tags",
    )

    NON_EMPTY_M2M_FIELDS = (
        "tags",
    )

    M2M_OWNER_FIELD_MAP = {
        "tags": "owner",
    }

    @classmethod
    def _validate_resolved_instance(cls, **kwargs):
        pass


def test_build_instance_creates_instance(user1):

    instance = DummyHelperService._build_instance(
        owner=user1,
        name="Example",
    )

    assert isinstance(instance, DummyItem)
    assert instance.owner == user1
    assert instance.name == "Example"


def test_apply_scalar_updates_changes_only_configured_fields(
    tagged1_item1,
):

    DummyHelperService._apply_scalar_updates(
        instance=tagged1_item1,
        validated_data={
            "name": "Updated",
            "unknown": "ignored",
        },
    )

    assert tagged1_item1.name == "Updated"


@pytest.mark.django_db
def test_save_calls_full_clean_and_persists(tagged1_item1):

    tagged1_item1.name = "Updated"

    DummyHelperService._save(tagged1_item1)

    refreshed = DummyItem.objects.get(
        pk=tagged1_item1.pk,
    )

    assert refreshed.name == "Updated"


def test_required_m2m_fields_are_required():

    with pytest.raises(BusinessRuleViolationError):

        DummyHelperService._validate_required_m2m_fields_exist(
            validated_data={},
        )


def test_required_m2m_fields_accept_existing_field():

    DummyHelperService._validate_required_m2m_fields_exist(
        validated_data={
            "tags": [],
        },
    )


def test_m2m_ownership_validation_accepts_owned_objects(
    user1,
    tag1_user1,
):

    DummyHelperService._validate_m2m_ownership(
        user=user1,
        validated_data={
            "tags": [
                tag1_user1,
            ],
        },
    )


def test_m2m_ownership_validation_rejects_foreign_objects(
    user1,
    tag1_user2,
):

    with pytest.raises(DomainInvariantViolationError):

        DummyHelperService._validate_m2m_ownership(
            user=user1,
            validated_data={
                "tags": [
                    tag1_user2,
                ],
            },
        )


@pytest.mark.django_db
def test_add_m2m_fields_adds_relations(
    item1,
    tag1_user1,
):

    DummyHelperService._add_m2m_fields(
        instance=item1,
        validated_data={
            "tags": [
                tag1_user1,
            ],
        },
    )

    assert item1.tags.filter(
        pk=tag1_user1.pk,
    ).exists()


@pytest.mark.django_db
def test_apply_m2m_updates_replaces_relations(
    item1,
    tag1_user1,
    tag2_user1,
):

    item1.tags.add(tag1_user1)

    DummyHelperService._apply_m2m_updates(
        instance=item1,
        validated_data={
            "tags": [
                tag2_user1,
            ],
        },
    )

    assert not item1.tags.filter(
        pk=tag1_user1.pk,
    ).exists()

    assert item1.tags.filter(
        pk=tag2_user1.pk,
    ).exists()


@pytest.mark.django_db
def test_m2m_non_empty_validation_rejects_empty_relations(
    item1,
):

    with pytest.raises(BusinessRuleViolationError):

        DummyHelperService._m2m_non_empty_validation(
            item1,
        )


@pytest.mark.django_db
def test_m2m_non_empty_validation_accepts_existing_relations(
    item1,
    tag1_user1,
):

    item1.tags.add(tag1_user1)

    DummyHelperService._m2m_non_empty_validation(
        item1,
    )
