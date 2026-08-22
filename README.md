# Aura AI Virtual Fitting & Fashion Commerce Platform

## 1. Project Overview
Aura is a B2B SaaS platform that enables fashion brands to offer a Virtual Fitting Room experience directly on their storefronts. Using generative AI, customers can instantly try on clothes on their own photos, drastically improving conversion rates and reducing return rates.

## 2. Problem Statement
The fashion e-commerce industry suffers from a high rate of returns due to poor fit and visualization. Customers struggle to imagine how garments look on their unique body shapes. Traditional try-on solutions require expensive 3D body mapping, which is inaccessible to most mid-market brands.

## 3. Objectives
- Provide a seamless virtual try-on experience using generative AI.
- Enable brands to manage their catalogs and monitor try-on conversion analytics.
- Create a modular, highly scalable Django backend to support multi-tenancy.
- Deliver an aesthetically premium, Tailwind-powered user interface.

## 4. Features
### Public/Consumer Features
- **Brand Storefronts**: Dedicated storefronts for different brands.
- **Consumer Profiles**: Consumers can upload base photos for size analysis and try-ons.
- **Virtual Try-On**: Generate realistic try-on composites with AI.
- **Size Recommendation**: AI-driven analysis of shoulder and waist widths.

### SaaS/Brand Features
- **Brand Dashboard**: Track conversion rates, average AI confidence, and top-performing garments.
- **Catalog Management**: Full CRUD capabilities for Garments and Variants.
- **Multi-Tenant Architecture**: Strict data isolation between brands.

## 5. User Roles
- **Consumer**: Shoppers who browse brand storefronts and use the Virtual Fitting Room.
- **Brand Owner**: SaaS tenants who manage their brand's catalog and monitor analytics.
- **Platform Admin**: Superusers managing the global Aura infrastructure.

## 6. System Architecture
The platform is built as a single, modular Django application optimized for maintainability and clear separation of concerns. The architecture follows a strict Service Layer pattern to keep views thin.

## 7. Technology Stack
- **Backend**: Python 3.12, Django 5+
- **Database**: PostgreSQL 16
- **Frontend**: Vanilla HTML/JS, Tailwind CSS
- **AI/ML (Mock)**: Pillow-based image generation engine (abstracted via Provider pattern)

## 8. Database Architecture
PostgreSQL is used as the primary relational database. The schema is highly normalized with strong foreign key constraints to enforce tenant isolation.

## 9. ER Diagram Description
- `User` (1) --- (1) `ConsumerProfile`
- `User` (1) --- (1) `Brand` (Owner)
- `Brand` (1) --- (M) `Garment`
- `Garment` (1) --- (M) `GarmentVariant`
- `GarmentVariant` (1) --- (M) `VirtualTryOn`
- `User` (1) --- (M) `VirtualTryOn`

## 10. Application Structure
The monolith has been split into dedicated modular apps:
- `accounts`: User authentication and consumer profiles.
- `analytics`: Aggregation queries and metrics services.
- `brands`: Tenant isolation and brand dashboard views.
- `catalog`: Garment and Variant CRUD logic.
- `fitting`: Virtual try-on views and AI Provider abstractions.
- `recommendations`: Body analysis engines.
- `shopping`: Mock app ready for cart functionality.
- `orders`: Mock app ready for checkout functionality.
- `core`: Shared infrastructure.

## 11. Installation
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 12. Environment Configuration
Create a `.env` file in the root based on `.env.example`:
```
DEBUG=True
SECRET_KEY=your-secret
DB_NAME=aura_db
```

## 13. Database Setup
```bash
psql -c "CREATE DATABASE aura_db;"
python manage.py migrate
python manage.py createsuperuser
```

## 14. Running the Project
```bash
python manage.py runserver
```
Visit `http://localhost:8000/`

## 15. API Documentation
*To be implemented in Phase 2 using Django REST Framework in `apps/*/serializers.py`*.

## 16. Authentication
Uses Django's built-in session-based authentication for the web portal.

## 17. Multi-Tenant Architecture
Brand-specific views are isolated by checking `request.user.owned_brand`. A standard `get_object_or_404(Garment, id=id, brand=brand)` pattern is strictly enforced across the catalog.

## 18. AI Architecture
The AI integration is built on a Provider pattern:
`BaseVirtualTryOnProvider` -> `MockGenerativeProvider`. 
This allows swapping the mock implementation for a real API (like Stable Diffusion) via environment variables without changing business logic.

## 19. Testing
*To be implemented.*

## 20. Security
- Clickjacking protection via `XFrameOptionsMiddleware` (with specific `@xframe_options_sameorigin` exemptions for try-ons).
- Strict ORM isolation for tenant data.

## 21. Future Improvements
- DRF API for mobile apps.
- Real Stable Diffusion integration.
- Cart and Checkout flows.
# audavto
# audavto
