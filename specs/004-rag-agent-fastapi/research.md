# Research Notes: RAG Agent with OpenAI Agents SDK

**Feature Branch**: `004-rag-agent-fastapi`
**Date**: 2025-12-26

## Resolved Clarifications & Research Findings

### 1. Integration of `retrieve` function from `retrieving.py` into `agent.py`

-   **Decision**: A refactored and consolidated `retrieve` function will be created within `retrieving.py` (or a dedicated `retriever` module) that encapsulates the steps of generating embeddings, searching Qdrant, and formatting results. This consolidated function will then be imported and called directly by `agent.py`.
-   **Rationale**: Encapsulating the retrieval logic in a single function promotes modularity, reusability, and cleaner integration with the agent. It avoids duplicating code or exposing the agent to the internal mechanics of embedding and vector search.
-   **Alternatives Considered**:
    -   *Directly calling `get_query_embedding`, `search_qdrant`, `format_results` from `agent.py`*: Rejected due to increased coupling and complexity in `agent.py`.
    -   *Making `retrieving.py` a script that `agent.py` executes and parses output*: Rejected due to performance overhead and less direct programmatic control.

### 2. Signature and Expected Output of the Refactored `retrieve` Function

-   **Decision**: The consolidated `retrieve` function will have the following signature and output:
    ```python
    # Example signature and return type
    from typing import List, Dict, Any

    def retrieve_chunks(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
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
        embedding = get_query_embedding(query) # from retrieving.py
        if not embedding:
            return []

        search_results = search_qdrant(embedding, top_k=top_k) # from retrieving.py
        if not search_results:
            return []

        formatted_results = format_results(search_results) # from retrieving.py
        return formatted_results
    ```
-   **Rationale**: This signature provides a clear interface for `agent.py` to get relevant chunks. The output format is directly derived from the existing `format_results` in `retrieving.py`, ensuring consistency.
-   **Alternatives Considered**:
    -   *Returning raw Qdrant results*: Rejected as `agent.py` would then need to handle formatting.
    -   *Returning a custom object*: Rejected for simplicity; dictionary is flexible and common in Python.

### 3. Specific Environment Variables for Cohere and OpenAI Agents SDK

-   **Decision**: The `.env` file should contain the following environment variables:
    -   `COHERE_API_KEY`: Required for Cohere embeddings.
    -   `QDRANT_URL`: URL for the Qdrant vector database.
    -   `QDRANT_API_KEY`: API key for Qdrant authentication.
    -   `OPENAI_API_KEY`: API key for the OpenAI Agents SDK (even when using compatible endpoints).
    -   `OPENAI_BASE_URL`: (Optional but recommended for flexibility) Base URL for OpenAI-compatible API endpoints (e.g., Gemini through OpenRouter). This allows switching between different LLM providers seamlessly.
-   **Rationale**: These variables cover all external service dependencies identified and adhere to best practices for managing sensitive information.
-   **Alternatives Considered**:
    -   *Hardcoding API keys*: Rejected due to severe security implications.
    -   *Passing keys as function arguments*: Rejected as environment variables are standard for global service configurations.

### 4. Internal Agent Output Structure

-   **Decision**: The agent will internally construct a dictionary that directly matches the external API response structure defined in the `spec.md` (FR-009): `{"answer": "...", "sources": [{"id": "...", "metadata": {}}], "chunks": ["..."]}`.
-   **Rationale**: By aligning the internal and external structures, the transition to FastAPI (in a later phase) will be seamless, requiring minimal data transformation at the API layer. This simplifies testing and ensures consistency.
-   **Alternatives Considered**:
    -   *Using a different internal structure*: Rejected as it would necessitate an additional mapping step when preparing the final response, adding unnecessary complexity.

## Phase 0 Completion

All initial unknowns and clarifications from the technical context have been researched and documented above. The `plan.md` has been updated with these findings.
