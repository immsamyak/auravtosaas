import sys
import os
import torch
from PIL import Image

# Import the engine directly
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.fitting.engines.mobile_vton import MobileVTONEngine

def test_local_vton():
    print("Initializing Mobile VTON Engine...")
    
    # Initialize engine
    engine = MobileVTONEngine()
    
    # Load test images (you will need to put two images in this folder)
    try:
        person_image = Image.open("test_person.jpg")
        garment_image = Image.open("test_garment.jpg")
    except FileNotFoundError:
        print("Error: test_person.jpg or test_garment.jpg not found in the current directory.")
        print("Please place these test images in the backend directory before running.")
        return
        
    print("Generating Virtual Try-On... (This may take several minutes on an i5/GTX 1050)")
    print("Generating Virtual Try-On... (This may take several minutes)")
    
    # Run inference
    result_image = engine.generate(
        person_image=person_image,
        garment_image=garment_image,
    result = engine.generate(
        user_photo_path="test_person.jpg",
        product_photo_path="test_garment.jpg",
        garment_type="upper_body" # or lower_body / dresses
    )
    
    result_image.save("vton_output.jpg")
    print("Success! Saved as vton_output.jpg")
    if result.get('status') == 'COMPLETED':
        file = result.get('result_image_file')
        with open("vton_output.jpg", "wb") as f:
            f.write(file.read())
        print("Success! Saved as vton_output.jpg")
    else:
        print("Failed:", result)

if __name__ == "__main__":
    test_local_vton()

