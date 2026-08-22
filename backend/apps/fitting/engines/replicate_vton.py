import os
import io
import replicate
from typing import Dict, Any
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.base import ContentFile
import requests
from .base import VTOEngine
from apps.core.models import GlobalSettings

class ReplicateVTONEngine(VTOEngine):
    """
    Serverless VTO Engine using Replicate API (e.g. Kolors Virtual Try-On).
    This offloads GPU requirements and allows standard VPS deployment.
    """
    def __init__(self):
        super().__init__()
        
    def generate(self, user_photo_path: str, product_photo_path: str, try_on_id: int = None, **kwargs) -> Dict[str, Any]:
        settings = GlobalSettings.get_settings()
        api_key = settings.replicate_api_key
        
        if not api_key:
            return {
                'status': 'FAILED',
                'error_message': 'Replicate API Key is not configured in Global Settings.'
            }
            
        # Set environment variable for replicate library
        os.environ['REPLICATE_API_TOKEN'] = api_key
        
        try:
            model_version = settings.replicate_model_version or "cuiaxi/kolors-virtual-try-on"
            
            # Open files
            with open(user_photo_path, "rb") as person_img, open(product_photo_path, "rb") as garment_img:
                # Kolors-virtual-try-on API format:
                # https://replicate.com/cuiaxi/kolors-virtual-try-on
                input_data = {
                    "person_img": person_img,
                    "garment_img": garment_img,
                    "garment_des": kwargs.get('garment_description', 'clothing')
                }
                
                # Run the prediction
                # replicate.run returns a URL to the output image
                output_url = replicate.run(
                    model_version,
                    input=input_data
                )
                
            if not output_url:
                raise Exception("API returned empty output.")
                
            # Download the result
            response = requests.get(output_url)
            if response.status_code != 200:
                raise Exception("Failed to download generated image from Replicate.")
                
            result_file = SimpleUploadedFile(
                name="vto_replicate_result.jpg",
                content=response.content,
                content_type="image/jpeg"
            )
            
            return {
                'status': 'COMPLETED',
                'result_image_file': result_file,
                'confidence_score': 0.99
            }
            
        except Exception as e:
            return {
                'status': 'FAILED',
                'error_message': f'Replicate Generation Failed: {str(e)}'
            }
