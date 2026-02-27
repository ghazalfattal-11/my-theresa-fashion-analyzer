"""
Download and save images to disk.
"""

import requests
import logging
from pathlib import Path
from typing import Optional
from scraper.config import IMAGES_DIR

logger = logging.getLogger(__name__)

# Headers to mimic browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


class ImageDownloader:
    """Download and save images to disk"""
    
    def __init__(self, output_dir: Path = IMAGES_DIR):
        """
        Initialize downloader.
        
        Args:
            output_dir: Directory to save images
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def download_and_save(
        self, 
        url: str, 
        category: str, 
        filename: str,
        timeout: int = 10
     ) -> Optional[str]:
        """
        Download image from URL and save to disk.
        
        Args:
            url: Image URL
            category: Category folder name
            filename: Filename to save as
            timeout: Request timeout
            
        Returns:
            Saved file path or None if failed
        """
        try:
            # Create category directory
            category_dir = self.output_dir / category
            category_dir.mkdir(exist_ok=True)
            
            # Download image
            response = requests.get(url, headers=HEADERS, timeout=timeout)
            response.raise_for_status()
            
            # Save to disk
            filepath = category_dir / filename
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"✓ Downloaded: {category}/{filename}")
            return str(filepath)
        
        except Exception as e:
            logger.error(f"✗ Failed to download {url}: {str(e)}")
            return None
    
    def get_next_filename(self, category: str, extension: str = "jpg") -> str:
        """
        Get next available filename in category.
        
        Args:
            category: Category name
            extension: File extension
            
        Returns:
            Next filename
        """
        category_dir = self.output_dir / category
        category_dir.mkdir(exist_ok=True)
        
        existing = list(category_dir.glob(f"*.{extension}"))
        next_num = len(existing) + 1
        
        return f"{category}_{next_num}.{extension}"
    
    def get_download_count(self, category: str) -> int:
        """
        Get count of downloaded images in category.
        
        Args:
            category: Category name
            
        Returns:
            Number of images
        """
        category_dir = self.output_dir / category
        if not category_dir.exists():
            return 0
        
        return len(list(category_dir.glob("*.*")))
