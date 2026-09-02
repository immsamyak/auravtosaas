# Aura - Virtual Try-On SaaS Commerce Platform

Aura is a modern, multi-tenant Django platform built for fashion brands and technology startups to offer Virtual Try-On (VTO) and digital storefront experiences. It features a complete Role-Based Access Control (RBAC) architecture isolating Customers, Brand Owners, and System Administrators.

## Overview

Aura is a complete out-of-the-box marketplace architecture where:
- **System Admins** oversee the entire platform and users.
- **Brand Owners** operate their own isolated dashboards, managing their product catalog, variations (colors/sizes), and orders.
- **Customers** browse products, generate Virtual Try-On previews using their personal fit profiles, and purchase apparel.

## Documentation Overview

- [Project Plan](./PROJECT_PLAN.md)
- [UML Diagram](./UML_DIAGRAM.md)
- [System Architecture](./SYSTEM_ARCHITECTURE.md)
- [User Manual](./USER_MANUAL.md)
- [Application Installation Manual](./APPLICATION_INSTALLATION_MANUAL.md)

## Key Features

- **Multi-Role Architecture:** Admin, Brand Owner, and Customer isolation.
- **VTO Integration Engine:** Backend pipeline ready for external Stable Diffusion/Replicate APIs to generate customer clothing previews.
- **Advanced Catalog:** Support for complex product variants (combinations of sizes, colors, and stock).
- **Security-First:** Proven IDOR (Insecure Direct Object Reference) prevention. Brands cannot access or mutate competitor data.
- **Modern UI:** Built heavily on Tailwind CSS for fully responsive and beautiful interfaces.
- **Commerce Ready:** Pre-built checkout flows and order tracking modules.

## Technology Stack

- **Backend Framework:** Python 3.12 / Django 5+
- **Database:** PostgreSQL (with SQLite for local development)
- **Frontend:** HTML5, Tailwind CSS, minimal vanilla JavaScript
- **Deployment:** Docker, Gunicorn, WhiteNoise (for static file serving)

## Server Requirements

| Requirement | Minimum | Recommended (Production) |
| :--- | :--- | :--- |
| **CPU** | 1 Core | 2+ Cores |
| **RAM** | 1 GB | 2 GB+ |
| **Storage** | 10 GB | 20 GB+ (SSD highly recommended for media) |
| **OS** | Linux (Ubuntu/Debian) | Linux (Ubuntu 22.04 LTS) |
| **Software** | Docker & Docker Compose | Docker & Docker Compose |

*(Note: The internal application runs headless backend ML queues. If you wish to run your own local Stable Diffusion weights rather than hitting the Replicate API, a dedicated GPU server is required.)*

## Installation & Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo> aura
   cd aura/backend
   ```

2. **Setup Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Database Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## Environment Variables (.env)

Aura utilizes `.env` files for configuration. The following variables dictate the application behavior:

| Variable | Purpose | Required? | Example | Security Note |
| :--- | :--- | :--- | :--- | :--- |
| `SECRET_KEY` | Django cryptographic key | **YES** | `django-insecure-xxx` | NEVER expose |
| `DEBUG` | Enable debug mode | **YES** | `False` | MUST be `False` in prod |
| `DATABASE_URL` | PostgreSQL connection string | Optional | `postgres://user:pass@host/db` | Keep private |
| `REPLICATE_API_TOKEN` | Generates VTO Images | **Required for VTO** | `r8_abc123` | Do not commit |
| `STRIPE_SECRET_KEY` | Processes Orders | **Required for Commerce**| `sk_test_xxx` | Do not commit |

## Virtual Try-On (VTO) Configuration Status

Aura ships with the internal workflow and database architecture to handle VTO. **However, external ML image generation is NOT included out-of-the-box.** 

- **AVAILABLE:** The user interface, the queuing system, the customer fit profile database, and the image upload architecture.
- **CONFIGURATION REQUIRED:** You MUST supply a valid `REPLICATE_API_TOKEN` in your `.env` for the platform to actually ping the Stable Diffusion model and receive generated images. Without this token, the VTO feature will safely block itself.

## Production Deployment (Docker)

Aura is production-ready via Docker.

```bash
cd aura
docker build -t aura-app .
docker run -d -p 8000:8000 --env-file .env aura-app
```
*(For full production, we recommend deploying behind a reverse proxy like Traefik, Caddy, or Nginx with Let's Encrypt SSL certificates.)*

## Demo & Testing

For marketplace review, please reference `DEMO_CREDENTIALS.md` for safe usernames and passwords to explore the various permission roles.

## License & Support
For installation and configuration support, please contact the developer profile directly. Extensive custom ML model integration (beyond the provided Replicate API structure) falls outside standard support.
