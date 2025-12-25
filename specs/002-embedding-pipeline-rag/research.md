# Research: RAG Ingestion Pipeline

**Date**: 2025-12-25
**Feature**: [Embedding Pipeline Setup](../spec.md)

## Decisions

### URL Discovery: `sitemap.xml`
- **Decision**: The system will fetch and parse the `sitemap.xml` file from the root of the target Docusaurus site to discover all URLs for ingestion.
- **Rationale**: The user explicitly requested this method. A `web_fetch` on the target URL (`https://new-hack-final-rag-kvxh.vercel.app/sitemap.xml`) confirms the sitemap is available and contains a standard list of URLs within `<loc>` tags. This is a reliable method for discovering all crawlable pages.
- **Alternatives considered**: Crawling links from the homepage. This is less reliable and more complex than parsing the sitemap.

### Python Package Management: `uv`
- **Decision**: Use `uv` for Python package management.
- **Rationale**: The user specified `uv`. It is a modern, extremely fast package manager and resolver that is a suitable replacement for `pip` and `venv`.
- **Alternatives considered**: Standard `pip` and `venv`. `uv` is a valid and often superior choice.

### Key Libraries
- **Decision**:
  - `requests` for fetching sitemap and page content.
  - `beautifulsoup4` for parsing HTML and extracting text.
  - `lxml` as the parser for `beautifulsoup4` for performance.
  - `cohere` for accessing the embedding API.
  - `qdrant-client` for interacting with the Qdrant vector database.
  - `python-dotenv` for managing environment variables.
- **Rationale**: These are the standard, well-supported libraries for these respective tasks in the Python ecosystem.
