from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.brands.models import Brand
from apps.brands.serializers import BrandSerializer

from apps.catalog.models import Product, ProductVariant
from apps.catalog.serializers import ProductSerializer, ProductVariantSerializer

from apps.fitting.models import VirtualTryOn
from apps.fitting.serializers import VirtualTryOnSerializer

class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public API to list and retrieve brand storefronts.
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'slug'

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public API to list products, filterable by brand.
    """
    queryset = Product.objects.all().prefetch_related('variants')
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        brand_slug = self.request.query_params.get('brand')
        if brand_slug:
            qs = qs.filter(brand__slug=brand_slug)
        return qs

class VirtualTryOnViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API to retrieve try-ons for the authenticated user.
    """
    serializer_class = VirtualTryOnSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return VirtualTryOn.objects.none()
        return VirtualTryOn.objects.filter(user=self.request.user)
