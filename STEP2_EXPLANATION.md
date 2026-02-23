# Step 2: File Upload - Explanation

## What We Added

### 1. New Dependency: `python-multipart`
**Why?** FastAPI needs this to handle file uploads (multipart/form-data).

```bash
python -m pip install python-multipart
```

### 2. New Imports in `app/main.py`

```python
from fastapi import File, UploadFile, HTTPException
```

**What each does:**
- `File`: Tells FastAPI this parameter is a file
- `UploadFile`: Special type for uploaded files (has methods like `.read()`)
- `HTTPException`: Used to return error responses

### 3. New Endpoint: `POST /analyze`

```python
@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
```

**Breaking it down:**
- `@app.post()` - This endpoint accepts POST requests (for uploading data)
- `file: UploadFile` - Parameter that receives the uploaded file
- `File(...)` - The `...` means this parameter is required

### 4. Validation Logic

```python
# Check if file was provided
if not file:
    raise HTTPException(status_code=400, detail="No file provided")
```

**What this does:** Returns error if no file is uploaded

```python
# Check if it's an image
if not file.content_type or not file.content_type.startswith("image/"):
    raise HTTPException(status_code=400, detail="File must be an image")
```

**What this does:** Checks the file type. Only allows images (image/jpeg, image/png, etc.)

```python
# Read the file
contents = await file.read()
```

**What this does:** Reads the file data into memory. `await` is used because it's an async operation.

```python
# Check if file is empty
if len(contents) == 0:
    raise HTTPException(status_code=400, detail="Empty file provided")
```

**What this does:** Makes sure the file isn't empty

## How to Test

### Option 1: Using the Interactive Docs (Easiest)

1. Make sure server is running:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

2. Open http://127.0.0.1:8000/docs

3. Click on `POST /analyze`

4. Click "Try it out"

5. Click "Choose File" and select an image

6. Click "Execute"

### Option 2: Using curl (Command Line)

```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/image.jpg"
```

### Option 3: Using Python requests

```python
import requests

url = "http://127.0.0.1:8000/analyze"
files = {"file": open("image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

## Expected Response

**Success:**
```json
{
  "status": "success",
  "filename": "fashion_item.jpg",
  "content_type": "image/jpeg",
  "size_bytes": 245678,
  "message": "File uploaded successfully. AI analysis coming in Step 4!"
}
```

**Error (not an image):**
```json
{
  "detail": "File must be an image. Got: application/pdf"
}
```

**Error (empty file):**
```json
{
  "detail": "Empty file provided"
}
```

## Key Concepts Learned

1. **File Upload in FastAPI** - Using `UploadFile` and `File()`
2. **Validation** - Checking file type and content
3. **Error Handling** - Using `HTTPException` for proper error responses
4. **Async File Reading** - Using `await file.read()`
5. **Content Type** - Understanding MIME types (image/jpeg, image/png)

## What's Next?

In Step 3, we'll add:
- Image processing with Pillow
- Image format validation
- Image size checks
- Convert images to proper format for AI analysis
