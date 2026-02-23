# Step 3: Image Processing - Explanation

## What We're Adding

In this step, we'll use **Pillow (PIL)** to:
1. Validate that uploaded files are actually valid images
2. Check image dimensions and size
3. Convert images to a standard format
4. Prepare images for AI analysis

## Why Pillow?

- **Pillow** is Python's most popular image processing library
- It can open, manipulate, and save many image formats
- It validates that files are actually images (not just checking file extension)
- It provides image information (size, format, mode)

## What We'll Learn

1. How to use Pillow to open and validate images
2. Working with image formats (JPEG, PNG, etc.)
3. Image size validation
4. Converting images to bytes for API processing
5. Better error handling with specific error messages

## Key Concepts

### Image Formats
- **JPEG** - Compressed, good for photos, no transparency
- **PNG** - Lossless, supports transparency
- **RGB** - Color mode (Red, Green, Blue)
- **RGBA** - RGB + Alpha (transparency)

### Image Validation
- Check if file can be opened as an image
- Verify image isn't corrupted
- Ensure reasonable dimensions (not too large)

### BytesIO
- In-memory file-like object
- Allows us to work with image data without saving to disk
- Efficient for API processing


## What We Added

### 1. New Dependency: Pillow

```bash
python -m pip install pillow
```

### 2. New File: `app/utils/image_processor.py`

This is our image processing module with the `ImageProcessor` class.

**Key features:**
- Validates image files
- Checks dimensions (not too big, not too small)
- Checks file size (max 10MB)
- Converts images to RGB format for consistency
- Returns detailed image information

### 3. Configuration Constants

```python
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_DIMENSION = 4096  # Max width or height
MIN_DIMENSION = 50    # Min width or height
```

**Why these limits?**
- **10MB max**: Prevents memory issues and slow uploads
- **4096px max**: Reasonable for high-quality images
- **50px min**: Too small images won't have useful details

### 4. Image Validation Process

```python
# Try to open image
image = Image.open(BytesIO(image_data))

# Verify it's actually an image
image.verify()
```

**What this does:**
- `Image.open()` - Tries to open the file as an image
- `image.verify()` - Checks if the image is corrupted
- If either fails, it's not a valid image

### 5. BytesIO Explained

```python
from io import BytesIO
image = Image.open(BytesIO(image_data))
```

**What is BytesIO?**
- Creates a file-like object in memory
- Allows Pillow to read image data without saving to disk
- More efficient for API processing

### 6. Image Mode Conversion

```python
if mode not in ("RGB", "L"):
    image = image.convert("RGB")
```

**Why convert to RGB?**
- Consistency: All images in same format
- AI models typically expect RGB
- Handles RGBA (with transparency), CMYK, etc.

## How to Test

### 1. Install the new dependency

```bash
python -m pip install pillow
```

### 2. Restart the server

The server should auto-reload, but if not:
```bash
python -m uvicorn app.main:app --reload
```

### 3. Test with different images

**Valid image (should work):**
- Upload any JPEG or PNG image
- Should return detailed info

**Too large (should fail):**
- Try uploading an image > 10MB
- Should get error: "Image too large"

**Corrupted file (should fail):**
- Rename a .txt file to .jpg
- Should get error: "Invalid image file"

**Too small (should fail):**
- Create a tiny 10x10 image
- Should get error: "Image dimensions too small"

## Expected Response

**Success:**
```json
{
  "status": "success",
  "filename": "fashion_dress.jpg",
  "content_type": "image/jpeg",
  "dimensions": {
    "width": 1920,
    "height": 1080
  },
  "format": "JPEG",
  "mode": "RGB",
  "size_bytes": 245678,
  "message": "Image validated successfully. AI analysis coming in Step 4!"
}
```

**Error (too large):**
```json
{
  "detail": "Image too large. Max size: 10.0MB"
}
```

**Error (corrupted):**
```json
{
  "detail": "Invalid image file. File may be corrupted."
}
```

## Code Walkthrough

### ImageProcessor Class

```python
class ImageProcessor:
    """Handle image validation and processing"""
```

This is a class that groups all image-related functions together.

### validate_and_process Method

```python
@staticmethod
def validate_and_process(image_data: bytes, filename: str) -> dict:
```

- `@staticmethod` - Can be called without creating an instance
- Takes raw bytes and filename
- Returns dictionary with image info
- Raises HTTPException if validation fails

### Error Handling

```python
try:
    image = Image.open(BytesIO(image_data))
    image.verify()
except Exception as e:
    raise HTTPException(status_code=400, detail="Invalid image file")
```

- Try to open and verify image
- If it fails, return proper error to user
- Log the error for debugging

## What We Learned

1. **Pillow basics** - Opening, verifying, and processing images
2. **Image validation** - Size, dimensions, format checks
3. **BytesIO** - Working with in-memory files
4. **Image modes** - RGB, RGBA, CMYK, etc.
5. **Error handling** - Specific error messages for different failures
6. **Logging** - Using Python's logging module
7. **Code organization** - Separating logic into utility modules

## Commit Message

```bash
git add .
git commit -m "feat: add image processing and validation

- Implement ImageProcessor class with Pillow
- Add image size and dimension validation
- Convert images to RGB format for consistency
- Add detailed error messages for invalid images
- Include logging for debugging
- Update API to return detailed image information

Validates:
- File size (max 10MB)
- Dimensions (50px - 4096px)
- Image format and integrity"
```

## What's Next?

**Step 4: AWS Bedrock Integration**
- Set up AWS credentials
- Connect to Bedrock API
- Send images to AI model
- Get detailed fashion item descriptions
- Handle AI responses and errors

Ready to move to Step 4?
