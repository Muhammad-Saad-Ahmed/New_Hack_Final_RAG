---

description: "Task list for RAG Agent using OpenAI Agents SDK"
---

# Tasks: RAG Agent using OpenAI Agents SDK

**Input**: Design documents from `/specs/004-rag-agent-fastapi/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 [P] Create `.env` file template in `backend/` (or project root based on `load_dotenv` config) for API keys and update `backend/requirements.txt` with necessary packages (`cohere`, `qdrant-client`, `openai`, `python-dotenv`).
- [X] T002 [P] Implement the `retrieve_chunks` function within `backend/retrieving.py` that encapsulates query embedding, Qdrant search, and result formatting, as defined in `research.md`.
  - This function should take a `query` string and `top_k` integer, and return `List[Dict[str, Any]]`.
  - It should leverage existing `get_query_embedding`, `search_qdrant`, and `format_results` functions from `backend/retrieving.py`.

## Phase 2: Core Agent Logic (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T003 Create `backend/agent.py` to house the core RAG agent logic.
- [X] T004 Implement agent initialization in `backend/agent.py`, including loading environment variables from `.env` and setting up OpenAI Agents SDK with `OPENAI_API_KEY` and `OPENAI_BASE_URL`.
- [X] T005 Define the agent's main processing function (e.g., `ask_agent`) in `backend/agent.py` that accepts a user `query` string and returns the agent's response.

## Phase 3: User Story 1 - Successful Query (Priority: P1) 🎯 MVP

**Goal**: The RAG agent can process a valid query and return a structured JSON response.

**Independent Test**: Call the `ask_agent` function with a sample query (e.g., "What is ROS 2 architecture?") and verify that it returns a JSON object conforming to `{"answer": "...", "sources": [{"id": "...", "metadata": {}}], "chunks": ["..."]}` with meaningful content.

### Implementation for User Story 1

- [X] T006 [US1] Integrate `retrieve_chunks` from `backend/retrieving.py` into the agent's processing flow in `backend/agent.py` to get relevant document chunks.
- [X] T007 [US1] Feed the retrieved `chunks` and the original `query` to the OpenAI Agents SDK to generate an `answer`.
- [X] T008 [US1] Construct the final response object within `backend/agent.py` according to the specified JSON structure (`{"answer": "...", "sources": [{"id": "...", "metadata": {}}], "chunks": ["..."]}`), mapping retrieved chunks and their metadata to `sources` and `chunks` fields.
- [X] T009 [P] [US1] Add a command-line interface (CLI) to `backend/agent.py` to accept a query as an argument and print the JSON response to `stdout`.

## Phase 4: User Story 2 - Invalid Input Handling (Priority: P2)

**Goal**: The RAG agent handles missing or empty queries gracefully, returning a structured error.

**Independent Test**: Call the `ask_agent` function with empty strings, `None`, or whitespace-only strings as the query and verify that it returns the is required."}}`.

## Phase 5: User Story 3 - No Results Found (Priority: P3)

**Goal**: The RAG agent responds appropriately when no relevant documents are found from Qdrant.

**Independent Test**: Call the `ask_agent` function with a query known to yield no results from Qdrant (e.g., a query about a completely unrelated topic) and verify that it returns the specified "no results" JSON response: `{"answer": "I could not find an answer to your question.", "sources": [], "chunks": []}`.

### Implementation for User Story 3

- [X] T012 [US3] Modify the `ask_agent` function in `backend/agent.py` to detect when `retrieve_chunks` returns an empty list (indicating no relevant documents were found).
- [X] T013 [US3] If no chunks are retrieved, construct and return the specified "no results" JSON response: `{"answer": "I could not find an answer to your question.", "sources": [], "chunks": []}`.

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and overall system quality.

- [X] T014 [P] Update `quickstart.md` in `specs/004-rag-agent-fastapi/` with final instructions to set up the `.env` file and run the `agent.py` script via CLI.
- [X] T015 [P] Add robust error handling and logging within `backend/agent.py` for all API calls (Cohere, OpenAI) and unexpected runtime issues, ensuring informative error messages without exposing sensitive details.
- [X] T016 [P] Create unit tests for the `retrieve_chunks` function in `backend/tests/test_retrieving.py` to ensure correct embedding generation, Qdrant search, and result formatting, including edge cases (empty query, no results from Qdrant).
- [X] T017 [P] Create unit tests for `backend/agent.py` (e.g., `backend/tests/test_agent.py`) covering query validation, successful response generation, and the "no results found" scenario, possibly using mocks for external API calls.
- [X] T018 Run `quickstart.md` validation to ensure all steps are accurate and reflect the current state of `agent.py`.

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Core Agent Logic (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Core Agent Logic phase completion.
  - User stories can then proceed in parallel (if staffed) or sequentially in priority order (P1 → P2 → P3).
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Core Agent Logic (Phase 2) - No dependencies on other stories.
- **User Story 2 (P2)**: Can start after Core Agent Logic (Phase 2) - No dependencies on other stories.
- **User Story 3 (P3)**: Can start after Core Agent Logic (Phase 2) - No dependencies on other stories.

### Within Each User Story

- Tests MUST be considered and ideally written (and fail) before implementation begins for that task.
- Core logic before edge cases.

### Parallel Opportunities

- All tasks marked [P] can run in parallel.
- Once Core Agent Logic phase completes, all user stories can start in parallel (if team capacity allows).
- Tests and implementation tasks for different components (e.g., `retrieving.py` tests and `agent.py` implementation) can often run in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Core Agent Logic (CRITICAL - blocks all stories).
3. Complete Phase 3: User Story 1.
4. **STOP and VALIDATE**: Test User Story 1 independently using the CLI.
5. Deploy/demo if ready.

### Incremental Delivery

1. Complete Setup + Core Agent Logic → Foundation ready.
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!).
3. Add User Story 2 → Test independently → Deploy/Demo.
4. Add User Story 3 → Test independently → Deploy/Demo.
5. Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Core Agent Logic together.
2. Once Core Agent Logic is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently.

---

## Notes

- [P] tasks = different files, no dependencies.
- [Story] label maps task to specific user story for traceability.
- Each user story should be independently completable and testable.
- Verify tests fail before implementing.
- Commit after each task or logical group.
- Stop at any checkpoint to validate story independently.
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence.