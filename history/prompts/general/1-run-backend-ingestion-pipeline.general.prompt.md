---
id: 1
title: Run Backend Ingestion Pipeline
stage: general
date_iso: 2025-12-28
surface: agent
model: gemini
feature: none
branch: main
user:
  command: python main.py
  labels: ["backend", "ingestion", "pipeline", "qdrant"]
  links:
    spec: null
    ticket: null
    adr: null
    pr: null
files_yaml:
  - backend/main.py
tests_yaml: []
prompt_text: |
  python main.py
response_text: |
  The `python main.py` command executed successfully. The output shows that the Docusaurus Embedding Pipeline started, processed URLs from `https://new-hack-final-rag-kvxh.vercel.app/`, created chunks, embedded them using Cohere, and saved them to the Qdrant collection named `New-Rag-Data`.

  The script seems to have completed its ingestion process.
outcome: success
---
