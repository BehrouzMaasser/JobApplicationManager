# Setup

## Clone repository

```bash
git clone ...
cd ...
```

## Create virtual environment

```bash
python -m venv your-venv-name
source your-venv-name/bin/activate
```

## Install dependencies

```bash
pip install -r requirements/base.txt
```

## Configure environment

Create `.env`

Example:

```env
SECRET_KEY=your-django-given-key
DEBUG=True
```

## Apply migrations

```bash
python manage.py migrate
```

## Run server

```bash
python manage.py runserver
```
