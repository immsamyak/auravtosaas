import logging
import os
import time
from django.core.files.base import ContentFile
from gradio_client import Client, handle_file

logger = logging.getLogger(__name__)

class HuggingFaceVTONEngine:
    def generate(self, user_photo_path, product_photo_path, **kwargs):
        """
        Process virtual try-on using Hugging Face Spaces (via Gradio Client)
        """
        logger.info("Initializing HuggingFace VTO generation")
        
        from apps.core.models import GlobalSettings
        settings = GlobalSettings.objects.first()
        
        space_id = settings.hf_space_id if settings and settings.hf_space_id else "yisol/IDM-VTON"
        api_token = settings.hf_api_token if settings and settings.hf_api_token else None
        
        logger.info(f"Connecting to Hugging Face Space: {space_id}")
        
        client = None
        try:
            # Initialize client with `hf_token` (gradio_client 1.3.0)
            client = Client(space_id, hf_token=api_token)
            
            logger.info("Sending prediction request to Hugging Face...")
            start_time = time.time()
            
            if "fashn" in space_id.lower():
                # Fashn VTON 1.5 signature
                category = "tops"
                garment_desc = kwargs.get('garment_description', 'clothing')
                if "dress" in garment_desc:
                    category = "one-pieces"
                elif "pant" in garment_desc or "skirt" in garment_desc or "short" in garment_desc:
                    category = "bottoms"
                    
                result = client.predict(
                    person_image=handle_file(user_photo_path),
                    garment_image=handle_file(product_photo_path),
                    category=category,
                    garment_photo_type="model",
                    num_timesteps=30,
                    guidance_scale=1.5,
                    seed=42,
                    segmentation_free=True,
                    api_name="/try_on"
                )
                output_path = result
            else:
                # yisol/IDM-VTON Signature: 
                garment_desc = kwargs.get('garment_description', 'clothing')
                result = client.predict(
                    dict={"background": handle_file(user_photo_path), "layers": [], "composite": None},
                    garm_img=handle_file(product_photo_path),
                    garment_des=garment_desc,
                    is_checked=True,
                    is_checked_crop=False,
                    denoise_steps=30,
                    seed=42,
                    api_name="/tryon"
                )
                
                # Result is a tuple: (output, masked_image_output)
                if isinstance(result, tuple) or isinstance(result, list):
                    output_path = result[0]
                else:
                    output_path = result
                
            elapsed_time = time.time() - start_time
            logger.info(f"Hugging Face generation completed in {elapsed_time:.2f} seconds")
            
            # Read output image to save to Django
            with open(output_path, "rb") as f:
                image_data = f.read()
                
            return {
                'status': 'COMPLETED',
                'result_image_file': ContentFile(image_data, name="hf_vto_result.jpg"),
                'confidence_score': 95.0
            }
            
        except Exception as e:
            logger.error(f"Hugging Face API failed: {str(e)}", exc_info=True)
            
            error_msg = str(e)
            if "Expecting value: line 1 column 1 (char 0)" in error_msg or "JSON" in error_msg:
                friendly_error = "Hugging Face is blocking your server's IP address (Cloudflare challenge). You MUST add a free Hugging Face API Token to your Global Settings in the Admin Panel to bypass this block."
            else:
                friendly_error = f"Failed to connect to Hugging Face Space: {error_msg}"
                
            if client is None:
                return {
                    'status': 'FAILED',
                    'error_message': friendly_error
                }
                
            # Try fallback without kwargs if the user is using a custom/unlabeled space
            logger.info("Attempting fallback to unnamed endpoint (fn_index=2)...")
            try:
                result = client.predict(
                    handle_file(user_photo_path),
                    handle_file(product_photo_path),
                    garment_desc,
                    True,
                    False,
                    30,
                    42,
                    fn_index=2
                )
                
                if isinstance(result, tuple) or isinstance(result, list):
                    output_path = result[0]
                else:
                    output_path = result
                    
                with open(output_path, "rb") as f:
                    image_data = f.read()
                    
                return {
                    'status': 'COMPLETED',
                    'result_image_file': ContentFile(image_data, name="hf_vto_result_fallback.jpg"),
                    'confidence_score': 95.0
                }
                
            except Exception as e2:
                logger.error(f"Fallback endpoint also failed: {str(e2)}")
                return {
                    'status': 'FAILED',
                    'error_message': f"Hugging Face API failed: {str(e)} | Fallback failed: {str(e2)}"
                }
