# Aura Application Installation Manual

## 1. Prerequisites
- Linux/macOS terminal (or WSL on Windows)
- Python 3.12+
- pip and virtualenv
- PostgreSQL (optional for local, recommended for production-like setup)
- Git
- Docker (optional for container deployment)

## 2. Local Installation (Python)
1. Clone repository and move to backend
   ```bash
   git clone https://github.com/immsamyak/auravtosaas.git
   cd auravtosaas/backend
   ```
2. Create and activate virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables (recommended)
   ```bash
   export SECRET_KEY='replace-me'
   export DJANGO_DEBUG='True'
   export DATABASE_URL='sqlite:///db.sqlite3'
   ```
5. Run migrations
   ```bash
   python manage.py migrate
   ```
6. Create admin user (optional)
   ```bash
   python manage.py createsuperuser
   ```
7. Start development server
   ```bash
   python manage.py runserver
   ```

## 3. Optional Integrations
- `REPLICATE_API_TOKEN` for real VTO generation
- `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` for payment flows
- `USE_REDIS=true` and `REDIS_URL` to enable Redis-backed cache/channel patterns

## 4. Docker Installation
1. Build image from repository root
   ```bash
   docker build -t aura-app .
   ```
2. Run container
   ```bash
   docker run -d -p 8000:8000 --env-file .env aura-app
   ```
3. Access application at `http://localhost:8000`

## 5. Post-Installation Verification
- Open home page and storefront
- Log in as customer and brand owner
- Verify product pages, cart, and order views
- If configured, verify VTO request and checkout flow

## 6. Common Setup Issues
- **Database connection failures**: verify `DATABASE_URL` and DB service status
- **Static files missing in production**: ensure static pipeline runs during deployment
- **External integration errors**: verify API keys and webhook/network settings
