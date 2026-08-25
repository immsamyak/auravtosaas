# Aura Feature Matrix

This matrix provides a transparent and honest breakdown of features across the three core roles within the Aura SaaS platform.

| Feature | Admin | Brand Owner | Customer | Status | Notes |
| :--- | :---: | :---: | :---: | :--- | :--- |
| **Authentication & RBAC** | | | | | |
| Secure Login & Logout | &check; | &check; | &check; | Implemented | Uses Django session auth |
| Cross-Tenant IDOR Protection | &check; | &check; | 🚫 | Implemented | Tested; 403/404 enforced |
| Registration | 🚫 | 🚫 | &check; | Implemented | Customer signup available |
| Password Reset Workflow | 🚫 | 🚫 | 🚫 | Coming Soon | SMTP configuration pending |
| **Storefront & Catalog** | | | | | |
| Browse Products | &check; | &check; | &check; | Implemented | |
| View Product Details | &check; | &check; | &check; | Implemented | Includes variant display |
| Select Colors / Sizes | 🚫 | 🚫 | &check; | Implemented | |
| Create & Manage Products | &check; | &check; | 🚫 | Implemented | Requires Brand relationship |
| Manage Categories | &check; | &check; | 🚫 | Implemented | |
| **Virtual Try-On (VTO)** | | | | | |
| Upload Customer Photo | 🚫 | 🚫 | &check; | Implemented | Image processing pipeline |
| Create Fit Profile | 🚫 | 🚫 | &check; | Implemented | Stores user measurements |
| Request VTO Generation | 🚫 | 🚫 | &check; | Configuration Required | Requires `REPLICATE_API_TOKEN` |
| View VTO Result History | 🚫 | 🚫 | &check; | Implemented | Fetches from DB/Storage |
| **Commerce & Orders** | | | | | |
| Add to Cart | 🚫 | 🚫 | &check; | Implemented | |
| Execute Checkout Payment | 🚫 | 🚫 | &check; | Configuration Required | Requires Stripe Webhook keys |
| View Order History | &check; | &check; | &check; | Implemented | Filtered by object ownership |
| Manage Order Fulfillment | &check; | &check; | 🚫 | Implemented | Status updates |
| **Platform Management** | | | | | |
| Manage Brand Stores | &check; | &check; | 🚫 | Implemented | Owners manage own store only |
| Global Settings Configuration | &check; | 🚫 | 🚫 | Implemented | Superuser only |
| Create/Suspend Users | &check; | 🚫 | 🚫 | Implemented | |

### Status Definitions:
- **Implemented**: Fully functional in the provided codebase.
- **Configuration Required**: The architecture and codebase exist, but the feature requires the buyer to supply their own external API keys (e.g., Stripe, Replicate, AWS) in the `.env` file to function.
- **Blocked**: Currently non-functional due to missing dependencies.
- **Coming Soon**: Not yet implemented in v1.0.0.
