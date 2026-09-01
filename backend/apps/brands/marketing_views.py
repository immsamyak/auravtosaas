from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Brand, PopupBanner, Coupon, NewsletterSubscriber, EmailCampaign, BrandContactMessage
from apps.core.models import ContactMessage, BlogPost

@login_required
def marketing_dashboard_view(request):
    return redirect('popup_list')

@login_required
def popup_list_view(request):
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
        
    popups = PopupBanner.objects.filter(brand=brand).order_by('-created_at')
    return render(request, 'brands/marketing/popup_list.html', {
        'brand': brand,
        'popups': popups
    })

@login_required
def coupon_list_view(request):
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
        
    coupons = Coupon.objects.filter(brand=brand).order_by('-created_at')
    return render(request, 'brands/marketing/coupon_list.html', {
        'brand': brand,
        'coupons': coupons
    })

@login_required
def popup_create_view(request):
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
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        banner_type = request.POST.get('banner_type', 'TOP_BAR')
        headline = request.POST.get('headline', '')
        body_content = request.POST.get('body_content', '')
        image = request.FILES.get('image')
        cta_text = request.POST.get('cta_text', '')
        cta_link = request.POST.get('cta_link', '')
        open_in_new_tab = request.POST.get('open_in_new_tab') == 'on'
        display_rule = request.POST.get('display_rule', 'ALL_PAGES')
        specific_url = request.POST.get('specific_url', '')
        delay_seconds = int(request.POST.get('delay_seconds') or 0)
        is_active = request.POST.get('is_active') == 'on'
        
        PopupBanner.objects.create(
            brand=brand,
            title=title,
            description=description,
            banner_type=banner_type,
            headline=headline,
            body_content=body_content,
            image=image,
            cta_text=cta_text,
            cta_link=cta_link,
            open_in_new_tab=open_in_new_tab,
            display_rule=display_rule,
            specific_url=specific_url,
            delay_seconds=delay_seconds,
            is_active=is_active
        )
        messages.success(request, "Popup Banner created successfully.")
        return redirect('popup_list')
        
    return render(request, 'brands/marketing/popup_form.html', {
        'brand': brand,
        'banner_types': PopupBanner.BANNER_TYPES,
        'display_rules': PopupBanner.DISPLAY_RULES,
    })

@login_required
def popup_edit_view(request, popup_id):
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
        
    popup = get_object_or_404(PopupBanner, id=popup_id, brand=brand)
    
    if request.method == 'POST':
        popup.title = request.POST.get('title')
        popup.description = request.POST.get('description', '')
        popup.banner_type = request.POST.get('banner_type', 'TOP_BAR')
        popup.headline = request.POST.get('headline', '')
        popup.body_content = request.POST.get('body_content', '')
        if 'image' in request.FILES:
            popup.image = request.FILES['image']
        popup.cta_text = request.POST.get('cta_text', '')
        popup.cta_link = request.POST.get('cta_link', '')
        popup.open_in_new_tab = request.POST.get('open_in_new_tab') == 'on'
        popup.display_rule = request.POST.get('display_rule', 'ALL_PAGES')
        popup.specific_url = request.POST.get('specific_url', '')
        popup.delay_seconds = int(request.POST.get('delay_seconds') or 0)
        popup.is_active = request.POST.get('is_active') == 'on'
        
        popup.save()
        messages.success(request, "Popup Banner updated successfully.")
        return redirect('popup_list')
        
    return render(request, 'brands/marketing/popup_form.html', {
        'brand': brand,
        'popup': popup,
        'banner_types': PopupBanner.BANNER_TYPES,
        'display_rules': PopupBanner.DISPLAY_RULES,
    })

@login_required
def popup_delete_view(request, popup_id):
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
        popup = get_object_or_404(PopupBanner, id=popup_id, brand=brand)
        popup.delete()
        messages.success(request, "Popup deleted successfully.")
    return redirect('popup_list')

