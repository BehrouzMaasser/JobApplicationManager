from apps.companies.models import (
    Company,
    CompanyNote,
    CompanyEmail,
    JobBenefit,
    JobTask,
    JobRequirement,
    EmploymentType,
    JobSite,
    JobPosition
)

from apps.companies.services.contexts.company_context import (
    CompanyContext,
    CompanyChildContext
)

from apps.workspaces.tests.conftest import *


@pytest.fixture
def co1_ws1_user1_context_no_id(db, workspace_user1):

    return CompanyContext(id=None, workspace_id=workspace_user1.workspace_id)


@pytest.fixture
def co1_ws1_user1(db, workspace_user1):

    return Company.objects.create(
        name="co1",
        workspace=workspace_user1,
    )


@pytest.fixture
def co1_ws1_user1_valid_data():

    return {"name": "Company 1", "website": "https://www.google.com"}


@pytest.fixture
def co1_ws1_user1_updated_valid_data():

    return {"name": "Company 1 Updated", "website": "https://www.updatedgoogle.com"}


@pytest.fixture
def co1_ws1_user1_context_with_id(db, co1_ws1_user1):

    return CompanyContext(
        id=co1_ws1_user1.id,
        workspace_id=co1_ws1_user1.workspace.workspace_id
    )


@pytest.fixture
def co1_ws2_user1(db, other_workspace_user1):

    return Company.objects.create(
        name="co1",
        workspace=other_workspace_user1,
    )


@pytest.fixture
def co2_ws1_user1(db, workspace_user1):

    return Company.objects.create(
        name="co2",
        workspace=workspace_user1,
    )


@pytest.fixture
def co1_ws1_user2(db, workspace_user2):

    return Company.objects.create(
        name="co2",
        workspace=workspace_user2,
    )


@pytest.fixture
def co1_child_context_ws1_user1_no_id(db, co1_ws1_user1_context_with_id):

    return CompanyChildContext(
        id=None,
        workspace_id=co1_ws1_user1_context_with_id.workspace_id,
        company_id=co1_ws1_user1_context_with_id.id
    )


@pytest.fixture
def co_note1_co1_ws1_user1_valid_data():

    return {"title": "Title", "content": "Some Content"}


@pytest.fixture
def co_note1_co1_ws1_user1_updated_valid_data():

    return {"title": "Title Updated", "content": "Some Content Updated"}


@pytest.fixture
def co_note1_co1_ws1_user1(db, co1_ws1_user1):

    return CompanyNote.objects.create(
        company=co1_ws1_user1,
        title="Title1",
        content="Content1",
    )


@pytest.fixture
def co_note1_co2_ws1_user1(db, co2_ws1_user1):

    return CompanyNote.objects.create(
        company=co2_ws1_user1,
        title="Title1",
        content="Content1",
    )


@pytest.fixture
def co_note1_co1_ws1_user1_context_with_id(db, co_note1_co1_ws1_user1):

    return CompanyChildContext(
        id=co_note1_co1_ws1_user1.id,
        workspace_id=co_note1_co1_ws1_user1.company.workspace.workspace_id,
        company_id=co_note1_co1_ws1_user1.company.id
    )


# Email Fixtures:

@pytest.fixture
def co_email1_co1_ws1_user1(db, co1_ws1_user1):

    return CompanyEmail.objects.create(
        company=co1_ws1_user1,
        title="Title1",
        email="email1@gmail.com",
    )


@pytest.fixture
def co_email1_co1_ws1_user1_valid_data():

    return {"title": "Title", "email": "email1@gmail.com"}


@pytest.fixture
def co_email1_co1_ws1_user1_updated_valid_data():

    return {"title": "Title Updated", "email": "updatedemail1@gmail.com"}


@pytest.fixture
def co_email1_co2_ws1_user1(db, co2_ws1_user1):

    return CompanyEmail.objects.create(
        company=co2_ws1_user1,
        title="Title1",
        email="email1@gmail.com",
    )


@pytest.fixture
def co_email1_co1_ws1_user1_context_with_id(db, co_email1_co1_ws1_user1):

    return CompanyChildContext(
        id=co_email1_co1_ws1_user1.id,
        workspace_id=co_email1_co1_ws1_user1.company.workspace.workspace_id,
        company_id=co_email1_co1_ws1_user1.company.id
    )


# Job Benefit Fixtures:

@pytest.fixture
def job_benefit1_user1_valid_data():

    return {"name": "Name1", "description": "Some Description"}


@pytest.fixture
def job_benefit1_user1_updated_valid_data():

    return {"name": "Name1 Updated", "description": "Some Description Updated"}


