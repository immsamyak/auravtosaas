from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.decorators.clickjacking import xframe_options_sameorigin
from apps.catalog.models import ProductVariant
from apps.fitting.models import VirtualTryOn, FitPassport, VTOPhotoVault, VTOSession

from django.utils import timezone

@xframe_options_sameorigin
def try_on_view(request, slug, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    
    # Identify user or session
    user = request.user if request.user.is_authenticated else None
    
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    
    # Get or create FitPassport
    if user:
        passport, _ = FitPassport.objects.get_or_create(user=user)
    else:
        passport, _ = FitPassport.objects.get_or_create(session_key=session_key)
        
    # Check for active VTO session
    vto_session = VTOSession.objects.filter(passport=passport, status='ACTIVE').order_by('-created_at').first()
    if not vto_session:
        vto_session = VTOSession.objects.create(passport=passport)
    
    photo_profile = VTOPhotoVault.objects.filter(passport=passport, is_default=True).order_by('-created_at').first()
    
    if not photo_profile:
        return redirect('guest_photo_upload', slug=slug, variant_id=variant_id)
        
    from apps.fitting.services.vto_service import VirtualTryOnService
    
    # Check if a recent try-on exists
    try_on = VirtualTryOn.objects.filter(
        session=vto_session,
        base_photo=photo_profile,
        product_variant=variant
    ).order_by('-created_at').first()
    
    # Only process a new try-on if there isn't one, or the last one is very old (e.g., > 1 hour)
    # If the last one failed, only retry if it's a POST request (user clicked retry)
    should_process = False
    if not try_on:
        should_process = True
    elif (timezone.now() - try_on.created_at).total_seconds() > 3600:
        should_process = True
    elif try_on.status == 'FAILED' and request.method == 'POST':
        should_process = True
        
    if should_process:
        # Check Billing Quota
        brand = variant.product.brand
        try:
            subscription = brand.subscription
        except:
            return render(request, 'fitting/error.html', {'message': 'This store does not have an active billing plan.'})

        if not subscription.can_try_on():
            return render(request, 'fitting/error.html', {'message': 'This store has exceeded its Try-On quota for the current billing cycle.'})

        try_on = VirtualTryOnService.process_try_on(
            session=vto_session,
            base_photo=photo_profile,
            variant=variant
        )
        
        # Increment quota usage
        subscription.try_ons_used += 1
        subscription.save()
    
    brand = variant.product.brand
    theme_base = f"storefront/{brand.theme.template_folder}/base.html" if brand.theme and brand.theme.is_active else "brands/store_base.html"
    
    from apps.catalog.models import Collection, Category
    from apps.fitting.services.size_intelligence import SizeIntelligenceService
    
    collections_qs = Collection.objects.filter(brand=brand, is_active=True).order_by('-created_at')
    categories_qs = Category.objects.filter(brand=brand, is_active=True).order_by('display_order')
    
    # Size Intelligence
    from apps.fitting.services.size_intelligence import SizeIntelligenceService
    recommended_size = SizeIntelligenceService.recommend_size(passport, variant)
    
    # Outfit Builder logic: Load all VTOProducts for this try_on
    outfit_items = []
    if try_on:
        from apps.fitting.models import VTOProduct
        outfit_items = VTOProduct.objects.filter(try_on=try_on).select_related('product_variant', 'product_variant__product')
        
    # Get products for selection modal (e.g. bottoms, shoes)
    from apps.catalog.models import Product
    store_products = Product.objects.filter(brand=brand, is_active=True).prefetch_related('variants')
    
    return render(request, 'fitting/try_on_result.html', {
        'try_on': try_on, 
        'variant': variant, 
        'is_guest': user is None,
        'theme_base': theme_base,
        'brand': brand,
        'collections': collections_qs,
        'categories': categories_qs,
        'recommended_size': recommended_size,
        'passport': passport,
        'outfit_items': outfit_items,
        'store_products': store_products,
    })

def guest_photo_upload_view(request, slug, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    
    if request.method == 'POST':
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        
        user = request.user if request.user.is_authenticated else None
        
        # Get or create FitPassport
        if user:
            passport, _ = FitPassport.objects.get_or_create(user=user)
        else:
            passport, _ = FitPassport.objects.get_or_create(session_key=session_key)
            
        height = request.POST.get('height_cm')
        weight = request.POST.get('weight_kg')
        fit_pref = request.POST.get('fit_preference')
        if height and weight:
            passport.height_cm = float(height)
            passport.weight_kg = float(weight)
        if fit_pref:
            passport.fit_preference = fit_pref
        passport.save()
            
        ai_avatar_id = request.POST.get('selected_avatar')
        selected_user_photo_id = request.POST.get('selected_user_photo_id')
        
        if ai_avatar_id:
            # User selected an AI model
            from apps.fitting.models import AIAvatarModel
            from django.core.files.base import ContentFile
            import os
            avatar = get_object_or_404(AIAvatarModel, id=ai_avatar_id)
            
            # Create a vault entry that copies the avatar image
            vault_entry = VTOPhotoVault.objects.create(
                passport=passport,
                pose_type='FRONT',
                is_default=True,
                quality_score=1.0,
                validation_metadata={'source': 'AI_AVATAR', 'avatar_id': avatar.id}
            )
            # Copy image file content
            vault_entry.image.save(os.path.basename(avatar.image.name), avatar.image.file, save=True)
            
            return redirect('try_on', slug=slug, variant_id=variant_id)
            
        elif selected_user_photo_id:
            # User selected a previously uploaded photo from their vault
            existing_photo = get_object_or_404(VTOPhotoVault, id=selected_user_photo_id, passport=passport)
            existing_photo.is_default = True
            existing_photo.save()
            return redirect('try_on', slug=slug, variant_id=variant_id)
            
        elif request.FILES.get('base_photo'):
            photo = request.FILES['base_photo']
            
            # Run AI Photo Quality Coach
            from apps.fitting.services.quality_coach import PhotoQualityCoach
            validation_result = PhotoQualityCoach.validate_photo(photo, pose_type='FRONT')
            
            if not validation_result['is_valid']:
                # Return to upload page with AI Coach feedback
                brand = variant.product.brand
                theme_base = f"storefront/{brand.theme.template_folder}/base.html" if brand.theme and brand.theme.is_active else "brands/store_base.html"
                from apps.catalog.models import Collection, Category
                collections_qs = Collection.objects.filter(brand=brand, is_active=True).order_by('-created_at')
                categories_qs = Category.objects.filter(brand=brand, is_active=True).order_by('display_order')
                
                from apps.fitting.models import AIAvatarModel
                avatars = AIAvatarModel.objects.filter(is_active=True).order_by('name')
                
                return render(request, 'fitting/upload_photo.html', {
                    'variant': variant,
                    'brand': brand,
                    'theme_base': theme_base,
                    'collections': collections_qs,
                    'categories': categories_qs,
                    'ai_coach_error': validation_result['feedback'],
                    'avatars': avatars,
                })
            
            # Save photo to vault
            VTOPhotoVault.objects.create(
                passport=passport,
                image=photo,
                pose_type='FRONT',
                is_default=True,
                quality_score=validation_result['score'],
                validation_metadata=validation_result['metadata']
            )
            return redirect('try_on', slug=slug, variant_id=variant_id)
        
    user = request.user if request.user.is_authenticated else None
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    
    if user:
        passport, _ = FitPassport.objects.get_or_create(user=user)
    else:
        passport, _ = FitPassport.objects.get_or_create(session_key=session_key)

    brand = variant.product.brand
    theme_base = f"storefront/{brand.theme.template_folder}/base.html" if brand.theme and brand.theme.is_active else "brands/store_base.html"
        
    from apps.catalog.models import Collection, Category
    collections_qs = Collection.objects.filter(brand=brand, is_active=True).order_by('-created_at')
    categories_qs = Category.objects.filter(brand=brand, is_active=True).order_by('display_order')
        
    from apps.fitting.models import AIAvatarModel
    avatars = AIAvatarModel.objects.filter(is_active=True).order_by('name')
    
    # Get previously uploaded photos for this user
    user_photos = VTOPhotoVault.objects.filter(passport=passport).order_by('-created_at')
        
    return render(request, 'fitting/upload_photo.html', {
        'variant': variant,
        'brand': brand,
        'theme_base': theme_base,
        'collections': collections_qs,
        'categories': categories_qs,
        'avatars': avatars,
        'user_photos': user_photos,
    })
    
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.fitting.models import VirtualWardrobeLook, VTOProduct
import json

def check_vto_status_view(request, slug, try_on_id):
    try_on = get_object_or_404(VirtualTryOn, id=try_on_id)
    return JsonResponse({
        'status': try_on.status,
        'progress_percent': try_on.progress_percent
    })

def virtual_wardrobe_view(request, slug):
    from apps.fitting.models import VirtualTryOn, VTOSession
    from apps.brands.models import Brand
    
    brand = get_object_or_404(Brand, slug=slug)

    # If logged in, get by user, else get by session_key
    if request.user.is_authenticated:
        try_ons = VirtualTryOn.objects.filter(
            session__passport__user=request.user, 
            status='COMPLETED'
        ).select_related('product_variant', 'product_variant__product').order_by('-processing_completed_at')
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        try_ons = VirtualTryOn.objects.filter(
            session__session_key=session_key, 
            status='COMPLETED'
        ).select_related('product_variant', 'product_variant__product').order_by('-processing_completed_at')
    
    return render(request, 'fitting/wardrobe.html', {
        'try_ons': try_ons,
        'brand': brand
    })

@require_POST
def save_look_api(request):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'Authentication required'}, status=401)
        
    try:
        data = json.loads(request.body)
        try_on_id = data.get('try_on_id')
        notes = data.get('notes', '')
        
        try_on = VirtualTryOn.objects.get(id=try_on_id)
        
        # Verify ownership
        if try_on.session.passport.user != request.user:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
            
        look, created = VirtualWardrobeLook.objects.get_or_create(
            user=request.user,
            try_on=try_on,
            defaults={'notes': notes}
        )
        
        return JsonResponse({'status': 'success', 'created': created})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@require_POST
