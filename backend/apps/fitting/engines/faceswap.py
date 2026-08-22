import io
import os
import sys
import json
import cv2
import numpy as np
from PIL import Image
from typing import Dict, Any
from django.core.files.uploadedfile import SimpleUploadedFile
from .base import VTOEngine

class FaceSwapEngine(VTOEngine):
    """
    Face Swap Engine (ID Transfer).
    Replaces the product model's face with the user's face using InsightFace (inswapper).
    """
    
    def __init__(self):
        super().__init__()
        self.face_analyzer = None
        self.face_swapper = None
        
    def _init_pipeline(self):
        if self.face_swapper is not None:
            return
            
        try:
            import insightface
            from insightface.app import FaceAnalysis
        except ImportError as e:
            raise ImportError(f"InsightFace modules not found. {e}")

        # Ensure the model is available locally
        model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../vendor/models/inswapper_128.onnx'))
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"inswapper_128.onnx not found at {model_path}")

        # Initialize Face Analyzer
        providers = ['CPUExecutionProvider']
        
        self.face_analyzer = FaceAnalysis(name='buffalo_l', providers=providers)
        self.face_analyzer.prepare(ctx_id=0, det_size=(640, 640))
        
        # Initialize Face Swapper
        self.face_swapper = insightface.model_zoo.get_model(model_path, providers=providers)

    def generate(self, user_photo_path: str, product_photo_path: str, **kwargs) -> Dict[str, Any]:
        """
        Executes Face Swap.
        product_photo_path: The catalog model photo (target body/background).
        user_photo_path: The user's photo (source face).
        """
        try:
            self._init_pipeline()
            
            # Load images using OpenCV (InsightFace expects BGR numpy arrays)
            # user_photo is the source face
            source_img = cv2.imread(user_photo_path)
            # product_photo is the target body
            target_img = cv2.imread(product_photo_path)
            
            if source_img is None:
                raise ValueError(f"Could not read user photo at {user_photo_path}")
            if target_img is None:
                raise ValueError(f"Could not read product photo at {product_photo_path}")
            
            # Detect faces in source image
            source_faces = self.face_analyzer.get(source_img)
            if not source_faces:
                raise ValueError("No face detected in the user photo.")
            # Use the most prominent face
            source_face = sorted(source_faces, key=lambda x: x.bbox[2] * x.bbox[3], reverse=True)[0]
            
            # Detect faces in target image (catalog model)
            target_faces = self.face_analyzer.get(target_img)
            if not target_faces:
                raise ValueError("No face detected in the product model photo.")
            # Use the most prominent face
            target_face = sorted(target_faces, key=lambda x: x.bbox[2] * x.bbox[3], reverse=True)[0]
            
            # Perform face swap
            result_img = self.face_swapper.get(target_img, target_face, source_face, paste_back=True)
            
            # Convert BGR back to RGB for PIL
            result_rgb = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
            result_pil = Image.fromarray(result_rgb)
            
            # Save to byte stream
            img_io = io.BytesIO()
            result_pil.save(img_io, format='JPEG', quality=95)
            img_io.seek(0)
            
            # Create Django UploadedFile
            file_name = f"faceswap_result_{os.path.basename(user_photo_path).split('.')[0]}.jpg"
            output_file = SimpleUploadedFile(file_name, img_io.getvalue(), content_type='image/jpeg')
            
            return {
                'status': 'COMPLETED',
                'result_image_file': output_file,
                'confidence_score': 0.99
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                'status': 'FAILED',
                'error_message': f'Face Swap Init/Execute Failed: {str(e)}'
            }
