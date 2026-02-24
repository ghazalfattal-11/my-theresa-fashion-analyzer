"""
Extract product data from page elements.
"""

from typing import Optional, Dict


class ProductExtractor:
    """Extracts product data from HTML elements"""
    
    def __init__(self, scroller):
        self.scroller = scroller
    
    def extract_from_element(self, img_element) -> Optional[Dict]:
        """Extract data from img element"""
        try:
            # Get image URL
            image_url = (
                img_element.get_attribute("src") or 
                img_element.get_attribute("data-src") or
                img_element.get_attribute("data-lazy-src")
            )
            
            if not image_url or 'mytheresa.com' not in image_url:
                return None
            
            # Get brand from alt text
            brand = "Unknown"
            alt = img_element.get_attribute("alt")
            if alt and "|" in alt:
                brand = alt.split("|")[-1].strip()
            
            return {
                "image_url": image_url,
                "brand": brand,
                "price": None
            }
        except:
            return None
