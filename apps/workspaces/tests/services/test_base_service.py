from datetime import timedelta
from unittest.mock import patch

import pytest

# Django
from django.utils import timezone

# Exceptions
from apps.core.exceptions.exceptions import (
    BusinessRuleViolationError,
    DomainInvariantViolationError
)

# Services
from apps.core.common.services.base_service import BaseService

#   ----------------------------------- ****** -----------------------------------


class FakeObjectWithFields:
    def __init__(self, **fields):
        for key, value in fields.items():
            setattr(self, key, value)


class FakeField:
    ID = 0

    def __init__(self, value, owner: list[str] | None = None):
        self.pk = FakeField.ID + 1
        FakeField.ID += 1
        self.value = value
        if owner and len(owner) == 2:
            setattr(self, owner[0], owner[1])


class FakeM2MField:
    def __init__(self, *values):
        self.values = [*values]

    def set(self, values):
        self.values = values

    def add(self, *values):
        for value in values:
            if value not in self.values:
                self.values.append(value)

    def exists(self):
        return bool(len(self.values))

    def all(self):
        return self.values


class TestBaseService:

    def test_update_non_m2m_fields_updates_given_fields_successfully(self):

        instance = FakeObjectWithFields(status="Status1", date_applied=None)

        update_non_m2m_data = {
            "status": "Status Updated",
            "date_applied": timezone.now() + timedelta(hours=1),
        }

        BaseService._update_non_m2m_fields(
            instance=instance,
            validated_data=update_non_m2m_data,
            fields_to_update={"status", "date_applied"}
        )

        assert instance.status == update_non_m2m_data["status"]
        assert instance.date_applied == update_non_m2m_data["date_applied"]

    def test_update_non_m2m_fields_updates_only_the_updatable_fields(self):

        instance = FakeObjectWithFields(status="Status1", created_at="H:M")

        update_non_m2m_data = {
            "status": "Updated",
            "created_at": "Updated"
        }

        BaseService._update_non_m2m_fields(
            instance=instance,
            validated_data=update_non_m2m_data,
            fields_to_update={"date_applied", "status"}
        )

        assert instance.status == update_non_m2m_data["status"]
        assert instance.created_at == "H:M"

    def test_update_m2m_fields_updates_calls_set_function_of_that_field(self):

        instance = FakeObjectWithFields(
            emails=FakeM2MField("Email1", "Email2"),
        )

        update_m2m_data = {"emails": ["E1", "E2"]}

        with patch.object(type(instance.emails), "set") as mock_set:

            BaseService._update_m2m_fields(
                instance=instance,
                validated_data=update_m2m_data,
                fields_to_update={"emails"}
            )

            mock_set.assert_called()

    def test_update_m2m_fields_updates_successfully(self):

        instance = FakeObjectWithFields(
            emails=FakeM2MField("Email1", "Email2"),
        )

        update_non_m2m_data = {
            "emails": ["E2", "E2"],
        }

        BaseService._update_m2m_fields(
            instance=instance,
            validated_data=update_non_m2m_data,
            fields_to_update={"emails"}
        )

        assert instance.emails.all() == update_non_m2m_data["emails"]

    def test_update_m2m_fields_updates_only_the_updatable_fields(self):

        instance = FakeObjectWithFields(
            documents=FakeM2MField("D1", "D2"),
            jobs=FakeM2MField(1, 2),
            emails=FakeM2MField("E1", "E2"),
        )

        update_non_m2m_data = {
            "documents": [],
            "jobs": [12, 23, 34]
        }

        BaseService._update_m2m_fields(
            instance=instance,
            validated_data=update_non_m2m_data,
            fields_to_update={"documents", "emails"}
        )

        assert instance.documents.all() == update_non_m2m_data["documents"]
        assert instance.emails.all() == ["E1", "E2"]
        assert instance.jobs.all() != update_non_m2m_data["jobs"]

    def test_add_m2m_fields_adds_given_fields_successfully(self):

        # instance with empty emails
        instance = FakeObjectWithFields(emails=FakeM2MField())

        update_non_m2m_data = {"emails": ["E1 U", "E2 U", "E3 U"]}

        BaseService._add_m2m_fields(
            instance=instance,
            validated_data=update_non_m2m_data,
            m2m_fields=["emails"]
        )

        assert instance.emails.all() == update_non_m2m_data["emails"]

        # instance with non-empty emails
        instance = FakeObjectWithFields(emails=FakeM2MField("E1"))

        update_non_m2m_data = {"emails": ["E1 U", "E2 U", "E3 U"]}

        BaseService._add_m2m_fields(
            instance=instance,
            validated_data=update_non_m2m_data,
            m2m_fields=["emails"]
        )

        assert instance.emails.all() == ["E1", *update_non_m2m_data["emails"]]

    def test_add_m2m_fields_calls_add_function_of_that_field(self):

        instance = FakeObjectWithFields(documents=FakeM2MField("D1", "D2"))

        update_non_m2m_data = {"documents": ["D3"]}

        with patch.object(type(instance.documents), "add") as mock_add:

            BaseService._add_m2m_fields(
                instance=instance,
                validated_data=update_non_m2m_data,
                m2m_fields=["emails", "documents"]
            )

            mock_add.assert_called_once()

    def test_m2m_non_empty_validation_calls_exists_function_of_that_field(self):

        instance = FakeObjectWithFields(emails=FakeM2MField("E1", "E2"))

        with patch.object(type(instance.emails), "exists") as mock_exists:

            BaseService._m2m_non_empty_validation(
                instance=instance,
                required_fields=["emails"]
            )

            mock_exists.assert_called_once()

    def test_m2m_non_empty_validation_raise_error_if_required_fields_are_empty(self):

        instance = FakeObjectWithFields(documents=FakeM2MField())

        with pytest.raises(BusinessRuleViolationError):
            BaseService._m2m_non_empty_validation(
                instance=instance,
                required_fields=["documents"]
            )

    def test_m2m_ownership_validation_passes_for_owned_items(self):

        BaseService._m2m_ownership_validation(
            user="U1",
            validated_data={
                "documents": [
                    FakeField(owner=["owner", "U1"], value="D1"),
                    FakeField(owner=["owner", "U1"], value="D2")
                ]
            },
            ownership_map={"documents": "owner"},
        )

    def test_m2m_ownership_validation_raises_if_any_item_unowned(self):

        validated_data = {
            "documents": [
                FakeField(owner=["owner", "U1"], value="D1"),
                FakeField(owner=["owner", "U2"], value="D2")
            ]
        }
        with pytest.raises(DomainInvariantViolationError) as e:
            BaseService._m2m_ownership_validation(
                user="U1",
                validated_data=validated_data,
                ownership_map={"documents": "owner"},
            )

        assert "documents" in str(e.value.message)
        assert f"{validated_data["documents"][1].pk}" in str(e.value.message)

    def test_m2m_ownership_validation_ignores_missing_ownership_attribute(self):

        BaseService._m2m_ownership_validation(
            user="U1",
            validated_data={
                "documents": [
                    FakeField(owner=["owner", "U1"], value="D1"),
                    FakeField(owner=["user", "U1"], value="D2")
                ]
            },
            ownership_map={"documents": "user"},    # Wrong ownership attribute
        )

#   ----------------------------------- ****** -----------------------------------
