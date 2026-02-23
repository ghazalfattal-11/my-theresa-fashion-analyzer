from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.utils.image_processor import ImageProcessor
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title="Fashion Design Analysis API",
    description="API for analyzing fashion items using AI",
    version="0.2.0"
)

# Initialize image processor
image_processor = ImageProcessor()


@app.get("/")
async def root():
    """Root endpoint - API welcome message"""
    return {
        "message": "Welcome to Fashion Design Analysis API",
        "version": "0.1.0",
        "docs": "/docs"
    }




@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    Upload an image file for analysis.
    
    Args:
        file: Image file (JPEG, PNG, etc.)
    
    Returns:
        JSON with image info and validation results
    """
    logger.info(f"Received file: {file.filename}")
    
    # Check if file was provided
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check if it's an image (basic check)
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, 
            detail=f"File must be an image. Got: {file.content_type}"
        )
    
    # Read the file
    contents = await file.read()
    
    # Check if file is empty
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file provided")
    
    # Validate and process image with Pillow
    image_info = image_processor.validate_and_process(contents, file.filename)
    
    # Return detailed image information
    return {
        "status": "success",
        "filename": file.filename,
        "content_type": file.content_type,
        "dimensions": {
            "width": image_info["width"],
            "height": image_info["height"]
        },
        "format": image_info["format"],
        "mode": image_info["mode"],
        "size_bytes": image_info["size_bytes"],
        "message": "Image validated successfully. AI analysis coming in Step 4!"
    }
