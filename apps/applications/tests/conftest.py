from apps.applications.services.contexts.application_context import (
    JobApplicationChildContext, JobApplicationContext
)

from apps.companies.tests.conftest import *

from apps.applications.models import (
    ApplicationStatus,
    JobApplication,
    JobApplicationNote
)

# ----------------------*****---------------------


# Fixtures:

# Status Fixtures:

@pytest.fixture
def status1(db):

    return ApplicationStatus.objects.create(label="Pending", order=1)


@pytest.fixture
def status2(db):

    return ApplicationStatus.objects.create(label="Interview", order=2)

# ----------------------*****---------------------


# Job Position Fixtures:

@pytest.fixture
def job_position1_co1_ws1_user1(db, co1_ws1_user1):

    return JobPosition.objects.create(
        title="Title 1",
        company=co1_ws1_user1,
        description="Description 1",
    )


@pytest.fixture
def job_position2_co1_ws1_user1(db, co1_ws1_user1):

    return JobPosition.objects.create(
        title="Title 2",
        company=co1_ws1_user1,
        description="Description 2"
    )


@pytest.fixture
def job_position1_co2_ws1_user1(db, co2_ws1_user1):

    return JobPosition.objects.create(
        title="Title 1",
        company=co2_ws1_user1,
        description="Description 1",
    )

# ----------------------*****---------------------


# Company Email Fixtures:

@pytest.fixture
def email1_co1_ws1_user1(db, co1_ws1_user1):

    return CompanyEmail.objects.create(
        company=co1_ws1_user1,
        email="email1@gmail.com",
        title="Title 1",
    )


@pytest.fixture
def email2_co1_ws1_user1(db, co1_ws1_user1):

    return CompanyEmail.objects.create(
        company=co1_ws1_user1,
        email="email2@gmail.com",
        title="Title 2",
    )

# ----------------------*****---------------------


# Job Application Fixtures:

@pytest.fixture
def job_application1_valid_data(status1, email1_co1_ws1_user1):

    return {
        "status": status1,
        "emails": [email1_co1_ws1_user1],
    }


@pytest.fixture
def job_application1_api_valid_data(status1, email1_co1_ws1_user1):

    return {
        "status": status1.id,
    }


@pytest.fixture
def job_application1_valid_data_updated(
        status2,
        email1_co1_ws1_user1,
        email2_co1_ws1_user1,
):

    return {
        "status": status2,
        "emails": [email1_co1_ws1_user1, email2_co1_ws1_user1],
    }


@pytest.fixture
def job_application1_api_valid_data_updated(
        status2,
        email1_co1_ws1_user1,
        email2_co1_ws1_user1,
):

    return {
        "status": status2.id,
        "emails": [email1_co1_ws1_user1.id, email2_co1_ws1_user1.id],
    }


@pytest.fixture
def job_application1(db, job_position1_co1_ws1_user1, status1, email1_co1_ws1_user1):

    app = JobApplication.objects.create(
        owner=job_position1_co1_ws1_user1.company.workspace.owner,
        workspace=job_position1_co1_ws1_user1.company.workspace,
        job_position=job_position1_co1_ws1_user1,
        status=status1,
    )

    app.emails.set([email1_co1_ws1_user1])

    return app


@pytest.fixture
def job_application1_context(db, job_application1):

    return JobApplicationContext(
        id=job_application1.id,
        workspace_id=job_application1.job_position.company.workspace.workspace_id,
        company_id=job_application1.job_position.company.id,
        job_position_id=job_application1.job_position.id,
    )


@pytest.fixture
def job_application_context_with_no_id(db, job_position1_co1_ws1_user1):

    return JobApplicationContext(
        id=None,
        workspace_id=job_position1_co1_ws1_user1.company.workspace.workspace_id,
        company_id=job_position1_co1_ws1_user1.company.id,
        job_position_id=job_position1_co1_ws1_user1.id,
    )


@pytest.fixture
def job_application2(db, job_position1_co2_ws1_user1, status1, email1_co1_ws1_user1):

    app = JobApplication.objects.create(
        owner=job_position1_co2_ws1_user1.company.workspace.owner,
        workspace=job_position1_co2_ws1_user1.company.workspace,
        job_position=job_position1_co2_ws1_user1,
        status=status1,
    )

    app.emails.set([email1_co1_ws1_user1])

    return app

# ----------------------*****---------------------


# Application Note Fixtures:

@pytest.fixture
def app_note1_valid_data():

    return {"title": "Job Application Title Test 1", "content": "Test Content 1"}


@pytest.fixture
def app_note1_valid_data_updated():

    return {
        "title": "Job Application Title Test 1 Edited",
        "content": "Test Content 1 Edited"
    }


@pytest.fixture
def app_note1(db, job_application1):

    return JobApplicationNote.objects.create(
        job_application=job_application1,
        title="Title 1",
        content="Content",
    )


@pytest.fixture
def app_note1_context_with_no_id(db, app_note1):

    return JobApplicationChildContext(
        id=None,
        workspace_id=app_note1.job_application.workspace.workspace_id,
        company_id=app_note1.job_application.job_position.company.id,
        job_position_id=app_note1.job_application.job_position.id,
        job_application_id=app_note1.job_application.id,
    )


@pytest.fixture
def app_note1_context_with_id(db, app_note1):

    return JobApplicationChildContext(
        id=app_note1.id,
        workspace_id=app_note1.job_application.workspace.workspace_id,
        company_id=app_note1.job_application.job_position.company.id,
        job_position_id=app_note1.job_application.job_position.id,
        job_application_id=app_note1.job_application.id,
    )
