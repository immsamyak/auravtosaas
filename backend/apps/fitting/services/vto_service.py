from django.conf import settings
from django.utils import timezone
from apps.fitting.models import VirtualTryOn, VTOSession
from apps.fitting.engines.local import LocalVTOEngine
from apps.fitting.engines.mock import MockVTOEngine
from apps.fitting.engines.tryon_diffusion import TryOnDiffusionEngine
from apps.fitting.services.size_intelligence import SizeIntelligenceService
from apps.fitting.services.quality_coach import PhotoQualityCoach

class VirtualTryOnService:
    """
    Dedicated boundary for Virtual Try-On processing.
    Handles validation, state tracking, and invokes the correct VTOEngine instance.
    """
    
    @staticmethod
    def get_engine():
        engine_type = getattr(settings, 'VTO_ENGINE', 'tryon_diffusion')
        if engine_type == 'mock':
            return MockVTOEngine()
        elif engine_type == 'tryon_diffusion':
            return TryOnDiffusionEngine()
        return LocalVTOEngine()
        
    @staticmethod
    def process_try_on(session, base_photo, variant, selected_size=None):
        """
        Coordinates the Virtual Try-On workflow.
        """
        # 1. Validation Checks via Quality Coach
        validation_result = PhotoQualityCoach.validate_photo(base_photo.image, base_photo.pose_type)
        if not validation_result['is_valid']:
            # Could raise exception or return failed try-on immediately
            pass

        # 2. Size Intelligence (if no size selected)
        if not selected_size:
            selected_size = SizeIntelligenceService.recommend_size(session.passport, variant)

        # 3. Cancel any previous active try-ons for this session to free up resources
        VirtualTryOn.objects.filter(
            session=session,
            status__in=['PENDING', 'VALIDATING', 'PROCESSING']
        ).update(status='CANCELLED')

        # 4. Initialize Record
        try_on = VirtualTryOn.objects.create(
            session=session,
            base_photo=base_photo,
            product_variant=variant,
            selected_size=selected_size,
            status='VALIDATING',
            provider=getattr(settings, 'VTO_ENGINE', 'tryon_diffusion').upper(),
            processing_started_at=timezone.now()
        )
        
        # Link the primary variant to the new Outfit Builder VTOProduct structure
        from apps.fitting.models import VTOProduct
        VTOProduct.objects.create(
            try_on=try_on,
            product_variant=variant,
            selected_size=selected_size,
            product_type='TOP' # Default to top for single item try-ons
        )
            
        if not variant.vto_assets.exists():
            try_on.status = 'FAILED'
            try_on.error_message = "Product variant does not have a VTO-ready asset (e.g. flat lay or mask)."
            try_on.save()
            return try_on
            
        # 4. Processing
        try_on.status = 'PROCESSING'
        try_on.save()
        
        # 5. Spawn Background Thread
        # IMPORTANT: Use on_commit to prevent race conditions where the background thread 
        # attempts to read the Try-On before the DB transaction commits.
        from django.db import transaction
        import threading
        
        def start_thread():
            thread = threading.Thread(target=VirtualTryOnService.execute_vto_background, args=(try_on.id,))
            thread.daemon = True
            thread.start()
            
        transaction.on_commit(start_thread)
        
        return try_on
        
    @staticmethod
    def execute_vto_background(try_on_id):
        """
        Executes the actual VTO engine inference in a background thread to prevent UI timeouts.
        """
        from apps.fitting.models import VirtualTryOn
        
        try:
            try_on = VirtualTryOn.objects.get(id=try_on_id)
            engine = VirtualTryOnService.get_engine()
            
            # Use the first VTO product asset instead of marketing image
            vto_asset = try_on.product_variant.vto_assets.first()
            
            
            # Construct a highly descriptive garment prompt for the Diffusion model
            color_name = try_on.product_variant.color.name.lower()
            product_name = try_on.product_variant.product.name.lower()
            cat_name = try_on.product_variant.product.category.name.lower() if try_on.product_variant.product.category else "clothing"
            
            base_desc = f"{color_name} {cat_name}, {product_name}"
            # Diffusion models need explicit hints for sleeve length if replacing long sleeves
            if 't-shirt' in base_desc or 'tshirt' in base_desc or 'tee' in base_desc:
                if 'short sleeve' not in base_desc:
                    base_desc = f"short sleeve {base_desc}"
                    
            result = engine.generate(
                user_photo_path=try_on.base_photo.image.path,
                product_photo_path=vto_asset.image.path if vto_asset else try_on.product_variant.image.path,
                try_on_id=try_on.id,
                fit_preference=try_on.session.passport.fit_preference if hasattr(try_on.session, 'passport') else 'REGULAR',
                garment_description=base_desc
            )
            
            # Result Handling
            if result.get('status') == 'COMPLETED':
                try_on.status = 'COMPLETED'
                try_on.generated_image = result.get('result_image_file')
                try_on.ai_confidence_score = result.get('confidence_score')
                
                # Notify customer
                from apps.core.utils import notify
                notify(
                    user=try_on.session.user,
                    title="Try-On Complete! 🎉",
                    message=f"Your fitting for {try_on.product_variant.product.name} is ready to view.",
                    icon_class="fa-solid fa-wand-magic-sparkles text-indigo-500",
                    action_url=f"/store/{try_on.product_variant.product.brand.slug}/try-on/status/{try_on.id}/"
                )
                
            elif result.get('status') == 'CANCELLED':
                # The try_on was already cancelled by a newer request
                try_on.status = 'CANCELLED'
            else:
                try_on.status = 'FAILED'
                try_on.error_message = result.get('error_message', 'Unknown VTO Engine failure')
                
            try_on.processing_completed_at = timezone.now()
            try_on.save()
            
        except Exception as e:
            # Handle catastrophic thread failures
            try:
                try_on = VirtualTryOn.objects.get(id=try_on_id)
                try_on.status = 'FAILED'
                try_on.error_message = f"Background Thread Exception: {str(e)}"
                try_on.processing_completed_at = timezone.now()
                try_on.save()
            except:
                pass
