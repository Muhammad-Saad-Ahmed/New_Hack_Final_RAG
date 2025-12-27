# Quickstart Guide: RAG Agent UI Integration

## Prerequisites
- Node.js 18+ for frontend development
- Python 3.11+ for backend development
- Docusaurus CLI installed globally
- Backend services running (FastAPI, Qdrant)

## Setup Backend
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the backend server:
   ```bash
   uvicorn main:app --reload
   ```

## Setup Frontend
1. Navigate to the Docusaurus directory:
   ```bash
   cd Docusaurus-Book
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## Running Both Services
For development, you'll need both services running simultaneously. You can use a tool like `concurrently` or run them in separate terminals.

## Testing the Integration
1. The RAG chat UI will appear as a floating widget in the bottom-right corner of the Docusaurus site
2. Type a question in the input field and submit it
3. The system will call the backend `/ask` endpoint and display the response with sources and text chunks
4. Loading states and error handling will be displayed appropriately

## Configuration
The frontend will make API calls to `http://localhost:8000/ask` by default. This can be configured via environment variables if needed for different deployment environments.