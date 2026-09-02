# Aura SaaS User Manual

## 1. Purpose
This manual explains daily operation of the Aura platform for each user role.

## 2. User Roles
- **System Admin**: platform-wide management and configuration.
- **Brand Owner**: brand storefront, products, orders, marketing, and settings.
- **Customer**: shopping, account, Virtual Try-On, and checkout.

## 3. Getting Started
1. Open the application URL.
2. Sign in from `/login/` (or role-specific entry points).
3. Confirm you land on the role-appropriate dashboard or storefront.

## 4. System Admin Guide
### Main Responsibilities
- Manage global settings and platform-level entities.
- Review user and brand records.
- Monitor platform-wide operations.

### Typical Workflow
1. Log in as admin.
2. Open admin dashboards/settings.
3. Update global configuration (e.g., payment/VTO defaults).
4. Review audit logs and content modules as needed.

## 5. Brand Owner Guide
### Catalog Management
1. Go to `Dashboard > Products`.
2. Create a product with category/type and media.
3. Add variants (size, color, stock, price).
4. Publish and verify on storefront.

### Store Operations
- Use dashboard modules for orders, returns, shipping, and customers.
- Manage store settings (theme, branding, and content blocks).
- Use marketing tools for coupons, popups, campaigns, and subscribers.

### Billing
1. Open `Dashboard > Billing`.
2. Select a plan.
3. Complete checkout and verify subscription status.

## 6. Customer Guide
### Shopping
1. Browse brand storefront and product pages.
2. Select preferred size/color variant.
3. Add to cart and proceed to checkout.

### Virtual Try-On
1. Open a product variant with try-on support.
2. Upload your photo in the try-on flow.
3. Submit request and wait for generation.
4. View output and saved looks in wardrobe/history.

### Orders
- Track order using tracking page and order references.
- Submit return request for eligible orders.

## 7. Troubleshooting
- **Cannot access dashboard**: confirm account role and authentication state.
- **Try-On not generating**: check VTO provider/API token configuration.
- **Payment verification failed**: confirm gateway keys/webhooks.
- **Missing media/static assets**: ensure static collection and media path setup are correct.
