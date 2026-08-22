import io
import time
from typing import Dict, Any
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from .base import VTOEngine

class MockVTOEngine(VTOEngine):
    """
    A mock provider strictly for development and testing.
    Composites the product image onto the user's photo using Pillow.
    This does NOT represent a real AI generation and must only be used when VTO_ENGINE = 'mock'.
    """
    
    def generate(self, user_photo_path: str, product_photo_path: str, **kwargs) -> Dict[str, Any]:
        """
        Mock generation that composites the product onto the user's photo.
        """
        import os
        from django.conf import settings
        
        # Security: Prevent MockEngine from ever running in a true production environment
        if os.environ.get('DJANGO_ENV') == 'production' or not settings.DEBUG:
            return {
                'status': 'FAILED',
                'error_message': 'MockVTOEngine is disabled in production environments for security.'
            }
            
        try:
            if not user_photo_path or not product_photo_path:
                raise ValueError("Missing user photo or product photo for mock composite.")
                
            # Open images
            user_img = Image.open(user_photo_path).convert("RGBA")
            product_img = Image.open(product_photo_path).convert("RGBA")
            
            # Resize product to be ~60% of the user image width
            target_width = int(user_img.width * 0.6)
            aspect_ratio = product_img.height / product_img.width
            target_height = int(target_width * aspect_ratio)
            product_img = product_img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            
            # Paste product in the center of user image (roughly chest height)
            x = (user_img.width - target_width) // 2
            y = int((user_img.height - target_height) * 0.4)  # slightly above center
            
            # Create a composite
            composite = Image.alpha_composite(
                Image.new("RGBA", user_img.size), user_img
            )
            composite.paste(product_img, (x, y), product_img)
            
            # Convert to RGB and save to buffer
            result_img = composite.convert("RGB")
            buffer = io.BytesIO()
            result_img.save(buffer, format="JPEG", quality=85)
            buffer.seek(0)
            
            mock_file = SimpleUploadedFile(
                name="mock_result.jpg",
                content=buffer.read(),
                content_type="image/jpeg"
            )
            
            return {
                'status': 'COMPLETED',
                'result_image_file': mock_file,
            }
            
        except Exception as e:
            # Fallback if image processing fails
            return {
                'status': 'FAILED',
                'error_message': f'Mock generation failed: {str(e)}'
            }
