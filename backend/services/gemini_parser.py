"""
Gemini parsing service for structured data extraction
"""

import json
from google import genai
from google.genai import types
from typing import Dict, Any, List
import os


class GeminiParser:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        self.client = genai.Client(api_key=api_key)
    
    async def parse_to_json(
        self, 
        query: str, 
        schema: Dict[str, Any], 
        relevant_content: str
    ) -> List[Dict[str, Any]]:
        """Parse relevant content into structured JSON using Gemini"""
        
        prompt = f"""
        You are a data extraction expert. Extract structured information from the provided content based on the user's query and desired schema.
        
        User Query: {query}
        Desired Schema: {json.dumps(schema, indent=2)}
        
        Relevant Content:
        {relevant_content}
        
        Instructions:
        1. Look through the content and find information that matches the user's query
        2. Extract data that fits the requested schema fields
        3. If you find multiple relevant items, return them as an array
        4. If a field cannot be determined from the content, use null
        5. For numbers, extract actual numeric values (not strings)
        6. For strings, extract the actual text content
        
        Return a JSON array of objects that match the schema. Each object should represent one relevant item found in the content.
        Return only the JSON array, no other text.
        """
        
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt,
                config=types.GenerateContentConfig(
                    thinking_config=types.ThinkingConfig(thinking_budget=128)  # Minimum thinking budget
                )
            )
            
            # Clean the response text - remove markdown code blocks if present
            response_text = response.text.strip()
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            # Parse JSON
            result = json.loads(response_text)
            
            # Ensure result is a list
            if isinstance(result, dict):
                result = [result]
            
            return result
            
        except Exception as e:
            print(f"Error parsing with Gemini: {e}")
            print(f"Response text was: {response.text if 'response' in locals() else 'No response'}")
            return []
