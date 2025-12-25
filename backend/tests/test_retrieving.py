import pytest
from unittest.mock import patch, MagicMock
from backend.retrieving import retrieve_chunks # Assuming retrieve_chunks is correctly imported

# Mock the external dependencies
@pytest.fixture
def mock_get_query_embedding():
    with patch('backend.retrieving.get_query_embedding') as mock:
        yield mock

@pytest.fixture
def mock_search_qdrant():
    with patch('backend.retrieving.search_qdrant') as mock:
        yield mock

@pytest.fixture
def mock_format_results():
    with patch('backend.retrieving.format_results') as mock:
        yield mock

# Test cases for retrieve_chunks function
def test_retrieve_chunks_success(mock_get_query_embedding, mock_search_qdrant, mock_format_results):
    """
    Test successful retrieval of chunks.
    """
    mock_get_query_embedding.return_value = [0.1, 0.2, 0.3] # Sample embedding
    mock_search_qdrant.return_value = ["qdrant_result_1", "qdrant_result_2"] # Sample Qdrant results
    mock_format_results.return_value = [
        {"id": "1", "payload": {"text": "chunk 1"}},
        {"id": "2", "payload": {"text": "chunk 2"}}
    ] # Sample formatted results

    query = "test query"
    result = retrieve_chunks(query)

    mock_get_query_embedding.assert_called_once_with(query)
    mock_search_qdrant.assert_called_once_with([0.1, 0.2, 0.3], top_k=5)
    mock_format_results.assert_called_once_with(["qdrant_result_1", "qdrant_result_2"])
    assert len(result) == 2
    assert result[0]["payload"]["text"] == "chunk 1"
    assert result[1]["payload"]["text"] == "chunk 2"

def test_retrieve_chunks_empty_query(mock_get_query_embedding, mock_search_qdrant, mock_format_results):
    """
    Test with an empty query, should return an empty list.
    """
    query = ""
    result = retrieve_chunks(query)

    mock_get_query_embedding.assert_called_once_with(query)
    mock_search_qdrant.assert_not_called()
    mock_format_results.assert_not_called()
    assert result == []

def test_retrieve_chunks_no_embedding(mock_get_query_embedding, mock_search_qdrant, mock_format_results):
    """
    Test case where embedding generation fails (returns None).
    """
    mock_get_query_embedding.return_value = None
    query = "test query"
    result = retrieve_chunks(query)

    mock_get_query_embedding.assert_called_once_with(query)
    mock_search_qdrant.assert_not_called()
    mock_format_results.assert_not_called()
    assert result == []

def test_retrieve_chunks_no_qdrant_results(mock_get_query_embedding, mock_search_qdrant, mock_format_results):
    """
    Test case where Qdrant search returns no results (empty list or None).
    """
    mock_get_query_embedding.return_value = [0.1, 0.2, 0.3]
    mock_search_qdrant.return_value = [] # No Qdrant results
    query = "test query"
    result = retrieve_chunks(query)

    mock_get_query_embedding.assert_called_once_with(query)
    mock_search_qdrant.assert_called_once_with([0.1, 0.2, 0.3], top_k=5)
    mock_format_results.assert_not_called() # format_results should not be called with empty list
    assert result == []

def test_retrieve_chunks_exception_in_embedding(mock_get_query_embedding, mock_search_qdrant, mock_format_results):
    """
    Test case where an exception occurs during embedding generation.
    """
    mock_get_query_embedding.side_effect = Exception("Cohere error")
    query = "test query"
    result = retrieve_chunks(query)

    mock_get_query_embedding.assert_called_once_with(query)
    mock_search_qdrant.assert_not_called()
    mock_format_results.assert_not_called()
    assert result == []

def test_retrieve_chunks_exception_in_qdrant_search(mock_get_query_embedding, mock_search_qdrant, mock_format_results):
    """
    Test case where an exception occurs during Qdrant search.
    """
    mock_get_query_embedding.return_value = [0.1, 0.2, 0.3]
    mock_search_qdrant.side_effect = Exception("Qdrant connection error")
    query = "test query"
    result = retrieve_chunks(query)

    mock_get_query_embedding.assert_called_once_with(query)
    mock_search_qdrant.assert_called_once_with([0.1, 0.2, 0.3], top_k=5)
    mock_format_results.assert_not_called()
    assert result == []

def test_retrieve_chunks_custom_top_k(mock_get_query_embedding, mock_search_qdrant, mock_format_results):
    """
    Test that custom top_k value is passed correctly.
    """
    mock_get_query_embedding.return_value = [0.1, 0.2, 0.3]
    mock_search_qdrant.return_value = ["qdrant_result_1"]
    mock_format_results.return_value = [{"id": "1", "payload": {"text": "chunk 1"}}]

    query = "test query"
    top_k = 3
    result = retrieve_chunks(query, top_k=top_k)

    mock_get_query_embedding.assert_called_once_with(query)
    mock_search_qdrant.assert_called_once_with([0.1, 0.2, 0.3], top_k=top_k)
    mock_format_results.assert_called_once()
    assert len(result) == 1
