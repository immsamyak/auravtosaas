# Aura SaaS Application Installation Manual

## 1. Prerequisites
- Python 3.12+
- pip and virtual environment support
- PostgreSQL (recommended for parity with production)
- Git
- Optional: Docker (for containerized deployment)

## 2. Clone Repository
```bash
git clone https://github.com/immsamyak/auravtosaas.git
cd auravtosaas/backend
```

## 3. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Environment Configuration
Create a `.env` file in `/home/runner/work/auravtosaas/auravtosaas/backend` (or export variables in your runtime):

| Variable | Purpose |
| --- | --- |
| `SECRET_KEY` | Django secret key |
| `DJANGO_DEBUG` | Set `True` for local debug |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts |
| `DATABASE_URL` | Database connection URL |
| `STRIPE_PUBLIC_KEY` | Stripe public key |
| `STRIPE_SECRET_KEY` | Stripe secret key |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook secret |
| `REPLICATE_API_TOKEN` / HF token | VTO provider token(s), depending on selected engine |
| `REDIS_URL` (optional) | Redis connection for cache/tasks |
| `USE_REDIS` (optional) | `true` to switch cache backend to Redis |

## 5. Database and Static Setup
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

## 6. Run Local Server
```bash
python manage.py runserver
```
Open `http://127.0.0.1:8000`.

## 7. Docker Installation
From repository root:
```bash
docker build -t aura-app .
docker run -d -p 8000:80 --env-file backend/.env aura-app
```

## 8. Production Notes
- Use `DJANGO_ENV=production`.
- Set secure values for all secrets and payment keys.
- Use PostgreSQL and persistent media/static strategy.
- Configure reverse proxy and HTTPS termination.
- Run `python manage.py migrate` on deploy.

## 9. Verification Checklist
- Home page loads.
- Login works for admin/brand/customer roles.
- Dashboard and storefront routes are reachable.
- Product creation and checkout page load correctly.
- VTO request path works when provider credentials are valid.
