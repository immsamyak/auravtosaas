# Aura System Architecture

## 1. Architectural Style
Aura follows a modular monolithic architecture on Django with clearly separated domain apps. It is designed for multi-tenant SaaS operation with role-based boundaries and secure queryset scoping.

## 2. Core Layers
1. **Presentation Layer**: Django templates, Tailwind CSS, and URL routing
2. **Application Layer**: app-specific views/services for accounts, brands, catalog, fitting, orders, inventory, billing, and analytics
3. **Domain/Data Layer**: Django models and ORM persistence
4. **Integration Layer**: Stripe (billing), Replicate (VTO generation), optional Redis/Channels/Celery integrations

## 3. Main Modules
- `apps.accounts`: authentication and consumer profiles
- `apps.brands`: tenant ownership and brand-facing flows
- `apps.catalog`: garments, variants, categories, storefront browsing
- `apps.fitting`: virtual try-on orchestration and result storage
- `apps.orders`: customer and brand order workflows
- `apps.inventory`: stock and operational inventory flows
- `apps.billing`: checkout and payment flow hooks
- `apps.analytics`: dashboard metrics aggregation
- `apps.core`: shared middleware, context processors, and platform-level logic

## 4. Security and Isolation
- Request flows are authenticated through Django auth/session middleware
- Tenant-aware filtering is used to prevent cross-brand access
- Production deployment supports secure static delivery and environment-based secrets

## 5. Runtime and Deployment
- App server: Gunicorn / Daphne-ready setup
- Static assets: WhiteNoise
- Database: PostgreSQL (production), SQLite (local)
- Deployment packaging: Docker

## 6. Data and Event Considerations
- Transactional data (users, products, orders, fitting records) is persisted via ORM
- Real-time/websocket features are enabled by Channels architecture when configured
- Background processing scale-out is available through Celery + Redis configuration
