from django.urls import path
from . import views

urlpatterns = [
    path('store/<slug:slug>/try-on/<slug:variant_slug>/', views.try_on_view, name='try_on'),
    path('store/<slug:slug>/try-on/<slug:variant_slug>/upload/', views.guest_photo_upload_view, name='guest_photo_upload'),
    path('store/<slug:slug>/try-on/status/<int:try_on_id>/', views.check_vto_status_view, name='check_vto_status'),
    path('store/<slug:slug>/wardrobe/', views.virtual_wardrobe_view, name='virtual_wardrobe'),
    path('api/wardrobe/save/', views.save_look_api, name='save_look_api'),
    path('api/outfit-builder/add/', views.add_to_outfit_api, name='add_to_outfit_api'),
]