@pytest.fixture
def job_benefit_user1(db, user):

    return JobBenefit.objects.create(
        user=user,
        name="Name1",
        description="Description1",
    )


@pytest.fixture
def job_benefit_user2(db, other_user):

    return JobBenefit.objects.create(
        user=other_user,
        name="Name1",
        description="Description1",
    )


# Job Task Fixtures:

@pytest.fixture
def job_task_user1_valid_data():

    return {"title": "Title1", "description": "Description1"}


@pytest.fixture
def job_task_user1_updated_valid_data():

    return {"title": "Title1 Updated", "description": "Description1 Updated"}


@pytest.fixture
def job_task_user1(db, user):

    return JobTask.objects.create(
        user=user,
        title="Title1",
        description="Description1",
    )


@pytest.fixture
def job_task_user2(db, other_user):

    return JobTask.objects.create(
        user=other_user,
        title="Title1",
        description="Description1",
    )


@pytest.fixture
def job_task2_user1(db, user):

    return JobTask.objects.create(
        user=user,
        title="Title2",
        description="Descriptions2",
    )


# Job Requirement Fixtures:

@pytest.fixture
def job_requirement_user1_valid_data():

    return {"title": "Title1", "description": "Description1"}


@pytest.fixture
def job_requirement_user1_updated_valid_data():

    return {"title": "Title1 Updated", "description": "Description1 Updated"}


@pytest.fixture
def job_requirement_user1(db, user):

    return JobRequirement.objects.create(
        user=user,
        title="Title1",
        description="Description1",
    )


@pytest.fixture
def job_requirement2_user1(db, user):

    return JobRequirement.objects.create(
        user=user,
        title="Title2",
        description="Description2",
    )


@pytest.fixture
def job_requirement_user2(db, other_user):

    return JobRequirement.objects.create(
        user=other_user,
        title="Title1",
        description="Description1",
    )

# Employment Type Fixtures:

@pytest.fixture
def empl_type1(db):

    return EmploymentType.objects.create(
        name="Type1",
    )


@pytest.fixture
def empl_type2(db):

    return EmploymentType.objects.create(
        name="Type2",
    )


# Job Site Fixtures:

@pytest.fixture
def job_site1(db):

    return JobSite.objects.create(
        name="Site1",
    )


@pytest.fixture
def job_site2(db):

    return JobSite.objects.create(
        name="Site2",
    )


# Job Position Fixtures:

@pytest.fixture
def job_position1_user1(
        db,
        co1_ws1_user1,
        empl_type1,
        job_requirement_user1,
        job_task_user1,
        job_site1,
):

    job_position = JobPosition.objects.create(
        company=co1_ws1_user1,
        title="Title1",
        description="Description1",
    )

    job_position.employment_types.set([empl_type1.id])
    job_position.job_sites.set([job_site1.id])
    job_position.tasks.set([job_task_user1.id])
    job_position.requirements.set([job_requirement_user1.id])

    return job_position


@pytest.fixture
def job_pos1_co2_ws1_user1(
        db,
        co2_ws1_user1,
        empl_type1,
        job_requirement_user1,
        job_task_user1,
        job_site1,
):

    job_position = JobPosition.objects.create(
        company=co2_ws1_user1,
        title="Title1",
        description="Description1",
    )

    job_position.employment_types.set([empl_type1.id])
    job_position.job_sites.set([job_site1.id])
    job_position.tasks.set([job_task_user1.id])
    job_position.requirements.set([job_requirement_user1.id])

    return job_position


@pytest.fixture
def job_position1_context(db, job_position1_user1):

    return CompanyChildContext(
        id=job_position1_user1.id,
        workspace_id=job_position1_user1.company.workspace.workspace_id,
        company_id=job_position1_user1.company.id
    )


@pytest.fixture
def job_pos_user1_valid_data(
        empl_type1,
        job_site1,
        job_task_user1,
        job_requirement_user1
):

    return {
        "title": "Title1",
        "description": "Description1",
        "employment_types": [empl_type1],
        "job_sites": [job_site1],
        "tasks": [job_task_user1],
        "requirements": [job_requirement_user1],
    }


@pytest.fixture
def job_pos_user1_updated_valid_data(
        empl_type1,
        empl_type2,
        job_site2,
        job_task2_user1,
        job_requirement2_user1,
        job_benefit_user1,
):

    return {
        "title": "Title1 Edited",
        "description": "Description1 Edited",
        "employment_types": [empl_type1, empl_type2],
        "job_sites": [job_site2],
        "tasks": [job_task2_user1],
        "requirements": [job_requirement2_user1],
        "benefits": [job_benefit_user1],
    }
