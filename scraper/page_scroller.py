"""
Smart page scrolling and content loading.
"""

import time
import logging
from selenium.webdriver.common.by import By
from scraper.config import SCROLL_PAUSE_TIME

logger = logging.getLogger(__name__)


class PageScroller:
    """Handles intelligent page scrolling and content loading"""
    
    def __init__(self, driver):
        """
        Initialize scroller.
        
        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
    
    def scroll_and_load(self, target_items: int = 100, max_scrolls: int = 20):
        """
        Scroll page and wait for content to load until target is reached.
        
        Args:
            target_items: Target number of items to load
            max_scrolls: Maximum number of scroll attempts
            
        Returns:
            Number of items loaded
        """
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        items_loaded = 0
        scroll_attempts = 0
        
        logger.info(f"Starting smart scroll. Target: {target_items} items")
        
        while scroll_attempts < max_scrolls:
            # Get current number of images
            products = self.driver.find_elements(By.TAG_NAME, "img")
            items_loaded = len(products)
            
            logger.info(f"Items loaded: {items_loaded}/{target_items}")
            
            # Stop if we have enough items
            if items_loaded >= target_items:
                logger.info(f"✓ Target reached: {items_loaded} items loaded")
                break
            
            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for page to load
            time.sleep(SCROLL_PAUSE_TIME)
            
            # Calculate new scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Check if we've reached the bottom (no new content)
            if new_height == last_height:
                logger.info(f"Reached bottom of page. Total items: {items_loaded}")
                
                # Try clicking "Load More" button if exists
                if self._try_load_more_button():
                    time.sleep(2)
                    continue
                else:
                    # No more content available
                    break
            
            last_height = new_height
            scroll_attempts += 1
        
        logger.info(
            f"Scrolling complete. Loaded {items_loaded} items "
            f"after {scroll_attempts} scrolls"
        )
        
        # Final wait for any lazy-loaded content
        time.sleep(2)
        
        return items_loaded
    
    def _try_load_more_button(self) -> bool:
        """
        Try to find and click "Load More" button.
        
        Returns:
            True if button was clicked, False otherwise
        """
        try:
            load_more = self.driver.find_element(
                By.CSS_SELECTOR, 
                "[data-testid='load-more'], .load-more, "
                "button[aria-label*='Load'], button[aria-label*='More']"
            )
            load_more.click()
            logger.info("✓ Clicked 'Load More' button")
            return True
        except:
            return False
    
    def scroll_element_into_view(self, element):
        """
        Scroll element into view (triggers lazy loading).
        
        Args:
            element: Selenium WebElement
        """
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.3)  # Brief pause for image to load