@login_required
def coupon_create_view(request):
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
        code = request.POST.get('code', '').upper()
        discount_type = request.POST.get('discount_type', 'PERCENTAGE')
        discount_value = float(request.POST.get('discount_value') or 0)
        condition = request.POST.get('condition', 'NONE')
        min_order_value = float(request.POST.get('min_order_value') or 0)
        max_uses = int(request.POST.get('max_uses') or 0)
        is_active = request.POST.get('is_active') == 'on'
        
        if Coupon.objects.filter(brand=brand, code=code).exists():
            messages.error(request, "A coupon with this code already exists.")
        else:
            Coupon.objects.create(
                brand=brand,
                code=code,
                discount_type=discount_type,
                discount_value=discount_value,
                condition=condition,
                min_order_value=min_order_value,
                max_uses=max_uses,
                is_active=is_active
            )
            messages.success(request, "Coupon created successfully.")
            return redirect('coupon_list')
            
    return render(request, 'brands/marketing/coupon_form.html', {
        'brand': brand,
        'discount_types': Coupon.DISCOUNT_TYPES,
        'conditions': Coupon.CONDITIONS,
    })

@login_required
def coupon_edit_view(request, coupon_id):
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
        
    coupon = get_object_or_404(Coupon, id=coupon_id, brand=brand)
    
    if request.method == 'POST':
        code = request.POST.get('code', '').upper()
        if code != coupon.code and Coupon.objects.filter(brand=brand, code=code).exists():
            messages.error(request, "A coupon with this code already exists.")
        else:
            coupon.code = code
            coupon.discount_type = request.POST.get('discount_type', 'PERCENTAGE')
            coupon.discount_value = float(request.POST.get('discount_value') or 0)
            coupon.condition = request.POST.get('condition', 'NONE')
            coupon.min_order_value = float(request.POST.get('min_order_value') or 0)
            coupon.max_uses = int(request.POST.get('max_uses') or 0)
            coupon.is_active = request.POST.get('is_active') == 'on'
            coupon.save()
            messages.success(request, "Coupon updated successfully.")
            return redirect('coupon_list')
            
    return render(request, 'brands/marketing/coupon_form.html', {
        'brand': brand,
        'coupon': coupon,
        'discount_types': Coupon.DISCOUNT_TYPES,
        'conditions': Coupon.CONDITIONS,
    })

@login_required
def coupon_delete_view(request, coupon_id):
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
        coupon = get_object_or_404(Coupon, id=coupon_id, brand=brand)
        coupon.delete()
        messages.success(request, "Coupon deleted successfully.")
    return redirect('marketing_dashboard')

# ─── Subscriber Views ────────────────────────────────────────
@login_required
def subscriber_list_view(request):
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
    
    subscribers = NewsletterSubscriber.objects.filter(brand=brand)
    
    # Search
    search_q = request.GET.get('q', '').strip()
    if search_q:
        subscribers = subscribers.filter(email__icontains=search_q)
    
    total_count = NewsletterSubscriber.objects.filter(brand=brand).count()
    active_count = NewsletterSubscriber.objects.filter(brand=brand, is_active=True).count()
    
    return render(request, 'brands/marketing/subscriber_list.html', {
        'brand': brand,
        'subscribers': subscribers,
        'total_count': total_count,
        'active_count': active_count,
        'filter_search': search_q,
    })

@login_required
def subscriber_delete_view(request, subscriber_id):
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
        subscriber = get_object_or_404(NewsletterSubscriber, id=subscriber_id, brand=brand)
        subscriber.delete()
        messages.success(request, f"Subscriber {subscriber.email} removed.")
    return redirect('subscriber_list')


from django.views.decorators.csrf import csrf_exempt

