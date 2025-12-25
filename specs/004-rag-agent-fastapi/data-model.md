# Data Model: RAG Agent with OpenAI Agents SDK

**Feature Branch**: `004-rag-agent-fastapi`
**Date**: 2025-12-26

## Key Entities

### 1. Query

-   **Description**: Represents the user's input question to the RAG agent.
-   **Attributes**:
    -   `text`: `string`
        -   The actual text of the question.

### 2. Response

-   **Description**: Represents the structured output returned by the RAG agent after processing the query and retrieving information. This structure directly aligns with the external API response defined in the feature specification (FR-009).
-   **Attributes**:
    -   `answer`: `string`
        -   The generated answer to the user's query.
    -   `sources`: `Array<Source>`
        -   A list of `Source` objects that were used to formulate the answer. Each source provides metadata about the retrieved document.
    -   `chunks`: `Array<string>`
        -   A list of the raw text chunks that were retrieved from the vector store and used by the agent.

### 3. Source

-   **Description**: Represents a single source document or a part of a document that contributed to the agent's answer. This is derived from the payload returned by Qdrant.
-   **Attributes**:
    -   `id`: `string`
        -   A unique identifier for the source document (e.g., Qdrant point ID).
    -   `metadata`: `object`
        -   A dictionary or object containing additional metadata about the source (e.g., `title`, `url`, `page_number`). The exact structure of metadata is dependent on what was indexed in Qdrant.

## Relationships

-   A `Response` contains an `answer` (string), a list of `Source` objects, and a list of `chunks` (strings).
-   `Source` objects are populated based on the `payload` received from Qdrant search results.
-   `chunks` are typically the `text` attribute within the `payload` of each `Source`.
