from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils.text import slugify
from django.db.models import Q
from apps.brands.models import Brand
from apps.catalog.models import Product, ProductVariant, Category, ProductType, Color, Size, Collection


def store_view(request, brand_slug):
    brand = get_object_or_404(Brand, slug=brand_slug)
    products = Product.objects.filter(brand=brand, is_active=True).prefetch_related('variants')
    collections = Collection.objects.filter(brand=brand, is_active=True)
    return render(request, 'catalog/store.html', {'products': products, 'brand': brand, 'collections': collections})


# ─── Helper: get brand-scoped + global items ───────────────────────────────
def _get_brand_attrs(brand):
    """Return categories, product_types, colors, sizes visible to this brand."""
    categories = Category.objects.filter(Q(brand=brand) | Q(brand__isnull=True), is_active=True).order_by('display_order')
    product_types = ProductType.objects.filter(Q(brand=brand) | Q(brand__isnull=True), is_active=True)
    colors = Color.objects.filter(Q(brand=brand) | Q(brand__isnull=True), is_active=True)
    sizes = Size.objects.filter(Q(brand=brand) | Q(brand__isnull=True), is_active=True).order_by('display_order')
    return categories, product_types, colors, sizes


# ─── Product Management ───────────────────────────────────────────────────
@login_required(login_url='/login/')
def manage_products_view(request):
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
        
    products_qs = Product.objects.filter(brand=brand).prefetch_related('variants').order_by('-created_at')
    
    # Stats
    total_products = products_qs.count()
    active_products = products_qs.filter(is_active=True).count()
    inactive_products = products_qs.filter(is_active=False).count()
    total_variants = ProductVariant.objects.filter(product__brand=brand).count()
    
    # Categories for filter dropdown
    categories = Category.objects.filter(Q(brand=brand) | Q(brand__isnull=True), is_active=True)
    
    # Filtering
    filter_category = request.GET.get('category', '')
    filter_search = request.GET.get('q', '')
    filter_active = request.GET.get('active', '')
    
    filtered_qs = products_qs
    if filter_category:
        filtered_qs = filtered_qs.filter(category_id=filter_category)
    if filter_search:
        filtered_qs = filtered_qs.filter(
            Q(name__icontains=filter_search) |
            Q(description__icontains=filter_search)
        )
    if filter_active == '1':
        filtered_qs = filtered_qs.filter(is_active=True)
    elif filter_active == '0':
        filtered_qs = filtered_qs.filter(is_active=False)
    
    # Toggle active status
    if request.method == 'POST':
        action = request.POST.get('action')
        product_id = request.POST.get('product_id')
        if action == 'toggle_active' and product_id:
            product = Product.objects.filter(id=product_id, brand=brand).first()
            if product:
                product.is_active = not product.is_active
                product.save()
                status = "activated" if product.is_active else "deactivated"
                messages.success(request, f'Product "{product.name}" {status}.')
            return redirect('manage_products')
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(filtered_qs, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'catalog/manage_products.html', {
        'brand': brand, 
        'products': page_obj,
        'page_obj': page_obj,
        'total_products': total_products,
        'active_products': active_products,
        'inactive_products': inactive_products,
        'total_variants': total_variants,
        'categories': categories,
        'filter_category': filter_category,
        'filter_search': filter_search,
        'filter_active': filter_active,
    })


