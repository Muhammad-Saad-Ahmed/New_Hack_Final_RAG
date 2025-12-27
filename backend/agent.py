import argparse
import json
import asyncio
import os
import httpx  # Use httpx for async requests
from dotenv import load_dotenv

from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, AsyncOpenAI

# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# --- LLM Configuration ---
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASEURL = os.getenv("LLM_BASEURL")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash-latest")

if not LLM_API_KEY:
    raise ValueError("LLM_API_KEY environment variable is not set. Please add it to your .env file.")

# --- Tool Definition ---
FASTAPI_RETRIEVE_URL = "http://127.0.0.1:8000/retrieve"

@function_tool
async def retrieve_from_fastapi_tool(query: str, top_k: int = 3) -> str:
    """
    Retrieves relevant information from the RAG FastAPI service based on a query.
    Uses httpx for asynchronous requests.
    """
    headers = {"Content-Type": "application/json"}
    payload = {"query": query, "top_k": top_k}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(FASTAPI_RETRIEVE_URL, headers=headers, json=payload)
            response.raise_for_status()
            return json.dumps(response.json(), indent=2)
    except httpx.RequestError as e:
        return f"Error connecting to FastAPI service: {e}. Please ensure the FastAPI server is running."
    except Exception as e:
        return f"An unexpected error occurred in retrieve_from_fastapi_tool: {e}"

# --- RAG Agent Class ---
class RAGAgent:
    def __init__(self):
        """
        Initializes the RAGAgent, setting up the LLM provider, model, and the agent itself.
        """
        self.provider = LLM_PROVIDER
        self.model_name = LLM_MODEL
        self.base_url = LLM_BASEURL
        self.api_key = LLM_API_KEY
        
        headers = self._get_provider_headers()
        
        if not self.base_url:
            raise ValueError("LLM_BASEURL is not set for the selected provider and no default is available.")

        print(f"Using LLM Provider: {self.provider}")
        print(f"Using LLM Model: {self.model_name}")
        print(f"Using Base URL: {self.base_url}")

        external_client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            default_headers=headers
        )
        
        external_model = OpenAIChatCompletionsModel(
            model=self.model_name,
            openai_client=external_client
        )

        self.agent = Agent(
            name="RAG Assistant",
            instructions=(
                "You are a helpful RAG assistant. Your primary goal is to answer user questions "
                "by retrieving information using the 'retrieve_from_fastapi_tool'. When a user asks a question, "
                "use this tool to get relevant information, then summarize or present the findings concisely."
            ),
            tools=[retrieve_from_fastapi_tool],
            model=external_model
        )

    def _get_provider_headers(self):
        """Builds the necessary headers based on the LLM provider."""
        if self.provider == "gemini":
            self.base_url = self.base_url or "https://generativelanguage.googleapis.com/v1beta/openai/"
            return {
                "x-goog-api-key": self.api_key,
                "x-goog-api-client": "agents-library"
            }
        elif self.provider == "openrouter":
            return {
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": "https://github.com/leeway-press/spec-driven-development", 
                "X-Title": "Spec-Driven Development"
            }
        elif self.provider == "qwen":
            self.base_url = self.base_url or "https://dashscope.aliyuncs.com/compatible-mode/v1"
            return {"Authorization": f"Bearer {self.api_key}"}
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    async def query_agent(self, query: str):
        """
        Runs the agent with a given user query and returns the final output.
        """
        result = await Runner.run(self.agent, f"User query: {query}")
        return result.final_output

# --- Main execution block for CLI ---
def main():
    parser = argparse.ArgumentParser(description="Agent for querying the RAG FastAPI service.")
    parser.add_argument("--query", type=str, required=True, help="The query string to send to the RAG service.")
    
    args = parser.parse_args()

    async def run_cli_query():
        try:
            print("Initializing RAGAgent for CLI query...")
            rag_agent = RAGAgent()
            print(f"Sending query to RAG Agent: '{args.query}'")
            final_output = await rag_agent.query_agent(args.query)
            
            print("\nAgent's Final Output:")
            print(final_output)
            
        except Exception as e:
            import traceback
            print(f"\nAn error occurred during agent execution: {e}")
            traceback.print_exc()

    asyncio.run(run_cli_query())

if __name__ == "__main__":
    main()

