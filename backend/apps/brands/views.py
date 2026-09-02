from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.contrib import messages
from apps.brands.models import Brand, BrandStaff, MediaAsset, APIKey, WebhookEndpoint
from apps.analytics.services import DashboardAnalyticsService
from apps.core.models import LandingPageConfig, LandingPageFeature, Testimonial, BlogPost, ContactMessage, FAQItem, Metric, IntegrationPlatform
from apps.catalog.models import Product
from apps.billing.models import SubscriptionPlan

def index_view(request):
    """Platform homepage showing all brands and SaaS landing content"""
    if request.method == 'POST' and 'contact_form' in request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            messages.success(request, "Your message has been sent. We'll get back to you soon!")
            return redirect('index')

    config = LandingPageConfig.objects.filter(is_active=True).first()
    brand_features = LandingPageFeature.objects.filter(config=config, audience='BRAND').order_by('display_order')
    shopper_features = LandingPageFeature.objects.filter(config=config, audience='SHOPPER').order_by('display_order')
    brands = Brand.objects.filter(status='ACTIVE')[:6]
    
    testimonials = Testimonial.objects.filter(is_active=True).order_by('display_order', '-created_at')
    latest_blogs = BlogPost.objects.filter(is_published=True).order_by('-published_at')[:3]
    faqs = FAQItem.objects.filter(is_active=True).order_by('display_order')
    metrics = Metric.objects.filter(is_active=True).order_by('display_order')
    integrations = IntegrationPlatform.objects.filter(is_active=True).order_by('display_order')
    
    plans = SubscriptionPlan.objects.all().order_by('monthly_price')

    return render(request, 'brands/index.html', {
        'cms': config,
        'brand_features': brand_features,
        'shopper_features': shopper_features,
        'brands': brands,
        'testimonials': testimonials,
        'latest_blogs': latest_blogs,
        'plans': plans,
        'faqs': faqs,
        'metrics': metrics,
        'integrations': integrations,
    })

@login_required(login_url='/login/')
def dashboard_view(request):
    """
    Brand Analytics Dashboard
    Filters by the logged-in brand owner.
    """
    # Multi-tenant Team Management Check
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index') # Regular users don't have a dashboard

    metrics = DashboardAnalyticsService.get_dashboard_metrics(brand)
    
    context = {
        'brand': brand,
        **metrics
    }
    return render(request, 'brands/dashboard.html', context)

@login_required(login_url='/login/')
def brand_settings_view(request):
    """
    Brand Settings Management View.
    """
    # Multi-tenant Team Management Check
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')

    if request.method == 'POST':
        # Simple save logic for demonstration
        brand.name = request.POST.get('name', brand.name)
        brand.slug = request.POST.get('slug', brand.slug)
        brand.contact_email = request.POST.get('contact_email', brand.contact_email)
        brand.status = request.POST.get('status', brand.status)
        
        # Enforce Custom Domain lock
        if brand.subscription and brand.subscription.plan and brand.subscription.plan.allow_custom_domain:
            brand.custom_domain = request.POST.get('custom_domain', brand.custom_domain)
        
        # New Store Details
        brand.description = request.POST.get('description', brand.description)
        brand.support_email = request.POST.get('support_email', brand.support_email)
        brand.support_phone = request.POST.get('support_phone', brand.support_phone)
        brand.address = request.POST.get('address', brand.address)
        brand.logo_alignment = request.POST.get('logo_alignment', brand.logo_alignment)
        
        # Currency Override
        brand.currency_code = request.POST.get('currency_code', brand.currency_code)
        brand.currency_symbol = request.POST.get('currency_symbol', brand.currency_symbol)
        
        # B2B Wholesale
        if brand.subscription and brand.subscription.plan and brand.subscription.plan.allow_b2b_wholesale:
            try:
                b2b_discount = request.POST.get('b2b_discount_percent')
                if b2b_discount is not None:
                    brand.b2b_discount_percent = float(b2b_discount)
            except ValueError:
                pass
        
        # New Social Links - We receive usernames, we store full URLs
        insta_user = request.POST.get('instagram_url', '').strip()
        if insta_user and not insta_user.startswith('http'):
            brand.instagram_url = f"https://instagram.com/{insta_user}"
        elif not insta_user:
            brand.instagram_url = ''
            
        fb_user = request.POST.get('facebook_url', '').strip()
        if fb_user and not fb_user.startswith('http'):
            brand.facebook_url = f"https://facebook.com/{fb_user}"
        elif not fb_user:
            brand.facebook_url = ''
            
        tiktok_user = request.POST.get('tiktok_url', '').strip()
        if tiktok_user and not tiktok_user.startswith('http'):
            brand.tiktok_url = f"https://tiktok.com/@{tiktok_user}"
        elif not tiktok_user:
            brand.tiktok_url = ''
            
        twitter_user = request.POST.get('twitter_url', '').strip()
        if twitter_user and not twitter_user.startswith('http'):
            brand.twitter_url = f"https://twitter.com/{twitter_user}"
        elif not twitter_user:
            brand.twitter_url = ''
            
        pinterest_user = request.POST.get('pinterest_url', '').strip()
        if pinterest_user and not pinterest_user.startswith('http'):
            brand.pinterest_url = f"https://pinterest.com/{pinterest_user}"
        elif not pinterest_user:
            brand.pinterest_url = ''
            
        # Banner Text Settings
        brand.banner_title = request.POST.get('banner_title', brand.banner_title)
        brand.banner_subtitle = request.POST.get('banner_subtitle', brand.banner_subtitle)
        brand.banner_cta_text = request.POST.get('banner_cta_text', brand.banner_cta_text)
        brand.banner_cta_link = request.POST.get('banner_cta_link', brand.banner_cta_link)
        
        # Advanced Customization
        brand.top_announcement_text = request.POST.get('top_announcement_text', brand.top_announcement_text)
        brand.banner_badge_text = request.POST.get('banner_badge_text', brand.banner_badge_text)
        brand.banner_secondary_cta_text = request.POST.get('banner_secondary_cta_text', brand.banner_secondary_cta_text)
        brand.banner_secondary_cta_link = request.POST.get('banner_secondary_cta_link', brand.banner_secondary_cta_link)
        brand.footer_copyright_text = request.POST.get('footer_copyright_text', brand.footer_copyright_text)
        
        if 'logo' in request.FILES:
            brand.logo = request.FILES['logo']
        if 'banner' in request.FILES:
            brand.banner = request.FILES['banner']
            
        brand.save()
        
        # Save POS QR Settings
        from apps.core.models import BrandSetting
        settings, created = BrandSetting.objects.get_or_create(brand=brand)
        settings.google_review_url = request.POST.get('google_review_url', settings.google_review_url)
        settings.wifi_network_name = request.POST.get('wifi_network_name', settings.wifi_network_name)
        settings.wifi_password = request.POST.get('wifi_password', settings.wifi_password)
        settings.pos_thermal_paper_size = request.POST.get('pos_thermal_paper_size', settings.pos_thermal_paper_size)
        
        settings.tax_id_type = request.POST.get('tax_id_type', settings.tax_id_type)
        settings.tax_id_number = request.POST.get('tax_id_number', settings.tax_id_number)
        settings.show_tax_on_receipt = request.POST.get('show_tax_on_receipt') == 'on'
        
        settings.save()
        messages.success(request, f'Settings for {brand.name} have been updated successfully.')
        return redirect('brand_settings')

    # Extract usernames for the template
    social_usernames = {
        'instagram': brand.instagram_url.replace('https://instagram.com/', '') if brand.instagram_url else '',
        'facebook': brand.facebook_url.replace('https://facebook.com/', '') if brand.facebook_url else '',
        'tiktok': brand.tiktok_url.replace('https://tiktok.com/@', '').replace('https://tiktok.com/', '') if brand.tiktok_url else '',
        'twitter': brand.twitter_url.replace('https://twitter.com/', '') if brand.twitter_url else '',
        'pinterest': brand.pinterest_url.replace('https://pinterest.com/', '') if brand.pinterest_url else '',
    }

    return render(request, 'brands/settings.html', {
        'brand': brand,
        'statuses': Brand.STATUS_CHOICES,
        'social_usernames': social_usernames,
    })

