"""
Main scraper orchestrator for mytheresa.com
Coordinates all scraping components.
"""

import logging
from typing import List, Dict, Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from scraper.config import CATEGORIES, MAX_PRICE_GUCCI
from scraper.selenium_driver import SeleniumDriver
from scraper.page_scroller import PageScroller
from scraper.product_extractor import ProductExtractor

logger = logging.getLogger(__name__)


class MytheresaScraper:
    """
    Main scraper for mytheresa.com
    Orchestrates driver, scroller, and extractor components.
    """
    
    def __init__(self, headless: bool = True):
        """
        Initialize the scraper.
        
        Args:
            headless: Run browser in headless mode
        """
        self.driver_manager = SeleniumDriver(headless=headless)
        self.driver = None
        self.scroller = None
        self.extractor = None
        
        logger.info("MytheresaScraper initialized")
    
    def _initialize_components(self):
        """Initialize all scraping components"""
        self.driver = self.driver_manager.setup()
        self.scroller = PageScroller(self.driver)
        self.extractor = ProductExtractor(self.scroller)
    
    def _cleanup(self):
        """Cleanup resources"""
        self.driver_manager.close()
        self.driver = None
        self.scroller = None
        self.extractor = None
    
    def scrape_category(
        self, 
        category: str, 
        limit: int = 100,
        brand_filter: Optional[str] = None,
        max_price: Optional[float] = None
    ) -> List[Dict]:
        """
        Scrape products from a category.
        
        Args:
            category: Category key from config.CATEGORIES
            limit: Maximum number of items to scrape
            brand_filter: Filter by brand name (optional)
            max_price: Maximum price filter (optional)
            
        Returns:
            List of product dictionaries with image URLs
        """
        if category not in CATEGORIES:
            logger.error(f"Invalid category: {category}")
            return []
        
        url = CATEGORIES[category]
        logger.info(f"Scraping {category} from {url}")
        
        try:
            # Initialize components
            self._initialize_components()
            
            # Load page
            self.driver.get(url)
            
            # Give page more time to load
            import time
            time.sleep(5)  # Wait 5 seconds for page to fully load
            
            # Wait for initial products to load
            if not self._wait_for_initial_load():
                return []
            
            # Scroll and load more products
            items_loaded = self.scroller.scroll_and_load(target_items=limit)
            
            # Get all product elements (images)
            products = self.driver.find_elements(By.TAG_NAME, "img")
            
            logger.info(f"Extracting data from {len(products)} products")
            
            # Extract data from each product
            results = self._extract_products(
                products, 
                limit, 
                brand_filter, 
                max_price
            )
            
            logger.info(f"✓ Successfully scraped {len(results)} items")
            return results
        
        except Exception as e:
            logger.error(f"Scraping failed: {str(e)}")
            return []
        
        finally:
            self._cleanup()
    
    def _wait_for_initial_load(self) -> bool:
        """
        Wait for initial products to load.
        
        Returns:
            True if products loaded, False if timeout
        """
        try:
            WebDriverWait(self.driver, 15).until(  # Increased from 10 to 15 seconds
                EC.presence_of_element_located((By.TAG_NAME, "img"))
            )
            logger.info("✓ Initial products loaded")
            return True
        except TimeoutException:
            logger.error("✗ Timeout waiting for products to load")
            logger.error(f"Current URL: {self.driver.current_url}")
            logger.error(f"Page title: {self.driver.title}")
            return False
    
    def _extract_products(
        self,
        products,
        limit: int,
        brand_filter: Optional[str],
        max_price: Optional[float]
    ) -> List[Dict]:
        """
        Extract data from product elements with filters.
        
        Args:
            products: List of product elements
            limit: Maximum items to extract
            brand_filter: Brand filter
            max_price: Price filter
            
        Returns:
            List of extracted product data
        """
        results = []
        
        for i, product in enumerate(products):
            if len(results) >= limit:
                break
            
            # Extract data
            data = self.extractor.extract_from_element(product)
            
            if not data:
                logger.debug(f"Item {i+1}: No data extracted")
                continue
            
            # Apply filters
            if brand_filter and brand_filter.lower() not in data["brand"].lower():
                logger.debug(f"Item {i+1}: Filtered by brand - {data['brand']}")
                continue
            
            if max_price and data["price"] and data["price"] > max_price:
                logger.debug(f"Item {i+1}: Filtered by price - ${data['price']}")
                continue
            
            results.append(data)
            logger.info(f"✓ Extracted: {data['brand']} - {data['image_url'][:60]}...")
        
        logger.info(f"Extraction complete: {len(results)} items from {len(products)} elements")
        return results
        return results
    
    # Convenience methods for specific requirements
    
    def scrape_men_clothing(self, limit: int = 500) -> List[Dict]:
        """Scrape men's clothing"""
        return self.scrape_category("men_clothing", limit=limit)
    
    def scrape_women_clothing(self, limit: int = 500) -> List[Dict]:
        """Scrape women's clothing"""
        return self.scrape_category("women_clothing", limit=limit)
    
    def scrape_men_shoes(self, limit: int = 100) -> List[Dict]:
        """Scrape men's shoes"""
        return self.scrape_category("men_shoes", limit=limit)
    
    def scrape_gucci_under_1000(self, limit: int = 20) -> List[Dict]:
        """Scrape Gucci items under $1000"""
        return self.scrape_category(
            "men_clothing",
            limit=limit,
            brand_filter="Gucci",
            max_price=MAX_PRICE_GUCCI
        )
    
    def scrape_elie_saab(self, limit: int = 50) -> List[Dict]:
        """Scrape Elie Saab items"""
        return self.scrape_category(
            "women_clothing",
            limit=limit,
            brand_filter="Elie Saab"
        )


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)  # Changed from INFO to DEBUG
    
    scraper = MytheresaScraper(headless=False)  # Set False to see browser
    
    print("=" * 60)
    print("Mytheresa Scraper - Modular Architecture")
    print("=" * 60)
    print("\nComponents:")
    print("  - SeleniumDriver: WebDriver management")
    print("  - PageScroller: Smart scrolling and loading")
    print("  - ProductExtractor: Data extraction")
    print("  - MytheresaScraper: Orchestrator")
    
    print("\n" + "=" * 60)
    print("Testing: Scraping 5 men's clothing items...")
    print("=" * 60)
    
    results = scraper.scrape_men_clothing(limit=5)
    
    print(f"\n✓ Results: {len(results)} items")
    for i, item in enumerate(results, 1):
        print(f"{i}. {item['brand']} - ${item['price']}")
        print(f"   URL: {item['image_url'][:60]}...")
    
    print("\n" + "=" * 60)
    print("Test complete!")
