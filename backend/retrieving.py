"""
This script provides retrieval functionality for a RAG (Retrieval-Augmented Generation) system.
It takes a user query, generates an embedding for it using Cohere, searches a Qdrant vector database
for semantically similar content, and returns the most relevant results.

It also includes a content accuracy test to verify the quality of embeddings and similarity calculations.
"""

import numpy as np
import os
import sys
import json
import logging # Import the logging module
import cohere
import qdrant_client
from typing import List, Dict, Any # Added for retrieve_chunks function

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the Qdrant collection name. This should match the collection used in the ingestion pipeline.
COLLECTION_NAME = "New-Rag-Data" 

def get_query_embedding(query: str, cohere_client: cohere.Client) -> list[float] | None:
    """
    Generates an embedding for the given query using the Cohere API.

    Args:
        query (str): The text query for which to generate an embedding.

    Returns:
        list[float] | None: A list of floats representing the embedding vector, or None if an error occurs.
    """
    if not query:
        logging.warning("Attempted to generate embedding for an empty query.")
        return None
    try:
        # Use 'embed-english-v3.0' model and 'search_query' input type for optimal retrieval.
        response = cohere_client.embed(
            texts=[query],
            model='embed-english-v3.0',
            input_type='search_query'
        )
        logging.info("Successfully generated embedding for query.")
        return response.embeddings[0]
    except cohere.CohereAPIError as e:
        logging.error(f"Cohere API error during embedding generation: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during embedding generation: {e}")
        return None


def search_qdrant(embedding: list[float], qdrant_client_instance: qdrant_client.QdrantClient, collection_name: str = COLLECTION_NAME, top_k: int = 5) -> List[Any] | None:
    """
    Searches the Qdrant collection for the most similar vectors to the given query embedding.

    Args:
        embedding (list[float]): The embedding vector of the search query.
        collection_name (str): The name of the Qdrant collection to search.
        top_k (int): The number of top similar results to retrieve.

    Returns:
        list | None: A list of search results (PointStructs) from Qdrant, or None if an error occurs.
    """
    if not embedding:
        logging.warning("Attempted to search Qdrant with an empty embedding.")
        return None
    try:
        logging.info(f"Searching Qdrant collection '{collection_name}' for top {top_k} results.")
        search_results = qdrant_client_instance.query_points(
            collection_name=collection_name,
            query=embedding,
            limit=top_k,
            with_payload=True # Ensure payload (original text, metadata) is returned
        )
        if search_results and hasattr(search_results, 'points'):
            logging.info(f"Found {len(search_results.points)} results in Qdrant.")
            return search_results.points
        else:
            logging.info("No results or invalid response structure from Qdrant search.")
            return []
    except Exception as e:
        logging.error(f"Qdrant search error: {e}")
        return None


def format_results(search_results: list) -> list[dict]:
    """
    Formats the raw Qdrant search results into a clean, human-readable JSON object.

    Args:
        search_results (list): A list of raw search results (PointStructs) from Qdrant.

    Returns:
        list[dict]: A list of dictionaries, each representing a formatted search result
                    with 'id', 'score', and 'payload' (which contains original text and metadata).
    """
    if not search_results:
        logging.info("No search results to format.")
        return []

    formatted_results = []
    for result in search_results:
        formatted_results.append({
            "id": str(result.id), # Convert UUID to string for JSON serialization
            "score": result.score,
            "payload": result.payload
        })
    logging.debug(f"Formatted {len(formatted_results)} search results.")
    return formatted_results


def retrieve_chunks(query: str, cohere_client: cohere.Client, qdrant_client_instance: qdrant_client.QdrantClient, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Generates embedding for the query, searches Qdrant, and formats the top_k results.

    Args:
        query (str): The user's query string.
        top_k (int): The number of top relevant documents to retrieve.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, where each dictionary
                               represents a retrieved chunk with 'id', 'score',
                               and 'payload' (containing 'text' and other metadata).
                               Returns an empty list if no results are found or an error occurs.
    """
    embedding = get_query_embedding(query, cohere_client)
    if not embedding:
        logging.error("Failed to generate embedding for query in retrieve_chunks.")
        return []

    search_results = search_qdrant(embedding, qdrant_client_instance, top_k=top_k)
    if not search_results:
        logging.info("No search results found in retrieve_chunks.")
        return []

    formatted_results = format_results(search_results)
    return formatted_results