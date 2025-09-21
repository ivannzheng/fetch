"""
Main pipeline service that orchestrates the entire process
"""

from typing import Dict, Any, List
from .google_search import search_google
from .html_fetcher import fetch_multiple_html
from .rag_service import RAGService
from .gemini_parser import GeminiParser


class PipelineService:
    def __init__(self):
        self.rag_service = RAGService()
        self.gemini_parser = GeminiParser()
    
    async def process_query_streaming(
        self, 
        query: str, 
        schema: Dict[str, Any], 
        num_urls: int = 10,
        max_answers: int = 50
    ):
        """Process a query through the complete pipeline with streaming logs"""
        
        results = {
            "query": query,
            "results": [],
            "total_found": 0
        }
        
        try:
            # Step 1: Search Google
            yield f"Initiating web search for: '{query}'"
            yield "Querying Google Custom Search API..."
            urls = await search_google(query, num_urls)
            yield f"Search complete! Discovered {len(urls)} relevant URLs"
            
            if not urls:
                yield "No URLs found for the given query"
                yield results
                return
            
            # Show some URLs
            for i, url in enumerate(urls[:3]):
                yield f"   {i+1}. {url[:60]}{'...' if len(url) > 60 else ''}"
            if len(urls) > 3:
                yield f"   ... and {len(urls) - 3} more URLs"
            
            # Step 2: Fetch HTML content
            yield "Starting content extraction from web pages..."
            yield f"Fetching content from {len(urls)} URLs in parallel..."
            html_contents = await fetch_multiple_html(urls)
            yield f"Content extraction complete! Successfully processed {len(html_contents)} pages"
            
            if not html_contents:
                yield "Failed to extract content from any URLs"
                yield results
                return
            
            # Show content stats
            total_chars = sum(len(content) for content in html_contents)
            yield f"Total content extracted: {total_chars:,} characters"
            
            # Step 3: Extract relevant content using RAG
            yield "Initializing RAG (Retrieval Augmented Generation) pipeline..."
            yield "Generating embeddings for query and content chunks..."
            yield "Performing semantic similarity search..."
            relevant_content = await self.rag_service.extract_relevant_content(
                query, schema, html_contents
            )
            yield f"RAG processing complete! Retrieved {len(relevant_content):,} characters of relevant content"
            
            # Step 4: Parse to structured JSON
            yield "Sending content to Gemini AI for structured data extraction..."
            yield f"Target schema: {list(schema.keys())}"
            yield f"Maximum answers requested: {max_answers}"
            parsed_results = await self.gemini_parser.parse_to_json(
                query, schema, relevant_content
            )
            
            if parsed_results:
                # Apply max_answers limit
                if len(parsed_results) > max_answers:
                    parsed_results = parsed_results[:max_answers]
                    yield f"Limited results to {max_answers} entries (found {len(parsed_results)} total)"
                
                results["results"] = parsed_results
                results["total_found"] = len(parsed_results)
                yield f"Success! Extracted {len(parsed_results)} structured data entries"
                yield f"Data fields populated: {sum(1 for item in parsed_results for v in item.values() if v is not None)}/{len(parsed_results) * len(schema)}"
            else:
                yield "No structured data could be extracted from the content"
            
        except Exception as e:
            yield f"Error: {str(e)}"
            results["error"] = str(e)
        
        # Yield the final result
        yield results
