# Data Model: RAG Agent UI Integration

## Entities

### Question
- **Fields**:
  - `id`: string (auto-generated unique identifier)
  - `text`: string (the user's question text)
  - `timestamp`: datetime (when the question was submitted)
  - `userId`: string (optional, for tracking purposes)

- **Validation**:
  - `text` must be 1-1000 characters
  - `text` must not be empty or whitespace only

### Answer
- **Fields**:
  - `id`: string (auto-generated unique identifier)
  - `questionId`: string (reference to the original question)
  - `text`: string (the RAG-generated answer)
  - `confidence`: number (confidence score, 0-1)
  - `timestamp`: datetime (when the answer was generated)
  - `sources`: array of Source objects
  - `textChunks`: array of TextChunk objects

- **Validation**:
  - `text` must not be empty
  - `confidence` must be between 0 and 1
  - `sources` and `textChunks` can be empty arrays

### Source
- **Fields**:
  - `id`: string (unique identifier for the source)
  - `url`: string (URL of the source document)
  - `title`: string (title of the source)
  - `documentId`: string (ID in the vector database)

- **Validation**:
  - `url` must be a valid URL format
  - `title` must not be empty

### TextChunk
- **Fields**:
  - `id`: string (unique identifier for the chunk)
  - `content`: string (the actual text content)
  - `sourceId`: string (reference to the source)
  - `similarityScore`: number (similarity to the original question, 0-1)

- **Validation**:
  - `content` must not be empty
  - `similarityScore` must be between 0 and 1

## Relationships
- One Question can have one Answer (1:1)
- One Answer can have multiple Sources (1:many)
- One Answer can have multiple TextChunks (1:many)
- One Source can be associated with multiple TextChunks (1:many)