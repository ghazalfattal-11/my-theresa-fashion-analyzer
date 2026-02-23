from PIL import Image
from io import BytesIO
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

# Configuration
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_DIMENSION = 4096  # Max width or height
MIN_DIMENSION = 50    # Min width or height


class ImageProcessor:
    """Handle image validation and processing"""
    
    @staticmethod
    def validate_and_process(image_data: bytes, filename: str) -> dict:
        """
        Validate image and return processed information.
        
        Args:
            image_data: Raw image bytes
            filename: Original filename
            
        Returns:
            dict with image info and processed data
            
        Raises:
            HTTPException: If image is invalid
        """
        # Check file size
        if len(image_data) > MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"Image too large. Max size: {MAX_IMAGE_SIZE / 1024 / 1024}MB"
            )
        
        try:
            # Try to open image
            image = Image.open(BytesIO(image_data))
            
            # Verify it's actually an image
            image.verify()
            
            # Re-open after verify (verify closes the file)
            image = Image.open(BytesIO(image_data))
            
        except Exception as e:
            logger.error(f"Failed to open image {filename}: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail="Invalid image file. File may be corrupted."
            )
        
        # Get image info
        width, height = image.size
        format_name = image.format
        mode = image.mode
        
        # Validate dimensions
        if width > MAX_DIMENSION or height > MAX_DIMENSION:
            raise HTTPException(
                status_code=400,
                detail=f"Image dimensions too large. Max: {MAX_DIMENSION}x{MAX_DIMENSION}px"
            )
        
        if width < MIN_DIMENSION or height < MIN_DIMENSION:
            raise HTTPException(
                status_code=400,
                detail=f"Image dimensions too small. Min: {MIN_DIMENSION}x{MIN_DIMENSION}px"
            )
        
        # Convert to RGB if needed (for consistency)
        if mode not in ("RGB", "L"):  # L is grayscale
            image = image.convert("RGB")
            mode = "RGB"
        
        logger.info(f"Processed image: {filename} - {width}x{height} {format_name} {mode}")
        
        return {
            "width": width,
            "height": height,
            "format": format_name,
            "mode": mode,
            "size_bytes": len(image_data),
            "image": image  # PIL Image object for further processing
        }
