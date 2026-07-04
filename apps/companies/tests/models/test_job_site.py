import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import JobSite


pytestmark = pytest.mark.django_db

#   ----------------------------------- ****** -----------------------------------


@pytest.fixture
def name1() -> str:
    
    return "Name1"


class TestJobSiteValidation:

    def test_job_site_requires_name(self):
        with pytest.raises(ValidationError):
            JobSite(name=None).full_clean()

    def test_job_site_requires_non_empty_name(self):
        with pytest.raises(ValidationError):
            JobSite(name="").full_clean()

#   ----------------------------------- ****** -----------------------------------


class TestJobSiteConstraint:

    def test_name_is_unique(self, name1):
        JobSite.objects.create(name=name1)

        with pytest.raises(IntegrityError):
            JobSite.objects.create(name=name1)

    def test_same_name_raise_error_when_call_full_clean(self, name1):
        JobSite.objects.create(name=name1)

        with pytest.raises(ValidationError) as e:
            JobSite(name=name1).full_clean()

            assert (e.error_dict["__all__"][0].code ==
                    "duplicate_job_site_name")

#   ----------------------------------- ****** -----------------------------------


class TestJobSiteCreation:

    def test_valid_job_site_creation(self, name1):
        job_site = JobSite.objects.create(name=name1)

        assert job_site.name == name1

    def test_ordering(self):
        job_site1 = JobSite.objects.create(name="C")
        job_site2 = JobSite.objects.create(name="A")
        job_site3 = JobSite.objects.create(name="B")

        correct_name_order = [
            job_site2,
            job_site3,
            job_site1,
        ]

        job_sites = JobSite.objects.all()

        for job_sites_correct_order, job_sites_given in (
                zip(correct_name_order, job_sites)):
            assert job_sites_correct_order == job_sites_given

#   ----------------------------------- ****** -----------------------------------


class TestJobSiteRepresentation:

    def test_job_site_string_representation(self, name1):
        job_site = JobSite.objects.create(name=name1)

        assert str(job_site) == job_site.name


#   ----------------------------------- ****** -----------------------------------
