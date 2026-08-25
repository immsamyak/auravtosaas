# Aura SaaS - Demo Credentials

To fully explore the Aura Virtual Try-On SaaS Platform, we have set up three distinct roles. Please use the safe credentials below to access the platform.

**Base URL**: `https://aura.alvicsxinfo.tech`

## 1. System Administrator
Explore the Django superuser portal for global settings, tenant management, and platform-wide configurations.
- **Login URL**: `https://aura.alvicsxinfo.tech/admin/login`
- **Username**: `admin`
- **Password**: `admin`
- **Role Permissions**: Full access to global database tables, brand management, user control, and global UI settings.

## 2. Brand Owner (Vendor)
Explore the multi-tenant SaaS dashboard where brands can manage their specific storefront, upload products, and process orders.
- **Login URL**: `https://aura.alvicsxinfo.tech/login`
- **Username**: `alvics`
- **Password**: `12345678`
- **Role Permissions**: Isolated dashboard access, product/variant creation, store settings, order fulfillment. Cannot access other brands' data (IDOR protected).

## 3. Customer (Shopper)
Explore the storefront, product discovery, and the VTO (Virtual Try-On) interface.
- **Login URL**: `https://aura.alvicsxinfo.tech/accounts/login/`
- **Username**: `demo_customer`
- **Password**: `customer123`
- **Role Permissions**: Storefront browsing, profile management, fit profile setup, VTO generation requests, checkout.

---

### Important Notes for Reviewers:
1. **Security Constraints**: The system relies on strict IDOR and RBAC protections. Try accessing the `/admin/` URL while logged in as a Brand Owner—you will be correctly rejected with a `403 Forbidden` error.
2. **Configuration Blocks**: If the VTO image generation fails or the Checkout webhook stalls during the demo, this is because the environment variables (`REPLICATE_API_TOKEN` for Stable Diffusion and Stripe API Keys) require your actual production keys to be configured via the `.env` file. We do not expose our production API keys in the demo package.
