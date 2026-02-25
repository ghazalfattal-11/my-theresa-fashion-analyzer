"""
HTTP client for Mytheresa GraphQL API
Handles all HTTP communication with the API
"""

import httpx
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class MytheresaAPIClient:
    """
    Low-level HTTP client for Mytheresa's GraphQL API
    """
    
    def __init__(self):
        self.base_url = "https://www.mytheresa.com/api"
        self.default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en',
            'Content-Type': 'application/json',
            'Referer': 'https://www.mytheresa.com/',
            'Origin': 'https://www.mytheresa.com',
            'X-Store': 'us',
            'X-Country': 'US',
        }
    
    def execute_query(
        self, 
        query: str, 
        variables: Dict,
        section: str = 'men'
      ) -> Optional[Dict]:
        """
        Execute a GraphQL query
        
        Args:
            query: GraphQL query string
            variables: Query variables
            section: Section ('men' or 'women')
            
        Returns:
            Response data or None if error
        """
        try:
            # Prepare headers with section
            headers = self.default_headers.copy()
            headers['X-Section'] = section
            
            # Prepare payload
            payload = {
                "query": query,
                "variables": variables
            }
            
            # Execute request
            with httpx.Client(http2=True, timeout=30.0) as client:
                response = client.post(self.base_url, json=payload, headers=headers)
                
                if response.status_code != 200:
                    logger.error(f"API returned status {response.status_code}")
                    return None
                
                data = response.json()
                
                # Check for GraphQL errors
                if 'errors' in data and data['errors']:
                    error_msg = data['errors'][0].get('message', 'Unknown error')
                    logger.error(f"GraphQL error: {error_msg}")
                    return None
                
                return data
        
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            return None
