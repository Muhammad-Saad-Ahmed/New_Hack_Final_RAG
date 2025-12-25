import argparse
import requests
import json

FASTAPI_RETRIEVE_URL = "http://127.0.0.1:8001/retrieve"

def retrieve_from_fastapi(query: str, top_k: int = 5):
    """
    Makes a POST request to the FastAPI /retrieve endpoint with the given query.
    """
    headers = {"Content-Type": "application/json"}
    payload = {"query": query, "top_k": top_k}
    try:
        response = requests.post(FASTAPI_RETRIEVE_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to FastAPI service: {e}")
        print("Please ensure the FastAPI server is running (uvicorn backend.main:app --reload)")
        return None

def main():
    parser = argparse.ArgumentParser(description="Agent for querying the RAG FastAPI service.")
    parser.add_argument("--query", type=str, required=True, help="The query string to send to the RAG service.")
    parser.add_argument("--top_k", type=int, default=5, help="The number of top results to retrieve.")
    
    args = parser.parse_args()

    print(f"Sending query to FastAPI RAG service: '{args.query}' (top_k: {args.top_k})")
    results = retrieve_from_fastapi(args.query, args.top_k)

    if results:
        print("\nRetrieval Results:")
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
