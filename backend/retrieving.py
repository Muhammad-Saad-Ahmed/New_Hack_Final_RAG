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
from dotenv import load_dotenv
import cohere
import qdrant_client

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
# This ensures that API keys and other configurations are loaded securely.
load_dotenv()

# Initialize Cohere client
# The Cohere client is used to generate embeddings for text.
co = cohere.Client(os.getenv("COHERE_API_KEY"))

# Initialize Qdrant client
# The Qdrant client connects to the vector database where document embeddings are stored.
qdrant_client = qdrant_client.QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# Define the Qdrant collection name. This should match the collection used in the ingestion pipeline.
COLLECTION_NAME = "New-Rag-Data" 

def get_query_from_cli():
    """
    Retrieves the search query or a special command from command-line arguments.

    Checks for a '--test-accuracy' flag to trigger the content accuracy test.
    Otherwise, it concatenates all arguments to form the search query.

    Returns:
        str: The search query string, '--test-accuracy' flag, or None if no valid input.
    """
    # Check for --test-accuracy flag first to prioritize testing mode
    if "--test-accuracy" in sys.argv:
        return "--test-accuracy"
    
    # Otherwise, parse regular query from remaining arguments
    # Exclude the script name (sys.argv[0]) and any flags
    query_parts = [arg for arg in sys.argv[1:] if arg != "--test-accuracy"]
    query = " ".join(query_parts)
    return query.strip() if query.strip() else None


def get_query_embedding(query: str) -> list[float] | None:
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
        response = co.embed(
            texts=[query],
            model='embed-english-v3.0',
            input_type='search_query'
        )
        logging.info("Successfully generated embedding for query.")
        return response.embeddings[0]
    except cohere.errors.CohereAPIError as e:
        logging.error(f"Cohere API error during embedding generation: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during embedding generation: {e}")
        return None


def search_qdrant(embedding: list[float], collection_name: str = COLLECTION_NAME, top_k: int = 5) -> list | None:
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
        search_results = qdrant_client.search(
            collection_name=collection_name,
            query_vector=embedding,
            limit=top_k,
            with_payload=True # Ensure payload (original text, metadata) is returned
        )
        logging.info(f"Found {len(search_results)} results in Qdrant.")
        return search_results
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


def calculate_cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """
    Calculates the cosine similarity between two vectors.

    Cosine similarity measures the cosine of the angle between two vectors.
    A value closer to 1 indicates higher similarity, and closer to 0 indicates lower similarity.

    Args:
        vec1 (list[float]): The first vector.
        vec2 (list[float]): The second vector.

    Returns:
        float: The cosine similarity between the two vectors. Returns 0.0 if either vector is a zero vector.
    """
    vec1_np = np.array(vec1)
    vec2_np = np.array(vec2)
    
    dot_product = np.dot(vec1_np, vec2_np)
    norm_a = np.linalg.norm(vec1_np)
    norm_b = np.linalg.norm(vec2_np)
    
    # Handle division by zero for zero vectors
    if norm_a == 0 or norm_b == 0:
        logging.warning("Encountered zero vector(s) in cosine similarity calculation. Returning 0.0.")
        return 0.0
    
    return dot_product / (norm_a * norm_b)


