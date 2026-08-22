from django.urls import path
from . import views

urlpatterns = [
    path('store/<slug:brand_slug>/', views.store_view, name='store'),
    
    # Products
    path('dashboard/products/', views.manage_products_view, name='manage_products'),
    path('dashboard/products/new/', views.create_product_view, name='create_product'),
    path('dashboard/products/<int:product_id>/', views.product_detail_view, name='product_detail'),
    path('dashboard/products/<int:product_id>/edit/', views.edit_product_view, name='edit_product'),
    path('dashboard/products/<int:product_id>/delete/', views.delete_product_view, name='delete_product'),
    path('dashboard/variants/<int:variant_id>/edit/', views.edit_variant_view, name='edit_variant'),
    path('dashboard/variants/<int:variant_id>/delete/', views.delete_variant_view, name='delete_variant'),
    
    # Catalog Settings (Categories, Types, Colors, Sizes)
    path('dashboard/catalog-settings/', views.catalog_settings_view, name='catalog_settings'),
    path('dashboard/catalog-settings/quick-create/', views.quick_create_attr, name='quick_create_attr'),
    
    # Collections
    path('dashboard/collections/', views.manage_collections_view, name='manage_collections'),
    path('dashboard/collections/<int:collection_id>/edit/', views.edit_collection_view, name='edit_collection'),
]
