import sys
import os
import torch
from PIL import Image
import shutil

# Import the engine directly
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.fitting.engines.mobile_vton import MobileVTONEngine

def batch_local_vton():
    print("Initializing Mobile VTON Engine...")
    engine = MobileVTONEngine()
    
    # Pairs based on the generated filenames
    pairs = [
        ("person_pose_1_1787805281017.jpg", "garment_1_1787805345957.jpg", "blue denim jacket"),
        ("person_pose_2_1787805296588.jpg", "garment_2_1787805358598.jpg", "yellow hoodie"),
        ("person_pose_3_1787805308792.jpg", "garment_3_1787805369676.jpg", "green knitted sweater"),
        ("person_pose_4_1787805320702.jpg", "garment_4_1787805383479.jpg", "black leather jacket"),
        ("person_pose_5_1787805333398.jpg", "garment_5_1787805395715.jpg", "white button-up shirt")
    ]
    
    artifact_dir = r"C:\Users\user\.gemini\antigravity\brain\787530cb-f8f5-4e96-b192-e3e72eefac0c"
    
    for i, (person, garment, desc) in enumerate(pairs, 1):
        print(f"\n--- Processing Pair {i}/5 ---")
        output_name = f"vton_batch_output_{i}.jpg"
        output_path = os.path.join(artifact_dir, output_name)
        
        if os.path.exists(output_path):
            print(f"Skipping pair {i} because {output_path} already exists.")
            continue
            
        print(f"Person: {person}")
        print(f"Garment: {garment} ({desc})")
        
        try:
            result = engine.generate(
                user_photo_path=person,
                product_photo_path=garment,
                garment_type="upper_body",
                garment_description=desc,
                fit_preference="REGULAR"
            )
            
            if result.get('status') == 'COMPLETED':
                file = result.get('result_image_file')
                with open(output_name, "wb") as f:
                    f.write(file.read())
                print(f"Success! Saved as {output_name}")
                
                # Copy to artifacts
                shutil.copy(output_name, os.path.join(artifact_dir, output_name))
            else:
                print("Failed:", result)
        except Exception as e:
            print(f"Error on pair {i}: {e}")

if __name__ == "__main__":
    batch_local_vton()

