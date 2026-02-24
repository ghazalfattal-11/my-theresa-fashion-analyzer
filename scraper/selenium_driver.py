"""
Selenium WebDriver setup and management.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging
from scraper.config import HEADLESS, WINDOW_SIZE, PAGE_LOAD_TIMEOUT

logger = logging.getLogger(__name__)


class SeleniumDriver:
    """Manages Selenium WebDriver lifecycle"""
    
    def __init__(self, headless: bool = HEADLESS):
        """
        Initialize driver manager.
        
        Args:
            headless: Run browser in headless mode
        """
        self.headless = headless
        self.driver = None
    
    def setup(self):
        """Setup and configure Chrome WebDriver"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
            logger.info("Running in headless mode")
        
        # Window size
        chrome_options.add_argument(f"--window-size={WINDOW_SIZE}")
        
        # Anti-detection options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User agent to avoid detection
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
        
        self.driver = webdriver.Chrome(options=chrome_options)
        
        # Hide webdriver property
        self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        })
        
        self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        
        logger.info("WebDriver setup complete")
        return self.driver
    
    def close(self):
        """Close the WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("WebDriver closed")
    
    def get_driver(self):
        """Get the driver instance"""
        if not self.driver:
            return self.setup()
        return self.driver
