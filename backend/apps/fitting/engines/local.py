import cv2
import logging
from typing import Dict, Any
from .base import VTOEngine
from .faceswap import FaceSwapEngine

logger = logging.getLogger(__name__)
_mobile_vton_engine_instance = None

class LocalVTOEngine(VTOEngine):
    """
    Hybrid Auto-Detect VTO Engine.
    Analyzes the product image to dynamically dispatch to the correct AI pipeline.
    - If product image has a face: Uses FaceSwapEngine
    - If product image has no face: Uses MobileVTONEngine
    """
    
    def __init__(self):
        super().__init__()
        self.face_analyzer = None
        self.face_swapper_engine = None
        self.mobile_vton_engine = None

    def _init_analyzer(self):
        if self.face_analyzer is not None:
            return
            
        try:
            from insightface.app import FaceAnalysis
        except ImportError as e:
            raise ImportError(f"InsightFace modules not found. {e}")

        # Initialize the lightweight face detector
        providers = ['CPUExecutionProvider']
        self.face_analyzer = FaceAnalysis(name='buffalo_l', providers=providers)
        self.face_analyzer.prepare(ctx_id=0, det_size=(640, 640))

    def detect_faces(self, image_path: str) -> int:
        """Returns the number of faces detected in the image."""
        try:
            self._init_analyzer()
            img = cv2.imread(image_path)
            if img is None:
                return 0
            faces = self.face_analyzer.get(img)
            return len(faces)
        except Exception as e:
            logger.error(f"Face detection failed: {e}")
            return 0

    def generate(self, user_photo_path: str, product_photo_path: str, **kwargs) -> Dict[str, Any]:
        global _mobile_vton_engine_instance
        try:
            # For Aura AI Studio: We ALWAYS want authentic VTO for clothing.
            # Face Swap is strictly forbidden for standard Virtual Try-On per Architecture Spec.
            # We bypass detect_faces and route directly to MobileVTONEngine.
            
            logger.info("Routing standard VTO request to MobileVTONEngine to guarantee authentic generation.")
            if _mobile_vton_engine_instance is None:
                from .mobile_vton import MobileVTONEngine
                _mobile_vton_engine_instance = MobileVTONEngine()
                
            return _mobile_vton_engine_instance.generate(user_photo_path, product_photo_path, **kwargs)
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                'status': 'FAILED',
                'error_message': f'Hybrid Engine Dispatch Failed: {str(e)}'
            }
