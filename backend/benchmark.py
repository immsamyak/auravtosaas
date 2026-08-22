import os
import sys
import time
import torch
import huggingface_hub
from PIL import Image

# Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VENDOR_DIR = os.path.join(BASE_DIR, 'apps/fitting/vendor')
MOBILE_VENDOR = os.path.join(VENDOR_DIR, 'MobileVTON')
CAT_VENDOR = os.path.join(VENDOR_DIR, 'CatVTON')

user_photo_path = 'media/users/photo_profiles/original/ChatGPT_Image_Jul_26_2026_09_54_40_PM_4M6naji.png'
product_photo_path = 'media/product_images/40year-old-happy-male-hr-600nw-2646474279.webp'

user_path = os.path.join(BASE_DIR, user_photo_path)
product_path = os.path.join(BASE_DIR, product_photo_path)

def test_mobile_vton():
    print("\n" + "="*50)
    print("TESTING MOBILE-VTON (0.41B)")
    print("="*50)
    
    if MOBILE_VENDOR not in sys.path:
        sys.path.insert(0, MOBILE_VENDOR)
        
    start_time = time.time()
    
    try:
        from diffusers import FlowMatchEulerDiscreteScheduler
        from diffusers.models.autoencoders import AutoencoderKL
        from transformers import AutoImageProcessor, AutoModel, CLIPTextModelWithProjection, CLIPTokenizer
        import json
        from Mobile_VTON.models.autoencoders.vae import Decoder
        from Mobile_VTON.models.unets.unet_2d_condition_tryon import UNet2DConditionModel as Unet_Tryon
        from Mobile_VTON.models.unets.unet_2d_condition_garment import UNet2DConditionModel as Unet_Garment
        from Mobile_VTON.pipelines.tryon_pipeline_full_cat import T2IMobilePipelineV1_3_NotLoadingT5_Decoder as TryonPipeline
        
        base_path = huggingface_hub.snapshot_download("FlashStight/Mobile-VTON")
        ckpt_path = os.path.join(base_path, "checkpoint")
        device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
        
        noise_scheduler = FlowMatchEulerDiscreteScheduler(num_train_timesteps=1000, shift=3.0)
        tokenizer_one = CLIPTokenizer.from_pretrained(ckpt_path, subfolder="tokenizer")
        tokenizer_two = CLIPTokenizer.from_pretrained(ckpt_path, subfolder="tokenizer_2")
        text_encoder_one = CLIPTextModelWithProjection.from_pretrained(ckpt_path, subfolder="text_encoder", low_cpu_mem_usage=False)
        text_encoder_two = CLIPTextModelWithProjection.from_pretrained(ckpt_path, subfolder="text_encoder_2", low_cpu_mem_usage=False)
        vae = AutoencoderKL.from_pretrained(ckpt_path, subfolder="vae", low_cpu_mem_usage=False)
        
        vd_cfg = os.path.join(ckpt_path, "vae_decoder/decoder.json")
        vd_ckpt = os.path.join(ckpt_path, "vae_decoder/decoder.pt")
        with open(vd_cfg, "r") as f:
            vd_cfg_json = json.load(f)
        vae_decoder = Decoder(**vd_cfg_json)
        vae_decoder.load_state_dict(torch.load(vd_ckpt, map_location="cpu"), strict=True)
        
        image_encoder = AutoModel.from_pretrained(ckpt_path, subfolder="image_encoder", low_cpu_mem_usage=False)
        denoiser = Unet_Tryon.from_pretrained(ckpt_path, subfolder="denoiser", low_cpu_mem_usage=False)
        denoiser_garment = Unet_Garment.from_pretrained(ckpt_path, subfolder="denoiser_garment", low_cpu_mem_usage=False)
        
        vae.to(device, dtype=torch.float32)
        vae_decoder.to(device, dtype=torch.float32)
        text_encoder_one.to(device, dtype=torch.float32)
        text_encoder_two.to(device, dtype=torch.float32)
        denoiser.to(device, dtype=torch.float32)
        denoiser_garment.to(device, dtype=torch.float32)
        image_encoder.to(device, dtype=torch.float32)
        
        pipe = TryonPipeline(
            vae=vae, vae_decoder=vae_decoder, scheduler=noise_scheduler,
            tokenizer=tokenizer_one, tokenizer_2=tokenizer_two,
            text_encoder=text_encoder_one, text_encoder_2=text_encoder_two,
            image_encoder=image_encoder, denoiser=denoiser, denoiser_garment=denoiser_garment,
        )
        image_processor = AutoImageProcessor.from_pretrained(ckpt_path + "/image_encoder")
        
        width, height = 768, 1024
        
        from torchvision import transforms
        def prep(img_pil, size, convert=False):
            img = img_pil.resize(size, Image.LANCZOS)
            if convert:
                return transforms.Compose([transforms.ToTensor(), transforms.Normalize([0.5], [0.5])])(img)
            return img
            
        user_pil = Image.open(user_path).convert("RGB")
        cloth_pil = Image.open(product_path).convert("RGB")
        
        cloth_trim = image_processor(images=cloth_pil, return_tensors="pt").pixel_values
        cloth_pure = prep(cloth_pil, (width, height), True).unsqueeze(0)
        image_tensor = prep(user_pil, (width, height), True).unsqueeze(0)
        
        prompt = ["Replace the upper body with clothing"]
        prompt_c = ["clothing"]
        neg = ["deformed, NSFW, ugly, disgusting, blurry"]
        
        with torch.no_grad():
            pe, npe, ppe, nppe = pipe.encode_prompt(
                prompt=prompt,
                prompt_2=prompt,
                device=device,
                num_images_per_prompt=1,
                do_classifier_free_guidance=True,
                negative_prompt=neg
            )
            pec, npec, ppec, nppec = pipe.encode_prompt(
                prompt=prompt_c,
                prompt_2=prompt_c,
                device=device,
                num_images_per_prompt=1,
                do_classifier_free_guidance=False,
                negative_prompt=neg
            )
            
            generator = torch.Generator(device=device).manual_seed(42)
            
            images = pipe(
                prompt_embeds=pe, negative_prompt_embeds=npe, pooled_prompt_embeds=ppe, negative_pooled_prompt_embeds=nppe,
                num_inference_steps=20, generator=generator, height=height, width=width, guidance_scale=2.0,
                text_embeds_cloth=pec, negative_text_embeds_cloth=npec,
                cloth=cloth_pure.to(device), image=(image_tensor.to(device) + 1.0) / 2.0, ip_adapter_image=cloth_trim.to(device),
                device=device
            )[0]
            
            images[0].save(os.path.join(BASE_DIR, 'media/mobile_vton_result.jpg'))
            
        print(f"Mobile-VTON Success! Time taken: {time.time() - start_time:.2f}s")
    except Exception as e:
        print(f"Mobile-VTON Failed: {str(e)}")

def test_cat_vton():
    print("\n" + "="*50)
    print("TESTING CAT-VTON (0.86B)")
    print("="*50)
    print("CatVTON cannot be tested automatically here because it requires a DensePose agnostic mask generated from a secondary parsing network, which defeats the purpose of an end-to-end local VTO pipeline.")
    
if __name__ == "__main__":
    # Test Mobile-VTON
    test_mobile_vton()
    
    # Test CatVTON
    # test_cat_vton()
