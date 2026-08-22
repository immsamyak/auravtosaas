from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.brands.models import Brand
from .models import Location, StockLevel

@login_required(login_url='/login/')
def manage_warehouses_view(request):
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
        
    locations = Location.objects.filter(brand=brand).order_by('-is_active', 'name')
    
    # Calculate stock for each location manually in view or we can just pass locations
    for loc in locations:
        loc.total_stock = sum(sl.quantity for sl in loc.stock_levels.all())
        
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'add':
            name = request.POST.get('name')
            loc_type = request.POST.get('location_type')
            address = request.POST.get('address')
            Location.objects.create(
                brand=brand,
                name=name,
                location_type=loc_type,
                address=address,
                is_active=True
            )
            messages.success(request, 'Warehouse created successfully.')
        elif action == 'edit':
            loc_id = request.POST.get('location_id')
            loc = get_object_or_404(Location, id=loc_id, brand=brand)
            loc.name = request.POST.get('name')
            loc.location_type = request.POST.get('location_type')
            loc.address = request.POST.get('address')
            loc.is_active = request.POST.get('is_active') == 'on'
            loc.save()
            messages.success(request, 'Warehouse updated.')
        elif action == 'delete':
            loc_id = request.POST.get('location_id')
            loc = get_object_or_404(Location, id=loc_id, brand=brand)
            loc.delete()
            messages.success(request, 'Warehouse deleted.')
            
        return redirect('manage_warehouses')
        
    return render(request, 'inventory/manage_warehouses.html', {
        'locations': locations,
        'location_types': Location.LOCATION_TYPES
    })

@login_required(login_url='/login/')
def warehouse_detail_view(request, location_id):
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
        
    location = get_object_or_404(Location, id=location_id, brand=brand)
    stock_levels = location.stock_levels.select_related('product_variant', 'product_variant__product').all()
    
    return render(request, 'inventory/warehouse_detail.html', {
        'location': location,
        'stock_levels': stock_levels
    })
