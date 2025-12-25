# Quickstart: RAG Retrieval Implementation

## Overview
This guide provides a quick start to implement and use the RAG retrieval functionality for querying Qdrant vector database.

## Prerequisites
- Python 3.11+
- Cohere API key
- Qdrant Cloud URL and API key
- Existing vector database with ingested content

## Setup

### 1. Environment Configuration
```bash
# Copy the environment file
cp .env.example .env

# Update .env with your API keys
COHERE_API_KEY=your_cohere_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

### 2. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

## Implementation

### 1. Create the Retrieval Module
Create `backend/retrieving.py` with the following functionality:

```python
# This will contain:
# - Query embedding generation
# - Qdrant search functionality
# - Result formatting
# - Error handling
```

### 2. Core Functions
The retrieval module will include:
- `get_query_embedding(query)`: Convert text query to embedding
- `search_qdrant(embedding, top_k=5)`: Search Qdrant for similar vectors
- `format_results(search_results)`: Format raw Qdrant results to clean JSON
- `retrieve(query, top_k=5)`: Main function to handle the full retrieval process

## Usage Example

### Command Line Usage
```bash
python backend/retrieving.py "What is ROS2?"
```

### Programmatic Usage
```python
from backend.retrieving import retrieve

results = retrieve("What is ROS2?", top_k=5)
print(results)
```

## Expected Output
```json
[
  {
    "id": "chunk_id_123",
    "score": 0.85,
    "payload": {
      "text": "ROS2 (Robot Operating System 2) is a set of libraries and tools...",
      "source_url": "https://example.com/ros2-intro",
      "page_title": "Introduction to ROS2"
    }
  }
]
```

## Testing
Run the retrieval functionality to verify it works:
```bash
python backend/retrieving.py "your test query here"
```

## Troubleshooting
- **Empty Results**: Verify that the Qdrant collection has ingested content
- **API Errors**: Check that your Cohere and Qdrant API keys are valid
- **Connection Issues**: Ensure the Qdrant URL is accessible