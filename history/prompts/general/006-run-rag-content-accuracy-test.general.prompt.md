---
id: 6
title: Run RAG content accuracy test
stage: general
date_iso: 2025-12-25
surface: agent
model: gemini-1.5-pro
feature: 003-rag-retrieval-testing
branch: main
user: Admin
command: python backend/retrieving.py --test-accuracy
labels: ["rag", "retrieval", "testing", "content-accuracy"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - backend/retrieving.py
  - specs/003-rag-retrieval-testing/tasks.md
tests_yaml:
  - T022
prompt_text: |
  python backend/retrieving.py --test-accuracy
response_text: |
  The content accuracy test (`python backend/retrieving.py --test-accuracy`) ran successfully.
  The output shows:
  -   `Cosine Similarity (Original vs. Modified): 0.8094`
  -   `Cosine Similarity (Original vs. Dissimilar): 0.1919`
  -   `Content accuracy test PASSED: Modified text is more similar to original than dissimilar text.`

  This indicates that the `calculate_cosine_similarity` function and the content accuracy test are working as expected. The similarity score for the modified text is significantly higher than for the dissimilar text, which is the desired outcome.
outcome: success
evaluation: The RAG content accuracy test was run and passed successfully.
---