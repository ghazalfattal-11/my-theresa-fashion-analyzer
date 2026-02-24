from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.utils.image_processor import ImageProcessor
from app.services.bedrock_service import BedrockService
from dotenv import load_dotenv
import logging
from io import BytesIO

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title="Fashion Design Analysis API",
    description="API for analyzing fashion items using AI",
    version="0.3.0"
)

# Initialize services
image_processor = ImageProcessor()
bedrock_service = BedrockService()


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
    Upload and analyze a fashion item image using AI.
    
    Args:
        file: Image file (JPEG, PNG, etc.)
    
    Returns:
        JSON with image info and AI-generated fashion analysis
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
    try:
        image_info = image_processor.validate_and_process(contents, file.filename)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Image processing error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process image")
    
    # Analyze with AWS Bedrock
    try:
        # Convert PIL image to bytes for Bedrock
        img_byte_arr = BytesIO()
        image_info["image"].save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Get AI analysis
        analysis = bedrock_service.analyze_fashion_item(img_byte_arr)
        
        # Return complete response
        return {
            "status": "success",
            "filename": file.filename,
            "image_info": {
                "dimensions": {
                    "width": image_info["width"],
                    "height": image_info["height"]
                },
                "format": image_info["format"],
                "mode": image_info["mode"],
                "size_bytes": image_info["size_bytes"]
            },
            "analysis": analysis
        }
    
    except Exception as e:
        logger.error(f"Bedrock analysis error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"AI analysis failed: {str(e)}"
        )
