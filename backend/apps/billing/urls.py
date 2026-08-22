from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/billing/', views.owner_billing_view, name='owner_billing'),
    path('dashboard/billing/checkout/<int:plan_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('api/billing/webhook/', views.stripe_webhook, name='stripe_webhook'),
]
