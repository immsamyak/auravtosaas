import os
import sys
import huggingface_hub

print("Downloading Mobile-VTON from HuggingFace to local cache...")
model_path = huggingface_hub.snapshot_download("FlashStight/Mobile-VTON")
print(f"Downloaded to: {model_path}")
