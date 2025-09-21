"""
Google Custom Search API service
"""

import httpx
from typing import List
import os


async def search_google(query: str, num_results: int = 10) -> List[str]:
    """Search Google Custom Search API and return URLs"""
    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    
    if not api_key or not search_engine_id:
        raise ValueError("Google API credentials not configured")
    
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": query,
        "num": num_results
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        urls = []
        for item in data.get("items", []):
            urls.append(item["link"])
        
        return urls
