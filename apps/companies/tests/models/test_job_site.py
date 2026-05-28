import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from apps.companies.models import JobSite


#   ----------------------------------- ****** -----------------------------------

# Invalid Creation:

@pytest.mark.django_db
def test_job_site_require_name():

    # Name is None
    with pytest.raises(ValidationError):
        JobSite(name=None).full_clean()

    # Name is not provided
    with pytest.raises(ValidationError):
        JobSite().full_clean()


@pytest.mark.django_db
def test_job_site_require_non_empty_name():

    with pytest.raises(ValidationError):
        JobSite(name="").full_clean()


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

    assert job_site.id is not None
    assert job_site.name == "In-Site"


#   ----------------------------------- ****** -----------------------------------
