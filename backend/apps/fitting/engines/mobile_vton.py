import io
import os
import sys
import json
import torch
import torchvision
import numpy as np
from PIL import Image
from typing import Dict, Any
from django.core.files.uploadedfile import SimpleUploadedFile
from .base import VTOEngine

# Append vendor directory for Mobile-VTON modules
VENDOR_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../vendor/MobileVTON'))
if VENDOR_DIR not in sys.path:
    sys.path.insert(0, VENDOR_DIR)

class MobileVTONEngine(VTOEngine):
    """
    Mobile-VTON Genuine Diffusion Engine (0.41B).
    Mask-free, DensePose-free high-fidelity VTO designed for local inference.
    """
    
    def __init__(self):
        super().__init__()
        self.pipeline = None
        
    def _init_pipeline(self):
        if self.pipeline is not None:
            return
            
        try:
            import huggingface_hub
            from diffusers import FlowMatchEulerDiscreteScheduler
            from diffusers.models.autoencoders import AutoencoderKL
            from transformers import AutoImageProcessor, AutoModel, CLIPTextModelWithProjection, CLIPTokenizer
            from Mobile_VTON.models.autoencoders.vae import Decoder
            from Mobile_VTON.models.unets.unet_2d_condition_tryon import UNet2DConditionModel as Unet_Tryon
            from Mobile_VTON.models.unets.unet_2d_condition_garment import UNet2DConditionModel as Unet_Garment
            from Mobile_VTON.pipelines.tryon_pipeline_full_cat import T2IMobilePipelineV1_3_NotLoadingT5_Decoder as TryonPipeline
        except ImportError as e:
            raise ImportError(f"Mobile-VTON modules not found. {e}")

        # Ensure the model is available locally (we download beforehand)
        base_path = huggingface_hub.snapshot_download("FlashStight/Mobile-VTON")
        ckpt_path = os.path.join(base_path, "checkpoint")
        
        self.device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        self.weight_dtype = torch.float16 if self.device.type != 'cpu' else torch.float32 # Speed up MPS
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            self.weight_dtype = torch.float16
        elif torch.backends.mps.is_available():
            self.device = torch.device("mps")
            self.weight_dtype = torch.float16
        else:
            self.device = torch.device("cpu")
            self.weight_dtype = torch.float32

        # Scheduler
        noise_scheduler = FlowMatchEulerDiscreteScheduler(
            num_train_timesteps=1000,
            shift=3.0,
        )

        # Tokenizers
        self.tokenizer_one = CLIPTokenizer.from_pretrained(ckpt_path, subfolder="tokenizer")
        self.tokenizer_two = CLIPTokenizer.from_pretrained(ckpt_path, subfolder="tokenizer_2")
        
        text_encoder_one = CLIPTextModelWithProjection.from_pretrained(ckpt_path, subfolder="text_encoder", low_cpu_mem_usage=False)
        text_encoder_two = CLIPTextModelWithProjection.from_pretrained(ckpt_path, subfolder="text_encoder_2", low_cpu_mem_usage=False)

        # VAE
        vae = AutoencoderKL.from_pretrained(ckpt_path, subfolder="vae", low_cpu_mem_usage=False)
        
        # Decoder
        vd_cfg = os.path.join(ckpt_path, "vae_decoder/decoder.json")
        vd_ckpt = os.path.join(ckpt_path, "vae_decoder/decoder.pt")
        with open(vd_cfg, "r") as f:
            vd_cfg_json = json.load(f)
        vae_decoder = Decoder(**vd_cfg_json)
        vae_decoder.load_state_dict(torch.load(vd_ckpt, map_location="cpu"), strict=True)
        
        # DINOv2
        image_encoder = AutoModel.from_pretrained(ckpt_path, subfolder="image_encoder", low_cpu_mem_usage=False)
        
        # UNets
        denoiser = Unet_Tryon.from_pretrained(ckpt_path, subfolder="denoiser", low_cpu_mem_usage=False)
        denoiser_garment = Unet_Garment.from_pretrained(ckpt_path, subfolder="denoiser_garment", low_cpu_mem_usage=False)
        
        # Load to MPS
        # Load to CPU
        vae.to(self.device, dtype=self.weight_dtype)
        vae_decoder.to(self.device, dtype=torch.float32) # MUST be fp32
        text_encoder_one.to(self.device, dtype=self.weight_dtype)
        text_encoder_two.to(self.device, dtype=self.weight_dtype)
        denoiser.to(self.device, dtype=self.weight_dtype)
        denoiser_garment.to(self.device, dtype=self.weight_dtype)
        image_encoder.to(self.device, dtype=self.weight_dtype)
        
        for m in [vae, vae_decoder, text_encoder_one, text_encoder_two, denoiser, denoiser_garment, image_encoder]:
            m.eval().requires_grad_(False)
            
        self.pipeline = TryonPipeline(
            vae=vae,
            vae_decoder=vae_decoder,
            scheduler=noise_scheduler,
            tokenizer=CLIPTokenizer.from_pretrained(ckpt_path, subfolder="tokenizer"),
            tokenizer_2=CLIPTokenizer.from_pretrained(ckpt_path, subfolder="tokenizer_2"),
            text_encoder=text_encoder_one,
            text_encoder_2=text_encoder_two,
            image_encoder=image_encoder,
            denoiser=denoiser,
            denoiser_garment=denoiser_garment,
        )
        self.pipeline.to(self.device)
        self.image_processor = AutoImageProcessor.from_pretrained(ckpt_path + "/image_encoder")

    def _prepare_image(self, pil_image, target_size=(768, 1024), convert_range=False):
        """Resizes image to target width x height and optionally scales to [-1, 1]"""
        from torchvision import transforms
        img = pil_image.resize(target_size, Image.LANCZOS)
        
        if convert_range:
            transform = transforms.Compose([
                transforms.ToTensor(), 
                transforms.Normalize([0.5], [0.5])
            ])
            return transform(img)
        return img

    def generate(self, user_photo_path: str, product_photo_path: str, try_on_id: int = None, **kwargs) -> Dict[str, Any]:
        try:
            self._init_pipeline()
        except Exception as e:
            return {
                'status': 'FAILED',
                'error_message': f'Mobile-VTON Init Failed: {str(e)}'
            }
            
        class GenerationCancelledException(Exception):
            pass
            
        # Set up progress tracking
        def progress_callback(pipe, step_index, timestep, callback_kwargs):
            if try_on_id is not None:
                try:
                    from apps.fitting.models import VirtualTryOn
                    try_on_record = VirtualTryOn.objects.get(id=try_on_id)
                    
                    if try_on_record.status == 'CANCELLED':
                        raise GenerationCancelledException("Generation cancelled by a newer request.")
                        
                    # Calculate percentage based on 20 inference steps
                    progress = int((step_index / 20.0) * 100)
                    try_on_record.progress_percent = progress
                    try_on_record.save(update_fields=['progress_percent'])
                except GenerationCancelledException:
                    raise
                except Exception as ex:
                    print(f"Failed to update progress: {ex}")
            return callback_kwargs

        try:
            width, height = 768, 1024
            
            user_pil = Image.open(user_photo_path).convert("RGB")
            cloth_pil_raw = Image.open(product_photo_path)
            
            # Remove background to fix concrete/grey blending issues
            try:
                import rembg
                # Remove background (returns RGBA)
                cloth_rgba = rembg.remove(cloth_pil_raw)
                # Composite onto pure white background
                cloth_pil = Image.new("RGB", cloth_rgba.size, (255, 255, 255))
                cloth_pil.paste(cloth_rgba, mask=cloth_rgba.split()[3])
            except ImportError:
                cloth_pil = cloth_pil_raw.convert("RGB")
                
            # Prepare inputs according to Mobile-VTON format
            cloth_trim = self.image_processor(images=cloth_pil, return_tensors="pt").pixel_values 
            cloth_pure = self._prepare_image(cloth_pil, (width, height), convert_range=True).unsqueeze(0)
            image_tensor = self._prepare_image(user_pil, (width, height), convert_range=True).unsqueeze(0)
            
            # Fit Preference Modifiers
            fit_preference = kwargs.get('fit_preference', 'REGULAR')
            garment_desc = kwargs.get('garment_description', 'clothing').lower()
            
            fit_prompt_map = {
                'TIGHT': "tight, form-fitting, figure-hugging",
                'REGULAR': "well-fitted",
                'LOOSE': "baggy, oversized, loose-fitting, relaxed"
            }
            fit_modifier = fit_prompt_map.get(fit_preference, "well-fitted")
            
            # Prompts
            prompt = [f"Replace the upper body with a {fit_modifier} {garment_desc}"]
            prompt_c = [f"a {fit_modifier} {garment_desc}"]
            neg_prompt = ["deformed, distorted, disfigured, poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, mutated hands and fingers, disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation, NSFW"]
            
            with torch.no_grad():
                (
                    prompt_embeds,
                    negative_prompt_embeds,
                    pooled_prompt_embeds,
                    negative_pooled_prompt_embeds,
                ) = self.pipeline.encode_prompt(
                    prompt=prompt,
                    prompt_2=prompt,
                    num_images_per_prompt=1,
                    do_classifier_free_guidance=True,
                    negative_prompt=neg_prompt,
                    device=self.device,
                )

                (
                    prompt_embeds_c,
                    negative_prompt_embeds_c,
                    pooled_prompt_embeds_c,
                    negative_pooled_prompt_embeds_c,
                ) = self.pipeline.encode_prompt(
                    prompt=prompt_c,
                    prompt_2=prompt_c,
                    num_images_per_prompt=1,
                    do_classifier_free_guidance=False,
                    negative_prompt=neg_prompt,
                    device=self.device,
                )
                
                generator = torch.Generator(device=self.device).manual_seed(42)
                
                images = self.pipeline(
                    prompt_embeds=prompt_embeds,
                    negative_prompt_embeds=negative_prompt_embeds,
                    pooled_prompt_embeds=pooled_prompt_embeds,
                    negative_pooled_prompt_embeds=negative_pooled_prompt_embeds,
                    num_inference_steps=20,
                    generator=generator,
                    height=height,
                    width=width,
                    guidance_scale=3.5,
                    text_embeds_cloth=prompt_embeds_c,
                    negative_text_embeds_cloth=negative_prompt_embeds_c,
                    cloth=cloth_pure.to(self.device), 
                    image=(image_tensor.to(self.device) + 1.0) / 2.0, 
                    ip_adapter_image=cloth_trim.to(self.device), 
                    device=self.device,
                    callback_on_step_end=progress_callback,
                )[0]
                
                result_pil = images[0]
            
            buffer = io.BytesIO()
            result_pil.save(buffer, format="JPEG", quality=90)
            buffer.seek(0)
            
            result_file = SimpleUploadedFile(
                name="vto_mobile_result.jpg",
                content=buffer.read(),
                content_type="image/jpeg"
            )
            
            return {
                'status': 'COMPLETED',
                'result_image_file': result_file,
                'confidence_score': 0.99
            }
        except GenerationCancelledException:
            return {
                'status': 'CANCELLED',
                'error_message': 'Cancelled'
            }
        except Exception as e:
            return {
                'status': 'FAILED',
                'error_message': f'Mobile-VTON Generation Failed: {str(e)}'
            }
