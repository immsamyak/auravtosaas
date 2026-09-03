# AURA - Virtual Try-On Multi-Tenant SaaS Platform

AURA is an enterprise-grade, multi-tenant B2B2C e-commerce platform built specifically for modern fashion brands. It features advanced **AI Virtual Try-On (VTO)** capabilities, allowing customers to visualize garments on their own personal fit profiles before purchasing.

**Subject:** DBMS
**Instructor:** Bikash Khadka
**Prepared & Developed by:** Samyak K. Chaudhary

---

> [!CAUTION]
> ## ⚠️ LEGAL DISCLAIMER & COPYRIGHT NOTICE
> **This repository contains proprietary, commercial software.** 
> AURA is a premium commercial product intended for exclusive distribution and sale via **CodeCanyon / Envato Market**. 
> 
> This source code is being made temporarily accessible **STRICTLY for the purpose of academic evaluation and assignment grading** by the designated instructor/institution. 
> 
> **UNAUTHORIZED USE IS STRICTLY PROHIBITED.** You may not copy, fork, distribute, share, or repurpose any part of this codebase for personal or commercial use. Any unauthorized sharing, piracy, or intellectual property theft will be subject to strict legal action and penalty.

---

## 📖 Complete Project Documentation

For a comprehensive breakdown of the project—including the Project Plan, UML Diagrams (Use Case, Sequence, Class, State, Activity, Component), System Architecture, Database Entity-Relationship (ER) model, and a visual User Manual—please open the official documentation file:

👉 **[docs/AURA_Documentation.pdf](docs/AURA_Documentation.pdf)**

*(Simply double-click the HTML file to open it in any web browser. It contains all architectural diagrams and live workflow screenshots.)*

---

## 🌟 Platform Overview

AURA is engineered with a strict **Role-Based Access Control (RBAC)** architecture that isolates three primary user groups:

1. **System Administrators:** Oversee the entire SaaS platform, manage global integrations, approve new tenant brands, and monitor platform health.
2. **Brand Owners (Tenants):** Operate their own isolated dashboards. They can manage their custom product catalog, upload high-resolution AI masks for garments, track orders, and customize their digital storefront themes.
3. **Customers:** Browse tenant storefronts, generate highly accurate Virtual Try-On previews using their personal fit passports (height/weight), and seamlessly purchase apparel through an encrypted checkout flow.

## 🔑 Demo Credentials

To evaluate the platform, use the following pre-configured credentials:

- **Admin Login:** `admin` / `admin`
- **Brand Owner Login:** `alvy` / `12345678`

## 🚀 Key Features

- **Multi-Tenant Isolation:** Complete data separation for individual brands, preventing any cross-tenant data leaks (IDOR prevention).
- **VTO Integration Engine:** A sophisticated pipeline designed to generate customer clothing previews via AI processing.
- **Dynamic Storefronts:** Brands can select UI themes and customize their digital presence dynamically.
- **Advanced Catalog & Inventory:** Support for complex product variants (size/color matrix) with real-time stock deductions.
- **Secure Commerce Flow:** PCI-compliant ready checkout architecture with dynamic shipping and discount configurations.

## 💻 Technology Stack

- **Backend Framework:** Python 3.12 & Django 5+
- **Database:** PostgreSQL (production) / SQLite (local dev fallback)
- **Caching & Queues:** Redis & Celery (for asynchronous VTO processing)
- **Frontend Engine:** HTML5, Tailwind CSS, Alpine.js (for reactive storefront components)
- **Deployment & Infra:** Docker, Gunicorn, WhiteNoise

## 🛠️ Local Development Setup

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

3. **Environment Configuration (.env)**
   Create a `.env` file in the `backend/` directory:
   ```env
   SECRET_KEY=your-secure-django-key
   DJANGO_DEBUG=True
   # DATABASE_URL=sqlite:///db.sqlite3  (Defaults to local SQLite)
   ```

4. **Restore Database (Required)**
   Do NOT run `python manage.py migrate` on a fresh database, as you will lose the pre-configured mock data, AI models, and user roles. Instead, restore the provided SQL dump:
   ```bash
   # From the project root
   cd ../database
   ./migrate.sh postgres://user:password@localhost:5432/aura_db
   cd ../backend
   ```

5. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

## 🔐 Environment Variables (.env) Reference

AURA utilizes `.env` files for core infrastructure configuration. Integrations (like Stripe for payments or Twilio for SMS) are **not** stored here; they are managed dynamically per-tenant in the Database for maximum security and multi-tenant flexibility.

| Variable | Purpose | Required? | Example |
| :--- | :--- | :--- | :--- |
| `SECRET_KEY` | Django cryptographic key | **YES** | `django-insecure-xxx` |
| `DJANGO_DEBUG` | Enable debug mode | **YES** | `True` or `False` |
| `DATABASE_URL` | DB Connection string | No | `postgres://user:pass@host/db` |
| `REDIS_URL` | Redis for Celery & Cache | No | `redis://localhost:6379/1` |

## 📦 Docker Deployment (Recommended)

AURA is completely container-ready. The included `Dockerfile` bundles the Python environment, ML models, and a robust WSGI server (Gunicorn) running on internal port 80.

### 1. Build the Docker Image
From the root of the project (where the `Dockerfile` is located), build the image. *(Note: This may take several minutes as it downloads large ML libraries like PyTorch).*
```bash
docker build -t aura-app .
```

### 2. Run the Container
You need to pass your local `.env` file to the container. If you are running PostgreSQL on your local Mac/Windows host machine, you **must** override the database URL to point to `host.docker.internal` instead of `localhost`, and specify your computer's OS username (e.g., `postgres://<your-mac-username>@host.docker.internal:5432/aura_db`) so the container doesn't try to log in as `root`.

```bash
docker run -d -p 8000:80 --env-file backend/.env -e DATABASE_URL="postgres://YOUR_MAC_USERNAME@host.docker.internal:5432/aura_db" aura-app
```
*(Replace `YOUR_MAC_USERNAME` with your actual computer username).*

### 3. Verify & Access
Once running, open your browser and navigate to:
👉 **http://localhost:8000/**

To check the live server logs:
```bash
docker logs -f <container_id>
```

To stop the container:
```bash
docker rm -f <container_id>
```
