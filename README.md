# Boutique

Boutique is a bilingual Django storefront for Kalkan Nilüfer Butik. It includes a product catalog, variant-aware cart, bank-transfer checkout, customer accounts, order history, password recovery, and a staff-only content management panel.

The interface and catalog content support Turkish and English. Turkish is the default language.

## Features

- Bilingual Turkish/English storefront and catalog content
- Homepage sections for featured products, new arrivals, and categories
- Product categories, detail pages, image galleries, sizes, and colors
- Guest and authenticated shopping carts
- Checkout with email, phone, delivery address, and bank-transfer instructions
- Customer registration, login, profile, logout, and order history
- Password reset by email through SMTP
- Privacy policy, terms, and cookie policy pages
- Staff panel for products, categories, galleries, and site content
- Django admin for orders, users, and underlying data

## Technology

- Python 3.12 or newer
- Django 5.2
- PostgreSQL via Docker Compose (SQLite remains the local default without `.env` database settings)
- Pillow for uploaded images
- environs / python-dotenv for `.env` configuration
- Celery and Redis for asynchronous email delivery
- Django templates, CSS, and vanilla JavaScript
- uv for dependency and environment management

## Project structure

```text
boutique/   Django project settings and root URLs
core/       Homepage, site settings, and legal pages
catalog/    Categories, products, variants, and product images
cart/       Guest/user carts and checkout
orders/     Orders, order items, order history, and admin
users/      Registration, profiles, authentication, and password reset
panel/      Staff-only content management panel
templates/  Django HTML templates
static/     CSS and JavaScript
locale/     Turkish translation catalog
media/      Uploaded images (created locally and ignored by Git)
```

## Local installation

Install [uv](https://docs.astral.sh/uv/), clone the repository, and run:

```bash
cp .env.example .env
uv sync
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

The storefront is then available at `http://127.0.0.1:8000/`.

## Docker Compose

The included Compose configuration starts Django and PostgreSQL with persistent database storage. The local `.env` contains generated database credentials and is ignored by Git.

```bash
docker compose up --build
```

The storefront is then available at `http://127.0.0.1:8000/`. Stop the services with `docker compose down`; use `docker compose down -v` only when the PostgreSQL data volume should also be removed.

Useful local URLs:

- `/tr/` — Turkish storefront
- `/en/` — English storefront
- `/manage/` — staff content panel
- `/tr/admin/` — Django admin in Turkish
- `/en/admin/` — Django admin in English

The `/manage/` panel requires a user with staff status. A superuser created with `createsuperuser` has the required access.

## Environment variables

Copy `.env.example` to `.env`. Never commit `.env`; it can contain the Django secret key, mail credentials, and bank details.

| Variable | Purpose | Example/default |
| --- | --- | --- |
| `SECRET_KEY` | Django cryptographic signing key | Generate a unique, long random value |
| `DEBUG` | Enables development debug mode | `True` locally, `False` in production |
| `ALLOWED_HOSTS` | Comma-separated accepted hostnames | `127.0.0.1,localhost` |
| `LANGUAGE_CODE` | Default interface language | `tr` |
| `STATIC_URL` | Public prefix for static assets | `/static/` |
| `POSTGRES_DB` | PostgreSQL database name used by Compose | Generate a local value |
| `POSTGRES_USER` | PostgreSQL user used by Compose | Generate a local value |
| `POSTGRES_PASSWORD` | PostgreSQL password used by Compose | Generate a unique value |
| `DATABASE_URL` | Django database connection URL used when `DEBUG=False`; debug mode always uses SQLite | PostgreSQL URL in Compose |
| `EMAIL_BACKEND` | Django email backend | SMTP backend |
| `EMAIL_HOST` | SMTP server | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_USE_TLS` | Enables STARTTLS | `True` |
| `EMAIL_HOST_USER` | Gmail/SMTP login address | Store email address |
| `EMAIL_HOST_PASSWORD` | Google app password | Never use the regular Google password |
| `DEFAULT_FROM_EMAIL` | Sender shown in password-reset mail | Store name and email |
| `PASSWORD_RESET_TIMEOUT` | Reset-link lifetime in seconds | `3600` |
| `BANK_TRANSFER_IBAN` | IBAN shown at checkout | Store bank account IBAN |
| `BANK_TRANSFER_RECIPIENT` | Bank transfer recipient | Account holder name |
| `CELERY_BROKER_URL` | Redis queue connection | `redis://redis:6379/0` |
| `CELERY_RESULT_BACKEND` | Celery task result storage | `redis://redis:6379/1` |

Generate a Django secret key, for example, with:

```bash
uv run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Gmail password recovery setup

Password recovery uses Django's SMTP email backend. For Gmail:

1. Enable two-step verification on the Google account.
2. Create a Google app password.
3. Put the Gmail address in `EMAIL_HOST_USER`.
4. Put the app password in `EMAIL_HOST_PASSWORD`. Spaces in the copied password are accepted.
5. Set `DEFAULT_FROM_EMAIL` to the sender name and the same verified address.

The reset link is valid for `PASSWORD_RESET_TIMEOUT` seconds. Django only sends reset mail for active users with a usable password and a matching email address. Existing accounts created before email became mandatory must have an email added through Django admin.

For local development without sending real email, temporarily use:

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

Reset emails will then be printed in the server terminal.

## Initial content

Optional sample Turkish/English categories and products can be created with:

```bash
uv run python manage.py seed_products
```

The command is safe to run repeatedly because it updates records by slug.

Site name, taglines, contact information, homepage images, and About text can be edited under `/manage/site-settings/`. Products, categories, featured/new flags, variants, and gallery images are managed in the same staff panel.

## Store and order flow

Guests can browse products and maintain a session-based cart. Checkout requires authentication. During checkout, the customer provides a valid email, phone number, and delivery address. Creating an order clears the cart and displays the configured bank-transfer details.

Orders begin with the `new` status. Staff can change an order to `paid` or `shipped` through Django admin. Customers can see their own order history from their profile/orders pages.

This project displays bank-transfer instructions; it does not currently integrate a card payment gateway or automatically confirm transfers.

## Localization

Translatable interface strings use Django i18n. Catalog categories and products have separate Turkish and English fields. When English content is empty, the Turkish content is used as a fallback.

After changing translatable strings, rebuild the Turkish message catalog:

```bash
uv run python manage.py makemessages -l tr
uv run python manage.py compilemessages -l tr
```

## Tests and checks

Run the complete test suite and Django configuration check with:

```bash
uv run python manage.py test
uv run python manage.py check
```

For deployment-oriented security warnings, run:

```bash
uv run python manage.py check --deploy
```

## Production notes

Before deployment:

- Set `DEBUG=False`.
- Use a new production-only `SECRET_KEY`.
- Set `ALLOWED_HOSTS` to the real domain names.
- Serve the application exclusively over HTTPS.
- Configure secure session/CSRF cookies and the reverse proxy correctly.
- Run `uv run python manage.py collectstatic`.
- Persist and back up the database and uploaded `media/` directory.
- Consider PostgreSQL instead of SQLite for concurrent production traffic.
- Verify Gmail SMTP sending and the public domain used in reset links.
- Keep `.env`, database files, uploads, and backups outside version control.

The current repository ignores `.env`, SQLite database files, virtual environments, and uploaded media.
