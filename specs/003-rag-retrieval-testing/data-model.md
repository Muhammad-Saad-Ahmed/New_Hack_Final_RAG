# Data Model: RAG Retrieval

## Overview
This document defines the data structures and models used in the RAG retrieval functionality.

## Entities

### Query
- **Description**: A text string submitted by the user for semantic search
- **Fields**:
  - `text`: string - The user's search query
  - `embedding`: list[float] - Vector representation of the query text
  - `top_k`: int - Number of top results to retrieve (default: 5)

### Retrieved Chunk
- **Description**: A text segment returned from the vector database that matches the query
- **Fields**:
  - `id`: string - Unique identifier for the chunk
  - `text`: string - The actual text content of the chunk
  - `score`: float - Similarity score between query and chunk
  - `source_url`: string - URL of the original document
  - `chunk_id`: string - Identifier for the specific chunk in the original document
  - `page_title`: string - Title of the original page

### Metadata
- **Description**: Information about the retrieved chunk including source URL and chunk identifier
- **Fields**:
  - `source_url`: string - URL of the original document
  - `chunk_id`: string - Identifier for the specific chunk
  - `page_title`: string - Title of the original page
  - `section_title`: string - Title of the section (if available)

### Search Result
- **Description**: A structured response containing the retrieved chunk and its metadata
- **Fields**:
  - `id`: string - Unique identifier for the result
  - `score`: float - Similarity score
  - `payload`: object - Contains text, source_url, page_title, and other metadata
  - `formatted_text`: string - Cleaned and formatted text content

## Relationships
- One `Query` can produce multiple `Retrieved Chunk` results
- Each `Retrieved Chunk` has associated `Metadata`
- Multiple `Retrieved Chunk` objects are aggregated into a `Search Result` list

## Validation Rules
- Query text must not be empty
- top_k value must be between 1 and 100
- Retrieved chunks must have a minimum similarity score of 0.1
- Source URL must be a valid URL format
- Text content must not exceed 10,000 characters per chunk