"""
Configuration for Mytheresa scraper.
"""

from pathlib import Path

# Output directories
RESULTS_DIR = Path("scraper/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Images directory - where scraped images are saved
IMAGES_DIR = Path("scraper/data")
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# Mytheresa URLs
BASE_URL = "https://www.mytheresa.com"
CATEGORIES = {
    "men_clothing": f"{BASE_URL}/en-us/men/clothing",
    "women_clothing": f"{BASE_URL}/en-us/women/clothing",
    "men_shoes": f"{BASE_URL}/en-us/men/shoes",
}

# Scraping settings
SCROLL_PAUSE_TIME = 2  # seconds between scrolls
PAGE_LOAD_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
ELEMENT_WAIT_TIME = 10  # seconds to wait for elements

# Selenium settings
HEADLESS = True  # Run browser in background
WINDOW_SIZE = "1920,1080"

# Brand filters
BRANDS = {
    "gucci": "Gucci",
    "elie_saab": "Elie Saab"
}

# Price limits
MAX_PRICE_GUCCI = 1000
