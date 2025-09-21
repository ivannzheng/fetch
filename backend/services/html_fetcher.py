"""
HTML fetching and cleaning service
"""

import httpx
from bs4 import BeautifulSoup
from typing import List, Tuple


async def fetch_html(url: str) -> str:
    """Fetch and clean HTML content from URL"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
            
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""


async def fetch_multiple_html(urls: List[str]) -> List[Tuple[str, str]]:
    """Fetch HTML from multiple URLs and return (url, content) pairs"""
    results = []
    
    for i, url in enumerate(urls):
        content = await fetch_html(url)
        if content:
            results.append((url, content))
            # This will be handled by the pipeline for streaming
    
    return results