def add_to_outfit_api(request):
    try:
        data = json.loads(request.body)
        try_on_id = data.get('try_on_id')
        product_id = data.get('product_id')
        product_type = data.get('product_type', 'BOTTOM')
        
        try_on = VirtualTryOn.objects.get(id=try_on_id)
        
        # Get first variant for this product for simplicity in MVP
        from apps.catalog.models import Product, ProductVariant
        product = Product.objects.get(id=product_id)
        variant = product.variants.first()
        
        if not variant:
            return JsonResponse({'status': 'error', 'message': 'Product has no variants'}, status=400)
            
        # Verify ownership
        is_owner = False
        if request.user.is_authenticated and try_on.session.passport.user == request.user:
            is_owner = True
        elif not request.user.is_authenticated and try_on.session.passport.session_key == request.session.session_key:
            is_owner = True
            
        if not is_owner:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
            
        # Check if already in outfit
        vto_product, created = VTOProduct.objects.get_or_create(
            try_on=try_on,
            product_type=product_type,
            defaults={
                'product_variant': variant
            }
        )
        if not created:
            vto_product.product_variant = variant
            vto_product.save()
            
        # Optional: Trigger re-generation of VTO with new items here
        # VirtualTryOnService.reprocess_outfit(try_on)
            
        return JsonResponse({
            'status': 'success',
            'added': {
                'name': product.name,
                'image': variant.image.url if variant.image else None
            }
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
