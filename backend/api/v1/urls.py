from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views

from apps.brands import api as brands_api

router = DefaultRouter()
router.register(r'brands', views.BrandViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'try-ons', views.VirtualTryOnViewSet, basename='tryon')

urlpatterns = [
    path('', include(router.urls)),
    
    # Custom Brand Authenticated Endpoints
    re_path(r'^brand/collections/?$', brands_api.collections_api, name='brand_collections_api'),
    re_path(r'^brand/products/?$', brands_api.products_api, name='brand_products_api'),
    re_path(r'^brand/products/(?P<product_id>\d+)/?$', brands_api.single_product_api, name='brand_single_product_api'),
    re_path(r'^brand/orders/?$', brands_api.orders_api, name='brand_orders_api'),
    re_path(r'^brand/orders/history/?$', brands_api.order_list_api, name='brand_orders_history_api'),
]
