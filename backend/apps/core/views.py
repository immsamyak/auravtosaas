from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, get_object_or_404
from .models import Page

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, 'core/page_detail.html', {'page': page})

def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)
