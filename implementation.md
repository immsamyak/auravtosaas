# Aura Platform Implementation Details

## Architecture Transition
The initial prototype was a monolithic Django app (`api`). It has been successfully refactored into a scalable, enterprise-grade modular structure within an `apps/` directory.

## Core Applications

### 1. `apps.accounts`
- **Models**: `ConsumerProfile` (1-to-1 with `User`).
- **Views**: Registration, login, logout, and the consumer profile management page.
- **Responsibility**: All user-level identity management.

### 2. `apps.brands`
- **Models**: `Brand` (1-to-1 with `User` for ownership).
- **Views**: The main SaaS dashboard and public landing page.
- **Responsibility**: Tenant isolation and brand-specific settings.

### 3. `apps.catalog`
- **Models**: `Garment`, `GarmentVariant`.
- **Views**: Product CRUD (Create, Edit, Delete Garments and Variants), Storefront browsing.
- **Responsibility**: Inventory and product display.

### 4. `apps.fitting`
- **Models**: `VirtualTryOn`.
- **Views**: The iframe-based slide-over try-on experience.
- **Responsibility**: AI generation abstraction and try-on persistence. 
- **Architecture**: Utilizes `MockGenerativeProvider` under `providers/` to decouple the AI implementation from the HTTP request cycle.

### 5. `apps.recommendations`
- **Models**: `SizeRecommendation`.
- **Engine**: Contains the `analyze_body_proportions` mock CV script.

### 6. `apps.analytics`
- **Services**: `DashboardAnalyticsService`.
- **Responsibility**: Extracts complex Django ORM aggregation logic (Try-on counts, conversion rates, AI confidence averages) away from the view layer.

### 7. `apps.shopping` & `apps.orders`
- Placeholders for future Phase 2 checkout flows. Currently scaffolded to maintain architectural completeness.

## Data Layer & Multi-Tenancy
- Powered by PostgreSQL 16.
- Multi-tenancy is enforced at the view layer by filtering all querysets by the authenticated user's `owned_brand` relation. No brand can mutate another's catalog.

## Frontend
- Vanilla Django Templates reorganized into app-specific folders (e.g., `apps/catalog/templates/catalog/`).
- Styled using a comprehensive Tailwind CSS setup.

## Next Steps
- Implement DRF Serializers across the `apps/` stack.
- Expand test coverage.
