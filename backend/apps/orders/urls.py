from django.urls import path
from . import views, views_pos

urlpatterns = [
    path('checkout/<slug:brand_slug>/', views.storefront_checkout_view, name='storefront_checkout'),
    path('checkout/<slug:brand_slug>/validate-coupon/', views.validate_coupon_api, name='validate_coupon_api'),
    path('track/<slug:brand_slug>/', views.track_order_view, name='track_order'),
    path('order/<uuid:order_id>/return/', views.request_return_view, name='request_return'),
    path('dashboard/orders/', views.manage_orders_view, name='manage_orders'),
    path('dashboard/returns/', views.returns_list_view, name='returns_list'),
    path('dashboard/abandoned-carts/', views.abandoned_carts_view, name='abandoned_carts'),
    path('dashboard/shipping/', views.shipping_settings_view, name='shipping_settings'),
    path('order/success/<uuid:order_id>/', views.order_success_view, name='order_success'),
    path('checkout/esewa/verify/', views.checkout_esewa_verify, name='checkout_esewa_verify'),
    path('checkout/khalti/verify/', views.checkout_khalti_verify, name='checkout_khalti_verify'),
    path('checkout/stripe/verify/', views.checkout_stripe_verify, name='checkout_stripe_verify'),
    path('checkout/paypal/verify/', views.checkout_paypal_verify, name='checkout_paypal_verify'),
    path('checkout/razorpay/verify/', views.checkout_razorpay_verify, name='checkout_razorpay_verify'),
    path('checkout/stripe/webhook/<slug:brand_slug>/', views.stripe_webhook, name='stripe_webhook'),
    
    # POS Routes
    path('dashboard/pos/', views_pos.pos_terminal_view, name='pos_terminal'),
    path('dashboard/pos/customer-display/', views_pos.pos_customer_display_view, name='pos_customer_display'),
    path('api/pos/products/', views_pos.pos_api_products, name='pos_api_products'),
    path('api/pos/drafts/', views_pos.pos_api_drafts, name='pos_api_drafts'),
    path('api/pos/checkout/', views_pos.pos_checkout_api, name='pos_checkout_api'),
    path('api/pos/lookup-customer/', views_pos.pos_lookup_customer_api, name='pos_lookup_customer_api'),
    
    # CRM
    path('dashboard/customers/', views.manage_customers_view, name='manage_customers'),
    path('dashboard/customers/<int:customer_id>/', views.customer_detail_view, name='customer_detail'),
]

