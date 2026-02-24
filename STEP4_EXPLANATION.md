# Step 4: AWS Bedrock Integration - Explanation

## What is AWS Bedrock?

**AWS Bedrock** is Amazon's service for accessing powerful AI models, including:
- Claude 3 (Anthropic) - What we're using
- Stable Diffusion (image generation)
- Titan (Amazon's models)
- And more

We're using **Claude 3 Sonnet** because it:
- Can analyze images (vision capability)
- Provides detailed, accurate descriptions
- Has good balance of speed and quality
- Is cost-effective

## What We're Adding

### 1. New Dependencies

```bash
python -m pip install boto3 python-dotenv
```

**boto3**: AWS SDK for Python - lets us talk to AWS services
**python-dotenv**: Loads environment variables from .env file

### 2. Environment Variables (.env file)

Create a `.env` file in your project root:

```env
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

**IMPORTANT**: Never commit .env to git! It contains secrets.

### 3. New Service: `app/services/bedrock_service.py`

This handles all AWS Bedrock communication.

## How AWS Bedrock Works

### Step-by-step process:

1. **Encode image to base64**
   ```python
   image_base64 = base64.b64encode(image_bytes).decode("utf-8")
   ```
   - AI models need images as base64 strings
   - Base64 converts binary data to text

2. **Create a prompt**
   ```python
   prompt = "Analyze this fashion item in detail..."
   ```
   - Tell the AI what to do
   - Be specific for better results

3. **Build request payload**
   ```python
   payload = {
       "messages": [
           {
               "role": "user",
               "content": [image, text]
           }
       ]
   }
   ```
   - Claude 3 uses a specific format
   - Combines image + text prompt

4. **Send to Bedrock**
   ```python
   response = client.invoke_model(modelId=model_id, body=payload)
   ```
   - Sends request to AWS
   - Waits for AI response

5. **Parse response**
   ```python
   caption = response_body["content"][0]["text"]
   ```
   - Extract the AI's analysis
   - Return to user

## Setting Up AWS Credentials

### Option 1: AWS Free Tier (Recommended for learning)

1. Go to https://aws.amazon.com/
2. Click "Create an AWS Account"
3. Follow signup process (requires credit card, but won't charge for free tier)
4. Enable Bedrock in your region

### Option 2: AWS IAM User (If you have AWS account)

1. Go to AWS Console → IAM
2. Create new user
3. Attach policy: `AmazonBedrockFullAccess`
4. Create access key
5. Copy Access Key ID and Secret Access Key

### Option 3: Use Mock/Test Mode (For development)

If you don't have AWS yet, you can modify the code to return mock responses for testing.

## Code Walkthrough

### BedrockService Class

```python
class BedrockService:
    def __init__(self):
        # Load credentials from environment
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        
        # Create Bedrock client
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=aws_region,
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key
        )
```

**What it does:**
- Reads AWS credentials from .env
- Creates connection to Bedrock
- Handles errors if credentials missing

### analyze_fashion_item Method

```python
def analyze_fashion_item(self, image_bytes: bytes) -> str:
```

**Takes:** Raw image bytes
**Returns:** AI-generated description
**Raises:** Exception if something goes wrong

### The Fashion Analysis Prompt

```python
prompt = """Analyze this fashion item in detail. Provide:
1. Item Type
2. Colors
3. Patterns
4. Style
5. Material
...
"""
```

**Why this prompt?**
- Structured output
- Covers all important aspects
- Specific to fashion analysis
- Helps AI give consistent results

## Updated API Endpoint

The `/analyze` endpoint now:
1. Validates the image (Step 3)
2. Converts image to JPEG format
3. Sends to Bedrock for analysis
4. Returns both image info AND AI analysis

## How to Test

### 1. Install dependencies

```bash
python -m pip install boto3 python-dotenv
```

### 2. Create .env file

Copy `.env.example` to `.env` and add your AWS credentials:

```bash
cp .env.example .env
```

Then edit `.env` with your actual credentials.

### 3. Restart server

```bash
python -m uvicorn app.main:app --reload
```

### 4. Test the endpoint

Go to http://127.0.0.1:8000/docs and try uploading a fashion image!

## Expected Response

**Success:**
```json
{
  "status": "success",
  "filename": "dress.jpg",
  "image_info": {
    "dimensions": {
      "width": 1920,
      "height": 1080
    },
    "format": "JPEG",
    "mode": "RGB",
    "size_bytes": 245678
  },
  "analysis": "This is a elegant evening dress featuring:

1. Item Type: Long evening gown
2. Colors: Deep navy blue with silver accents
3. Patterns: Sequined bodice with flowing fabric
4. Style: Formal, elegant, red-carpet style
5. Material: Appears to be silk or satin with sequin embellishments
6. Design Features: V-neckline, fitted bodice, flowing skirt
7. Occasion: Formal events, galas, weddings
8. Brand Indicators: High-end construction, luxury materials"
}
```

**Error (no AWS credentials):**
```json
{
  "detail": "AI analysis failed: AWS Bedrock not configured. Please set AWS credentials in .env file"
}
```

## Key Concepts Learned

1. **AWS Bedrock** - Cloud AI service
2. **boto3** - AWS SDK for Python
3. **Environment variables** - Storing secrets securely
4. **Base64 encoding** - Converting images for APIs
5. **API authentication** - Using access keys
6. **Prompt engineering** - Writing good AI prompts
7. **Error handling** - Graceful failures

## Security Best Practices

### ✅ DO:
- Store credentials in .env file
- Add .env to .gitignore
- Use IAM users with minimal permissions
- Rotate access keys regularly

### ❌ DON'T:
- Commit credentials to git
- Share your .env file
- Use root AWS account credentials
- Hardcode credentials in code

## Cost Considerations

**Claude 3 Sonnet pricing (approximate):**
- Input: $3 per million tokens
- Output: $15 per million tokens
- Images: ~1,600 tokens per image

**Example cost:**
- 100 image analyses ≈ $0.50
- 1,000 image analyses ≈ $5.00

**Free tier:** AWS offers free tier credits for new accounts.

## Troubleshooting

### Error: "Could not connect to Bedrock"
- Check AWS credentials in .env
- Verify region supports Bedrock
- Check internet connection

### Error: "Model not found"
- Verify model ID is correct
- Check if Bedrock is enabled in your region
- Some models require special access

### Error: "Access denied"
- Check IAM permissions
- Ensure user has BedrockFullAccess policy

## Testing Without AWS (Mock Mode)

If you want to test without AWS credentials, add this to `bedrock_service.py`:

```python
def analyze_fashion_item(self, image_bytes: bytes) -> str:
    # Mock response for testing
    if not self.client:
        return """[MOCK ANALYSIS - AWS not configured]
        
This is a fashion item with various design elements.
To get real AI analysis, configure AWS Bedrock credentials."""
    
    # ... rest of the code
```

## Commit Message

```bash
git add .
git commit -m "feat: integrate AWS Bedrock for AI image analysis

- Add BedrockService for Claude 3 integration
- Implement fashion-specific analysis prompt
- Add environment variable configuration
- Update /analyze endpoint with AI capabilities
- Include comprehensive error handling
- Add security best practices documentation

Features:
- Detailed fashion item analysis
- Support for multiple image formats
- Graceful fallback if AWS not configured"
```

## What's Next?

**Step 5: Web Scraping Basics**
- Learn web scraping fundamentals
- Use requests and BeautifulSoup
- Download images from URLs
- Save images to disk

Ready to move to Step 5?
