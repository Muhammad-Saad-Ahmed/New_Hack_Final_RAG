import argparse
import requests
import json
import asyncio
import os # New import
from dotenv import load_dotenv # New import

from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, AsyncOpenAI

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env')) # New line




FASTAPI_RETRIEVE_URL = "http://127.0.0.1:8001/retrieve"

@function_tool
def retrieve_from_fastapi_tool(query: str, top_k: int = 3) -> str:
    """
    Retrieves relevant information from the RAG FastAPI service based on a query.

    Args:
        query (str): The search query string.
        top_k (int): The number of top results to retrieve.

    Returns:
        str: A JSON string of the retrieval results, or an error message.
    """
    headers = {"Content-Type": "application/json"}
    payload = {"query": query, "top_k": top_k}
    try:
        response = requests.post(FASTAPI_RETRIEVE_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        return json.dumps(response.json(), indent=2)
    except requests.exceptions.RequestException as e:
        return f"Error connecting to FastAPI service: {e}. Please ensure the FastAPI server is running (uvicorn backend.main:app --reload) and accessible at {FASTAPI_RETRIEVE_URL}"

def main():
    parser = argparse.ArgumentParser(description="Agent for querying the RAG FastAPI service.")
    parser.add_argument("--query", type=str, required=True, help="The query string to send to the RAG service.")
    parser.add_argument("--top_k", type=int, default=5, help="The number of top results to retrieve.")
    
    args = parser.parse_args()

    # Old direct call
    # print(f"Sending query to FastAPI RAG service: '{args.query}' (top_k: {args.top_k})")
    # results = retrieve_from_fastapi(args.query, args.top_k)

    # if results:
    #     print("\nRetrieval Results:")
    #     print(json.dumps(results, indent=2))

    # New agent-based execution
    async def run_agent():
        agent = Agent(
            name="RAG Assistant",
            instructions="You are a helpful RAG assistant. Your primary goal is to answer user questions by retrieving information using the 'retrieve_from_fastapi_tool'. When a user asks a question, use this tool to get relevant information, then summarize or present the findings concisely.",
            tools=[retrieve_from_fastapi_tool],
            model=OpenAIChatCompletionsModel(
                model="gpt-4o",
                openai_client=AsyncOpenAI()
            )
        )
        result = await Runner.run(agent, f"User query: {args.query}")
        
        print("\nAgent's Final Output:")
        print(result.final_output)

    try:
        asyncio.run(run_agent())
    except Exception as e:
        import traceback
        print(f"\nAn error occurred during agent execution: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()

