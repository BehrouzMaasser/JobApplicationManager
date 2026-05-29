from datetime import timedelta
from unittest.mock import patch

from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.workspaces.services.base_service import BaseService

from apps.applications.tests.conftest import *
from apps.documents.tests.conftest import *

#   ----------------------------------- ****** -----------------------------------


@pytest.mark.django_db
def test_update_non_m2m_fields_updates_given_fields_in_validated_data_successfully(
        job_application1, status2
):

    update_non_m2m_data = {
        "status": status2,
        "date_applied": timezone.now() + timedelta(hours=1),
    }

    assert job_application1.status != update_non_m2m_data["status"]
    assert job_application1.date_applied != update_non_m2m_data["date_applied"]

    BaseService._update_non_m2m_fields(
        instance=job_application1,
        validated_data=update_non_m2m_data,
        fields_to_update={"status", "date_applied"}
    )

    job_application1.save()
    job_application1.refresh_from_db()

    assert job_application1.status == update_non_m2m_data["status"]
    assert job_application1.date_applied == update_non_m2m_data["date_applied"]


@pytest.mark.django_db
def test_update_non_m2m_fields_updates_only_the_updatable_fields(job_application1):

    old_created_at = job_application1.created_at

    update_non_m2m_data = {
        "date_applied": timezone.now() + timedelta(hours=1),
        "created_at":  timezone.now() + timedelta(hours=1)
    }

    assert job_application1.date_applied != update_non_m2m_data["date_applied"]
    assert job_application1.created_at != update_non_m2m_data["created_at"]

    BaseService._update_non_m2m_fields(
        instance=job_application1,
        validated_data=update_non_m2m_data,
        fields_to_update={"date_applied", "status"}
    )

    job_application1.save()
    job_application1.refresh_from_db()

    assert job_application1.date_applied == update_non_m2m_data["date_applied"]
    assert job_application1.created_at != update_non_m2m_data["created_at"]
    assert job_application1.created_at == old_created_at


@pytest.mark.django_db
def test_update_m2m_fields_updates_calls_set_function_of_that_field(
        job_application1, email1_co1_ws1_user1, email2_co1_ws1_user1
):

    update_non_m2m_data = {
        "emails": [email1_co1_ws1_user1, email2_co1_ws1_user1],
    }

    with (
        patch.object(type(job_application1.emails), "set") as
        mock_emails_set
    ):

        BaseService._update_m2m_fields(
            instance=job_application1,
            validated_data=update_non_m2m_data,
            fields_to_update={"emails"}
        )

        mock_emails_set.assert_called()


@pytest.mark.django_db
def test_update_m2m_fields_updates_given_fields_in_validated_data_successfully(
        job_application1, email1_co1_ws1_user1, email2_co1_ws1_user1
):

    update_non_m2m_data = {
        "emails": [email1_co1_ws1_user1, email2_co1_ws1_user1],
    }

    assert list(job_application1.emails.all()) != update_non_m2m_data["emails"]

    BaseService._update_m2m_fields(
        instance=job_application1,
        validated_data=update_non_m2m_data,
        fields_to_update={"emails"}
    )

    job_application1.refresh_from_db()

    assert list(job_application1.emails.all()) == update_non_m2m_data["emails"]


@pytest.mark.django_db
def test_update_m2m_fields_updates_only_the_updatable_fields(
        job_application1, doc1_user1
):

    update_non_m2m_data = {
        "documents": [doc1_user1],
        "jobs": [12, 23, 34]
    }

    assert list(job_application1.documents.all()) != update_non_m2m_data["documents"]

    BaseService._update_m2m_fields(
        instance=job_application1,
        validated_data=update_non_m2m_data,
        fields_to_update={"documents", "emails"}
    )

    job_application1.refresh_from_db()

    assert list(job_application1.documents.all()) == update_non_m2m_data["documents"]
    with pytest.raises(AttributeError):
        assert list(job_application1.jobs.all()) == update_non_m2m_data["jobs"]


@pytest.mark.django_db
def test_add_m2m_fields_adds_given_fields_in_validated_data_successfully(
        job_application1, email1_co1_ws1_user1, email2_co1_ws1_user1
):

    update_non_m2m_data = {
        "emails": [email1_co1_ws1_user1, email2_co1_ws1_user1],
    }

    assert list(job_application1.emails.all()) == []

    BaseService._add_m2m_fields(
        instance=job_application1,
        validated_data=update_non_m2m_data,
        m2m_fields={"emails", "documents"}
    )

    job_application1.refresh_from_db()

    assert list(job_application1.emails.all()) == update_non_m2m_data["emails"]


@pytest.mark.django_db
def test_add_m2m_fields_calls_add_function_of_that_field(
        job_application1, doc1_user1
):

    update_non_m2m_data = {
        "documents": [doc1_user1],
    }

    with (
        patch.object(type(job_application1.documents), "add") as
        mock_documents_set
    ):

        BaseService._add_m2m_fields(
            instance=job_application1,
            validated_data=update_non_m2m_data,
            m2m_fields={"emails", "documents"}
        )

        mock_documents_set.assert_called_once()


@pytest.mark.django_db
def test_m2m_non_empty_validation_calls_exists_function_of_that_field(
        job_application1
):

    with (
        patch.object(type(job_application1.emails), "exists") as
        mock_emails_exists
    ):

        BaseService._m2m_non_empty_validation(
            instance=job_application1,
            required_fields={"emails"},
        )

        mock_emails_exists.assert_called_once()


@pytest.mark.django_db
def test_m2m_non_empty_validation_raise_error_if_required_fields_are_empty(
        job_application1
):

    assert list(job_application1.documents.all()) == []

    with pytest.raises(ValidationError):
        BaseService._m2m_non_empty_validation(
            instance=job_application1,
            required_fields={"documents"},
        )


@pytest.mark.django_db
def test_m2m_ownership_validation_passes_for_owned_items(doc1_user1):

    BaseService._m2m_ownership_validation(
        user=doc1_user1.owner,
        validated_data={"documents": [doc1_user1]},
        ownership_map={"documents": "owner"},
    )


@pytest.mark.django_db
def test_m2m_ownership_validation_raises_if_any_item_unowned(
    other_user, doc1_user1
):

    with pytest.raises(ValidationError) as e:
        BaseService._m2m_ownership_validation(
            user=other_user,
            validated_data={
                "documents": [doc1_user1]
            },
            ownership_map={"documents": "owner"},
        )

    assert "documents" in e.value.detail


def test_m2m_ownership_validation_ignores_attribute_error(doc1_user1):

    BaseService._m2m_ownership_validation(
        user=doc1_user1.owner,
        validated_data={"documents": [doc1_user1]},
        ownership_map={"documents": "user"},    # Wrong ownership attribute
    )

#   ----------------------------------- ****** -----------------------------------
