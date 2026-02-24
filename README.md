# Fashion Design Analysis Application

FastAPI-based application for scraping fashion items from mytheresa.com and analyzing them using AWS Bedrock AI.

## Project Structure

```
.
├── app/                     # FastAPI application
│   ├── main.py             # API endpoints
│   ├── services/           # Business logic (Bedrock)
│   ├── utils/              # Utilities (image processing)
│   └── models/             # Data models
├── scraper/                # Scraping engine
│   ├── mytheresa_scraper.py    # Main scraper
│   ├── selenium_driver.py      # WebDriver management
│   ├── page_scroller.py        # Smart scrolling
│   ├── product_extractor.py    # Data extraction
│   ├── image_downloader.py     # Save images to disk
│   ├── config.py               # Configuration
│   └── data/                   # Scraped images
├── scrape_and_save.py      # Automated scraping engine
├── requirements.txt        # Dependencies
└── .env                    # AWS credentials
```

## Two Main Components

### 1. Automated Scraping Engine

**Purpose:** Scrape fashion images from mytheresa.com and save to disk

**Requirements:**
- 500 men clothing pictures
- 500 women clothing pictures
- 20 Gucci items under $1000
- 50 Elie Saab items
- 100 men shoes

**Usage:**
```bash
# One command to scrape everything
python scrape_and_save.py
```

**Output:** Images saved to `scraper/data/`

### 2. FastAPI Analysis Application

**Purpose:** Accept uploaded images and analyze with AWS Bedrock AI

**Features:**
- Upload any fashion image
- Get detailed AI-powered analysis
- Handle edge cases and errors
- Interactive API documentation

**Usage:**
```bash
# Start the API server
python -m uvicorn app.main:app --reload
```

**Access:** http://127.0.0.1:8000/docs

## Setup

### 1. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Configure AWS Credentials

Create `.env` file:
```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
BEDROCK_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
```

### 3. Run Scraping Engine

```bash
python scrape_and_save.py
```

This will:
- Open Chrome browser (automated)
- Visit mytheresa.com
- Scrape all required images
- Save to `scraper/data/`

### 4. Start FastAPI Server

```bash
python -m uvicorn app.main:app --reload
```

### 5. Use the API

Visit http://127.0.0.1:8000/docs

**Endpoints:**
- `GET /` - API information
- `GET /health` - Health check
- `GET /scraped-images` - List scraped images
- `POST /analyze` - Upload and analyze image

## Workflow

```
1. Run scraping engine
   ↓
2. Images saved to scraper/data/
   ↓
3. Start FastAPI server
   ↓
4. Upload images via API
   ↓
5. Get AI analysis
```

## API Usage Examples

### Upload Image for Analysis

**Using the interactive docs:**
1. Go to http://127.0.0.1:8000/docs
2. Click on `POST /analyze`
3. Click "Try it out"
4. Upload an image file
5. Click "Execute"

**Using curl:**
```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@scraper/data/men_clothing/men_clothing_1.jpg"
```

**Using Python:**
```python
import requests

url = "http://127.0.0.1:8000/analyze"
files = {"file": open("scraper/data/men_clothing/men_clothing_1.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### Response Example

```json
{
  "status": "success",
  "filename": "men_clothing_1.jpg",
  "image_info": {
    "dimensions": {"width": 1920, "height": 1080},
    "format": "JPEG",
    "mode": "RGB",
    "size_bytes": 245678
  },
  "analysis": "This is a navy blue blazer featuring:
  
  1. Item Type: Men's tailored blazer
  2. Colors: Deep navy blue
  3. Patterns: Solid color, no patterns
  4. Style: Formal business attire
  5. Material: Appears to be wool or wool blend
  6. Design Features: Notch lapel, two-button closure
  7. Occasion: Business meetings, formal events
  8. Brand Indicators: High-quality construction"
}
```

## Error Handling

The API handles:
- Invalid file types
- Empty files
- Corrupted images
- Images too large/small
- AWS Bedrock errors
- Missing credentials

## Project Requirements Met

✅ Automated scraping engine for mytheresa
✅ Scrapes 500 men clothing pictures
✅ Scrapes 500 women clothing pictures
✅ Scrapes 20 Gucci items under 1000
✅ Scrapes 50 Elie Saab items
✅ Scrapes 100 men shoes
✅ FastAPI app accepts images
✅ Uses Bedrock model for detailed captions
✅ Handles edge cases and unexpected input

## Technologies Used

- **FastAPI** - Modern Python web framework
- **Selenium** - Browser automation for scraping
- **AWS Bedrock** - AI image analysis (Claude 3)
- **Pillow** - Image processing
- **Pydantic** - Data validation

## Development

### Run in development mode:
```bash
python -m uvicorn app.main:app --reload
```

### Test scraper with small limits:
```python
from scraper.mytheresa_scraper import MytheresaScraper

scraper = MytheresaScraper(headless=False)
results = scraper.scrape_men_clothing(limit=5)
```

## Notes

- Scraping takes time (be patient)
- Respect mytheresa.com's servers
- AWS Bedrock requires valid credentials
- Images are saved locally for API use

## License

For internship/educational purposes.
