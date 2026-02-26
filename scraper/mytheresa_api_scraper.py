"""
Mytheresa API Scraper - Professional modular version
Uses pure HTTP requests via GraphQL API 
"""

import logging
from typing import List, Dict, Optional

from scraper.api_client import MytheresaAPIClient
from scraper.graphql_queries import PRODUCT_LISTING_QUERY, build_listing_variables
from scraper.models import Product

logger = logging.getLogger(__name__)


class MytheresaAPIScraper:
    """
    High-level scraper for Mytheresa products
    Uses GraphQL API for fast, reliable scraping
    """
    
    def __init__(self):
        self.client = MytheresaAPIClient()
    
    def scrape_category(
        self, 
        category_slug: str, 
        limit: int = 100,
        brand_filter: Optional[str] = None,
        max_price: Optional[float] = None,
        section: Optional[str] = None
        ) -> List[Dict]:
        """
        Scrape products from a category
        
        Args:
            category_slug: Category slug (e.g., "/clothing", "/designers/gucci")
            limit: Maximum products to return
            brand_filter: Filter by brand name (optional)
            max_price: Maximum price filter (optional)
            section: Force section to 'men' or 'women' (optional, auto-detected)
            
        Returns:
            List of product dictionaries
        """
        all_products = []
        page = 1
        
        # Determine section if not provided
        if section is None:
            section = self._detect_section(category_slug)
        
        logger.info(f"Scraping category: {category_slug} (section: {section})")
        
        while len(all_products) < limit:
            logger.info(f"Fetching page {page}...")
            
            products = self._fetch_page(category_slug, page, section)
            
            if not products:
                logger.info("No more products found")
                break
            
            # Apply filters
            for product in products:
                if len(all_products) >= limit:
                    break
                
                # Brand filter
                if brand_filter and brand_filter.lower() not in product.brand.lower():
                    continue
                
                # Price filter
                if max_price and product.price and product.price > max_price:
                    continue
                
                all_products.append(product.to_dict())
            
            page += 1
            
            # Stop if we got fewer products than expected (last page)
            if len(products) < 60:
                break
        
        logger.info(f"✓ Scraped {len(all_products)} products")
        return all_products[:limit]
    
    def _fetch_page(
        self, 
        category_slug: str, 
        page: int, 
        section: str
        ) -> List[Product]:
        """
        Fetch a single page of products
        
        Args:
            category_slug: Category slug
            page: Page number (1-indexed)
            section: Section ('men' or 'women')
            
        Returns:
            List of Product objects
        """
        # Build query variables
        variables = build_listing_variables(
            slug=category_slug,
            page=page,
            size=60
        )
        
        # Execute query
        data = self.client.execute_query(
            query=PRODUCT_LISTING_QUERY,
            variables=variables,
            section=section
        )
        
        if not data:
            return []
        
        # Parse products
        products = self._parse_products(data)
        
        logger.info(f"  Found {len(products)} products on page {page}")
        
        return products
    
    def _parse_products(self, data: Dict) -> List[Product]:
        """
        Parse products from API response
        
        Args:
            data: API response data
            
        Returns:
            List of Product objects
        """
        products = []
        
        try:
            product_list = data.get('data', {}).get('xProductListingPage', {}).get('products', [])
            
            for item in product_list:
                product = Product.from_api_response(item)
                if product:
                    products.append(product)
        
        except Exception as e:
            logger.error(f"Error parsing products: {str(e)}")
        
        return products
    
    def _detect_section(self, category_slug: str) -> str:
        """
        Detect section from category slug
        
        Args:
            category_slug: Category slug
            
        Returns:
            'men' or 'women'
        """
        if '/men/' in category_slug or category_slug.startswith('/men'):
            return 'men'
        elif '/women/' in category_slug or category_slug.startswith('/women'):
            return 'women'
        else:
            return 'men'  # Default to men
    
    # Convenience methods for specific categories
    
    def scrape_men_clothing(self, limit: int = 500) -> List[Dict]:
        """Scrape men's clothing"""
        return self.scrape_category("/clothing", limit=limit, section='men')
    
    def scrape_women_clothing(self, limit: int = 500) -> List[Dict]:
        """Scrape women's clothing"""
        return self.scrape_category("/clothing", limit=limit, section='women')
    
    def scrape_men_shoes(self, limit: int = 100) -> List[Dict]:
        """Scrape men's shoes"""
        return self.scrape_category("/shoes", limit=limit, section='men')
    
    def scrape_gucci_under_1000(self, limit: int = 20) -> List[Dict]:
        """Scrape Gucci items under $1000"""
        return self.scrape_category(
            "/designers/gucci",
            limit=limit,
            max_price=1000,
            section='men'
        )
    
    def scrape_elie_saab(self, limit: int = 50) -> List[Dict]:
        """Scrape Elie Saab items"""
        return self.scrape_category(
            "/designers/elie-saab",
            limit=limit,
            section='women'
        )


# Test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    scraper = MytheresaAPIScraper()
    
    print("="*70)
    print("Mytheresa API Scraper - Modular Professional Version")
    print("="*70)
    print("\nNo Selenium, no browser - just pure HTTP requests")
    print("\nTesting with Saint Laurent products...")
    
    # Test with designer category
    products = scraper.scrape_category("/designers/saint-laurent", limit=5)
    
    print(f"\n✓ Found {len(products)} products:")
    for i, p in enumerate(products, 1):
        print(f"\n{i}. {p['brand']} - {p['name']}")
        print(f"   Price: ${p['price']:.2f}" if p['price'] else "   Price: N/A")
        print(f"   Color: {p['color']}")
    
    print("\n" + "="*70)
    print("SUCCESS! Modular scraper working perfectly!")
    print("="*70)
