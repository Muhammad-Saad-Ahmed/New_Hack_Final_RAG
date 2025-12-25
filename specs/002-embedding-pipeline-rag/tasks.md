# Tasks: Embedding Pipeline Setup

**Feature**: `Embedding Pipeline Setup`
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

This document breaks down the work required to implement the RAG ingestion pipeline.

## Phase 1: Project Setup

- [X] T001 Create the `backend` directory for the Python script and related files.
- [X] T002 Create an empty `backend/main.py` file.
- [X] T003 Create a `backend/requirements.txt` file and add the required dependencies: `cohere`, `qdrant-client`, `requests`, `beautifulsoup4`, `lxml`, `python-dotenv`, and `uv`.
- [X] T004 Create a `.env` file in the project root for storing API keys (`COHERE_API_KEY`, `QDRANT_URL`, `QDRANT_API_KEY`).
- [X] T005 Add `.env` to the root `.gitignore` file to prevent committing secrets.

## Phase 2: Foundational Code

- [X] T006 [P] In `backend/main.py`, implement loading of environment variables from the `.env` file using `python-dotenv`.
- [X] T007 [P] In `backend/main.py`, initialize the Cohere client using the `COHERE_API_KEY`.
- [X] T008 [P] In `backend/main.py`, initialize the Qdrant client using the `QDRANT_URL` and `QDRANT_API_KEY`.
- [X] T009 In `backend/main.py`, create the Qdrant collection `RAG-DATA` if it doesn't already exist.

## Phase 3: User Story 1 - Index Docusaurus Site

**Goal**: Automate the extraction, embedding, and storage of text content from Docusaurus sites.

**Independent Test Criteria**: Provide a Docusaurus site URL. Verify that text content and vectors are correctly stored in the Qdrant collection.

### Implementation Tasks

- [X] T010 [US1] In `backend/main.py`, implement a function `fetch_sitemap_urls(sitemap_url)` that fetches the `sitemap.xml` and returns a list of URLs.
- [X] T011 [US1] In `backend/main.py`, implement a function `fetch_page_content(url)` that takes a URL and returns the cleaned text content using `requests` and `beautifulsoup4`.
- [X] T012 [US1] In `backend/main.py`, implement a function `chunk_text(text)` that splits the text into fixed-size chunks with overlap as defined in the spec.
- [X] T013 [US1] In `backend/main.py`, implement a function `generate_embeddings(chunks)` that uses the Cohere client to generate embeddings for a list of text chunks.
- [X] T014 [US1] In `backend/main.py`, implement a function `store_in_qdrant(chunks, vectors)` that upserts the text chunks, their embeddings, and metadata (source URL, page title, section title) into the Qdrant collection.
- [X] T015 [US1] In `backend/main.py`, implement the main orchestration logic that:
    1. Fetches URLs from the sitemap.
    2. Iterates through each URL, fetching and chunking the content.
    3. Generates embeddings for the chunks.
    4. Stores the results in Qdrant.
- [X] T016 [US1] Integrate logging throughout the script to report progress and errors.
- [X] T017 [US1] Implement error handling, including retries for failed HTTP requests, and logging for URLs that fail processing.

## Phase 4: Polish & Documentation

- [X] T018 Add detailed comments and docstrings to all functions in `backend/main.py`.
- [X] T019 Create a `backend/README.md` that explains how to set up and run the ingestion script, based on the `quickstart.md`.

## Dependencies

- **Phase 2** depends on **Phase 1**.
- **Phase 3** depends on **Phase 2**.
- **Phase 4** depends on **Phase 3**.

All user story tasks ([US1]) can be worked on after Phase 2 is complete.

## Parallel Execution

- Within Phase 2, tasks T006, T007, and T008 can be developed in parallel.
- Within Phase 3, once the main orchestration loop is stubbed out, the core functions (T010-T014) can be developed and tested in parallel by different team members using mock data.