def test_content_accuracy():
    """
    Tests content accuracy by comparing the embedding of an original text
    with a slightly modified version and a dissimilar text.

    This function fetches a random document from the Qdrant collection,
    creates a slightly altered version of its text, and a completely
    unrelated text. It then generates embeddings for all three and
    calculates cosine similarities to verify that similar texts yield
    higher scores than dissimilar texts.
    """
    logging.info("--- Running Content Accuracy Test ---")
    try:
        # 1. Fetch a random point from the Qdrant collection for testing
        count_result = qdrant_client.count(collection_name=COLLECTION_NAME, exact=True)
        total_points = count_result.count
        
        if total_points == 0:
            logging.error(f"No points found in collection '{COLLECTION_NAME}' to test content accuracy. "
                          "Please ensure the ingestion pipeline has run successfully.")
            return

        logging.info(f"Fetching a random point from '{COLLECTION_NAME}' (total points: {total_points}).")
        # Fetch a single random point. For very large collections, a more sophisticated
        # random sampling or pagination strategy might be needed.
        scroll_result, _ = qdrant_client.scroll(
            collection_name=COLLECTION_NAME,
            limit=1,
            offset=np.random.randint(0, total_points), # Random offset for variety in tests
            with_vectors=True, # We need the original embedding for comparison
            with_payload=True  # We need the original text from the payload
        )
        
        if not scroll_result or not scroll_result[0].payload or not scroll_result[0].vector:
            logging.error("Failed to fetch a random point with sufficient data for content accuracy test.")
            return

        original_point = scroll_result[0]
        original_text = original_point.payload["text"]
        original_embedding = original_point.vector
        logging.info(f"Fetched original point ID: {original_point.id}")

        # 2. Create a slightly modified text and a dissimilar text for comparison
        # A simple replacement to create a "similar" but not identical text
        modified_text = original_text.replace("ROS 2", "Robot OS 2", 1) 
        if modified_text == original_text: # Fallback if "ROS 2" isn't in the text
            modified_text += " This is a slight addition to the original content."

        # A completely unrelated text to represent "dissimilar" content
        dissimilar_text = "The quick brown fox jumps over the lazy dog. This text is unrelated to robotics or programming."

        logging.info(f"Original Text (excerpt): {original_text[:150]}...")
        logging.info(f"Modified Text (excerpt): {modified_text[:150]}...")
        logging.info(f"Dissimilar Text (excerpt): {dissimilar_text[:150]}...")

        # 3. Generate embeddings for test texts using the Cohere API
        # Using 'search_query' input type for consistency with query embeddings.
        modified_embedding = get_query_embedding(modified_text)
        dissimilar_embedding = get_query_embedding(dissimilar_text)

        if original_embedding is None or modified_embedding is None or dissimilar_embedding is None:
            logging.error("Failed to generate embeddings for one or more test texts. Cannot proceed with accuracy test.")
            return

        # 4. Calculate and print cosine similarities to assess content accuracy
        similarity_original_modified = calculate_cosine_similarity(original_embedding, modified_embedding)
        similarity_original_dissimilar = calculate_cosine_similarity(original_embedding, dissimilar_embedding)

        logging.info(f"Cosine Similarity (Original vs. Modified): {similarity_original_modified:.4f}")
        logging.info(f"Cosine Similarity (Original vs. Dissimilar): {similarity_original_dissimilar:.4f}")

        # Basic assertion to validate the test's success
        # A good RAG system should show higher similarity for modified/similar texts
        # compared to completely dissimilar ones.
        if similarity_original_modified > similarity_original_dissimilar:
            logging.info("Content accuracy test PASSED: Modified text is more similar to original than dissimilar text, as expected.")
        else:
            logging.warning("Content accuracy test FAILED: Modified text is NOT more similar to original than dissimilar text. "
                            "This might indicate an issue with embeddings or similarity calculation.")

    except Exception as e:
        logging.critical(f"An unexpected error occurred during content accuracy test: {e}", exc_info=True)
    finally:
        logging.info("--- Content Accuracy Test Finished ---\n")


def main():
    """
    Main function to orchestrate the RAG retrieval process or run the content accuracy test.

    It parses command-line arguments to determine whether to execute a search query
    or run a specific content accuracy test. It handles argument parsing,
    embedding generation, Qdrant search, and result formatting/output.
    """
    logging.info("Starting retrieving.py script.")

    # Check if accuracy test is requested via command-line argument
    if "--test-accuracy" in sys.argv:
        test_content_accuracy()
        sys.exit(0) # Exit after running the test

    # Get the search query from command line arguments for normal retrieval
    query = get_query_from_cli()

    # Handle cases where no query is provided or only whitespace
    if not query or not query.strip():
        error_response = {
            "error": "Usage: python retrieving.py <search query> or python retrieving.py --test-accuracy",
            "query": None,
            "results": [],
            "total_results": 0
        }
        logging.error("No query provided or query is empty/whitespace. Exiting with error.")
        print(json.dumps(error_response, indent=2))
        sys.exit(1) # Exit with an error code

    logging.info(f"Searching for: '{query}'")

    # Generate embedding for the query using Cohere
    embedding = get_query_embedding(query)
    if not embedding:
        error_response = {
            "error": "Failed to generate query embedding. Check Cohere API key and network connection.",
            "query": query,
            "results": [],
            "total_results": 0
        }
        logging.error("Failed to generate query embedding. Exiting with error.")
        print(json.dumps(error_response, indent=2))
        sys.exit(1)

    # Search Qdrant for similar vectors to the query embedding
    search_results = search_qdrant(embedding)
    if not search_results:
        # If no results are found, return an empty but successful response
        success_response = {
            "query": query,
            "results": [],
            "total_results": 0,
            "message": "No relevant results found in Qdrant for the given query."
        }
        logging.info("No relevant results found in Qdrant.")
        print(json.dumps(success_response, indent=2))
        sys.exit(0) # Exit successfully even if no results

    # Format the retrieved results into a clean JSON structure
    formatted_results = format_results(search_results)
    logging.info(f"Successfully retrieved and formatted {len(formatted_results)} results.")

    # Create the final response object
    response = {
        "query": query,
        "results": formatted_results,
        "total_results": len(formatted_results)
    }

    # Print the results as clean JSON to standard output
    print(json.dumps(response, indent=2))
    logging.info("Script finished successfully.")

if __name__ == "__main__":
    main()