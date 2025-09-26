"""
House Image Validation Module
Validates that uploaded images are actually houses before allowing CBIR search.
Uses pre-trained models and can be extended with Gemini API support.
"""

import os
import numpy as np
from PIL import Image
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from typing import Tuple, Dict, Any, Optional
import logging
import base64
import io

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HouseValidator:
    """
    Validates if an uploaded image is a house using pre-trained models and Gemini API.
    """
    
    def __init__(self, use_gemini: bool = True, gemini_api_key: Optional[str] = None):
        """
        Initialize the house validator with pre-trained models and optional Gemini API.
        
        Args:
            use_gemini: Whether to use Gemini API for additional validation
            gemini_api_key: Gemini API key (if None, will try to get from environment)
        """
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {self.device}")
        
        # Load pre-trained ResNet50 model for general object classification
        self.model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
        self.model.eval()
        self.model.to(self.device)
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # House-related keywords from ImageNet classes
        self.house_keywords = {
            'house', 'home', 'building', 'residence', 'mansion', 'villa', 'bungalow',
            'cottage', 'palace', 'castle', 'dwelling', 'abode', 'habitation',
            'architecture', 'structure', 'edifice', 'construction', 'property',
            'real estate', 'housing', 'residential', 'domicile'
        }
        
        # Non-house keywords that should be rejected
        self.non_house_keywords = {
            'cat', 'dog', 'person', 'people', 'animal', 'car', 'vehicle', 'food',
            'nature', 'landscape', 'sky', 'tree', 'flower', 'plant', 'text',
            'document', 'paper', 'phone', 'computer', 'furniture',
            'clothing', 'accessory', 'tool', 'equipment', 'toy', 'game',
            'tv', 'television', 'monitor', 'display'  # More specific screen types
        }
        
        # Initialize Gemini API
        self.use_gemini = use_gemini
        self.gemini_model = None
        if use_gemini:
            self._initialize_gemini(gemini_api_key)
    
    def _initialize_gemini(self, api_key: Optional[str] = None):
        """Initialize Gemini API for image analysis."""
        try:
            import google.generativeai as genai
            
            # Get API key from parameter, environment, or .env file
            if api_key:
                self.gemini_api_key = api_key
            else:
                self.gemini_api_key = os.getenv('GEMINI_API_KEY')
                if not self.gemini_api_key:
                    # Try to load from .env file
                    try:
                        from dotenv import load_dotenv
                        load_dotenv()
                        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
                    except ImportError:
                        pass
            
            if not self.gemini_api_key:
                logger.warning("Gemini API key not found. Disabling Gemini validation.")
                self.use_gemini = False
                return
            
            # Configure Gemini
            genai.configure(api_key=self.gemini_api_key)
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Gemini API initialized successfully")
            
        except ImportError:
            logger.warning("google-generativeai not installed. Install with: pip install google-generativeai")
            self.use_gemini = False
        except Exception as e:
            logger.error(f"Failed to initialize Gemini API: {e}")
            self.use_gemini = False
    
    def _validate_with_gemini(self, image_path: str) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate image using Gemini API.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Tuple of (is_house, reasoning, details)
        """
        if not self.use_gemini or not self.gemini_model:
            return None, "Gemini not available", {}
        
        try:
            # Load and encode image
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
            
            # Create prompt for Gemini
            prompt = """
            Analyze this image and determine if it shows a house, home, or residential building.
            
            Please respond with:
            1. YES or NO (is this a house/residential building?)
            2. A brief explanation of what you see in the image
            3. Your confidence level (0-100%)
            
            Format your response as:
            RESULT: YES/NO
            EXPLANATION: [your explanation]
            CONFIDENCE: [0-100]
            """
            
            # Generate content with Gemini
            response = self.gemini_model.generate_content([prompt, {
                "mime_type": "image/jpeg",
                "data": image_data
            }])
            
            response_text = response.text.strip()
            logger.info(f"Gemini response: {response_text}")
            
            # Parse response
            is_house = False
            explanation = "No explanation provided"
            confidence = 0
            
            lines = response_text.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('RESULT:'):
                    result = line.replace('RESULT:', '').strip().upper()
                    is_house = result in ['YES', 'Y']
                elif line.startswith('EXPLANATION:'):
                    explanation = line.replace('EXPLANATION:', '').strip()
                elif line.startswith('CONFIDENCE:'):
                    try:
                        confidence = int(line.replace('CONFIDENCE:', '').strip().replace('%', ''))
                    except ValueError:
                        confidence = 0
            
            details = {
                'gemini_response': response_text,
                'confidence': confidence,
                'explanation': explanation
            }
            
            return is_house, explanation, details
            
        except Exception as e:
            logger.error(f"Gemini validation failed: {e}")
            return None, f"Gemini validation error: {str(e)}", {}
    
    def validate_image(self, image_path: str, confidence_threshold: float = 0.05) -> Tuple[bool, Dict[str, Any]]:
        """
        Validate if an image is a house using both ResNet and Gemini (if available).
        
        Args:
            image_path: Path to the image file
            confidence_threshold: Minimum confidence threshold for house detection
            
        Returns:
            Tuple of (is_house, validation_info)
        """
        try:
            # Get ResNet validation
            resnet_is_house, resnet_info = self._validate_with_resnet(image_path, confidence_threshold)
            
            # Get Gemini validation (if available)
            gemini_is_house, gemini_reasoning, gemini_details = self._validate_with_gemini(image_path)
            
            # Combine results
            validation_info = {
                'resnet_validation': resnet_info,
                'gemini_validation': gemini_details if gemini_is_house is not None else None,
                'final_decision': resnet_is_house,  # Default to ResNet result
                'validation_methods': ['resnet'],
                'house_score': resnet_info.get('house_score', 0.0),
                'non_house_score': resnet_info.get('non_house_score', 0.0)
            }
            
            # If Gemini is available, use it as the primary validator
            if gemini_is_house is not None:
                validation_info['final_decision'] = gemini_is_house
                validation_info['validation_methods'] = ['gemini', 'resnet']
                validation_info['reasoning'] = gemini_reasoning
                
                # Log the decision
                logger.info(f"Gemini validation: {gemini_is_house} - {gemini_reasoning}")
                logger.info(f"ResNet validation: {resnet_is_house} - {resnet_info.get('reasoning', 'N/A')}")
            else:
                validation_info['reasoning'] = resnet_info.get('reasoning', 'ResNet validation only')
                logger.info(f"ResNet validation only: {resnet_is_house} - {resnet_info.get('reasoning', 'N/A')}")
            
            validation_info['is_house'] = validation_info['final_decision']
            
            return validation_info['final_decision'], validation_info
            
        except Exception as e:
            logger.error(f"Error validating image {image_path}: {str(e)}")
            return False, {
                'is_house': False,
                'error': str(e),
                'reasoning': 'Error occurred during image validation'
            }
    
    def _validate_with_resnet(self, image_path: str, confidence_threshold: float) -> Tuple[bool, Dict[str, Any]]:
        """Validate image using ResNet model."""
        try:
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            input_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Get predictions
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            
            # Get top predictions
            top_prob, top_class = torch.topk(probabilities, 10)
            top_prob = top_prob.cpu().numpy()
            top_class = top_class.cpu().numpy()
            
            # Load ImageNet class names
            from torchvision.models import ResNet50_Weights
            class_names = ResNet50_Weights.IMAGENET1K_V1.meta['categories']
            
            # Analyze predictions
            house_score = 0.0
            non_house_score = 0.0
            top_predictions = []
            
            for i in range(len(top_class)):
                class_idx = top_class[i]
                prob = top_prob[i]
                class_name = class_names[class_idx].lower()
                
                top_predictions.append({
                    'class': class_name,
                    'confidence': float(prob)
                })
                
                # Check if this class is house-related
                if any(keyword in class_name for keyword in self.house_keywords):
                    house_score += float(prob)
                elif any(keyword in class_name for keyword in self.non_house_keywords):
                    non_house_score += float(prob)
            
            # Determine if it's a house
            is_house = house_score > confidence_threshold and house_score > non_house_score
            
            validation_info = {
                'is_house': is_house,
                'house_score': house_score,
                'non_house_score': non_house_score,
                'confidence_threshold': confidence_threshold,
                'top_predictions': top_predictions[:5],  # Top 5 predictions
                'reasoning': self._get_reasoning(house_score, non_house_score, top_predictions)
            }
            
            return is_house, validation_info
            
        except Exception as e:
            logger.error(f"ResNet validation failed: {e}")
            return False, {'error': str(e), 'reasoning': 'ResNet validation failed'}
    
    def _get_reasoning(self, house_score: float, non_house_score: float, predictions: list) -> str:
        """Generate human-readable reasoning for the validation result."""
        if house_score > non_house_score and house_score > 0.05:
            return f"✅ ตรวจพบรูปบ้าน (ความมั่นใจ: {house_score:.2f})"
        elif non_house_score > house_score:
            return "❌ กรุณาอัปโหลดรูปบ้านที่ชัดเจน"
        else:
            return "⚠️ ไม่สามารถระบุได้ชัดเจน กรุณาลองรูปบ้านที่ชัดเจนกว่า"
    
    def _get_detailed_rejection_message(self, detected_objects: list) -> str:
        """Generate detailed rejection message with helpful guidance."""
        return "❌ กรุณาอัปโหลดรูปบ้านที่ชัดเจน"
    
    def validate_image_file(self, file_path: str) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Validate an image file and return user-friendly results.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            Tuple of (is_valid, message, validation_info)
        """
        if not os.path.exists(file_path):
            return False, "Image file not found", {}
        
        # Check file size (max 10MB)
        file_size = os.path.getsize(file_path)
        if file_size > 10 * 1024 * 1024:  # 10MB
            return False, "Image file is too large (max 10MB)", {}
        
        # Check file extension
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}
        file_ext = os.path.splitext(file_path)[1].lower()
        if file_ext not in allowed_extensions:
            return False, f"Unsupported file format. Please use: {', '.join(allowed_extensions)}", {}
        
        is_house, validation_info = self.validate_image(file_path)
        
        if is_house:
            return True, "✅ ตรวจสอบรูปบ้านสำเร็จ", validation_info
        else:
            reasoning = validation_info.get('reasoning', 'Image does not appear to be a house')
            # Add helpful tips for users
            tips = self._get_house_image_tips()
            full_message = f"{reasoning}\n\n{tips}"
            return False, full_message, validation_info
    
    def _get_house_image_tips(self) -> str:
        """Get helpful tips for users on what makes a good house image."""
        return """💡 เคล็ดลับการถ่ายรูปบ้าน:
• ถ่ายรูปบ้านทั้งหลังให้ชัดเจน
• แสงสว่างเพียงพอและโฟกัสชัด
• หลีกเลี่ยงรูปสัตว์ คน รถ หรืออาหาร"""


# Global validator instance
_validator = None

def get_validator() -> HouseValidator:
    """Get the global house validator instance."""
    global _validator
    if _validator is None:
        _validator = HouseValidator()
    return _validator

def validate_house_image(image_path: str) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Convenience function to validate a house image.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Tuple of (is_valid, message, validation_info)
    """
    validator = get_validator()
    return validator.validate_image_file(image_path)


# Example usage and testing
if __name__ == "__main__":
    # Test the validator
    validator = HouseValidator()
    
    # Test with a sample image (if available)
    test_image = "static/uploads/test_house.jpg"
    if os.path.exists(test_image):
        is_valid, message, info = validate_house_image(test_image)
        print(f"Validation result: {is_valid}")
        print(f"Message: {message}")
        print(f"Info: {info}")
    else:
        print("No test image found. Please add a test image to test the validator.")
