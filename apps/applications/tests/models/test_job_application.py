from datetime import timedelta

import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils import timezone

from apps.applications.models import JobApplication


pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------
# M-01: Persistence Schema
# ---------------------------------------------------------------------------


class TestJobApplicationSchema:

    def test_job_application_requires_owner(
        self,
        job_position1_co2_ws1_user1,
        status1,
    ):
        application = JobApplication(
            owner=None,
            workspace=job_position1_co2_ws1_user1.company.workspace,
            job_position=job_position1_co2_ws1_user1,
            status=status1,
        )

        with pytest.raises(ValidationError):
            application.full_clean()

    def test_job_application_requires_workspace(
        self,
        job_position1_co2_ws1_user1,
        status1,
    ):
        application = JobApplication(
            owner=job_position1_co2_ws1_user1.company.workspace.owner,
            workspace=None,
            job_position=job_position1_co2_ws1_user1,
            status=status1,
        )

        with pytest.raises(ValidationError):
            application.full_clean()

    def test_job_application_requires_job_position(
        self,
        workspace1_user1,
        status1,
    ):
        application = JobApplication(
            owner=workspace1_user1.owner,
            workspace=workspace1_user1,
            job_position=None,
            status=status1,
        )

        with pytest.raises(ValidationError):
            application.full_clean()

    def test_valid_job_application_creation(
        self,
        job_position1_co2_ws1_user1,
        status1,
    ):
        application = JobApplication(
            owner=job_position1_co2_ws1_user1.company.workspace.owner,
            workspace=job_position1_co2_ws1_user1.company.workspace,
            job_position=job_position1_co2_ws1_user1,
            status=status1,
        )

        application.full_clean()
        application.save()

        assert application.id is not None
        assert application.owner == (
            job_position1_co2_ws1_user1.company.workspace.owner
        )
        assert application.workspace == (
            job_position1_co2_ws1_user1.company.workspace
        )
        assert application.job_position == (
            job_position1_co2_ws1_user1
        )
        assert application.status == status1

    def test_date_applied_is_optional(
        self,
        job_position1_co2_ws1_user1,
        status1,
    ):
        application = JobApplication(
            owner=job_position1_co2_ws1_user1.company.workspace.owner,
            workspace=job_position1_co2_ws1_user1.company.workspace,
            job_position=job_position1_co2_ws1_user1,
            status=status1,
            date_applied=None,
        )

        application.full_clean()
        application.save()

        assert application.date_applied is None


class TestJobApplicationConstraints:

    def test_same_user_cannot_create_duplicate_application_for_same_job_position(
        self,
        job_position1_co2_ws1_user1,
        status1,
    ):
        JobApplication.objects.create(
            owner=job_position1_co2_ws1_user1.company.workspace.owner,
            workspace=job_position1_co2_ws1_user1.company.workspace,
            job_position=job_position1_co2_ws1_user1,
            status=status1,
        )

        with pytest.raises(IntegrityError):
            JobApplication.objects.create(
                owner=job_position1_co2_ws1_user1.company.workspace.owner,
                workspace=job_position1_co2_ws1_user1.company.workspace,
                job_position=job_position1_co2_ws1_user1,
                status=status1,
            )


# ---------------------------------------------------------------------------
# M-02: Domain Invariants
# ---------------------------------------------------------------------------


class TestJobApplicationValidation:

    def test_owner_must_match_workspace_owner(
        self,
        job_position1_co2_ws1_user1,
        workspace1_user2,
        status1,
    ):
        application = JobApplication(
            owner=workspace1_user2.owner,
            workspace=job_position1_co2_ws1_user1.company.workspace,
            job_position=job_position1_co2_ws1_user1,
            status=status1,
        )

        with pytest.raises(ValidationError):
            application.full_clean()

    def test_workspace_must_match_job_position_workspace(
        self,
        job_position1_co2_ws1_user1,
        workspace2_user1,
        status1,
    ):
        application = JobApplication(
            owner=job_position1_co2_ws1_user1.company.workspace.owner,
            workspace=workspace2_user1,
            job_position=job_position1_co2_ws1_user1,
            status=status1,
        )

        with pytest.raises(ValidationError):
            application.full_clean()

    def test_date_applied_cannot_be_before_job_posted_date(
        self,
        job_position1_co2_ws1_user1,
        status1,
    ):
        job_position1_co2_ws1_user1.date_posted = timezone.now()

        application = JobApplication(
            owner=job_position1_co2_ws1_user1.company.workspace.owner,
            workspace=job_position1_co2_ws1_user1.company.workspace,
            job_position=job_position1_co2_ws1_user1,
            status=status1,
            date_applied=timezone.now() - timedelta(days=1),
        )

        with pytest.raises(ValidationError):
            application.full_clean()

    def test_date_applied_cannot_be_in_future(
        self,
        job_position1_co2_ws1_user1,
        status1,
    ):
        application = JobApplication(
            owner=job_position1_co2_ws1_user1.company.workspace.owner,
            workspace=job_position1_co2_ws1_user1.company.workspace,
            job_position=job_position1_co2_ws1_user1,
            status=status1,
            date_applied=timezone.now() + timedelta(days=1),
        )

        with pytest.raises(ValidationError):
            application.full_clean()

    def test_valid_date_applied_is_allowed(
        self,
        job_position1_co2_ws1_user1,
        status1,
    ):
        job_position1_co2_ws1_user1.date_posted = (
            timezone.now() - timedelta(days=1)
        )

        application = JobApplication(
            owner=job_position1_co2_ws1_user1.company.workspace.owner,
            workspace=job_position1_co2_ws1_user1.company.workspace,
            job_position=job_position1_co2_ws1_user1,
            status=status1,
            date_applied=timezone.now(),
        )

        application.full_clean()
        application.save()

        assert application.id is not None


# ---------------------------------------------------------------------------
# Model Convenience Behavior
# ---------------------------------------------------------------------------


class TestJobApplicationProperties:

    def test_string_representation(
        self,
        job_position1_co2_ws1_user1,
        status1,
    ):
        application = JobApplication(
            owner=job_position1_co2_ws1_user1.company.workspace.owner,
            workspace=job_position1_co2_ws1_user1.company.workspace,
            job_position=job_position1_co2_ws1_user1,
            status=status1,
        )

        expected = (
            f"{job_position1_co2_ws1_user1.company.name} - "
            f"{job_position1_co2_ws1_user1} - "
            f"{status1}"
        )

        assert str(application) == expected
