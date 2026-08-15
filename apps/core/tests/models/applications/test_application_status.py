from datetime import datetime

import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.applications.models import ApplicationStatus


pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------
# M-01: Define the Persistence Schema
# ---------------------------------------------------------------------------


class TestApplicationStatusSchema:

    def test_application_status_requires_label(self):
        application_status = ApplicationStatus(
            label=None,
        )

        with pytest.raises(ValidationError):
            application_status.full_clean()

    def test_application_status_label_cannot_be_blank(self):
        application_status = ApplicationStatus(
            label="",
        )

        with pytest.raises(ValidationError):
            application_status.full_clean()

    def test_application_status_requires_order(self):
        application_status = ApplicationStatus(
            order=None,
        )

        with pytest.raises(ValidationError):
            application_status.full_clean()

    def test_application_status_uses_default_label(self):
        application_status = ApplicationStatus()

        application_status.full_clean()
        application_status.save()

        assert application_status.label == "Pending"

    def test_application_status_uses_default_order(self):
        application_status = ApplicationStatus()

        application_status.full_clean()
        application_status.save()

        assert application_status.order == 1

    def test_application_status_uses_default_is_final_value(self):
        application_status = ApplicationStatus()

        application_status.full_clean()
        application_status.save()

        assert application_status.is_final is False

    def test_application_status_sets_created_at_automatically(self):
        application_status = ApplicationStatus.objects.create()

        assert isinstance(
            application_status.created_at,
            datetime,
        )

    def test_application_status_can_be_created_with_valid_data(self):
        application_status = ApplicationStatus(
            label="Rejected",
            order=3,
            is_final=True,
        )

        application_status.full_clean()
        application_status.save()

        assert application_status.id is not None
        assert application_status.label == "Rejected"
        assert application_status.order == 3
        assert application_status.is_final is True

    def test_application_status_ordering_is_by_order(self):
        status1 = ApplicationStatus.objects.create(
            label="Rejected",
            order=3,
        )

        status2 = ApplicationStatus.objects.create(
            label="Pending",
            order=1,
        )

        status3 = ApplicationStatus.objects.create(
            label="Interview",
            order=2,
        )

        statuses = list(ApplicationStatus.objects.all())

        assert statuses == [
            status2,
            status3,
            status1,
        ]


class TestApplicationStatusConstraints:

    def test_application_status_label_is_case_insensitive_unique(self):
        ApplicationStatus.objects.create(
            label="Pending",
            order=1,
        )

        with pytest.raises(IntegrityError):
            ApplicationStatus.objects.create(
                label="penDING",
                order=2,
            )

    def test_application_status_order_is_unique(self):
        ApplicationStatus.objects.create(
            label="Pending",
            order=1,
        )

        with pytest.raises(IntegrityError):
            ApplicationStatus.objects.create(
                label="Rejected",
                order=1,
            )


# ---------------------------------------------------------------------------
# Model Convenience Behavior
# ---------------------------------------------------------------------------


class TestApplicationStatusProperties:

    def test_application_status_string_representation(self):
        application_status = ApplicationStatus(
            label="Interview",
        )

        assert str(application_status) == "Interview"
