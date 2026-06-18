# Setup

## Requirements

See the `requirements/requirements.txt`


## Clone Repository

```bash
git clone https://github.com/BehrouzMaasser/JobApplicationManager.git
cd JobApplicationManager
```

## Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create:

```bash
.env
```

Example:

```env
DEBUG=True
SECRET_KEY=...
DATABASE_URL=...
```

## Apply Migrations

```bash
python manage.py migrate
```

## Create Superuser

```bash
python manage.py createsuperuser
```

## Run Development Server

```bash
python manage.py runserver
```

## Run Tests

```bash
pytest --cov=apps --cov-report=term-missing
```