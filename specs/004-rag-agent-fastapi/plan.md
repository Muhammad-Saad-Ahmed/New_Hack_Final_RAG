# Implementation Plan: RAG Agent using OpenAI Agents SDK

**Branch**: `004-rag-agent-fastapi` | **Date**: 2025-12-26 | **Spec**: [specs/004-rag-agent-fastapi/spec.md](specs/004-rag-agent-fastapi/spec.md)
**Input**: Feature specification from `/specs/004-rag-agent-fastapi/spec.md`

## Summary

The primary requirement is to build a RAG agent capable of processing user queries, retrieving information from Qdrant, and generating answers using OpenAI Agents SDK. The technical approach involves implementing the agent in Python using the OpenAI Agents SDK, leveraging Cohere for embeddings, and Qdrant for vector retrieval. It will integrate with an existing `retrieving.py` file for retrieval logic. This phase focuses solely on the agent's core logic and retrieval integration, independent of FastAPI, which will be integrated in a later stage.

## Technical Context

**Language/Version**: Python 3.9+
**Primary Dependencies**: OpenAI Agents SDK, Cohere API (for embeddings), Qdrant Client, dependencies of `retrieving.py`.
**Storage**: Qdrant (vector store).
**Testing**: `pytest` (standard for Python projects).
**Target Platform**: Linux server (standard for backend services).
**Project Type**: Single backend component (`agent.py`).
**Performance Goals**: Average p95 response time for a query under 8 seconds.
**Constraints**:
- Output format must conform to the specified JSON structure (`{"answer": "...", "sources": [{"id": "...", "metadata": {}}], "chunks": ["..."]}`).
- API keys and base URLs for 3rd party APIs will be sourced from environment variables (e.g., `.env` file).
- The `retrieve` function from `retrieving.py` must be used for retrieval.
- No FastAPI implementation in this phase.
**Scale/Scope**: Focus on core RAG agent logic and retrieval integration.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

-   **I. Technical Accuracy**: Adheres to using OpenAI Agents, Cohere, and Qdrant.
-   **V. Separation of Concerns**: Agent logic is separated from potential FastAPI integration (for this phase), aligning with this principle.
-   **VII. Spec-Kit Plus Workflow**: Following the defined workflow.
-   **VIII. Defined Tech Stack**:
    -   **Violation**: The constitution specifies FastAPI as part of the RAG system, but this phase explicitly excludes FastAPI.
    -   **Justification**: This is a deliberate, incremental approach to focus on the core RAG agent and retrieval logic first. FastAPI integration will be a subsequent phase, allowing for modular development and easier testing of the agent's core functionality. Neon Postgres (also in constitution) is for the ingestion pipeline and not directly relevant to this agent development phase.

## Project Structure

### Documentation (this feature)

```text
specs/004-rag-agent-fastapi/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── main.py
├── requirements.txt
├── retrieving.py
└── agent.py # New file to contain the core RAG agent logic
```

**Structure Decision**: The "Single project" structure is adapted, with the new `agent.py` file placed within the existing `backend/` directory alongside `retrieving.py`, maintaining a logical grouping of backend components. This choice aligns with the project's current structure for backend services.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Exclusion of FastAPI in this phase | Focus on incremental development and core agent logic. Facilitates isolated testing of the RAG agent before API exposure. | Including FastAPI now would add unnecessary complexity to the initial development and debugging of the core RAG logic. |