@login_required(login_url='/login/')
def team_management_view(request):
    """
    Manage Brand Staff (Add/Remove members, set roles)
    Only accessible to OWNER and ADMIN roles.
    """
    # Multi-tenant Team Management Check
    brand = None
    role = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
        role = 'OWNER'
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            role = staff.role
            
    if not brand:
        return redirect('index')

    if role not in ['OWNER', 'ADMIN']:
        messages.error(request, "You do not have permission to manage the team.")
        return redirect('dashboard')

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            email = request.POST.get('email')
            role_choice = request.POST.get('role')
            
            from django.contrib.auth.models import User
            try:
                user_to_add = User.objects.get(email=email)
                
                # Check if already staff
                if BrandStaff.objects.filter(brand=brand, user=user_to_add).exists():
                    messages.warning(request, f"{email} is already on the team.")
                else:
                    BrandStaff.objects.create(brand=brand, user=user_to_add, role=role_choice)
                    messages.success(request, f"{email} has been added as {role_choice}.")
            except User.DoesNotExist:
                messages.error(request, f"No user found with email {email}. They must register an account first.")
                
        elif action == 'remove':
            staff_id = request.POST.get('staff_id')
            try:
                staff_member = BrandStaff.objects.get(id=staff_id, brand=brand)
                if staff_member.role == 'OWNER':
                    messages.error(request, "Cannot remove the store owner.")
                else:
                    staff_member.delete()
                    messages.success(request, f"Staff member removed.")
            except BrandStaff.DoesNotExist:
                pass
                
        return redirect('team_management')

    staff_members = BrandStaff.objects.filter(brand=brand).select_related('user')
    
    return render(request, 'brands/team.html', {
        'brand': brand,
        'staff_members': staff_members,
        'roles': BrandStaff.ROLE_CHOICES,
        'active_tab': 'team'
    })

@login_required(login_url='/login/')
def customers_view(request):
    """
    Brand Owner view to manage storefront customers and their B2B wholesale status.
    """
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')

    from apps.brands.models import BrandCustomer

    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        is_b2b_val = request.POST.get('is_b2b') == 'on'
        
        try:
            customer = BrandCustomer.objects.get(id=customer_id, brand=brand)
            customer.is_b2b = is_b2b_val
            customer.save()
            status_text = "enabled" if is_b2b_val else "disabled"
            messages.success(request, f"Wholesale B2B status {status_text} for {customer.user.email}.")
        except BrandCustomer.DoesNotExist:
            messages.error(request, "Customer not found.")
            
        return redirect('customers_management')

    # Get all customers for this brand
    customers = BrandCustomer.objects.filter(brand=brand).select_related('user').order_by('-created_at')
    
    # Calculate some stats for the UI
    total_customers = customers.count()
    b2b_customers = customers.filter(is_b2b=True).count()
    
    # Optional: We can annotate order count if we want, but for now simple query is fine.
    
    return render(request, 'brands/customers.html', {
        'brand': brand,
        'customers': customers,
        'total_customers': total_customers,
        'b2b_customers': b2b_customers,
        'active_tab': 'customers'
    })

@xframe_options_sameorigin
def storefront_view(request, slug):
    """
    Public storefront for a specific brand.
    Displays brand info and active VTO-ready catalog.
    Renders dynamic theme if selected.
    """
    brand = get_object_or_404(Brand, slug=slug)
    
    if brand.status == 'MAINTENANCE':
        return render(request, 'brands/store_maintenance.html', {'brand': brand})
    elif brand.status == 'INACTIVE':
        return render(request, 'brands/store_inactive.html', {'brand': brand})
        
    products = brand.products.filter(is_active=True).order_by('-created_at')
    
    cat_id = request.GET.get('category')
    if cat_id:
        products = products.filter(category_id=cat_id)
        
    col_id = request.GET.get('collection')
    if col_id:
        products = products.filter(collections__id=col_id)
    
    # Try to load collections and categories
    from apps.catalog.models import Collection, Category
    collections = Collection.objects.filter(brand=brand, is_active=True).order_by('-created_at')
    categories = Category.objects.filter(brand=brand, is_active=True).order_by('display_order')
    
    theme_base = f"storefront/{brand.theme.template_folder}/base.html" if brand.theme and brand.theme.is_active else "brands/store_base.html"

    template_name = 'brands/storefront.html'
    if brand.theme and brand.theme.is_active:
        template_name = f'storefront/{brand.theme.template_folder}/index.html'
    
    from apps.brands.models import BrandIntegration
    whatsapp_addon = BrandIntegration.objects.filter(
        brand=brand, 
        integration__provider_code='WHATSAPP', 
        is_active=True
    ).first()
    
    blog_posts = BlogPost.objects.filter(brand=brand, is_published=True).order_by('-published_at')

    return render(request, template_name, {
        'brand': brand,
        'products': products,
        'collections': collections,
        'categories': categories,
        'theme_base': theme_base,
        'whatsapp_addon': whatsapp_addon,
        'blog_posts': blog_posts,
    })