@login_required(login_url='/login/')
def create_product_view(request):
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
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        product_type_id = request.POST.get('product_type')
        price = request.POST.get('price')
        
        color_id = request.POST.get('color')
        size_id = request.POST.get('size')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')
        
        product = Product.objects.create(
            brand=brand, 
            name=name, 
            description=description, 
            category_id=category_id, 
            product_type_id=product_type_id,
            price=price,
            seo_title=request.POST.get('seo_title', ''),
            seo_description=request.POST.get('seo_description', ''),
            seo_keywords=request.POST.get('seo_keywords', '')
        )
        if 'seo_og_image' in request.FILES:
            product.seo_og_image = request.FILES['seo_og_image']
            product.save()
        
        variant = ProductVariant.objects.create(
            product=product, 
            color_id=color_id, 
            size_id=size_id, 
            image=image
        )
        
        if stock:
            from apps.inventory.models import Location, StockLevel
            location, _ = Location.objects.get_or_create(brand=brand, name="Primary Store", defaults={'location_type': 'STORE'})
            StockLevel.objects.create(location=location, product_variant=variant, quantity=int(stock))
            
        messages.success(request, f'Product "{product.name}" created successfully.')
        return redirect('manage_products')
        
    categories, product_types, colors, sizes = _get_brand_attrs(brand)
    
    context = {
        'brand': brand, 
        'categories': categories, 
        'product_types': product_types, 
        'sizes': sizes, 
        'colors': colors,
    }
    return render(request, 'catalog/create_product.html', context)


@login_required(login_url='/login/')
def product_detail_view(request, product_id):
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
        
    product = get_object_or_404(Product, id=product_id, brand=brand)
    
    if request.method == 'POST':
        color_id = request.POST.get('color')
        size_id = request.POST.get('size')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')
        
        if color_id and size_id and image:
            variant = ProductVariant.objects.create(
                product=product, color_id=color_id, size_id=size_id, image=image
            )
            if stock:
                from apps.inventory.models import Location, StockLevel
                location, _ = Location.objects.get_or_create(brand=brand, name="Primary Store", defaults={'location_type': 'STORE'})
                StockLevel.objects.create(location=location, product_variant=variant, quantity=int(stock))
            
            messages.success(request, 'New variant added successfully.')
            return redirect('product_detail', product_id=product.id)
            
    _, _, colors, sizes = _get_brand_attrs(brand)
    return render(request, 'catalog/product_detail.html', {'brand': brand, 'product': product, 'sizes': sizes, 'colors': colors})


@login_required(login_url='/login/')
def edit_product_view(request, product_id):
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
        
    product = get_object_or_404(Product, id=product_id, brand=brand)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.description = request.POST.get('description')
        product.category_id = request.POST.get('category')
        product.product_type_id = request.POST.get('product_type')
        product.price = request.POST.get('price')
        
        # SEO Settings
        product.seo_title = request.POST.get('seo_title', product.seo_title)
        product.seo_description = request.POST.get('seo_description', product.seo_description)
        product.seo_keywords = request.POST.get('seo_keywords', product.seo_keywords)
        if 'seo_og_image' in request.FILES:
            product.seo_og_image = request.FILES['seo_og_image']
            
        product.save()
        messages.success(request, f'Product "{product.name}" updated successfully.')
        return redirect('manage_products')
        
    categories, product_types, colors, sizes = _get_brand_attrs(brand)
    return render(request, 'catalog/edit_product.html', {
        'product': product,
        'categories': categories,
        'product_types': product_types,
        'colors': colors,
        'sizes': sizes,
    })


@login_required(login_url='/login/')
def edit_variant_view(request, variant_id):
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
        
    variant = get_object_or_404(ProductVariant, id=variant_id, product__brand=brand)
    
    if request.method == 'POST':
        variant.color_id = request.POST.get('color')
        variant.size_id = request.POST.get('size')
        if request.FILES.get('image'):
            variant.image = request.FILES.get('image')
        variant.save()
        
        stock = request.POST.get('stock')
        if stock is not None and stock != '':
            from apps.inventory.models import Location, StockLevel
            location, _ = Location.objects.get_or_create(brand=brand, name="Primary Store", defaults={'location_type': 'STORE'})
            stock_level, _ = StockLevel.objects.get_or_create(location=location, product_variant=variant)
            stock_level.quantity = int(stock)
            stock_level.save()
            
        messages.success(request, 'Variant updated successfully.')
        return redirect('product_detail', product_id=variant.product.id)
        
    _, _, colors, sizes = _get_brand_attrs(brand)
    return render(request, 'catalog/edit_variant.html', {'variant': variant, 'sizes': sizes, 'colors': colors})


