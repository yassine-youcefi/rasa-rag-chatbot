# Rasa RAG Chatbot with PDF Knowledge Base

A complete self-hosted Retrieval-Augmented Generation (RAG) chatbot built with Rasa that can answer questions based on uploaded PDF documents.

## 🚀 Features

- **PDF Document Processing**: Upload and process PDF files automatically
- **Intelligent Question Answering**: Ask questions about your documents and get relevant answers
- **Vector Search**: Uses ChromaDB for efficient similarity search
- **Self-Hosted**: Complete Docker-based deployment with no external dependencies
- **RESTful API**: Upload documents and interact with the chatbot via HTTP APIs
- **Persistent Storage**: Documents and conversations are stored locally
- **Real-time Processing**: Background processing of uploaded documents

## 🏗 Architecture

The system consists of 5 Docker services:

1. **Rasa Server**: Main conversational AI service
2. **Action Server**: Custom actions for RAG functionality
3. **PDF Processor**: Handles document upload, text extraction, and embeddings
4. **ChromaDB**: Vector database for document embeddings
5. **Redis**: Caching and session storage

## 📋 Prerequisites

- Docker and Docker Compose installed
- At least 4GB RAM recommended
- 2GB free disk space

## 🛠 Installation & Setup

1. **Clone or Download the project files**

2. **Navigate to the project directory**:
   ```bash
   cd /path/to/rasa
   ```

3. **Build and start all services**:
   ```bash
   docker-compose up --build
   ```

4. **Wait for all services to be ready**:
   - Rasa server: http://localhost:5005
   - PDF processor: http://localhost:8001
   - ChromaDB: http://localhost:8000
   - Redis: localhost:6379

## 🎯 Usage

### 1. Upload PDF Documents

Upload a PDF document using curl:

```bash
curl -X POST "http://localhost:8001/upload-pdf" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/document.pdf"
```

Or using Python:

```python
import requests

url = "http://localhost:8001/upload-pdf"
files = {"file": open("document.pdf", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### 2. Chat with the Bot

#### Via REST API:

```bash
curl -X POST "http://localhost:5005/webhooks/rest/webhook" \
     -H "Content-Type: application/json" \
     -d '{
       "sender": "user1",
       "message": "What does the document say about artificial intelligence?"
     }'
```

#### Via Python:

```python
import requests

def chat_with_bot(message):
    url = "http://localhost:5005/webhooks/rest/webhook"
    data = {
        "sender": "user1",
        "message": message
    }
    response = requests.post(url, json=data)
    return response.json()

# Example usage
response = chat_with_bot("Hello!")
for msg in response:
    print(msg['text'])
```

## 📚 API Endpoints

### Rasa Server (Port 5005)
- `POST /webhooks/rest/webhook` - Send messages to the bot
- `GET /` - Server status

### PDF Processor (Port 8001)
- `POST /upload-pdf` - Upload a PDF document
- `GET /search?query=...` - Search documents
- `GET /documents` - List all uploaded documents
- `GET /status/{file_id}` - Get processing status
- `DELETE /documents/{file_id}` - Delete a specific document
- `DELETE /documents` - Clear all documents
- `GET /health` - Service health check

### ChromaDB (Port 8000)
- `GET /api/v1/heartbeat` - Database health check

## 💬 Supported Commands

The chatbot understands these types of messages:

- **Questions about documents**: "What does the document say about X?"
- **Greetings**: "Hello", "Hi", "Good morning"
- **Document management**: "List documents", "Upload a PDF"
- **Knowledge base**: "Clear all documents"
- **Goodbyes**: "Bye", "Goodbye", "See you later"

## 🔧 Configuration

### Environment Variables

Key configuration options in `.env`:

```bash
# Service ports
RASA_SERVER_PORT=5005
PDF_PROCESSOR_PORT=8001
CHROMA_PORT=8000
REDIS_PORT=6379

# PDF processing
MAX_FILE_SIZE_MB=50
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Search configuration
MAX_SEARCH_RESULTS=5
SIMILARITY_THRESHOLD=0.7
```

### Customization

#### Adding New Intents

1. Edit `rasa/data/nlu.yml` to add training examples
2. Update `rasa/data/stories.yml` and `rasa/data/rules.yml`
3. Create new actions in `actions/actions.py`
4. Update `rasa/domain.yml`
5. Retrain the model:
   ```bash
   docker-compose exec rasa rasa train
   ```

#### Improving Answer Generation

The current implementation uses simple keyword matching. To improve answer quality:

1. **Use OpenAI GPT**: Add OpenAI API integration to `actions/actions.py`
2. **Local LLM**: Deploy a local language model (like Ollama)
3. **Better chunking**: Implement semantic chunking strategies

## 🔍 Monitoring

### Health Checks

Check service health:

```bash
# Overall system health
curl http://localhost:8001/health

# ChromaDB
curl http://localhost:8000/api/v1/heartbeat

# Rasa server
curl http://localhost:5005/
```

### Logs

View logs for debugging:

```bash
# All services
docker-compose logs

# Specific service
docker-compose logs rasa
docker-compose logs pdf-processor
docker-compose logs chroma
```

## 📖 Example Conversation

```
User: Hello!
Bot: Hello! I'm your AI assistant with access to uploaded documents. How can I help you today?

User: What does the document say about machine learning?
Bot: Based on the uploaded documents: Machine learning is a subset of artificial intelligence that focuses on algorithms and statistical models that enable computer systems to improve their performance on a specific task through experience...

📚 Sources: ML_Guide.pdf

User: List documents
Bot: 📚 Uploaded Documents:
✅ ML_Guide.pdf (completed) - 45 chunks
✅ AI_Research.pdf (completed) - 32 chunks

User: Goodbye
Bot: Goodbye! Feel free to ask me anything about your documents anytime.
```

## 🚧 Troubleshooting

### Common Issues

1. **"No relevant documents found"**
   - Ensure PDFs are uploaded and processed (status: completed)
   - Check if your question relates to document content

2. **Services won't start**
   - Check Docker is running: `docker --version`
   - Verify ports aren't in use: `lsof -i :5005`
   - Check logs: `docker-compose logs`

3. **PDF processing fails**
   - Ensure PDF is text-based (not just images)
   - Check file size limits
   - Verify PDF isn't password protected

4. **Memory issues**
   - Increase Docker memory limits
   - Reduce chunk size in configuration
   - Process fewer documents simultaneously

### Performance Optimization

1. **Faster responses**: Reduce `MAX_SEARCH_RESULTS` and `CHUNK_SIZE`
2. **Better accuracy**: Use a larger embedding model
3. **Memory optimization**: Implement document pagination
4. **Scaling**: Use external Redis and ChromaDB instances