# Project Architecture - Beginner's Guide

## 🎯 Project Goal
Build a fashion analysis system that:
1. Scrapes fashion images from mytheresa.com
2. Analyzes images using AI (AWS Bedrock)
3. Provides an API for image captioning

---

## 📁 Project Structure (Final)

```
fashion-analysis/
├── app/                          # FastAPI application
│   ├── __init__.py
│   ├── main.py                   # API entry point
│   ├── models/                   # Data models
│   │   ├── __init__.py
│   │   └── schemas.py            # Request/response models
│   └── services/                 # Business logic
│       ├── __init__.py
│       └── bedrock_service.py    # AWS Bedrock integration
├── scraper/                      # Web scraping module
│   ├── __init__.py
│   └── scraper.py                # Scraping logic
├── tests/                        # Tests (optional)
├── .env                          # Environment variables (secrets)
├── .env.example                  # Template for .env
├── .gitignore                    # Files to ignore in git
├── requirements.txt              # Python dependencies
└── README.md                     # Documentation
```

---

## 🚀 Learning Path - Step by Step

### ✅ Step 1: Basic FastAPI Setup (CURRENT)
**What you'll learn:**
- How to create a FastAPI application
- What endpoints are
- How to run a web server

**Files involved:**
- `app/main.py` - Simple API with 2 endpoints
- `requirements.txt` - FastAPI + uvicorn

**Try it:**
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

### 📝 Step 2: Add File Upload
**What you'll learn:**
- How to accept file uploads in FastAPI
- File validation (checking if it's an image)
- Working with uploaded files

**What we'll add:**
- New endpoint: `POST /analyze`
- File type validation
- Basic error handling

**New dependency:** `python-multipart`

---

### 🖼️ Step 3: Image Processing
**What you'll learn:**
- How to read and validate image files
- Working with PIL/Pillow library
- Handling different image formats

**What we'll add:**
- Image validation logic
- Image size checks
- Convert images to proper format

**New dependency:** `pillow`

---

### ☁️ Step 4: AWS Bedrock Integration
**What you'll learn:**
- How to use AWS services from Python
- API authentication with AWS
- Sending images to AI models
- Environment variables for secrets

**What we'll add:**
- `app/services/bedrock_service.py`
- AWS credentials configuration
- Image captioning logic

**New dependencies:** `boto3`, `python-dotenv`

---

### 🕷️ Step 5: Web Scraping Basics
**What you'll learn:**
- How web scraping works
- Using requests library
- Parsing HTML with BeautifulSoup

**What we'll add:**
- `scraper/scraper.py` (basic version)
- Download images from URLs
- Save images to disk

**New dependencies:** `requests`, `beautifulsoup4`

---

### 🌐 Step 6: Advanced Scraping with Selenium
**What you'll learn:**
- Why Selenium is needed for dynamic websites
- Browser automation
- Handling JavaScript-rendered content

**What we'll add:**
- Selenium setup
- Scraping mytheresa.com
- Handling pagination

**New dependency:** `selenium`

---

### 🎨 Step 7: Complete Scraping Requirements
**What you'll learn:**
- Organizing scraping tasks
- Filtering by brand/category
- Managing large datasets

**What we'll add:**
- Scrape 500 men clothing
- Scrape 500 women clothing
- Scrape 20 Gucci items under 1000
- Scrape 50 Elie Saab items
- Scrape 100 men shoes

---

### ✨ Step 8: Polish & Best Practices
**What you'll learn:**
- Error handling
- Logging
- Code organization
- Documentation

**What we'll add:**
- Comprehensive error handling
- Logging throughout the app
- Better documentation
- Code comments

---

## 🧩 Key Concepts Explained

### What is FastAPI?
A modern Python framework for building APIs. It's fast, easy to learn, and automatically generates documentation.

### What is an API endpoint?
A URL path that accepts requests and returns responses. Example: `GET /health` returns server status.

### What is async/await?
A way to write code that can handle multiple requests efficiently without blocking.

### What is AWS Bedrock?
Amazon's service for using AI models. We'll use it to analyze fashion images.

### What is web scraping?
Automatically extracting data from websites. We'll scrape fashion images from mytheresa.com.

---

## 📚 Resources for Learning

- **FastAPI Tutorial:** https://fastapi.tiangolo.com/tutorial/
- **Python Requests:** https://requests.readthedocs.io/
- **BeautifulSoup:** https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **AWS Bedrock:** https://docs.aws.amazon.com/bedrock/

---

## 🎓 Current Status

- ✅ Step 1: Basic FastAPI Setup
- ✅ Step 2: Add File Upload
- ⏳ Step 3: Image Processing (NEXT)
- ⬜ Step 4: AWS Bedrock Integration
- ⬜ Step 5: Web Scraping Basics
- ⬜ Step 6: Advanced Scraping
- ⬜ Step 7: Complete Requirements
- ⬜ Step 8: Polish & Best Practices

---

**Ready for the next step?** Just say "next" or "step 2" and we'll continue!
