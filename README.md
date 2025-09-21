# Fetch

Transform the internet into a structured database. This full-stack application lets you query the web and get back clean, structured JSON data using Google Custom Search and Gemini AI.

## What This Does

Instead of manually scraping websites or dealing with messy HTML, you can simply describe what you want to find and get back organized data. Want to find the best laptops under $1000? Just ask, and get back a list with names, prices, and ratings. Looking for upcoming tech conferences? Get dates, locations, and ticket prices in a structured format.

## Demo 
https://github.com/user-attachments/assets/e81e90a3-cd8b-469e-8dd9-530be4862ddc

## Tech Stack

**Frontend**: Next.js 15 with TypeScript, TailwindCSS for styling, and CodeMirror for the code editor
**Backend**: FastAPI with Python, using httpx for web requests and BeautifulSoup for HTML parsing
**AI**: Google's Gemini API for intelligent data extraction and Google Custom Search for finding relevant content

## Getting Started

### Prerequisites

You'll need API keys from Google:
- Google Custom Search API key
- Google Custom Search Engine ID  
- Gemini API key

### Setup

1. Clone this repository and navigate to the project directory

2. Set up your environment variables by creating a `.env` file in the backend directory:

```bash
# Google Custom Search API
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_SEARCH_ENGINE_ID=your_search_engine_id_here

# Gemini API
GEMINI_API_KEY=your_gemini_api_key_here
```

3. Start the backend server:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

The backend will be running on `http://localhost:8000`

4. In a new terminal, start the frontend:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000`

## How to Use

The interface is split into two main panels. On the left, you'll see a code editor where you can modify the query. On the right, you'll see the results and processing logs.

1. **Modify the Query**: Change the query text and define what fields you want to extract
2. **Click Fetch**: Hit the fetch button to start the data extraction process
3. **Watch the Process**: See real-time logs showing what's happening behind the scenes
4. **Get Your Data**: View the structured results in the right panel

### Example Queries

Here are some examples of what you can search for:

**Find the best smartphones under $500:**
```json
{
  "query": "best smartphones under $500",
  "output": {
    "brand": "string",
    "model": "string", 
    "price": "number",
    "rating": "number"
  }
}
```

**Get upcoming tech conferences:**
```json
{
  "query": "tech conferences 2024 San Francisco",
  "output": {
    "name": "string",
    "date": "string",
    "location": "string",
    "price": "number"
  }
}
```

## How It Works

The system follows a sophisticated four-step pipeline that combines web search, content extraction, semantic analysis, and AI-powered parsing:

### 1. Google Custom Search API
The process begins by sending your query to Google's Custom Search API, which returns the top 10 most relevant URLs. This ensures we're working with high-quality, authoritative sources rather than random web pages.

### 2. Beautiful Soup Content Extraction
Once we have the URLs, the system uses **httpx** to fetch the HTML content from each page in parallel, then **Beautiful Soup** to parse and clean the raw HTML. This step removes all the noise - navigation menus, ads, scripts, and styling - leaving only the meaningful text content.

### 3. RAG Pipeline with Semantic Search
The cleaned content then goes through a **Retrieval-Augmented Generation (RAG)** pipeline:
- **Text Chunking**: Content is split into manageable 500-word chunks
- **Embedding Generation**: Each chunk is converted to a 768-dimensional vector using Google's Gemini embedding model
- **Semantic Similarity**: **NumPy** and **scikit-learn** calculate cosine similarity between your query and each content chunk
- **Relevant Content Retrieval**: Only the most semantically relevant chunks are selected for processing

### 4. Gemini AI Data Extraction
Finally, the most relevant content chunks are sent to **Gemini 2.5 Pro** with a carefully crafted prompt that includes your query, desired schema, and the cleaned content. The AI then extracts structured data that matches your exact specifications, returning clean JSON results.

This approach ensures you get accurate, relevant data by combining the power of Google's search algorithms, semantic understanding through embeddings, and advanced AI reasoning - all while processing content in real-time with streaming updates.

## Project Structure

```
fetch/
├── frontend/              # Next.js frontend application
│   ├── src/
│   │   ├── app/          # Next.js app router pages
│   │   └── components/   # React components
│   └── package.json
├── backend/              # FastAPI backend application
│   ├── services/         # Individual service modules
│   ├── run.py           # Main application entry point
│   └── .env             # Environment variables (not in git)
└── README.md
```

## API Reference

**POST /fetch** - Main endpoint for processing queries
- Accepts a JSON payload with query, output schema, and max results
- Returns streaming results with real-time progress updates

**GET /health** - Health check endpoint
- Returns the current status of the service

## Features

- **Real-time Processing**: Watch the extraction process happen live with detailed logs
- **Smart Code Editor**: Syntax highlighting and validation for your queries
- **Error Handling**: Graceful handling of failed requests and malformed data
- **Streaming Results**: Get results as they're processed, not all at once
- **Flexible Schema**: Define exactly what fields you want to extract

## Limitations

- Processes up to 10 URLs per query to balance speed and comprehensiveness
- Content is cleaned and processed to focus on the most relevant information
- Requires valid API keys for Google services
- Rate limits apply based on your Google API quotas

## Contributing

This is a demo project, but feel free to fork it and build upon it. The codebase is structured to be easily extensible - you can add new data sources, improve the parsing logic, or enhance the frontend interface.
