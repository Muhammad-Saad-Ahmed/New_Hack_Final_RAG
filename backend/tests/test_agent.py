import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from backend.agent import RAGAgent
import openai

# Mock environment variables for testing
@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("COHERE_API_KEY", "test_cohere_key")
    monkeypatch.setenv("QDRANT_URL", "http://localhost:6333")
    monkeypatch.setenv("QDRANT_API_KEY", "test_qdrant_key")
    monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")
    monkeypatch.setenv("OPENAI_BASE_URL", "http://localhost:8000/v1") # Mock base URL if needed

# Mock retrieve_chunks
@pytest.fixture
def mock_retrieve_chunks():
    with patch('backend.agent.retrieve_chunks', new_callable=MagicMock) as mock:
        yield mock

# Mock openai.chat.completions.create
@pytest.fixture
def mock_openai_chat_completions_create():
    with patch('openai.chat.completions.create', new_callable=AsyncMock) as mock:
        # Create a mock response object that has .choices[0].message.content
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock(content="Mocked OpenAI answer.")
        mock.return_value = mock_response
        yield mock

@pytest.mark.asyncio
async def test_ask_agent_empty_query(mock_retrieve_chunks, mock_openai_chat_completions_create):
    """
    Test query validation for empty string. (T010, T011)
    """
    agent = RAGAgent()
    result = await agent.ask_agent("")
    assert result == {
        "error": {
            "code": "missing_input",
            "message": "Query parameter is required."
        }
    }
    mock_retrieve_chunks.assert_not_called()
    mock_openai_chat_completions_create.assert_not_called()

@pytest.mark.asyncio
async def test_ask_agent_whitespace_query(mock_retrieve_chunks, mock_openai_chat_completions_create):
    """
    Test query validation for whitespace-only string. (T010, T011)
    """
    agent = RAGAgent()
    result = await agent.ask_agent("   ")
    assert result == {
        "error": {
            "code": "missing_input",
            "message": "Query parameter is required."
        }
    }
    mock_retrieve_chunks.assert_not_called()
    mock_openai_chat_completions_create.assert_not_called()

@pytest.mark.asyncio
async def test_ask_agent_no_chunks_found(mock_retrieve_chunks, mock_openai_chat_completions_create):
    """
    Test scenario where retrieve_chunks returns an empty list. (T012, T013)
    """
    mock_retrieve_chunks.return_value = []
    agent = RAGAgent()
    query = "query with no results"
    result = await agent.ask_agent(query)
    assert result == {
        "answer": "I could not find an answer to your question.",
        "sources": [],
        "chunks": []
    }
    mock_retrieve_chunks.assert_called_once_with(query)
    mock_openai_chat_completions_create.assert_not_called()

@pytest.mark.asyncio
async def test_ask_agent_successful_response(mock_retrieve_chunks, mock_openai_chat_completions_create):
    """
    Test a successful end-to-end flow.
    """
    sample_chunks = [
        {"id": "doc1", "payload": {"text": "Context for doc1", "title": "Doc One"}},
        {"id": "doc2", "payload": {"text": "Context for doc2", "url": "http://doc2.com"}}
    ]
    mock_retrieve_chunks.return_value = sample_chunks
    
    agent = RAGAgent()
    query = "What is the capital of France?"
    result = await agent.ask_agent(query)

    mock_retrieve_chunks.assert_called_once_with(query)
    mock_openai_chat_completions_create.assert_called_once()
    
    assert result["answer"] == "Mocked OpenAI answer."
    assert result["sources"] == [
        {"id": "doc1", "metadata": {"text": "Context for doc1", "title": "Doc One"}},
        {"id": "doc2", "metadata": {"text": "Context for doc2", "url": "http://doc2.com"}}
    ]
    assert result["chunks"] == ["Context for doc1", "Context for doc2"]

@pytest.mark.asyncio
async def test_ask_agent_openai_api_error(mock_retrieve_chunks, mock_openai_chat_completions_create):
    """
    Test error handling when OpenAI API call fails.
    """
    mock_retrieve_chunks.return_value = [
        {"id": "doc1", "payload": {"text": "Context for doc1"}}
    ]
    mock_openai_chat_completions_create.side_effect = openai.APIError("OpenAI API is down", request=None, body=None)

    agent = RAGAgent()
    query = "some query"
    result = await agent.ask_agent(query)

    assert result["answer"].startswith("An error occurred while generating the answer.")
    assert result["sources"] == [{"id": "doc1", "metadata": {"text": "Context for doc1"}}]
    assert result["chunks"] == ["Context for doc1"]

@pytest.mark.asyncio
async def test_ask_agent_unexpected_error(mock_retrieve_chunks, mock_openai_chat_completions_create):
    """
    Test handling of unexpected errors within ask_agent.
    """
    mock_retrieve_chunks.side_effect = Exception("Some unexpected retrieval error")

    agent = RAGAgent()
    query = "some query"
    result = await agent.ask_agent(query)

    assert result == {
        "error": {
            "code": "internal_server_error",
            "message": "An unexpected internal error occurred."
        }
    }
    mock_retrieve_chunks.assert_called_once_with(query)
    mock_openai_chat_completions_create.assert_not_called()
