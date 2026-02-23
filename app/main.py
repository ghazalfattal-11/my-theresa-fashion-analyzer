from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

# Create FastAPI app instance
app = FastAPI(
    title="Fashion Design Analysis API",
    description="API for analyzing fashion items using AI",
    version="0.1.0"
)


@app.get("/")
async def root():
    """Root endpoint - API welcome message"""
    return {
        "message": "Welcome to Fashion Design Analysis API",
        "version": "0.1.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    """
    Upload an image file for analysis.
    
    Args:
        file: Image file (JPEG, PNG, etc.)
    
    Returns:
        JSON with filename and basic info
    """
    # Check if file was provided
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check if it's an image
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
    
    # For now, just return basic info (we'll add AI analysis in Step 4)
    return {
        "status": "success",
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(contents),
        "message": "File uploaded successfully. AI analysis coming in Step 4!"
    }
