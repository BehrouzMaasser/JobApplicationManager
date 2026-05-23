import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import JobSite


#   ----------------------------------- ****** -----------------------------------

# Invalid Creation:

@pytest.mark.django_db
def test_job_site_require_name():

    # Name is None
    job_site = JobSite(name=None)

    with pytest.raises(ValidationError):
        job_site.full_clean()

    # Name is not provided
    job_site = JobSite()

    with pytest.raises(ValidationError):
        job_site.full_clean()


@pytest.mark.django_db
def test_job_site_require_non_empty_name():

    job_site = JobSite(name="")

    with pytest.raises(ValidationError):
        job_site.full_clean()


#   ----------------------------------- ****** -----------------------------------

# Constraint Tests:

@pytest.mark.django_db
def test_job_site_name_is_lower_unique():

    JobSite.objects.create(name="Home Office")

    with pytest.raises(IntegrityError):
        JobSite.objects.create(name="home oFFIcE")


#   ----------------------------------- ****** -----------------------------------


# Valid Creation:

@pytest.mark.django_db
def test_job_site_valid():

    job_site = JobSite(name="In-Site")

    job_site.full_clean()
    job_site.save()

    assert job_site.name == "In-Site"


#   ----------------------------------- ****** -----------------------------------
