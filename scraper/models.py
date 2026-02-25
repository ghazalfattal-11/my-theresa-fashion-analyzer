"""
Data models for scraped products
"""

from typing import Optional
from dataclasses import dataclass


@dataclass
class Product:
    """
    Product data model
    """
    image_url: str
    brand: str
    name: str
    price: Optional[float]
    sku: str
    slug: str
    color: str
    description: str
    has_stock: bool
    
    @classmethod
    def from_api_response(cls, item: dict) -> Optional['Product']:
        """
        Create Product from API response item
        
        Args:
            item: Product item from API response
            
        Returns:
            Product instance or None if invalid
        """
        # Extract main image
        images = item.get('displayImages', [])
        image_url = images[0] if images else None
        
        if not image_url:
            return None
        
        # Extract price (convert from cents to dollars)
        main_price = item.get('mainPrice', 0)
        price = main_price / 100 if main_price else None
        
        return cls(
            image_url=image_url,
            brand=item.get('designer', 'Unknown'),
            name=item.get('name', ''),
            price=price,
            sku=item.get('sku', ''),
            slug=item.get('slug', ''),
            color=item.get('color', ''),
            description=item.get('description', ''),
            has_stock=item.get('hasStock', False),
        )
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            'image_url': self.image_url,
            'brand': self.brand,
            'name': self.name,
            'price': self.price,
            'sku': self.sku,
            'slug': self.slug,
            'color': self.color,
            'description': self.description,
            'has_stock': self.has_stock,
        }