# ─── Public Storefront Subscribe API ─────────────────────────
@csrf_exempt
@require_POST
def newsletter_subscribe_api(request, brand_slug):
    """Public AJAX endpoint for storefront footer subscribe forms."""
    brand = get_object_or_404(Brand, slug=brand_slug)
    email = request.POST.get('email', '').strip().lower()
    
    if not email or '@' not in email:
        return JsonResponse({'success': False, 'message': 'Please enter a valid email address.'}, status=400)
    
    _, created = NewsletterSubscriber.objects.get_or_create(
        brand=brand, email=email,
        defaults={'is_active': True}
    )
    
    if created:
        # Trigger email notification async
        from apps.core.email_utils import dispatch_async_email
        context = {
            'email': email,
        }
        dispatch_async_email('newsletter_subscribed', context, [email], brand)
        return JsonResponse({'success': True, 'message': 'You have been subscribed successfully!'})
    else:
        return JsonResponse({'success': True, 'message': 'You are already subscribed!'})

@require_POST
def contact_submit_api(request, brand_slug):
    """Public AJAX endpoint for storefront contact forms."""
    brand = get_object_or_404(Brand, slug=brand_slug)
    first_name = request.POST.get('first_name', '').strip()
    last_name = request.POST.get('last_name', '').strip()
    email = request.POST.get('email', '').strip().lower()
    message = request.POST.get('message', '').strip()
    
    if not email or '@' not in email or not message:
        return JsonResponse({'success': False, 'message': 'Please provide a valid email and message.'}, status=400)
    
    name = f"{first_name} {last_name}".strip() or "Anonymous"
    
    # Save to the brand's specific contact messages table
    message_obj = BrandContactMessage.objects.create(
        brand=brand,
        name=name,
        email=email,
        message=message
    )
    
    # Trigger email notification async
    from apps.core.email_utils import dispatch_async_email
    context = {
        'user': {'first_name': name},
        'ticket_id': str(message_obj.id).zfill(6),
        'subject': 'Support Ticket Received'
    }
    dispatch_async_email('support_ticket_created', context, [email], brand)
    
    return JsonResponse({'success': True, 'message': 'Your message has been sent successfully!'})

# ==========================================
# EMAIL CAMPAIGNS
# ==========================================

@login_required
def campaign_list_view(request):
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
        
    campaigns = EmailCampaign.objects.filter(brand=brand).order_by('-created_at')
    
    return render(request, 'brands/marketing/campaign_list.html', {
        'brand': brand,
        'campaigns': campaigns
    })

@login_required
def campaign_create_view(request):
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
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        target_audience = request.POST.get('target_audience')
        html_content = request.POST.get('html_content')
        
        EmailCampaign.objects.create(
            brand=brand,
            name=name,
            subject=subject,
            target_audience=target_audience,
            html_content=html_content
        )
        
        messages.success(request, "Email campaign created successfully.")
        return redirect('campaign_list')
        
    return render(request, 'brands/marketing/campaign_form.html', {
        'brand': brand
    })

@login_required
def campaign_edit_view(request, campaign_id):
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
        
    campaign = get_object_or_404(EmailCampaign, id=campaign_id, brand=brand)
    
    # Do not allow editing if already sent
    if campaign.status == 'SENT':
        messages.error(request, "Cannot edit a campaign that has already been sent.")
        return redirect('campaign_list')
        
    if request.method == 'POST':
        campaign.name = request.POST.get('name')
        campaign.subject = request.POST.get('subject')
        campaign.target_audience = request.POST.get('target_audience')
        campaign.html_content = request.POST.get('html_content')
        campaign.save()
        
        messages.success(request, "Email campaign updated successfully.")
        return redirect('campaign_list')
        
    return render(request, 'brands/marketing/campaign_form.html', {
        'brand': brand,
        'campaign': campaign
    })

@login_required
def campaign_delete_view(request, campaign_id):
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
        
    campaign = get_object_or_404(EmailCampaign, id=campaign_id, brand=brand)
    
    if request.method == 'POST':
        campaign.delete()
        messages.success(request, "Email campaign deleted successfully.")
        
    return redirect('campaign_list')