@login_required(login_url='/login/')
def delete_product_view(request, product_id):
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
        
    product = get_object_or_404(Product, id=product_id, brand=brand)
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted.')
    return redirect('manage_products')


@login_required(login_url='/login/')
def delete_variant_view(request, variant_id):
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
        
    variant = get_object_or_404(ProductVariant, id=variant_id, product__brand=brand)
    product_id = variant.product.id
    
    if request.method == 'POST':
        variant.delete()
        messages.success(request, 'Variant deleted successfully.')
    return redirect('product_detail', product_id=product_id)


# ─── Catalog Settings (CRUD for attributes) ───────────────────────────────
@login_required(login_url='/login/')
def catalog_settings_view(request):
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
        entity = request.POST.get('entity')

        if action == 'create':
            name = request.POST.get('name', '').strip()
            if not name:
                messages.error(request, 'Name is required.')
                return redirect('catalog_settings')

            base_slug = slugify(name)
            slug = base_slug
            counter = 1

            if entity == 'category':
                while Category.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                Category.objects.create(brand=brand, name=name, slug=slug)
                messages.success(request, f'Category "{name}" created.')

            elif entity == 'product_type':
                while ProductType.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                ProductType.objects.create(brand=brand, name=name, slug=slug)
                messages.success(request, f'Product Type "{name}" created.')

            elif entity == 'color':
                hex_code = request.POST.get('hex_code', '#000000')
                while Color.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                Color.objects.create(brand=brand, name=name, slug=slug, hex_code=hex_code)
                messages.success(request, f'Color "{name}" created.')

            elif entity == 'size':
                code = request.POST.get('code', name[:10].upper())
                while Size.objects.filter(code=code).exists():
                    code = f"{code[:8]}{counter}"
                    counter += 1
                while Size.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                order = request.POST.get('display_order', 0)
                Size.objects.create(brand=brand, name=name, slug=slug, code=code, display_order=int(order) if order else 0)
                messages.success(request, f'Size "{name}" created.')

        elif action == 'delete':
            item_id = request.POST.get('item_id')
            if entity == 'category':
                Category.objects.filter(id=item_id, brand=brand).delete()
            elif entity == 'product_type':
                ProductType.objects.filter(id=item_id, brand=brand).delete()
            elif entity == 'color':
                Color.objects.filter(id=item_id, brand=brand).delete()
            elif entity == 'size':
                Size.objects.filter(id=item_id, brand=brand).delete()
            messages.success(request, 'Item deleted.')

        return redirect('catalog_settings')

    # Get brand-specific + global items
    categories_brand = Category.objects.filter(brand=brand, is_active=True)
    categories_global = Category.objects.filter(brand__isnull=True, is_active=True)
    types_brand = ProductType.objects.filter(brand=brand, is_active=True)
    types_global = ProductType.objects.filter(brand__isnull=True, is_active=True)
    colors_brand = Color.objects.filter(brand=brand, is_active=True)
    colors_global = Color.objects.filter(brand__isnull=True, is_active=True)
    sizes_brand = Size.objects.filter(brand=brand, is_active=True).order_by('display_order')
    sizes_global = Size.objects.filter(brand__isnull=True, is_active=True).order_by('display_order')

    return render(request, 'catalog/catalog_settings.html', {
        'brand': brand,
        'categories_brand': categories_brand,
        'categories_global': categories_global,
        'types_brand': types_brand,
        'types_global': types_global,
        'colors_brand': colors_brand,
        'colors_global': colors_global,
        'sizes_brand': sizes_brand,
        'sizes_global': sizes_global,
    })


