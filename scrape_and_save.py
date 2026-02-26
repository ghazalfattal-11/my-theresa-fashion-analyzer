"""
Automated scraping engine for mytheresa.com
One-click script to scrape all required images and save to disk.
Uses HTTP-based API scraping - NO SELENIUM REQUIRED!
"""

import logging
import time
from scraper.mytheresa_api_scraper import MytheresaAPIScraper
from scraper.image_downloader import ImageDownloader
from scraper.config import IMAGES_DIR

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def scrape_and_save_category(
    scraper: MytheresaAPIScraper,
    downloader: ImageDownloader,
    scrape_func,
    category: str,
    limit: int
    ):
    """
    Scrape a category and save images to disk.
    
    Args:
        scraper: MytheresaAPIScraper instance
        downloader: ImageDownloader instance
        scrape_func: Function to call for scraping
        category: Category name
        limit: Number of items to scrape
    """
    print(f"\n{'='*70}")
    print(f"SCRAPING: {category.upper()} ({limit} items)")
    print(f"{'='*70}")
    
    # Step 1: Scrape URLs
    logger.info(f"Step 1/2: Scraping URLs from mytheresa.com API...")
    items = scrape_func(limit)
    
    if not items:
        logger.warning(f"No items found for {category}")
        return
    
    logger.info(f"✓ Found {len(items)} items")
    
    # Step 2: Download and save images
    logger.info(f"Step 2/2: Downloading and saving images...")
    
    downloaded = 0
    for i, item in enumerate(items, 1):
        filename = downloader.get_next_filename(category)
        filepath = downloader.download_and_save(
            item['image_url'],
            category,
            filename
        )
        
        if filepath:
            downloaded += 1
        
        # Progress update
        if i % 10 == 0:
            logger.info(f"Progress: {i}/{len(items)} processed, {downloaded} saved")
        
        # Small delay to be polite
        time.sleep(0.1)  # Reduced delay since we're using API
    
    logger.info(f"✓ COMPLETE: {downloaded}/{len(items)} images saved to scraper/data/{category}/")
    print(f"\n✓ {category}: {downloaded} images saved")


def main():
    """Run the complete automated scraping engine"""
    
    print("=" * 70)
    print("MYTHERESA AUTOMATED SCRAPING ENGINE")
    print("HTTP-Based API Scraping - Fast & Efficient!")
    print("=" * 70)
    print(f"\nImages will be saved to: {IMAGES_DIR}")
    print("\nRequirements:")
    print("  - 500 men clothing pictures")
    print("  - 500 women clothing pictures")
    print("  - 20 Gucci items under 1000")
    print("  - 50 Elie Saab items")
    print("  - 100 men shoes")
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    # Initialize components 
    scraper = MytheresaAPIScraper()
    downloader = ImageDownloader()
    
    # Define scraping tasks
    tasks = [
        (scraper.scrape_men_clothing, "men_clothing", 500),
        (scraper.scrape_women_clothing, "women_clothing", 500),
        (scraper.scrape_gucci_under_1000, "gucci_under_1000", 20),
        (scraper.scrape_elie_saab, "elie_saab", 50),
        (scraper.scrape_men_shoes, "men_shoes", 100),
    ]
    
    # Execute all tasks
    total_downloaded = 0
    for scrape_func, category, limit in tasks:
        try:
            scrape_and_save_category(
                scraper,
                downloader,
                scrape_func,
                category,
                limit
            )
            total_downloaded += downloader.get_download_count(category)
        except Exception as e:
            logger.error(f"Failed to scrape {category}: {str(e)}")
            continue
    
    # Final summary
    print("\n" + "=" * 70)
    print("SCRAPING COMPLETE!")
    print("=" * 70)
    print(f"\nTotal images downloaded: {total_downloaded}")
    print(f"Images location: {IMAGES_DIR}")
    print("\nBreakdown:")
    for _, category, _ in tasks:
        count = downloader.get_download_count(category)
        print(f"  - {category}: {count} images")
    
    print("\n" + "=" * 70)
    print("Next step: Use the FastAPI app to analyze images")
    print("Run: python -m uvicorn app.main:app --reload")
    print("=" * 70)


if __name__ == "__main__":
    main()