@login_required
@require_POST
def campaign_send_view(request, campaign_id):
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    from django.utils import timezone
    from django.conf import settings
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
        
    campaign = get_object_or_404(EmailCampaign, id=campaign_id, brand=brand)
    
    if campaign.status == 'SENT':
        messages.error(request, "This campaign has already been sent.")
        return redirect('campaign_list')
        
    # Get recipients based on target_audience
    recipients = []
    
    if campaign.target_audience in ['SUBSCRIBERS', 'BOTH']:
        subscribers = NewsletterSubscriber.objects.filter(brand=brand, is_active=True).values_list('email', flat=True)
        recipients.extend(list(subscribers))
        
    if campaign.target_audience in ['CUSTOMERS', 'BOTH']:
        # Fetching customers dynamically based on orders
        from apps.orders.models import Order
        customer_emails = Order.objects.filter(brand=brand).exclude(customer_email='').values_list('customer_email', flat=True).distinct()
        recipients.extend(list(customer_emails))
        
    # Remove duplicates
    recipients = list(set(recipients))
    
    if not recipients:
        messages.warning(request, "No valid recipients found for the selected target audience.")
        return redirect('campaign_list')
        
    # Render the base HTML with the campaign content injected
    html_body = render_to_string('brands/marketing/emails/campaign_email_base.html', {
        'brand': brand,
        'content': campaign.html_content
    })
    
    try:
        from apps.core.email_utils import dispatch_async_email
        context = {
            'subject': campaign.subject,
            'campaign_content': campaign.html_content
        }
        dispatch_async_email('custom_campaign', context, recipients, brand)
        
        # Mark as sent
        campaign.status = 'SENT'
        campaign.sent_at = timezone.now()
        campaign.save()
        
        messages.success(request, f"Campaign successfully sent to {len(recipients)} recipient(s).")
    except Exception as e:
        messages.error(request, f"Failed to send campaign: {str(e)}")
        
    return redirect('campaign_list')

# ==========================================
# CONTACT MESSAGES
# ==========================================

@login_required
def contact_messages_list_view(request):
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')
        
    messages_list = BrandContactMessage.objects.filter(brand=brand).order_by('-created_at')
    total_count = messages_list.count()
    unread_count = messages_list.filter(is_read=False).count()
    read_count = total_count - unread_count
    
    return render(request, 'brands/marketing/contact_messages.html', {
        'brand': brand,
        'messages_list': messages_list,
        'total_count': total_count,
        'unread_count': unread_count,
        'read_count': read_count,
        'active_tab': 'marketing'
    })

@login_required
@require_POST
def contact_message_toggle_read_view(request, message_id):
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')
        
    contact_msg = get_object_or_404(BrandContactMessage, id=message_id, brand=brand)
    contact_msg.is_read = not contact_msg.is_read
    contact_msg.save()
    
    return redirect('contact_messages_list')

@login_required
@require_POST
def contact_message_reply_view(request, message_id):
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')
        
    contact_msg = get_object_or_404(BrandContactMessage, id=message_id, brand=brand)
    reply_body = request.POST.get('reply_body', '').strip()
    
    if not reply_body:
        messages.error(request, "Reply cannot be empty.")
        return redirect('contact_messages_list')
    
    try:
        from apps.core.email_utils import dispatch_async_email
        context = {
            'user': {'first_name': contact_msg.name},
            'ticket_id': str(contact_msg.id).zfill(6),
            'subject': f"Re: Your message to {brand.name}",
            'reply_body': reply_body
        }
        dispatch_async_email('support_ticket_replied', context, [contact_msg.email], brand)
        
        # Mark as read after replying
        contact_msg.is_read = True
        contact_msg.save()
        messages.success(request, f"Reply sent successfully to {contact_msg.email}.")
    except Exception as e:
        messages.error(request, f"Failed to send reply: {str(e)}")
    
    return redirect('contact_messages_list')

