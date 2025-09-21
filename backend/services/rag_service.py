"""
RAG (Retrieval Augmented Generation) service using Gemini embeddings
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from google import genai
from google.genai import types
from typing import List, Dict, Any, Tuple
import os


class RAGService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        self.client = genai.Client(api_key=api_key)
    
    async def chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """Split text into chunks for processing"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        return chunks
    
    async def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Get embeddings for a list of texts"""
        result = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=texts,
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_DOCUMENT",
                output_dimensionality=768
            )
        )
        
        # Normalize embeddings for smaller dimensions
        embeddings = []
        for embedding_obj in result.embeddings:
            embedding_values = np.array(embedding_obj.values)
            normed_embedding = embedding_values / np.linalg.norm(embedding_values)
            embeddings.append(normed_embedding)
        
        return np.array(embeddings)
    
    async def get_query_embedding(self, query: str, schema: Dict[str, Any]) -> np.ndarray:
        """Get embedding for query + schema context"""
        # Combine query and schema for better context
        context = f"Query: {query}\nSchema: {schema}"
        
        result = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=[context],
            config=types.EmbedContentConfig(
                task_type="RETRIEVAL_QUERY",
                output_dimensionality=768
            )
        )
        
        # Normalize embedding
        embedding_values = np.array(result.embeddings[0].values)
        normed_embedding = embedding_values / np.linalg.norm(embedding_values)
        
        return normed_embedding
    
    async def retrieve_relevant_chunks(
        self, 
        query: str, 
        schema: Dict[str, Any], 
        text_chunks: List[str], 
        top_k: int = 5
    ) -> List[str]:
        """Retrieve most relevant chunks using RAG"""
        
        # Get query embedding
        query_embedding = await self.get_query_embedding(query, schema)
        
        # Get chunk embeddings
        chunk_embeddings = await self.get_embeddings(text_chunks)
        
        # Calculate similarities
        similarities = cosine_similarity([query_embedding], chunk_embeddings)[0]
        
        # Get top-k most similar chunks
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        relevant_chunks = [text_chunks[i] for i in top_indices]
        
        return relevant_chunks
    
    async def extract_relevant_content(
        self, 
        query: str, 
        schema: Dict[str, Any], 
        html_contents: List[Tuple[str, str]]
    ) -> str:
        """Extract relevant content from HTML using RAG"""
        
        # Combine all text content
        all_text = ""
        for url, content in html_contents:
            all_text += f"\n\n--- Content from {url} ---\n{content}"
        
        # Chunk the text
        chunks = await self.chunk_text(all_text)
        
        # Retrieve relevant chunks
        relevant_chunks = await self.retrieve_relevant_chunks(query, schema, chunks)
        
        # Combine relevant chunks
        relevant_content = "\n\n".join(relevant_chunks)
        
        return relevant_content
