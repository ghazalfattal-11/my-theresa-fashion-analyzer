from fastapi import FastAPI

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