@login_required
@require_POST
def contact_message_mark_all_read_view(request):
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')
    
    BrandContactMessage.objects.filter(brand=brand, is_read=False).update(is_read=True)
    messages.success(request, "All messages marked as read.")
    return redirect('contact_messages_list')

@login_required
@require_POST
def contact_message_delete_view(request, message_id):
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')
        
    contact_msg = get_object_or_404(BrandContactMessage, id=message_id, brand=brand)
    contact_msg.delete()
    messages.success(request, "Message deleted successfully.")
    
    return redirect('contact_messages_list')


# ==========================================
# BRAND DASHBOARD: BLOG MANAGEMENT
# ==========================================

@login_required
def dashboard_blog_list_view(request):
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')
        
    posts = BlogPost.objects.filter(brand=brand).order_by('-created_at')
    
    from django.core.paginator import Paginator
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'brands/marketing/blog_list.html', {
        'brand': brand,
        'posts': page_obj,  # Pass the paginated object as 'posts'
        'page_obj': page_obj, # Pass 'page_obj' for pagination.html
        'active_tab': 'marketing'
    })

@login_required
def dashboard_blog_create_view(request):
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
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        content = request.POST.get('content')
        excerpt = request.POST.get('excerpt', '')
        author_name = request.POST.get('author_name', 'Aura Team')
        is_published = request.POST.get('is_published') == 'on'
        featured_image = request.FILES.get('featured_image')
        
        from django.utils import timezone
        published_at = timezone.now() if is_published else None
        
        try:
            BlogPost.objects.create(
                brand=brand,
                title=title,
                slug=slug,
                content=content,
                excerpt=excerpt,
                author_name=author_name,
                is_published=is_published,
                published_at=published_at,
                featured_image=featured_image
            )
            messages.success(request, "Blog post created successfully.")
            return redirect('dashboard_blog_list')
        except Exception as e:
            messages.error(request, f"Error creating blog post: {str(e)}")
            
    from django.urls import reverse
    breadcrumb_links = [{'name': 'Blog Posts', 'url': reverse('dashboard_blog_list')}]
    return render(request, 'brands/marketing/blog_form.html', {
        'brand': brand,
        'active_tab': 'marketing',
        'breadcrumb_links': breadcrumb_links
    })

@login_required
def dashboard_blog_edit_view(request, post_id):
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')
        
    post = get_object_or_404(BlogPost, id=post_id, brand=brand)
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.slug = request.POST.get('slug')
        post.content = request.POST.get('content')
        post.excerpt = request.POST.get('excerpt', '')
        post.author_name = request.POST.get('author_name', 'Aura Team')
        
        was_published = post.is_published
        post.is_published = request.POST.get('is_published') == 'on'
        
        if post.is_published and not was_published:
            from django.utils import timezone
            post.published_at = timezone.now()
            
        if 'featured_image' in request.FILES:
            post.featured_image = request.FILES['featured_image']
            
        try:
            post.save()
            messages.success(request, "Blog post updated successfully.")
            return redirect('dashboard_blog_list')
        except Exception as e:
            messages.error(request, f"Error updating blog post: {str(e)}")
            
    from django.urls import reverse
    breadcrumb_links = [{'name': 'Blog Posts', 'url': reverse('dashboard_blog_list')}]
    return render(request, 'brands/marketing/blog_form.html', {
        'brand': brand,
        'post': post,
        'active_tab': 'marketing',
        'breadcrumb_links': breadcrumb_links
    })

@login_required
@require_POST
def dashboard_blog_delete_view(request, post_id):
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')
        
    post = get_object_or_404(BlogPost, id=post_id, brand=brand)
    post.delete()
    messages.success(request, "Blog post deleted successfully.")
    
    return redirect('dashboard_blog_list')

