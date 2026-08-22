import os
import torch
from diffusers import DiffusionPipeline
from PIL import Image

def test_catvton():
    print("Testing genuine CatVTON loading via Diffusers...")
    try:
        pipeline = DiffusionPipeline.from_pretrained(
            "zhengchong/CatVTON", 
            trust_remote_code=True,
            torch_dtype=torch.float32 # Try standard fp32 first, fallback to mps
        )
        print("Pipeline loaded successfully!")
    except Exception as e:
        print(f"Error loading pipeline: {str(e)}")

if __name__ == '__main__':
    test_catvton()
