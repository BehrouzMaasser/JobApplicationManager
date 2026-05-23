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
def test_is_final_with_label():

    application_status1 = ApplicationStatus.objects.create()
    application_status2 = ApplicationStatus.objects.create(
        label="Not Pending", order=2
    )

    application_status3 = ApplicationStatus.objects.create(label="Rejected", order=3)
    application_status4 = ApplicationStatus.objects.create(label="Claimed", order=4)
    application_status5 = ApplicationStatus.objects.create(label="Refused", order=5)

    assert application_status1.is_final is False
    assert application_status2.is_final is False
    assert application_status3.is_final is True
    assert application_status4.is_final is True
    assert application_status5.is_final is True


@pytest.mark.django_db
def test_order_doesnt_affect_is_final():

    application_status1 = ApplicationStatus.objects.create(label="Pending", order=1)
    assert application_status1.is_final is False

    application_status1.delete()

    application_status2 = ApplicationStatus.objects.create(label="Rejected", order=1)
    assert application_status2.is_final is True

    application_status2.delete()

    application_status3 = ApplicationStatus.objects.create(label="Rejected", order=2)
    assert application_status3.is_final is True

    application_status3.delete()

    application_status4 = ApplicationStatus.objects.create(label="Rejected", order=3)
    assert application_status4.is_final is True

    application_status4.delete()

    application_status5 = ApplicationStatus.objects.create(label="Rejected", order=5)
    assert application_status5.is_final is True

    application_status5.delete()

    application_status6 = ApplicationStatus.objects.create(label="Pending", order=1)
    assert application_status6.is_final is False

    application_status6.delete()

    application_status7 = ApplicationStatus.objects.create(label="Pending", order=2)
    assert application_status7.is_final is False

#   ----------------------------------- ****** -----------------------------------
