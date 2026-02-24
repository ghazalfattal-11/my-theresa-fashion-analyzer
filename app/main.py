from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.utils.image_processor import ImageProcessor
from app.services.bedrock_service import BedrockService
from dotenv import load_dotenv
import logging
from io import BytesIO
from pathlib import Path

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app instance
app = FastAPI(
    title="Fashion Design Analysis API",
    description="Upload fashion images for AI-powered analysis using AWS Bedrock",
    version="1.0.0"
)

# Initialize services
image_processor = ImageProcessor()
bedrock_service = BedrockService()


@app.get("/")
async def root():
    """Root endpoint - API welcome message"""
    return {
        "message": "Fashion Design Analysis API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "scraped_images": "/scraped-images",
            "analyze": "/analyze (POST)"
        },
        "description": "Upload fashion images from scraped data for detailed AI analysis"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "bedrock_configured": bedrock_service.client is not None
    }


@app.get("/scraped-images")
async def list_scraped_images():
    """
    List all scraped images available for analysis.
    
    Returns:
        Dictionary with categories and image counts
    """
    images_dir = Path("scraper/data")
    
    if not images_dir.exists():
        return {
            "message": "No scraped images found. Run scrape_and_save.py first.",
            "categories": {}
        }
    
    categories = {}
    for category_dir in images_dir.iterdir():
        if category_dir.is_dir():
            images = list(category_dir.glob("*.jpg")) + list(category_dir.glob("*.png"))
            categories[category_dir.name] = {
                "count": len(images),
                "sample_files": [img.name for img in images[:5]]
            }
    
    return {
        "total_images": sum(cat["count"] for cat in categories.values()),
        "categories": categories,
        "location": str(images_dir)
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
