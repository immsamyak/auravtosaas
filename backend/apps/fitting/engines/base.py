from abc import ABC, abstractmethod
from typing import Dict, Any

class VTOEngine(ABC):
    """
    Base interface for Virtual Try-On engines.
    Ensures the Django application is decoupled from the ML implementation.
    """
    
    @abstractmethod
    def generate(self, user_photo_path: str, product_photo_path: str, **kwargs) -> Dict[str, Any]:
        """
        Executes the virtual try on logic.
        
        Args:
            user_photo_path (str): Absolute path to the customer's photo.
            product_photo_path (str): Absolute path to the product image.
            **kwargs: Configuration flags, such as product category or target size.
            
        Returns:
            Dict[str, Any]: A structured response dictionary containing:
                - 'status': 'COMPLETED' or 'FAILED'
                - 'result_image_file': SimpleUploadedFile containing the result image buffer.
                - 'error_message': Optional error string if status is FAILED.
                - 'confidence_score': Optional float representing AI confidence.
        """
        pass
