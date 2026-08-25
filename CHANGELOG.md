# Changelog

All notable changes to the Aura SaaS platform will be documented in this file.

## [v1.0.0] - 2026-08-24
### Added
- **Multi-Role Authentication**: Complete architecture for System Admins, Brand Owners (Vendors), and Customers.
- **Admin Dashboard**: Global platform configuration, user suspension, and tenant oversight.
- **Brand Owner Dashboard**: Isolated analytics, order management, and store configuration settings.
- **Catalog Management**: Creation and editing of Products, Variants, Sizes, and Colors.
- **Storefront**: Responsive Tailwind CSS frontend for product discovery, categories, and shopping.
- **Customer Profiles**: Saved fit profiles and Virtual Try-On (VTO) request history.
- **VTO Architecture**: Complete photo processing pipeline and queuing system for Replicate API / Stable Diffusion generation.
- **Commerce API**: Cart functionality and Khalti/Stripe checkout webhook integration endpoints.
- **Security**: Complete Cross-Tenant IDOR protection and comprehensive input sanitization (XSS protected).
- **Deployment**: Dockerized production setup with Gunicorn and reverse-proxy ready configurations.