# ─── Quick Create (AJAX endpoint for inline creation) ─────────────────────
@login_required(login_url='/login/')
def quick_create_attr(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        brand = request.user.owned_brand
    except Brand.DoesNotExist:
        return JsonResponse({'error': 'No brand'}, status=403)

    entity = request.POST.get('entity')
    name = request.POST.get('name', '').strip()
    if not name:
        return JsonResponse({'error': 'Name is required'}, status=400)

    base_slug = slugify(name)
    slug = base_slug
    counter = 1

    if entity == 'category':
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"; counter += 1
        obj = Category.objects.create(brand=brand, name=name, slug=slug)
        return JsonResponse({'id': obj.id, 'name': obj.name})

    elif entity == 'product_type':
        while ProductType.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"; counter += 1
        obj = ProductType.objects.create(brand=brand, name=name, slug=slug)
        return JsonResponse({'id': obj.id, 'name': obj.name})

    elif entity == 'color':
        hex_code = request.POST.get('hex_code', '#000000')
        while Color.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"; counter += 1
        obj = Color.objects.create(brand=brand, name=name, slug=slug, hex_code=hex_code)
        return JsonResponse({'id': obj.id, 'name': obj.name})

    elif entity == 'size':
        code = request.POST.get('code', name[:10].upper())
        while Size.objects.filter(code=code).exists():
            code = f"{code[:8]}{counter}"; counter += 1
        while Size.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"; counter += 1
        obj = Size.objects.create(brand=brand, name=name, slug=slug, code=code)
        return JsonResponse({'id': obj.id, 'name': f"{obj.name} ({obj.code})"})

    return JsonResponse({'error': 'Unknown entity'}, status=400)


# ─── Collections ──────────────────────────────────────────────────────────
@login_required(login_url='/login/')
def manage_collections_view(request):
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

        if action == 'create':
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '')
            image = request.FILES.get('image')
            product_ids = request.POST.getlist('products')

            base_slug = slugify(name)
            slug = base_slug
            counter = 1
            while Collection.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"; counter += 1

            collection = Collection.objects.create(
                brand=brand, name=name, slug=slug,
                description=description, image=image
            )
            if product_ids:
                collection.products.set(product_ids)
            messages.success(request, f'Collection "{name}" created.')

        elif action == 'delete':
            coll_id = request.POST.get('collection_id')
            Collection.objects.filter(id=coll_id, brand=brand).delete()
            messages.success(request, 'Collection deleted.')

        elif action == 'toggle_active':
            coll_id = request.POST.get('collection_id')
            coll = Collection.objects.filter(id=coll_id, brand=brand).first()
            if coll:
                coll.is_active = not coll.is_active
                coll.save()

        return redirect('manage_collections')

    collections_qs = Collection.objects.filter(brand=brand).prefetch_related('products').order_by('-created_at')
    
    # Pagination for collections
    from django.core.paginator import Paginator
    paginator = Paginator(collections_qs, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    products = Product.objects.filter(brand=brand, is_active=True)

    return render(request, 'catalog/collections.html', {
        'brand': brand,
        'collections': page_obj,
        'page_obj': page_obj,
        'products': products,
    })


@login_required(login_url='/login/')
def edit_collection_view(request, collection_id):
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

    collection = get_object_or_404(Collection, id=collection_id, brand=brand)

    if request.method == 'POST':
        collection.name = request.POST.get('name', '').strip()
        collection.description = request.POST.get('description', '')
        if request.FILES.get('image'):
            collection.image = request.FILES.get('image')
        collection.save()

        product_ids = request.POST.getlist('products')
        collection.products.set(product_ids)
        messages.success(request, f'Collection "{collection.name}" updated.')
        return redirect('manage_collections')

    products = Product.objects.filter(brand=brand, is_active=True)
    return render(request, 'catalog/edit_collection.html', {
        'brand': brand,
        'collection': collection,
        'products': products,
    })
