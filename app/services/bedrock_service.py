import boto3
import json
import base64
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class BedrockService:
    """Service for interacting with AWS Bedrock AI models"""
    
    def __init__(self):
        """Initialize Bedrock service"""
        logger.info("Bedrock service initialized")
    
    @property
    def client(self):
        """Create a fresh Bedrock client for each request (handles SSO token refresh)"""
        # Read config fresh each time
        aws_region = os.getenv("AWS_REGION", "us-east-1")
        aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        
        try:
            if aws_access_key and aws_secret_key:
                return boto3.client(
                    service_name="bedrock-runtime",
                    region_name=aws_region,
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key
                )
            else:
                # Use default AWS credentials (SSO/aws configure)
                # Create a new session to get fresh credentials
                session = boto3.Session()
                return session.client(
                    service_name="bedrock-runtime",
                    region_name=aws_region
                )
        except Exception as e:
            logger.error(f"Failed to create Bedrock client: {str(e)}")
            return None
    
    @property
    def model_id(self):
        """Get model ID from environment"""
        return os.getenv(
            "BEDROCK_MODEL_ID",
            "anthropic.claude-3-sonnet-20240229-v1:0"
        )
    
    def analyze_fashion_item(self, image_bytes: bytes) -> str:
        """
        Analyze a fashion item image using AWS Bedrock.
        
        Args:
            image_bytes: Raw image data as bytes
            
        Returns:
            str: Detailed description of the fashion item
            
        Raises:
            Exception: If Bedrock is not configured or analysis fails
        """
        # Check if client is initialized
        if not self.client:
            raise Exception(
                "AWS Bedrock not configured. Please set AWS credentials in .env file"
            )
        
        try:
            # Encode image to base64
            image_base64 = base64.b64encode(image_bytes).decode("utf-8")
            
            # Prepare the prompt for fashion analysis
            prompt = """Analyze this fashion item in detail. Provide:

                        1. Item Type: What type of clothing/accessory is this?
                        2. Colors: What are the main colors?
                        3. Patterns: Any patterns, prints, or textures?
                        4. Style: What style category (casual, formal, sporty, etc.)?
                        5. Material: What materials does it appear to be made from?
                        6. Design Features: Notable design elements, cuts, or details?
                        7. Occasion: What occasions would this be suitable for?
                        8. Brand Indicators: Any visible brand elements or luxury indicators?

                        Be specific and detailed in your analysis."""
            
            # Prepare request payload for Claude 3
            payload = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_base64
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            }
            
            logger.info(f"Sending request to Bedrock model: {self.model_id}")
            
            # Invoke Bedrock model
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(payload)
            )
            
            # Parse response
            response_body = json.loads(response["body"].read())
            
            # Extract the text from Claude's response
            caption = response_body["content"][0]["text"]
            
            logger.info("Successfully received analysis from Bedrock")
            return caption
        
        except Exception as e:
            logger.error(f"Bedrock API error: {str(e)}")
            raise Exception(f"Failed to analyze image with Bedrock: {str(e)}")
