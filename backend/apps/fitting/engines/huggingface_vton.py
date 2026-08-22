import logging
import os
import time
from django.core.files.base import ContentFile
from gradio_client import Client, handle_file

logger = logging.getLogger(__name__)

class HuggingFaceVTONEngine:
    def process_try_on(self, user_photo_path, product_photo_path, **kwargs):
        """
        Process virtual try-on using Hugging Face Spaces (via Gradio Client)
        """
        logger.info("Initializing HuggingFace VTO generation")
        
        from apps.core.models import GlobalSettings
        settings = GlobalSettings.objects.first()
        
        space_id = settings.hf_space_id if settings and settings.hf_space_id else "Kwai-Kolors/Kolors-Virtual-Try-On"
        api_token = settings.hf_api_token if settings and settings.hf_api_token else None
        
        logger.info(f"Connecting to Hugging Face Space: {space_id}")
        
        try:
            # Initialize client
            client = Client(space_id, hf_token=api_token)
            
            # Prepare inputs (Assuming a standard Kolors VTON interface for Hugging Face)
            # This attempts to match common gradio endpoints for Kolors VTON spaces
            # Usually: person_img, garment_img, seed, randomize_seed
            
            logger.info("Sending prediction request to Hugging Face...")
            start_time = time.time()
            
            # Most VTON spaces on HF take human_img and garm_img and return the result at index 0 or as a tuple
            # We will use the handle_file helper to upload local files safely to Gradio
            result = client.predict(
                handle_file(user_photo_path),
                handle_file(product_photo_path),
                0,      # seed
                True,   # randomize_seed
                api_name="/tryon" # Try to hit named endpoint first
            )
            
            # Result could be a tuple (image_path, mask_path) or just the image string path
            if isinstance(result, tuple) or isinstance(result, list):
                output_path = result[0]
            else:
                output_path = result
                
            elapsed_time = time.time() - start_time
            logger.info(f"Hugging Face generation completed in {elapsed_time:.2f} seconds")
            
            # Read output image to save to Django
            with open(output_path, "rb") as f:
                image_data = f.read()
                
            return ContentFile(image_data, name="hf_vto_result.jpg")
            
        except Exception as e:
            logger.error(f"Hugging Face API failed: {str(e)}", exc_info=True)
            
            # Try fallback to unlabeled fn_index=2 if /tryon doesn't exist
            logger.info("Attempting fallback to unnamed endpoint (fn_index=2)...")
            try:
                result = client.predict(
                    handle_file(user_photo_path),
                    handle_file(product_photo_path),
                    0,
                    True,
                    fn_index=2
                )
                
                if isinstance(result, tuple) or isinstance(result, list):
                    output_path = result[0]
                else:
                    output_path = result
                    
                with open(output_path, "rb") as f:
                    image_data = f.read()
                    
                return ContentFile(image_data, name="hf_vto_result_fallback.jpg")
                
            except Exception as e2:
                logger.error(f"Fallback endpoint also failed: {str(e2)}")
                raise Exception(f"Hugging Face Generation Failed: {str(e)}\nFallback failed: {str(e2)}")
