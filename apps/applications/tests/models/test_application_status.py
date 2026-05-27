from datetime import datetime

import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.applications.models import ApplicationStatus


#   ----------------------------------- ****** -----------------------------------

# Invalid Creation:

@pytest.mark.django_db
def test_application_status_requires_label():

    application_status = ApplicationStatus(label=None)

    with pytest.raises(ValidationError):
        application_status.full_clean()


@pytest.mark.django_db
def test_application_status_requires_non_empty_label():

    application_status = ApplicationStatus(label="")

    with pytest.raises(ValidationError):
        application_status.full_clean()

    # Non-Empty Label
    ApplicationStatus(label="Label").full_clean()


@pytest.mark.django_db
def test_application_status_order_cannot_be_null():

    application_status = ApplicationStatus(order=None)

    with pytest.raises(ValidationError):
        application_status.full_clean()


# Constraint Check:

@pytest.mark.django_db
def test_application_status_lower_case_label_is_unique():

    ApplicationStatus.objects.create(label="Pending", order=1)

    with pytest.raises(IntegrityError):
        ApplicationStatus.objects.create(label="penDING", order=2)


@pytest.mark.django_db
def test_application_status_order_is_unique():

    ApplicationStatus.objects.create(label="Pending", order=1)

    with pytest.raises(IntegrityError):
        ApplicationStatus.objects.create(label="Rejected", order=1)


#   ----------------------------------- ****** -----------------------------------


# Valid Creation:
@pytest.mark.django_db
def test_valid_application_status():

    application_status = ApplicationStatus(
        label="Rejected",
        order=3
    )

    application_status.full_clean()
    application_status.save()

    assert application_status.label == "Rejected"
    assert application_status.order == 3


@pytest.mark.django_db
def test_label_default_is_pending():

    application_status = ApplicationStatus(
        order=1
    )

    application_status.full_clean()
    application_status.save()

    assert application_status.label == "Pending"


@pytest.mark.django_db
def test_order_default_is_1():

    application_status = ApplicationStatus()

    application_status.full_clean()
    application_status.save()

    assert application_status.order == 1


@pytest.mark.django_db
def test_created_at_is_created_automatically():

    application_status = ApplicationStatus.objects.create()

    assert isinstance(application_status.created_at, datetime)

#   ----------------------------------- ****** -----------------------------------
