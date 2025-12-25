# Quickstart: RAG Ingestion Pipeline

**Date**: 2025-12-25
**Feature**: [Embedding Pipeline Setup](../spec.md)

This guide explains how to set up and run the backend script to ingest content into the Qdrant vector database.

## 1. Prerequisites

- Python 3.11+
- `uv` installed (`pip install uv`)

## 2. Setup

### a. Create a Virtual Environment

From the project root directory, navigate to the `backend` folder and create a virtual environment.

```bash
cd backend
uv venv
```

### b. Activate the Environment

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
source .venv/bin/activate
```

### c. Install Dependencies

Install the required Python packages.

```bash
uv pip install -r requirements.txt
```

### d. Configure Environment Variables

The script requires API keys for Cohere and Qdrant. Create a `.env` file in the `backend` directory and add the following:

```env
# .env file

# Cohere API Key
COHERE_API_KEY="your_cohere_api_key_here"

# Qdrant Configuration
QDRANT_URL="your_qdrant_cloud_url_or_localhost"
QDRANT_API_KEY="your_qdrant_api_key_if_applicable"
```

## 3. Running the Script

Execute the `main.py` script to start the ingestion process.

```bash
python main.py
```

The script will fetch URLs from the sitemap, process each page, and upsert the text chunks and embeddings into your Qdrant collection named `RAG-DATA`.
