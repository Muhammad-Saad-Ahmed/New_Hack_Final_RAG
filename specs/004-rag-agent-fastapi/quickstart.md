# Quickstart Guide: RAG Agent with OpenAI Agents SDK

**Feature Branch**: `004-rag-agent-fastapi`
**Date**: 2025-12-26

This guide provides instructions to set up the environment and run the core RAG agent (`agent.py`) for testing and development purposes.

## 1. Environment Setup

### Create `.env` file

Create a file named `.env` in the **project root directory** with the following variables. Replace the placeholder values with your actual API keys and service URLs.

```
COHERE_API_KEY=your_cohere_api_key_here
QDRANT_URL=your_qdrant_instance_url_here # e.g., https://<cluster_id>.qdrant.tech
QDRANT_API_KEY=your_qdrant_api_key_here
OPENAI_API_KEY=your_openai_or_compatible_api_key_here
OPENAI_BASE_URL=your_openai_compatible_api_base_url_here # e.g., https://api.openrouter.ai/api/v1 (optional, for custom endpoints)
```

**Note**: Ensure your `.env` file is properly configured and loaded by your application (e.g., using `python-dotenv`).

### Install Dependencies

Navigate to the `backend/` directory and install the required Python packages.

```bash
cd backend/
pip install -r requirements.txt
```
**Make sure `backend/requirements.txt` includes the necessary dependencies: `cohere-ai`, `qdrant-client`, `openai`, `python-dotenv`.**

## 2. Running the RAG Agent

The `agent.py` script will be designed to accept a query and output the RAG response to standard output.

### Example Usage

To run the agent with a sample query:

```bash
python backend/agent.py "What is ROS 2 architecture?"
```

### Expected Output

The script should output a JSON object to the console, similar to the following:

```json
{
  "answer": "ROS 2 architecture involves several key concepts such as nodes, topics, services, actions, and parameters...",
  "sources": [
    {
      "id": "some-unique-doc-id-1",
      "metadata": {
        "title": "What is ROS 2",
        "chapter": "01-what-is-ros2",
        "page_number": 5
      }
    },
    {
      "id": "another-doc-id-2",
      "metadata": {
        "title": "ROS 2 Architecture",
        "chapter": "02-architecture",
        "url": "https://example.com/ros2-architecture"
      }
    }
  ],
  "chunks": [
    "ROS 2 uses a decentralized architecture where individual components called nodes communicate...",
    "The Data Distribution Service (DDS) is the middleware used by ROS 2 for communication..."
  ]
}
```

## 3. Testing (Conceptual)

While `agent.py` does not have an HTTP endpoint in this phase, you can test its core functionality by calling its main function directly within a test script or by using the command line as shown above and verifying the JSON output.

**(Note: Specific test instructions will be detailed in the `tasks.md` file.)**
