# Setup

## Requirements

The project requires Python and the dependencies listed in:

```text
requirements/requirements.txt
```

The pinned requirements currently include:

- Django
- Django REST Framework
- Simple JWT
- django-filter
- pytest
- pytest-django
- pytest-cov
- PostgreSQL driver support

The repository currently uses SQLite as its default local database configuration.

---

## Clone the Repository

```bash
git clone https://github.com/BehrouzMaasser/JobApplicationManager.git
cd JobApplicationManager
```

---

## Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On systems where the activation command differs, use the corresponding virtual-environment activation command.

---

## Install Dependencies

```bash
pip install -r requirements/requirements.txt
```

---

## Environment Configuration

The project reads configuration through `python-decouple`.

At minimum, configure the secret key in the environment or in a local `.env` file.

Example:

```env
SECRET_KEY=replace-with-a-local-secret-key
DEBUG=True
```

`DEBUG` defaults to `False` when it is not provided.

Do not commit production secrets to the repository.

---

## Database

The current default database configuration is SQLite:

```text
db.sqlite3
```

Apply migrations with:

```bash
python manage.py migrate
```

The dependency set also contains PostgreSQL support, making PostgreSQL available for a production deployment configuration. The current checked-in settings, however, use SQLite by default.

---

## Create a Superuser

```bash
python manage.py createsuperuser
```

This creates an administrative account for Django's admin interface.

---

## Run the Development Server

```bash
python manage.py runserver
```

The default development address is:

```text
http://127.0.0.1:8000/
```

---

## Run Tests

Run the complete test suite:

```bash
pytest
```

Run the suite with coverage:

```bash
pytest --cov=apps --cov-report=term-missing
```

The repository does not treat a fixed test count or coverage percentage as a permanent quality target. The meaningful requirement is that the suite passes and that important architectural, domain, security, and presentation behavior is covered.

---

## Static and Media Files

Static files are configured under:

```text
static/
```

Uploaded files are stored under:

```text
media/
```

The media directory is application data and should not be treated as source code.

Production deployments require an appropriate strategy for serving static and media files.

---

## REST API

The API is available under:

```text
/api/v1/
```

JWT authentication endpoints are:

```text
/api/v1/auth/
/api/v1/auth/refresh/
```

See `docs/rest_api.md` for the API structure and authentication workflow.

---

## Production Considerations

The repository is structured as a production-oriented Django application, but the default local settings are intentionally development-oriented.

A production deployment should explicitly review at least:

- `DEBUG=False`
- `ALLOWED_HOSTS`
- Secret management
- Database configuration
- Static file collection and serving
- Media storage and serving
- HTTPS
- Secure cookies
- CSRF configuration
- Security middleware configuration
- Logging
- Database backups
- Deployment and process management

These are deployment concerns rather than requirements for local development.

---

## Administrative Interface

Django's administrative interface is available at:

```text
/admin/
```

after creating a superuser.

---

## Project Documentation

Additional documentation is available in `docs/`:

- `architecture.md` — system architecture.
- `domain.md` — domain model and ownership rules.
- `rest_api.md` — REST API behavior.
- `testing.md` — testing strategy.
- `roadmap.md` — future development direction.
- `architecture_layer_contracts/` — architectural contracts and checklists.
