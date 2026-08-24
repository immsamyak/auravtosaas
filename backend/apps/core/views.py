from django.shortcuts import render, get_object_or_404
from .models import Page, BlogPost, LandingPageConfig

def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_published=True)
    return render(request, 'core/page_detail.html', {'page': page})

def custom_404_view(request, exception=None):
    return render(request, '404.html', status=404)

def landing_blog_list(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-published_at')
    config = LandingPageConfig.objects.filter(is_active=True).first()
    return render(request, 'landing/blog_list.html', {'posts': posts, 'cms': config})

def landing_blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    config = LandingPageConfig.objects.filter(is_active=True).first()
    
    # Get recent posts for sidebar
    recent_posts = BlogPost.objects.filter(is_published=True).exclude(id=post.id).order_by('-published_at')[:3]
    
    return render(request, 'landing/blog_detail.html', {
        'post': post, 
        'cms': config,
        'recent_posts': recent_posts
    })
