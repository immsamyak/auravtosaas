import os
import sys

# Setup django
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.fitting.engines.local import LocalVTOEngine

def main():
    engine = LocalVTOEngine()
    
    # User's image (source face)
    user_photo = "media/users/photo_profiles/original/ChatGPT_Image_Jul_26_2026_09_54_40_PM_4M6naji.png"
    # Catalog model (target body)
    product_photo = "media/product_images/40year-old-happy-male-hr-600nw-2646474279.webp"
    
    print("Executing Face Swap...")
    result = engine.generate(user_photo_path=user_photo, product_photo_path=product_photo)
    
    if result.get('status') == 'COMPLETED':
        print("Success!")
        # save the bytes back to disk
        out_path = "media/faceswap_test_output.jpg"
        with open(out_path, "wb") as f:
            f.write(result['result_image_file'].read())
        print(f"Saved to {out_path}")
    else:
        print("Failed:", result)

if __name__ == '__main__':
    main()