def storefront_shop_view(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    if brand.status == 'MAINTENANCE': return render(request, 'brands/store_maintenance.html', {'brand': brand})
    elif brand.status == 'INACTIVE': return render(request, 'brands/store_inactive.html', {'brand': brand})
    
    from apps.catalog.models import Collection, Category, Color, Size
    
    products = brand.products.filter(is_active=True).order_by('-created_at')
    
    # Filtering logic
    cat_id = request.GET.get('category')
    col_id = request.GET.get('collection')
    color_ids = request.GET.getlist('color')
    size_ids = request.GET.getlist('size')
    
    search_q = request.GET.get('q')
    if request.method == 'POST':
        search_q = request.POST.get('q')
    
    if cat_id:
        products = products.filter(category_id=cat_id)
    if col_id:
        products = products.filter(collections__id=col_id)
    if color_ids:
        products = products.filter(variants__color_id__in=color_ids).distinct()
    if size_ids:
        products = products.filter(variants__size_id__in=size_ids).distinct()
    
    if search_q:
        from django.db.models import Q
        products = products.filter(
            Q(name__icontains=search_q) |
            Q(description__icontains=search_q)
        )
        
    from django.core.paginator import Paginator
    
    # Paginate after all filters are applied
    paginator = Paginator(products, 12) # 12 products per page (3x4 or 4x3 grid)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Prefetch logic only on the paginated object list!
    page_obj.object_list = list(page_obj.object_list) # evaluate
    for p in page_obj.object_list:
        seen_colors = set()
        p.unique_colors = []
        for v in p.variants.all():
            if v.color and v.color.id not in seen_colors:
                p.unique_colors.append(v.color)
                seen_colors.add(v.color.id)
        
    collections_qs = Collection.objects.filter(brand=brand, is_active=True).order_by('-created_at')
    categories_qs = Category.objects.filter(brand=brand, is_active=True).order_by('display_order')
    colors_qs = Color.objects.filter(brand=brand, is_active=True)
    sizes_qs = Size.objects.filter(brand=brand, is_active=True).order_by('display_order')
    
    theme_base = f"storefront/{brand.theme.template_folder}/base.html" if brand.theme and brand.theme.is_active else "brands/store_base.html"
    
    from apps.brands.models import BrandIntegration
    whatsapp_addon = BrandIntegration.objects.filter(brand=brand, integration__provider_code='WHATSAPP', is_active=True).first()
    
    return render(request, 'brands/store_shop.html', {
        'brand': brand,
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'collections': collections_qs,
        'categories': categories_qs,
        'filter_colors': colors_qs,
        'filter_sizes': sizes_qs,
        'selected_category': cat_id,
        'selected_collection': col_id,
        'selected_colors': color_ids,
        'selected_sizes': size_ids,
        'theme_base': theme_base,
        'whatsapp_addon': whatsapp_addon,
    })

def storefront_collections_view(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    if brand.status == 'MAINTENANCE': return render(request, 'brands/store_maintenance.html', {'brand': brand})
    elif brand.status == 'INACTIVE': return render(request, 'brands/store_inactive.html', {'brand': brand})
    
    from apps.catalog.models import Collection, Category
    collections_qs = Collection.objects.filter(brand=brand, is_active=True).order_by('-created_at')
    categories_qs = Category.objects.filter(brand=brand, is_active=True).order_by('display_order')
    
    theme_base = f"storefront/{brand.theme.template_folder}/base.html" if brand.theme and brand.theme.is_active else "brands/store_base.html"
    
    from apps.brands.models import BrandIntegration
    whatsapp_addon = BrandIntegration.objects.filter(brand=brand, integration__provider_code='WHATSAPP', is_active=True).first()
    
    return render(request, 'brands/store_collections.html', {
        'brand': brand,
        'collections': collections_qs,
        'categories': categories_qs,
        'theme_base': theme_base,
        'whatsapp_addon': whatsapp_addon,
    })

def storefront_categories_view(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    if brand.status == 'MAINTENANCE': return render(request, 'brands/store_maintenance.html', {'brand': brand})
    elif brand.status == 'INACTIVE': return render(request, 'brands/store_inactive.html', {'brand': brand})
    
    from apps.catalog.models import Collection, Category
    collections_qs = Collection.objects.filter(brand=brand, is_active=True).order_by('-created_at')
    categories_qs = Category.objects.filter(brand=brand, is_active=True).order_by('display_order')
    
    theme_base = f"storefront/{brand.theme.template_folder}/base.html" if brand.theme and brand.theme.is_active else "brands/store_base.html"
    
    from apps.brands.models import BrandIntegration
    whatsapp_addon = BrandIntegration.objects.filter(brand=brand, integration__provider_code='WHATSAPP', is_active=True).first()
    
    return render(request, 'brands/store_categories.html', {
        'brand': brand,
        'collections': collections_qs,
        'categories': categories_qs,
        'theme_base': theme_base,
        'whatsapp_addon': whatsapp_addon,
    })

@login_required(login_url='/login/')
def theme_gallery_view(request):
    # Multi-tenant Team Management Check
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')

    from .models import StoreTheme
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'apply_theme':
            theme_id = request.POST.get('theme_id')
            if theme_id:
                theme = get_object_or_404(StoreTheme, id=theme_id, is_active=True)
                brand.theme = theme
                brand.save()
                messages.success(request, f'Successfully applied the {theme.name} theme!')


            else:
                brand.theme = None
                brand.save()
                messages.success(request, 'Successfully reverted to the default theme.')
            return redirect('theme_gallery')

    themes = StoreTheme.objects.filter(is_active=True).order_by('name')
    
    return render(request, 'brands/theme_gallery.html', {
        'themes': themes,
        'current_theme': brand.theme
    })
def store_product_detail_view(request, slug, product_slug):
    """
    Public product detail page for a specific brand's product.
    Allows shoppers to select variants (color/size) before trying on.
    """
    brand = get_object_or_404(Brand, slug=slug)
    
    if brand.status == 'MAINTENANCE':
        return render(request, 'brands/store_maintenance.html', {'brand': brand})
    elif brand.status == 'INACTIVE':
        return render(request, 'brands/store_inactive.html', {'brand': brand})
        
    product = get_object_or_404(Product, slug=product_slug, brand=brand, is_active=True)
    
    # We will pass the variants as a list of dicts so AlpineJS can easily filter them
    variants = product.variants.all().select_related('color', 'size')
    
    # Extract unique colors and sizes for the UI pickers
    colors = []
    sizes = []
    seen_colors = set()
    seen_sizes = set()
    
    variants_json = []
    
    for v in variants:
        if v.color.id not in seen_colors:
            colors.append({'id': v.color.id, 'name': v.color.name, 'hex_code': v.color.hex_code})
            seen_colors.add(v.color.id)
            
        if v.size.id not in seen_sizes:
            sizes.append({'id': v.size.id, 'name': v.size.name, 'code': v.size.code})
            seen_sizes.add(v.size.id)
            
        variants_json.append({
            'id': v.id,
            'slug': v.slug,
            'color_id': v.color.id,
            'color_name': v.color.name,
            'size_id': v.size.id,
            'size_code': v.size.code,
            'image_url': v.image.url if v.image else '',
            'stock': v.total_stock,
        })
        
    theme_base = f"storefront/{brand.theme.template_folder}/base.html" if brand.theme and brand.theme.is_active else "brands/store_base.html"
    
    # Load categories and collections for the theme base navigation and footer
    from apps.catalog.models import Collection, Category
    from apps.brands.models import BrandIntegration
    collections_qs = Collection.objects.filter(brand=brand, is_active=True).order_by('-created_at')
    categories_qs = Category.objects.filter(brand=brand, is_active=True).order_by('display_order')
    
    whatsapp_addon = BrandIntegration.objects.filter(
        brand=brand, 
        integration__provider_code='WHATSAPP', 
        is_active=True
    ).first()
    
    whatsapp_message = ""
    if whatsapp_addon:
        base_msg = whatsapp_addon.credentials.get('instructions', '')
        product_url = request.build_absolute_uri()
        whatsapp_message = f"{base_msg}\n\nI am interested in: {product.name}\n{product_url}".strip()
        
    related_products = Product.objects.filter(brand=brand, category=product.category).exclude(id=product.id)[:4]
    if not related_products.exists():
        related_products = Product.objects.filter(brand=brand).exclude(id=product.id)[:4]
        
    # We load reviews from ProductReview, avoiding circular imports or using existing imports if any.
    from apps.catalog.models import ProductReview
    reviews = ProductReview.objects.filter(product=product).order_by('-created_at')
    
    is_b2b_customer = False
    b2b_price = product.price
    if request.user.is_authenticated:
        from apps.brands.models import BrandCustomer
        customer_record, _ = BrandCustomer.objects.get_or_create(brand=brand, user=request.user)
        is_b2b_customer = customer_record.is_b2b
        
        if is_b2b_customer and brand.subscription and brand.subscription.plan and brand.subscription.plan.allow_b2b_wholesale:
            if brand.b2b_discount_percent > 0:
                from decimal import Decimal
                discount = (product.price * brand.b2b_discount_percent) / Decimal('100.00')
                b2b_price = product.price - discount
    
    return render(request, 'brands/store_product_detail.html', {
        'brand': brand,
        'product': product,
        'colors': colors,
        'sizes': sizes,
        'variants_json': variants_json,
        'theme_base': theme_base,
        'collections': collections_qs,
        'categories': categories_qs,
        'whatsapp_addon': whatsapp_addon,
        'whatsapp_message': whatsapp_message,
        'related_products': related_products,
        'reviews': reviews,
        'is_b2b_customer': is_b2b_customer,
        'b2b_price': b2b_price,
    })

@login_required(login_url='/login/')
def finance_view(request):
    # Multi-tenant Team Management Check
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')
    
    from apps.orders.models import Order
    from django.db.models import Sum, Count, Q
    from django.db.models.functions import TruncDate
    from django.utils import timezone
    import datetime
    import json
    
    # --- Filter logic ---
    filter_status = request.GET.get('status', '')
    filter_payment = request.GET.get('payment', '')
    filter_range = request.GET.get('range', '30')  # default last 30 days
    
    try:
        days_back = int(filter_range)
    except ValueError:
        days_back = 30
    
    date_from = timezone.now() - datetime.timedelta(days=days_back)
    
    orders_qs = Order.objects.filter(brand=brand, created_at__gte=date_from)
    if filter_status:
        orders_qs = orders_qs.filter(status=filter_status)
    if filter_payment:
        orders_qs = orders_qs.filter(payment_provider=filter_payment)
    
    from django.db.models import F
    orders_qs = orders_qs.annotate(
        calc_grand_total=F('total_amount') + F('shipping_cost') + F('tax_amount') - F('discount_amount')
    )

    # --- CSV Export ---
    if request.GET.get('export') == 'csv':
        import csv
        from django.http import HttpResponse as DjangoHttpResponse
        from django.core.paginator import Paginator
        response = DjangoHttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="finance_export_{timezone.now().strftime("%Y%m%d")}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Order ID', 'Customer', 'Phone', 'Items Total', 'Discount', 'Shipping', 'Grand Total', 'Coupon', 'Payment Method', 'Status', 'Date'])
        for o in orders_qs.order_by('-created_at'):
            writer.writerow([
                str(o.id)[:8],
                o.customer_name or (o.user.get_full_name() if o.user else 'N/A'),
                o.customer_phone or 'N/A',
                str(o.total_amount),
                str(o.discount_amount),
                str(o.shipping_cost),
                str(o.calc_grand_total),
                o.coupon.code if o.coupon else 'None',
                o.payment_provider or 'N/A',
                o.status,
                o.created_at.strftime('%Y-%m-%d %H:%M'),
            ])
        return response
    
    # --- Stat cards (real data) ---
    total_revenue = orders_qs.filter(status__in=['PAID', 'SHIPPED', 'DELIVERED', 'COMPLETED']).aggregate(total=Sum('calc_grand_total'))['total'] or 0
    pending_amount = orders_qs.filter(status='PENDING').aggregate(total=Sum('calc_grand_total'))['total'] or 0
    total_orders = orders_qs.count()
    paid_orders = orders_qs.filter(status__in=['PAID', 'SHIPPED', 'DELIVERED', 'COMPLETED']).count()
    
    # --- Payment method breakdown ---
    payment_breakdown = orders_qs.values('payment_provider').annotate(
        count=Count('id'),
        revenue=Sum('calc_grand_total')
    ).order_by('-revenue')
    
    # Provide friendly labels
    PAYMENT_LABELS = {
        'CUSTOM_MANUAL': 'Cash / Bank / QR',
        'ESEWA': 'eSewa',
        'KHALTI': 'Khalti',
        None: 'Not Set',
        '': 'Not Set',
    }
    payment_methods_data = []
    for entry in payment_breakdown:
        provider = entry['payment_provider']
        payment_methods_data.append({
            'provider': PAYMENT_LABELS.get(provider, provider or 'Not Set'),
            'count': entry['count'],
            'revenue': float(entry['revenue'] or 0),
        })
    
    # --- Daily revenue chart (real data) ---
    daily_revenue = orders_qs.filter(
        status__in=['PAID', 'SHIPPED', 'DELIVERED', 'COMPLETED']
    ).annotate(
        day=TruncDate('created_at')
    ).values('day').annotate(
        revenue=Sum('calc_grand_total'),
        day_count=Count('id')
    ).order_by('day')
    
    revenue_dict = {}
    for entry in daily_revenue:
        if entry['day']:
            revenue_dict[entry['day'].strftime('%b %d')] = float(entry['revenue'] or 0)
    
    chart_labels = []
    chart_data = []
    today = timezone.now().date()
    for i in range(min(days_back, 30) - 1, -1, -1):
        date_label = (today - datetime.timedelta(days=i)).strftime('%b %d')
        chart_labels.append(date_label)
        chart_data.append(revenue_dict.get(date_label, 0))
    
    # --- Recent orders (real) ---
    recent_orders = orders_qs.order_by('-created_at')[:10]
    
    # --- Status breakdown ---
    status_breakdown = orders_qs.values('status').annotate(count=Count('id'))
    status_counts = {s['status']: s['count'] for s in status_breakdown}
    
    # Get unique payment providers for the filter dropdown
    all_payment_providers = Order.objects.filter(brand=brand).values_list('payment_provider', flat=True).distinct()
    provider_choices = []
    for p in all_payment_providers:
        if p:
            provider_choices.append({'code': p, 'label': PAYMENT_LABELS.get(p, p)})
    
    return render(request, 'brands/finance.html', {
        'brand': brand,
        'total_revenue': total_revenue,
        'pending_amount': pending_amount,
        'total_orders': total_orders,
        'paid_orders': paid_orders,
        'payment_methods_data': payment_methods_data,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'recent_orders': recent_orders,
        'status_counts': status_counts,
        'filter_status': filter_status,
        'filter_payment': filter_payment,
        'filter_range': filter_range,
        'provider_choices': provider_choices,
    })

@login_required(login_url='/login/')
def media_gallery_view(request):
    # Multi-tenant Team Management Check
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')
        
    assets = brand.media_assets.all().order_by('-uploaded_at')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'delete':
            asset_id = request.POST.get('asset_id')
            asset = MediaAsset.objects.filter(id=asset_id, brand=brand).first()
            if asset:
                asset.file.delete(save=False)
                asset.delete()
                messages.success(request, 'Media file deleted.')
            return redirect('media_gallery')
        elif request.FILES.get('file'):
            file = request.FILES['file']
            MediaAsset.objects.create(
                brand=brand,
                file=file,
                name=file.name,
                file_type=file.content_type,
                file_size=file.size
            )
            messages.success(request, 'Media uploaded successfully.')
            return redirect('media_gallery')

    from apps.catalog.models import ProductImage, ProductVariant
    product_images = ProductImage.objects.filter(product__brand=brand).order_by('-id')
    product_variants = ProductVariant.objects.filter(product__brand=brand).exclude(image='').order_by('-id')
    
    return render(request, 'brands/media_gallery.html', {
        'brand': brand,
        'assets': assets,
        'product_images': product_images,
        'product_variants': product_variants,
    })

from apps.core.models import PlatformIntegration
from apps.brands.models import BrandIntegration

@login_required(login_url='/login/')
def addons_view(request):
    # Multi-tenant Team Management Check
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')
        
    if request.method == 'POST':
        action = request.POST.get('action')
        integration_id = request.POST.get('integration_id')
        
        if action == 'configure' and integration_id:
            integration = get_object_or_404(PlatformIntegration, id=integration_id)
            brand_int, created = BrandIntegration.objects.get_or_create(brand=brand, integration=integration)
            
            # Save dynamic credentials based on what was submitted
            credentials = brand_int.credentials or {}
            
            # The full list of supported integration credential keys across all platforms
            supported_keys = [
                'merchant_id', 'api_key', 'api_secret', 'api_token',
                'client_id', 'client_secret', 'username', 'password', 
                'instructions', 'custom_payment_type', 'phone_number',
                'publishable_key', 'secret_key', 'webhook_secret',
                'key_id', 'key_secret', 'pixel_id', 'site_id',
                'public_api_key', 'private_api_key', 'property_id',
                'account_sid', 'auth_token', 'from_phone', 'webhook_url',
                'account_number', 'store_id', 'measurement_id'
            ]
            
            for field in supported_keys:
                val = request.POST.get(field)
                if val:
                    credentials[field] = val
                    
            # Handle file upload for QR code
            if 'qr_code_image' in request.FILES:
                from django.core.files.storage import FileSystemStorage
                fs = FileSystemStorage(location='media/qr_codes/', base_url='/media/qr_codes/')
                file = request.FILES['qr_code_image']
                filename = fs.save(f"{brand.id}_{file.name}", file)
                credentials['qr_code_url'] = fs.url(filename)
            elif request.POST.get('qr_code_url'):
                credentials['qr_code_url'] = request.POST.get('qr_code_url')
                
            brand_int.credentials = credentials
            brand_int.is_active = True
            brand_int.save()
            messages.success(request, f'{integration.name} has been configured and activated.')
            
        elif action == 'disable' and integration_id:
            integration = get_object_or_404(PlatformIntegration, id=integration_id)
            brand_int = BrandIntegration.objects.filter(brand=brand, integration=integration).first()
            if brand_int:
                brand_int.is_active = False
                brand_int.save()
                messages.success(request, f'{integration.name} has been disabled.')
                
        return redirect('addons')
        
    # Get all active platform integrations
    platform_addons = PlatformIntegration.objects.filter(is_active_globally=True)
    
    # Get brand's configured integrations
    brand_configs = {bi.integration_id: bi for bi in BrandIntegration.objects.filter(brand=brand)}
    
    # Combine data for the template
    import json
    addons_data = []
    for addon in platform_addons:
        config = brand_configs.get(addon.id)
        creds = config.credentials if config else {}
        addons_data.append({
            'addon': addon,
            'is_configured': bool(config),
            'is_active': config.is_active if config else False,
            'credentials': creds,
            'credentials_json': json.dumps(creds)
        })

    return render(request, 'brands/addons.html', {
        'brand': brand,
        'addons_data': addons_data
    })

import secrets
@login_required(login_url='/login/')
def developer_api_view(request):
    # Multi-tenant Team Management Check
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')
        
    has_api_access = False
    if hasattr(brand, 'subscription') and brand.subscription and brand.subscription.plan:
        has_api_access = brand.subscription.plan.allow_api_access
        
    if request.method == 'POST':
        if not has_api_access:
            messages.error(request, "API Access is not available on your current plan.")
            return redirect('developer_api')
            
        action = request.POST.get('action')
        if action == 'create_key':
            name = request.POST.get('name', 'New API Key')
            raw_token = secrets.token_hex(24)
            full_key = f"aura_live_{raw_token}"
            prefix = full_key[:8] # aura_liv
            
            # For this simple implementation, we store the full key in key_hash so the user can view it.
            # In a highly secure system, we would only store a hash (e.g., make_password(full_key))
            APIKey.objects.create(brand=brand, name=name, prefix=prefix, key_hash=full_key)
            messages.success(request, f'API Key "{name}" created successfully.')
        elif action == 'create_webhook':
            url = request.POST.get('url')
            if url:
                WebhookEndpoint.objects.create(
                    brand=brand,
                    url=url,
                    secret_key=f"whsec_{secrets.token_hex(16)}"
                )
                messages.success(request, 'Webhook endpoint added successfully.')
        elif action == 'delete_key':
            key_id = request.POST.get('key_id')
            if key_id:
                try:
                    key = APIKey.objects.get(id=key_id, brand=brand)
                    name = key.name
                    key.delete()
                    messages.success(request, f'API Key "{name}" deleted successfully.')
                except APIKey.DoesNotExist:
                    messages.error(request, 'API Key not found.')
        elif action == 'delete_webhook':
            webhook_id = request.POST.get('webhook_id')
            if webhook_id:
                try:
                    webhook = WebhookEndpoint.objects.get(id=webhook_id, brand=brand)
                    webhook.delete()
                    messages.success(request, 'Webhook deleted successfully.')
                except WebhookEndpoint.DoesNotExist:
                    messages.error(request, 'Webhook not found.')
        
        return redirect('developer_api')

    api_keys = brand.api_keys.all().order_by('-created_at')
    webhooks = brand.webhooks.all().order_by('-created_at')
    
    # Import APILog
    from .models import APILog
    
    api_logs = brand.api_logs.all().order_by('-created_at')[:50] # Get latest 50

    return render(request, 'brands/developer_api.html', {
        'brand': brand,
        'api_keys': api_keys,
        'webhooks': webhooks,
        'api_logs': api_logs,
        'has_api_access': has_api_access
    })

@login_required(login_url='/login/')
def notifications_view(request):
    # Multi-tenant Team Management Check
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')
        
    try:
        from apps.core.models import Notification
        notifications = Notification.objects.filter(user=request.user)
    except Exception:
        notifications = []
        
    return render(request, 'brands/notifications.html', {
        'notifications': notifications,
        'brand': brand
    })

@login_required(login_url='/login/')
def mark_notifications_read(request):
    try:
        from apps.core.models import Notification
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from apps.accounts.models import ConsumerProfile
from apps.orders.models import Order
from apps.fitting.models import VirtualWardrobeLook

def storefront_account_view(request, slug):
    if not request.user.is_authenticated:
        from django.contrib import messages
        messages.error(request, 'Please sign in to view your account.')
        return redirect('storefront', slug=slug)
        
    brand = get_object_or_404(Brand, slug=slug)
    
    if brand.status == 'MAINTENANCE':
        return render(request, 'brands/store_maintenance.html', {'brand': brand})
    elif brand.status == 'INACTIVE':
        return render(request, 'brands/store_inactive.html', {'brand': brand})
        
    theme_base = f"storefront/{brand.theme.template_folder}/base.html" if brand.theme and brand.theme.is_active else "brands/store_base.html"
    
    orders = Order.objects.filter(user=request.user, brand=brand).order_by('-created_at')
    wardrobe_looks = VirtualWardrobeLook.objects.filter(user=request.user).order_by('-saved_at')
    
    # Profile AI logic: Recommend 4 products based on catalog recency (until ML engine integrated)
    ai_recommendations = Product.objects.filter(brand=brand, is_active=True).order_by('-created_at')[:4]
    
    template_name = f"storefront/{brand.theme.template_folder}/account.html" if brand.theme and brand.theme.is_active else 'brands/store_account.html'
    
    return render(request, template_name, {
        'brand': brand,
        'theme_base': theme_base,
        'orders': orders,
        'wardrobe_looks': wardrobe_looks,
        'ai_recommendations': ai_recommendations,
    })

def storefront_login(request, slug):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Successfully logged in.')
            else:
                messages.error(request, 'Invalid credentials.')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
            
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('storefront', slug=slug)

def storefront_register(request, slug):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email and password and not User.objects.filter(email=email).exists():
            username = email.split('@')[0] + str(User.objects.count())
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = name
            user.save()
            ConsumerProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Account created successfully.')
        else:
            messages.error(request, 'Email already exists or invalid data.')
            
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('storefront', slug=slug)

def storefront_logout(request, slug):
    logout(request)
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('storefront', slug=slug)


@login_required(login_url='/login/')
def reports_view(request):
    # Multi-tenant Team Management Check
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')
        
    from apps.orders.models import Order, OrderItem
    from apps.catalog.models import ProductVariant, Product
    from django.db.models import Sum, Count, F, Q
    from django.db.models.functions import TruncDate
    from django.utils import timezone
    import datetime
    import csv
    from django.http import HttpResponse as DjangoHttpResponse
    from django.core.paginator import Paginator
    
    # Base filter
    filter_range = request.GET.get('range', '30')
    filter_tab = request.GET.get('tab', 'finance') # finance, products, customers
    
    if filter_range == 'all':
        date_from = timezone.now() - datetime.timedelta(days=3650) # 10 years
    else:
        try:
            days_back = int(filter_range)
        except ValueError:
            days_back = 30
        date_from = timezone.now() - datetime.timedelta(days=days_back)
        
    orders_qs = Order.objects.filter(brand=brand, created_at__gte=date_from)
    orders_qs = orders_qs.annotate(
        calc_grand_total=F('total_amount') + F('shipping_cost') + F('tax_amount') - F('discount_amount')
    )
    
    # --- CSV EXPORTS ---
    export_type = request.GET.get('export', '')
    if export_type == 'orders':
        response = DjangoHttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="orders_report_{timezone.now().strftime("%Y%m%d")}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Order ID', 'Customer', 'Phone', 'Items Total', 'Discount', 'Shipping', 'Grand Total', 'Coupon', 'Payment Method', 'Status', 'Date'])
        for o in orders_qs.order_by('-created_at'):
            writer.writerow([
                str(o.id)[:8],
                o.customer_name or (o.user.get_full_name() if o.user else 'N/A'),
                o.customer_phone or 'N/A',
                str(o.total_amount),
                str(o.discount_amount),
                str(o.shipping_cost),
                str(o.calc_grand_total),
                o.coupon.code if o.coupon else 'None',
                o.payment_provider or 'N/A',
                o.status,
                o.created_at.strftime('%Y-%m-%d %H:%M'),
            ])
        return response
        
    elif export_type == 'products':
        response = DjangoHttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="products_report_{timezone.now().strftime("%Y%m%d")}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Product Name', 'Variant', 'SKU', 'Price', 'Units Sold', 'Revenue Generated'])
        
        products_data = OrderItem.objects.filter(order__brand=brand, order__created_at__gte=date_from, order__status__in=['PAID', 'SHIPPED', 'DELIVERED', 'COMPLETED']).values(
            'product_variant__product__name', 'product_variant__color__name', 'product_variant__size__code', 'price_at_purchase'
        ).annotate(
            sold=Sum('quantity'),
            rev=Sum(F('price_at_purchase') * F('quantity'))
        )
        
        for p in products_data:
            writer.writerow([
                p['product_variant__product__name'],
                f"{p['product_variant__color__name']} / {p['product_variant__size__code']}",
                'N/A',
                str(p['price_at_purchase']),
                str(p['sold']),
                str(p['rev'])
            ])
        return response
        
    elif export_type == 'customers':
        response = DjangoHttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="customers_report_{timezone.now().strftime("%Y%m%d")}.csv"'
        writer = csv.writer(response)
        writer.writerow(['Customer Name', 'Phone', 'Email', 'Total Orders', 'Total Spent', 'Last Order Date'])
        
        customers = orders_qs.values('customer_name', 'customer_phone').annotate(
            order_count=Count('id'),
            total_spent=Sum('calc_grand_total')
        ).order_by('-total_spent')
        
        for c in customers:
            if c['customer_name']:
                writer.writerow([
                    c['customer_name'] or 'Unknown',
                    c['customer_phone'] or 'N/A',
                    
                    str(c['order_count']),
                    str(c['total_spent']),
                    'N/A' # Simplifying for now
                ])
        return response

    # --- UI DATA COLLECTION ---
    context = {
        'brand': brand,
        'filter_range': filter_range,
        'filter_tab': filter_tab,
    }
    
    if filter_tab == 'finance':
        context['total_revenue'] = orders_qs.filter(status__in=['PAID', 'SHIPPED', 'DELIVERED', 'COMPLETED']).aggregate(total=Sum('calc_grand_total'))['total'] or 0
        context['total_orders'] = orders_qs.count()
        context['completed_orders'] = orders_qs.filter(status__in=['PAID', 'SHIPPED', 'DELIVERED', 'COMPLETED']).count()
        orders = orders_qs.order_by('-created_at')
        paginator = Paginator(orders, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context['recent_orders'] = page_obj
        context['page_obj'] = page_obj
        
        status_breakdown = orders_qs.values('status').annotate(count=Count('id'))
        context['status_counts'] = {s['status']: s['count'] for s in status_breakdown}
        
    elif filter_tab == 'products':
        product_performance = OrderItem.objects.filter(
            order__brand=brand, 
            order__created_at__gte=date_from,
            order__status__in=['PAID', 'SHIPPED', 'DELIVERED', 'COMPLETED']
        ).values(
            'product_variant__product__name', 
            'product_variant__color__name', 
            'product_variant__size__code',
            
            'product_variant__product__id'
        ).annotate(
            sold=Sum('quantity'),
            rev=Sum(F('price_at_purchase') * F('quantity'))
        ).order_by('-rev')
        paginator = Paginator(product_performance, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context['product_performance'] = page_obj
        context['page_obj'] = page_obj
        
    elif filter_tab == 'customers':
        customers = orders_qs.values('customer_name', 'customer_phone').annotate(
            order_count=Count('id'),
            total_spent=Sum('calc_grand_total')
        ).exclude(customer_name__isnull=True, customer_phone__isnull=True).order_by('-total_spent')
        paginator = Paginator(customers, 15)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context['customers'] = page_obj
        context['page_obj'] = page_obj

    return render(request, 'brands/reports.html', context)




@login_required(login_url='/login/')
def global_search_view(request):
    brand = getattr(request.user, 'owned_brand', None)
    if not brand:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')

    query = request.GET.get('q', '').strip()
    
    products = []
    orders = []
    customers = []
    
    if query:
        from django.db.models import Q
        products = Product.objects.filter(brand=brand).filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )[:10]
        
        # Search orders by ID or Customer Name or Email or Phone
        orders = Order.objects.filter(brand=brand).filter(
            Q(id__icontains=query) | 
            Q(customer_name__icontains=query) |
            Q(customer_phone__icontains=query)
        )[:10]
        
    context = {
        'brand': brand,
        'query': query,
        'products': products,
        'orders': orders,
    }
    return render(request, 'brands/search_results.html', context)

import json
from django.views.decorators.csrf import csrf_exempt
from .models import StorefrontLayout, StorefrontSection

def website_designer_view(request):
    # Multi-tenant Team Management Check
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')

    layout, created = StorefrontLayout.objects.get_or_create(brand=brand)
    
    # Initialize default layout if created
    if created or not layout.sections.exists():
        StorefrontSection.objects.create(layout=layout, section_type='hero', display_order=10)
        StorefrontSection.objects.create(layout=layout, section_type='products', display_order=20)
        StorefrontSection.objects.create(layout=layout, section_type='collections', display_order=30)
        StorefrontSection.objects.create(layout=layout, section_type='categories', display_order=40)
        StorefrontSection.objects.create(layout=layout, section_type='header', display_order=0)
        StorefrontSection.objects.create(layout=layout, section_type='footer', display_order=100)

    if request.method == 'POST':
        if request.FILES.get('hero_banner_upload'):
            file = request.FILES['hero_banner_upload']
            brand.banner = file
            brand.save()
            from .models import MediaAsset
            MediaAsset.objects.create(
                brand=brand,
                file=file,
                name=file.name,
                file_size=file.size,
                file_type=file.content_type
            )
            return JsonResponse({'success': True, 'url': brand.banner.url})

        if request.FILES.get('generic_media_upload'):
            file = request.FILES['generic_media_upload']
            from .models import MediaAsset
            asset = MediaAsset.objects.create(
                brand=brand,
                file=file,
                name=file.name,
                file_size=file.size,
                file_type=file.content_type
            )
            return JsonResponse({'success': True, 'url': asset.file.url})

        import json
        try:
            data = json.loads(request.body)
            action = data.get('action')
            
            if action == 'save_global_styles':
                layout.global_styles = data.get('global_styles', {})
                layout.save()
                return JsonResponse({'status': 'success'})
                
            elif action == 'save_sections':
                sections_data = data.get('sections', [])
                
                # Delete removed sections
                keep_ids = [s.get('id') for s in sections_data if s.get('id')]
                layout.sections.exclude(id__in=keep_ids).delete()
                
                # Update or create
                for idx, s_data in enumerate(sections_data):
                    if s_data.get('id'):
                        sec = layout.sections.get(id=s_data['id'])
                        sec.display_order = idx * 10
                        sec.is_active = s_data.get('is_active', True)
                        sec.settings = s_data.get('settings', {})
                        sec.save()
                    else:
                        StorefrontSection.objects.create(
                            layout=layout,
                            section_type=s_data['type'],
                            display_order=idx * 10,
                            is_active=s_data.get('is_active', True),
                            settings=s_data.get('settings', {})
                        )
                return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    from .models import StoreTheme
    themes = StoreTheme.objects.filter(is_active=True).order_by('name')

    import json
    
    # Serialize available items for the UI picker
    available_products = list(brand.products.filter(is_active=True).values('id', 'name'))
    available_collections = list(brand.collections.filter(is_active=True).values('id', 'name'))
    available_categories = list(brand.categories.filter(is_active=True).values('id', 'name'))

    return render(request, 'brands/website_designer.html', {
        'brand': brand,
        'layout': layout,
        'themes': themes,
        'active_tab': 'designer',
        'available_products_json': json.dumps(available_products),
        'available_collections_json': json.dumps(available_collections),
        'available_categories_json': json.dumps(available_categories),
    })


# ==========================================
# STOREFRONT BLOG / JOURNAL
# ==========================================

def storefront_blog_list_view(request, slug):
    brand = get_object_or_404(Brand, slug=slug)
    if brand.status == 'MAINTENANCE':
        return render(request, 'brands/store_maintenance.html', {'brand': brand})
    elif brand.status == 'INACTIVE':
        return render(request, 'brands/store_inactive.html', {'brand': brand})
    
    from django.core.paginator import Paginator
    from apps.catalog.models import Collection, Category
    from apps.brands.models import BrandIntegration
    
    posts = BlogPost.objects.filter(brand=brand, is_published=True).order_by('-published_at', '-created_at')
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    theme_base = f"storefront/{brand.theme.template_folder}/base.html" if brand.theme and brand.theme.is_active else "brands/store_base.html"
    collections = Collection.objects.filter(brand=brand, is_active=True).order_by('-created_at')
    categories = Category.objects.filter(brand=brand, is_active=True).order_by('display_order')
    
    whatsapp_addon = BrandIntegration.objects.filter(
        brand=brand, 
        integration__provider_code='WHATSAPP', 
        is_active=True
    ).first()
    
    return render(request, 'brands/store_blog_list.html', {
        'brand': brand,
        'page_obj': page_obj,
        'theme_base': theme_base,
        'collections': collections,
        'categories': categories,
        'whatsapp_addon': whatsapp_addon,
    })


def storefront_blog_detail_view(request, slug, post_slug):
    brand = get_object_or_404(Brand, slug=slug)
    if brand.status == 'MAINTENANCE':
        return render(request, 'brands/store_maintenance.html', {'brand': brand})
    elif brand.status == 'INACTIVE':
        return render(request, 'brands/store_inactive.html', {'brand': brand})
    
    from apps.catalog.models import Collection, Category
    from apps.brands.models import BrandIntegration
    
    post = get_object_or_404(BlogPost, slug=post_slug, brand=brand, is_published=True)
    
    # Related posts: other published posts, excluding the current one
    related_posts = BlogPost.objects.filter(brand=brand, is_published=True).exclude(id=post.id).order_by('?')[:3]
    
    # Build the absolute URL for social sharing
    share_url = request.build_absolute_uri()
    
    theme_base = f"storefront/{brand.theme.template_folder}/base.html" if brand.theme and brand.theme.is_active else "brands/store_base.html"
    collections = Collection.objects.filter(brand=brand, is_active=True).order_by('-created_at')
    categories = Category.objects.filter(brand=brand, is_active=True).order_by('display_order')
    
    whatsapp_addon = BrandIntegration.objects.filter(
        brand=brand, 
        integration__provider_code='WHATSAPP', 
        is_active=True
    ).first()
    
    return render(request, 'brands/store_blog_detail.html', {
        'brand': brand,
        'post': post,
        'related_posts': related_posts,
        'share_url': share_url,
        'theme_base': theme_base,
        'collections': collections,
        'categories': categories,
        'whatsapp_addon': whatsapp_addon,
    })

