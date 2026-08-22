import os
import django
from django.core.files.uploadedfile import SimpleUploadedFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.fitting.engines.local import LocalVTOEngine

def run_test():
    print("--- REAL MOBILE-VTON END-TO-END INFERENCE TEST ---")
    
    # REAL VALID IMAGES
    # I am overriding the database test fixtures with verified real images in the media directory
    # User Photo: An actual uploaded PNG (not 15 bytes)
    user_photo_path = 'media/users/photo_profiles/original/ChatGPT_Image_Jul_26_2026_09_54_40_PM.png'
    # Product Photo: An actual image (not 15 bytes)
    product_photo_path = 'media/product_images/40year-old-happy-male-hr-600nw-2646474279.webp'
    
    user_path = os.path.join(os.getcwd(), user_photo_path)
    product_path = os.path.join(os.getcwd(), product_photo_path)
    
    if not os.path.exists(user_path) or not os.path.exists(product_path):
        print(f"Error: Could not find real test images.")
        print(f"User: {user_path}")
        print(f"Product: {product_path}")
        return
        
    print(f"Executing Genuine Mobile-VTON Pipeline...")
    print(f"User Image: {user_path}")
    print(f"Product Image: {product_path}")
    
    engine = LocalVTOEngine()
    
    import time
    start = time.time()
    
    result = engine.generate(
        user_photo_path=user_path,
        product_photo_path=product_path
    )
    
    print(f"\nStatus: {result.get('status')}")
    if result.get('status') == 'COMPLETED':
        img_file = result.get('result_image_file')
        # Save output so we can verify it
        output_path = 'media/vto_diffusion_output.jpg'
        with open(output_path, 'wb') as f:
            f.write(img_file.read())
        print(f"Result Image successfully generated via Diffusion and Saved at: {output_path}")
        print(f"AI Confidence: {result.get('confidence_score')}")
    else:
        print(f"Error Message: {result.get('error_message')}")
        
    print(f"Processing Time: {time.time() - start:.2f} seconds")

if __name__ == '__main__':
    run_test()
