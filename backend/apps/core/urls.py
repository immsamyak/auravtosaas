from django.urls import path
from . import views

urlpatterns = [
    path('blog/', views.landing_blog_list, name='landing_blog_list'),
    path('blog/<slug:slug>/', views.landing_blog_detail, name='landing_blog_detail'),
    path('<slug:slug>/', views.page_detail, name='page_detail'),
]
