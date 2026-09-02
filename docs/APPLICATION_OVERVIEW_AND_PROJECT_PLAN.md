# Aura Virtual Try-On SaaS — Complete Application Overview

## 1. Product Summary
Aura is a multi-tenant Django-based SaaS platform for fashion commerce with integrated Virtual Try-On (VTO) workflows. The platform supports three primary personas:
- **System Admin**: platform-wide governance and operations
- **Brand Owner**: store management, products, inventory, and order fulfillment
- **Customer**: storefront browsing, try-on experience, checkout, and order tracking

## 2. Business Goals
- Enable brands to launch digital storefronts with minimal setup
- Improve purchase confidence using fit profiles and AI-assisted preview generation
- Keep tenant data isolated for security and privacy
- Provide an extensible architecture for billing, analytics, and future integrations

## 3. Functional Scope
### Customer-facing
- Authentication and profile setup
- Product browsing, product details, variant selection
- Fit profile creation and VTO request flow
- Cart and checkout
- Order history and tracking

### Brand-facing
- Product and variant CRUD
- Inventory and order operations
- Store settings and dashboard analytics

### Admin-facing
- Platform administration and user/store oversight
- Global operational controls and audit support

## 4. Non-Functional Scope
- Multi-tenant access control
- Production-ready deployment using Docker + Gunicorn + WhiteNoise
- Optional PostgreSQL and Redis-backed scalability components
- Extensible asynchronous capabilities through Channels and Celery-ready settings

## 5. Project Plan
### Phase 1 — Foundation (Completed)
- Core Django project setup and modular app structure
- Role-based workflows and tenant boundaries
- Catalog, fitting, orders, inventory, and billing routing

### Phase 2 — Operational Hardening (In Progress)
- Expand automated tests for critical user flows
- Strengthen observability for fitting and checkout paths
- Validate production environment defaults and deployment checklists

### Phase 3 — Product Expansion (Planned)
- API-first surfaces for integrations
- Enhanced recommendation and analytics intelligence
- Additional payment, shipping, and notifications integrations

## 6. Deliverables in this Documentation Set
- Project overview and plan (this file)
- UML diagrams (`UML_DIAGRAM.md`)
- System architecture (`SYSTEM_ARCHITECTURE.md`)
- User manual (`USER_MANUAL.md`)
- Installation manual in Markdown and PDF (`INSTALLATION_MANUAL.md`, `INSTALLATION_MANUAL.pdf`)
