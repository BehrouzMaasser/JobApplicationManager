import pytest

from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import JobSite


pytestmark = pytest.mark.django_db


@pytest.fixture
def name1() -> str:
    return "Name1"


# ---------------------------------------------------------------------------
# M-01: Persistence Schema
# ---------------------------------------------------------------------------


class TestJobSiteSchema:

    def test_job_site_requires_name(self):
        job_site = JobSite(
            name=None,
        )

        with pytest.raises(ValidationError):
            job_site.full_clean()

    def test_job_site_name_cannot_be_empty(self):
        job_site = JobSite(
            name="",
        )

        with pytest.raises(ValidationError):
            job_site.full_clean()

    def test_valid_job_site_creation(
        self,
        name1,
    ):
        job_site = JobSite(
            name=name1,
        )

        job_site.full_clean()
        job_site.save()

        assert job_site.id is not None
        assert job_site.name == name1


class TestJobSiteConstraints:

    def test_name_must_be_globally_unique(
        self,
        name1,
    ):
        JobSite.objects.create(
            name=name1,
        )

        with pytest.raises(IntegrityError):
            JobSite.objects.create(
                name=name1,
            )

    def test_name_is_case_insensitively_unique(
        self,
    ):
        JobSite.objects.create(
            name="Remote",
        )

        with pytest.raises(IntegrityError):
            JobSite.objects.create(
                name="remote",
            )

    def test_full_clean_reports_duplicate_job_site_name(
        self,
        name1,
    ):
        JobSite.objects.create(
            name=name1,
        )

        with pytest.raises(ValidationError) as exc:
            JobSite(
                name=name1,
            ).full_clean()

        assert (
            exc.value.error_dict["__all__"][0].code
            == "duplicate_job_site_name"
        )


# ---------------------------------------------------------------------------
# Model Convenience Behavior
# ---------------------------------------------------------------------------


class TestJobSiteProperties:

    def test_string_representation(
        self,
        name1,
    ):
        job_site = JobSite(
            name=name1,
        )

        assert str(job_site) == name1
