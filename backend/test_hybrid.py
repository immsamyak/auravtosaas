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
    
    user_photo = "media/users/photo_profiles/original/ChatGPT_Image_Jul_26_2026_09_54_40_PM_4M6naji.png"
    
    # 1. Product with Face
    print("--- Test 1: Product WITH Face ---")
    product_with_face = "media/product_images/40year-old-happy-male-hr-600nw-2646474279.webp"
    result1 = engine.generate(user_photo_path=user_photo, product_photo_path=product_with_face)
    print("Result 1:", result1.get('status'))
    
    # 2. Product WITHOUT Face
    # Let's see if there is an image without a face. If not, I'll just use a small dummy image.
    print("--- Test 2: Product WITHOUT Face ---")
    product_without_face = "dummy.jpg"
    import cv2, numpy as np
    cv2.imwrite(product_without_face, np.zeros((100, 100, 3), dtype=np.uint8))
    
    # I won't run full Mobile-VTON, just checking if it dispatches correctly.
    # To avoid 2 mins of Mobile-VTON generation, I'll mock the generate method of MobileVTONEngine
    engine.mobile_vton_engine = type('MockMobile', (object,), {'generate': lambda self, u, p, **kwargs: {'status': 'DISPATCHED_TO_MOBILE_VTON'}})()
    
    result2 = engine.generate(user_photo_path=user_photo, product_photo_path=product_without_face)
    print("Result 2:", result2.get('status'))

if __name__ == '__main__':
    main()
