"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

urlpatterns = [
    path('admin/', include('apps.admin.urls')),
    path('api/', include('api.urls')),
    path('p/', include('apps.core.urls')),
    path('', include('apps.billing.urls')),
    path('', include('apps.brands.urls')),
    path('', include('apps.accounts.urls')),
    path('', include('apps.catalog.urls')),
    path('', include('apps.orders.urls')),
    path('', include('apps.fitting.urls')),
    path('', include('apps.inventory.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        path('404/', lambda request: render(request, '404.html')),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    from django.urls import re_path
    from apps.core.views import custom_404_view
    urlpatterns += [
        re_path(r'^.*$', custom_404_view),
    ]

handler404 = 'apps.core.views.custom_404_view'
