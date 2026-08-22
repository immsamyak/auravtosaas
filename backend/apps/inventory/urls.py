from django.urls import path
from . import views

urlpatterns = [
    path('warehouses/', views.manage_warehouses_view, name='manage_warehouses'),
    path('warehouses/<int:location_id>/', views.warehouse_detail_view, name='warehouse_detail'),
]
