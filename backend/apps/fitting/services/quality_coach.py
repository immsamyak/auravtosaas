import cv2
import numpy as np
from PIL import Image

class PhotoQualityCoach:
    """
    Validates user uploaded photos for VTO readiness using Computer Vision.
    """
    _face_analyzer = None

    @classmethod
    def _init_analyzer(cls):
        if cls._face_analyzer is None:
            try:
                from insightface.app import FaceAnalysis
                providers = ['CPUExecutionProvider']
                cls._face_analyzer = FaceAnalysis(name='buffalo_l', providers=providers)
                cls._face_analyzer.prepare(ctx_id=0, det_size=(640, 640))
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Failed to load InsightFace: {e}")
                
    @classmethod
    def validate_photo(cls, image_file, pose_type='FRONT'):
        """
        Validates the photo and returns a quality score and metadata.
        """
        if not image_file:
            return {
                'is_valid': False,
                'score': 0.0,
                'feedback': "No image provided.",
                'metadata': {}
            }
            
        try:
            # Read image from file-like object or path
            if hasattr(image_file, 'read'):
                image_bytes = image_file.read()
                if hasattr(image_file, 'seek'):
                    image_file.seek(0)
                nparr = np.frombuffer(image_bytes, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            else:
                img = cv2.imread(image_file.path if hasattr(image_file, 'path') else str(image_file))
                
            if img is None:
                raise ValueError("Could not read image file.")
                
            # 1. Blur Detection
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # 2. Brightness/Exposure
            brightness_score = np.mean(gray) / 255.0
            
            # 3. Face/Person Detection
            num_faces = 0
            try:
                # Use OpenCV's built-in Haar cascades for face detection (no heavy ML models required)
                cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                face_cascade = cv2.CascadeClassifier(cascade_path)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                num_faces = len(faces)
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Failed to run face detection: {e}")
                # Fallback to bypass strict blocking if detection fails internally
                num_faces = 1
                
            metadata = {
                'blur_variance': float(blur_score),
                'brightness_score': float(brightness_score),
                'faces_detected': num_faces,
                'pose_detected': pose_type
            }
            
            is_valid = True
            feedback_msgs = []
            
            if brightness_score < 0.2:
                is_valid = False
                feedback_msgs.append("The photo is too dark. Please use a well-lit room.")
            elif brightness_score > 0.85:
                is_valid = False
                feedback_msgs.append("The photo is overexposed (too bright).")
                
            if blur_score < 50: # Threshold for blur
                is_valid = False
                feedback_msgs.append("The photo is too blurry. Please hold the camera steady.")
                
            if num_faces == 0:
                is_valid = False
                feedback_msgs.append("No person detected. Please make sure your face is visible.")
            elif num_faces > 1:
                is_valid = False
                feedback_msgs.append("Multiple people detected. Please upload a solo photo.")

            score = 1.0
            if not is_valid:
                score = 0.2
                
            feedback = " ".join(feedback_msgs) if not is_valid else "Photo looks great! AI Coach approves."

            return {
                'is_valid': is_valid,
                'score': score,
                'feedback': feedback,
                'metadata': metadata
            }
            
        except Exception as e:
            return {
                'is_valid': False,
                'score': 0.0,
                'feedback': f"Error analyzing photo: {str(e)}",
                'metadata': {}
            }
