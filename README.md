# 🤖 Rasa RAG Chatbot with PDF Knowledge Base

> **Status: ✅ FULLY OPERATIONAL** - A complete self-hosted Retrieval-Augmented Generation (RAG) chatbot built with Rasa that intelligently answers questions based on your uploaded PDF documents.

## 🌟 Features

- ✅ **Complete Self-Hosted Solution** - No external API dependencies
- ✅ **PDF Document Processing** - Automatic text extraction and intelligent chunking
- ✅ **Vector Search** - ChromaDB for semantic similarity search
- ✅ **Conversational Interface** - Natural language interaction via Rasa
- ✅ **RESTful APIs** - Easy integration with other applications
- ✅ **Persistent Storage** - Documents and embeddings stored locally
- ✅ **Multi-Document Support** - Handle multiple PDFs simultaneously
- ✅ **Real-time Processing** - Background document processing
- ✅ **Source Attribution** - Answers include source document references
- ✅ **Production Ready** - Docker-based deployment with proper error handling

## 🏗 System Architecture

The system consists of 5 Docker services working together:

### Core Services
- **Rasa Core** (Port 5005): Conversational AI engine
- **Action Server** (Port 5055): Custom RAG actions with DeepSeek LLM integration
- **PDF Processor** (Port 8001): Document processing and embedding service
- **ChromaDB** (Port 8000): Vector database for embeddings
- **Redis** (Port 6379): Caching and session storage

### Technologies Stack
- **Rasa 3.6.20-full**: Conversational AI framework
- **ChromaDB 0.4.15**: Vector database for similarity search
- **FastAPI**: PDF processing REST API
- **DeepSeek API**: External LLM for intelligent answer generation
- **sentence-transformers**: Self-hosted embedding models
- **Redis 7**: High-performance caching
- **Docker Compose**: Service orchestration

## 🤖 **AI Models & Integration**

### **Large Language Model (LLM) - DeepSeek API**

Your system uses **DeepSeek's external API** for intelligent answer generation:

**🧠 Model Details:**
- **Provider**: DeepSeek AI (External API)
- **Model**: `deepseek-chat` (configurable)
- **Purpose**: Generate intelligent, context-aware answers
- **Integration**: RESTful API calls (no self-hosting required)
- **Cost**: Pay-per-use API pricing
- **Performance**: High-quality responses with minimal latency

**⚙️ Configuration:**
```bash
# In .env file:
LLM_TYPE=deepseek_api
DEEPSEEK_API_KEY=your_actual_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
LLM_TEMPERATURE=0.1        # Response creativity (0.0-1.0)
LLM_MAX_TOKENS=500         # Maximum response length
```

**📋 Setup Instructions:**
1. **Get API Key**: Visit [DeepSeek Console](https://platform.deepseek.com) and create an account
2. **Generate API Key**: Navigate to API Keys section and create a new key
3. **Configure Environment**: Add your API key to `.env` file:
   ```bash
   DEEPSEEK_API_KEY=sk-your-actual-key-here
   ```
4. **Restart Services**: `docker-compose down && docker-compose up -d`

### **Embedding Models - HuggingFace (Self-Hosted)**

Your system uses **sentence-transformers** for document embeddings:

**📊 Primary Embedding Model:**
- **Model**: `all-MiniLM-L6-v2` (Hugging Face)
- **Size**: ~90MB
- **Dimensions**: 384
- **Purpose**: Convert text to vector embeddings for similarity search
- **Self-hosted**: ✅ Downloaded and cached locally in Docker containers
- **No API Key Required**: ✅ Completely free and private

**🔄 Fallback Model:**
- **Model**: `paraphrase-MiniLM-L6-v2`
- **Purpose**: Backup if primary model fails to load
- **Same specifications as primary model**

**⚙️ Configuration:**
```bash
# In .env file:
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_FALLBACK_MODEL=paraphrase-MiniLM-L6-v2

# Model cache directories (inside containers):
HF_HOME=/tmp/huggingface
SENTENCE_TRANSFORMERS_HOME=/tmp/sentence_transformers
TRANSFORMERS_CACHE=/tmp/transformers
```

**🏃‍♂️ How It Works:**
1. **First Run**: Models automatically download from Hugging Face Hub (~180MB total)
2. **Subsequent Runs**: Models load from local cache (fast startup)
3. **Processing**: Text chunks converted to 384-dimensional vectors
4. **Storage**: Vectors stored in ChromaDB for similarity search
5. **Query Time**: User questions converted to vectors and matched against document vectors

### **Model Performance & Resource Usage**

**💾 Memory Requirements:**
- **DeepSeek API**: ~0MB (external service)
- **Embedding Models**: ~1GB RAM for model loading
- **ChromaDB**: ~500MB for vector storage
- **Total System**: ~4GB RAM recommended

**⚡ Performance Characteristics:**
- **Answer Generation**: 1-3 seconds (DeepSeek API)
- **Embedding Generation**: 100ms per document chunk
- **Vector Search**: <50ms for similarity queries
- **PDF Processing**: 2-5 seconds per MB of PDF content

**🔐 Privacy & Security:**
- **LLM**: External API (data sent to DeepSeek)
- **Embeddings**: Fully local (no data leaves your server)
- **Documents**: Stored locally in ChromaDB
- **Cache**: All embeddings cached locally for privacy

### **Model Comparison & Alternatives**

**🎯 Current Setup Benefits:**
- **Best of Both Worlds**: High-quality LLM responses + Private embeddings
- **Cost Effective**: Pay only for LLM usage, embeddings are free
- **Fast Setup**: No need to download large LLM models
- **Scalable**: DeepSeek handles LLM infrastructure

**🔄 Alternative Configurations:**

**Option 1: Fully Local (Privacy-First)**
```bash
# Use local Ollama + local embeddings
LLM_TYPE=ollama
OLLAMA_HOST=ollama
OLLAMA_PORT=11434
# Requires additional Docker service for Ollama
```

**Option 2: Full External APIs**
```bash
# Use OpenAI + local embeddings
LLM_TYPE=openai
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-3.5-turbo
```

**Option 3: Different Embedding Models**
```bash
# Use larger, more accurate embedding model
EMBEDDING_MODEL=all-mpnet-base-v2  # 420MB, 768 dimensions
# Or smaller, faster model
EMBEDDING_MODEL=all-MiniLM-L12-v2  # 120MB, 384 dimensions
```

## 📋 Prerequisites

- **Docker & Docker Compose**: Latest version installed
- **Hardware Requirements**: 
  - At least 4GB RAM (8GB recommended for production)
  - 2GB free disk space (more for document storage)
- **Network**: Ports 5005, 5055, 8000, 8001, 6379 available

## 🚀 Quick Start Guide

### 1. Get DeepSeek API Key (Required)
Before starting, you need a DeepSeek API key for intelligent answer generation:

1. **Visit DeepSeek Platform**: Go to [https://platform.deepseek.com](https://platform.deepseek.com)
2. **Create Account**: Sign up for a new account
3. **Generate API Key**: 
   - Navigate to "API Keys" in your dashboard
   - Click "Create new secret key"
   - Copy the generated key (starts with `sk-`)
4. **Add to Environment**: 
   ```bash
   # Edit .env file
   DEEPSEEK_API_KEY=sk-your-actual-api-key-here
   ```

### 2. System Startup
```bash
# Navigate to project directory
cd /Users/Yassine/Desktop/rasa

# Configure DeepSeek API key (REQUIRED)
# Edit .env file and add: DEEPSEEK_API_KEY=sk-your-actual-key

# Start all services (first run downloads embedding models ~180MB)
docker-compose up --build -d

# Check all services are running
docker-compose ps

# Run system health check
./test-system.sh
```

### 2. Upload Your First PDF
```bash
# Upload a PDF document
curl -X POST "http://localhost:8001/upload-pdf" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/document.pdf"

# Check processing status
curl "http://localhost:8001/documents"
```

### 3. Start Chatting
```bash
# Interactive chat in terminal (recommended for testing)
python3 chat.py

# Or via API directly
curl -X POST "http://localhost:5005/webhooks/rest/webhook" \
     -H "Content-Type: application/json" \
     -d '{"sender": "user", "message": "Hello! What can you tell me about the uploaded document?"}'
```

## 📁 Project Structure

```
rasa/
├── docker-compose.yml         # 🐳 Service orchestration
├── .env                       # ⚙️ Environment configuration  
├── .env.example              # 📋 Production configuration template
├── .gitignore                # 🚫 Git ignore rules
├── README.md                 # 📖 Complete documentation (this file)
├──
├── rasa/                     # 💬 Rasa chatbot configuration
│   ├── domain.yml           # 🤖 Bot capabilities and responses
│   ├── config.yml           # 🔧 ML pipeline configuration
│   ├── endpoints.yml        # 🔗 Service endpoints
│   ├── nlu.yml             # 🧠 Natural language understanding (training data)
│   ├── stories.yml         # 📚 Conversation flows (training data)  
│   └── rules.yml           # ⚖️ Conversation rules (training data)
├──
├── actions/                  # 🎯 Custom action server
│   ├── Dockerfile           # 🐳 Action server container
│   ├── requirements.txt     # 📦 Python dependencies
│   └── actions.py           # 🔍 RAG functionality implementation
├──
├── pdf-processor/           # 📄 Document processing service
│   ├── Dockerfile           # 🐳 Processor container
│   ├── requirements.txt     # 📦 Python dependencies
│   ├── main.py             # 🚀 FastAPI server with all endpoints
│   ├── pdf_processor.py    # 📝 PDF text extraction utilities
│   └── embeddings.py       # 🧮 Vector embeddings management
├──
├── start.sh                 # ▶️ Quick system startup script
├── stop.sh                  # ⏹️ Quick system shutdown script
├── test-system.sh          # 🧪 Health check and system testing
├── upload-and-test.sh      # 📤 PDF upload and testing script
├── chat.py                 # 💬 Interactive chat client
└──
└── logs/                   # 📊 Application logs (created at runtime)
```

### 🛠 Utility Scripts

The project includes several utility scripts to help manage your RAG chatbot system:

- **`start.sh`** - ▶️ Quick system startup (builds and starts all services)
- **`stop.sh`** - ⏹️ Clean system shutdown (stops all services and containers)
- **`test-system.sh`** - 🧪 Comprehensive health check and system validation
- **`upload-and-test.sh`** - 📤 Automated PDF upload and testing demonstration
- **`chat.py`** - 💬 Interactive terminal chat client for easy conversation testing

```bash
# Quick start commands
./start.sh                    # Start the entire system
./test-system.sh             # Verify everything is working
python3 chat.py              # Start chatting
./stop.sh                    # Clean shutdown when done
```

## 🎯 Usage Guide
```
```

## 🎯 Usage Guide

### Document Management

#### Upload PDF Documents
```bash
# Single document upload
curl -X POST "http://localhost:8001/upload-pdf" \
     -F "file=@your-document.pdf"

# Python example
import requests
url = "http://localhost:8001/upload-pdf"
files = {"file": open("document.pdf", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

#### Check Document Status
```bash
# List all documents
curl "http://localhost:8001/documents"

# Get specific document status
curl "http://localhost:8001/status/FILE_ID"
```

#### Search Documents
```bash
# Direct search API
curl "http://localhost:8001/search?query=your question about the document"
```

### Conversational Interface

#### Chat via REST API
```bash
curl -X POST "http://localhost:5005/webhooks/rest/webhook" \
     -H "Content-Type: application/json" \
     -d '{
       "sender": "user1",
       "message": "What does the document say about artificial intelligence?"
     }'
```

#### Interactive Chat Client
```bash
# Start interactive terminal chat
python3 chat.py

# Custom server configuration
python3 chat.py http://localhost:5005 your_user_id
```

### Supported Conversation Patterns

The chatbot understands and responds to:

- **Greetings**: "Hello", "Hi", "Good morning", "Hey there"
- **Document Questions**: "What does the document say about X?", "Tell me about Y"
- **Document Management**: "List documents", "Upload PDF", "Show me all documents"
- **Knowledge Operations**: "Clear all documents", "Delete document X"
- **Help Requests**: "How do I upload a file?", "What can you do?"
- **Farewells**: "Goodbye", "See you later", "Bye"

## 🚀 Complete API Reference

### PDF Processor Service (http://localhost:8001)
- `GET /` - Service information
- `GET /health` - Service health check with dependency status
- `POST /upload-pdf` - Upload PDF documents (multipart/form-data)
- `GET /documents` - List all processed documents
- `GET /status/{file_id}` - Check specific document processing status
- `GET /search?query={query}&limit={n}` - Search documents by query
- `DELETE /documents/{file_id}` - Delete specific document
- `DELETE /clear-knowledge-base` - Clear all documents
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /openapi.json` - OpenAPI specification

### Action Server (http://localhost:5055)
- `GET /health` - Service health check
- `POST /webhook` - Rasa action webhook (internal use)

### Rasa Server (http://localhost:5005)
- `GET /` - Server status and model information
- `POST /webhooks/rest/webhook` - Main chat interface
- `GET /status` - Detailed server status
- `GET /model` - Current model information
- `POST /model/train` - Trigger model training
- `GET /version` - Rasa version information

### ChromaDB (http://localhost:8000)
- `GET /api/v1/heartbeat` - Database health check
- Vector operations (internal API used by PDF processor)

### Redis (localhost:6379)
- Standard Redis operations for caching and session storage

## 🔧 Configuration & Customization

### Environment Variables

Key configuration options in `.env`:

```bash
# Service Ports
RASA_SERVER_PORT=5005
ACTION_SERVER_PORT=5055
PDF_PROCESSOR_PORT=8001
CHROMA_PORT=8000
REDIS_PORT=6379

# PDF Processing Configuration
MAX_FILE_SIZE_MB=50
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
EMBEDDING_MODEL=all-MiniLM-L6-v2

# Search & RAG Configuration  
MAX_SEARCH_RESULTS=5
SIMILARITY_THRESHOLD=0.7
MIN_CHUNK_LENGTH=100
MAX_CONTEXT_LENGTH=2000

# Performance Tuning
REDIS_MAX_MEMORY=512mb
CHROMA_PERSIST_DIRECTORY=/chroma/chroma
SENTENCE_TRANSFORMERS_HOME=/tmp/sentence_transformers
```

### Advanced Customization

#### Adding New Conversation Intents
1. **Update Training Data**: Edit `rasa/nlu.yml` with new intent examples
2. **Create Stories**: Add conversation flows in `rasa/stories.yml`
3. **Implement Actions**: Add custom logic in `actions/actions.py`
4. **Update Domain**: Define new responses in `rasa/domain.yml`
5. **Retrain Model**: Run `docker-compose exec rasa rasa train`

#### Enhancing Answer Generation
The system currently uses retrieval + simple response generation. To improve:

```python
# In actions/actions.py, replace simple responses with:

# Option 1: OpenAI GPT Integration
import openai
def generate_answer(context, question):
    prompt = f"Based on this context: {context}\nAnswer: {question}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Option 2: Local LLM (Ollama)
import requests
def generate_answer(context, question):
    response = requests.post("http://localhost:11434/api/generate",
        json={"model": "llama2", "prompt": f"Context: {context}\nQ: {question}\nA:"})
    return response.json()["response"]
```

#### Supporting Additional File Types
Extend `pdf_processor/main.py` to handle more formats:

```python
# Add support for .docx, .txt, .html
from docx import Document
import textract

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([paragraph.text for paragraph in doc.paragraphs])

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
```

## 🔍 Monitoring & Maintenance

### Health Monitoring

#### Automated Health Checks
```bash
# Comprehensive system test
./test-system.sh

# Individual service checks
curl http://localhost:8001/health  # PDF Processor
curl http://localhost:5055/health  # Action Server  
curl http://localhost:8000/api/v1/heartbeat  # ChromaDB
```

#### Service Status Dashboard
```bash
# View all service status
docker-compose ps

# Resource usage monitoring  
docker-compose top

# Real-time resource stats
docker stats $(docker-compose ps -q)
```

### Log Management

#### Viewing Logs
```bash
# All services
docker-compose logs

# Specific services with follow
docker-compose logs -f rasa
docker-compose logs -f pdf-processor  
docker-compose logs -f chroma

# Last 100 lines
docker-compose logs --tail=100
```

#### Log Rotation
```bash
# Add to docker-compose.yml for production:
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### Performance Optimization

#### For Better Speed
```bash
# Reduce search results for faster response
export MAX_SEARCH_RESULTS=3

# Use smaller embedding model
export EMBEDDING_MODEL=all-MiniLM-L12-v2  

# Optimize chunk sizes
export CHUNK_SIZE=500
export CHUNK_OVERLAP=100
```

#### For Better Accuracy  
```bash
# Use larger embedding model
export EMBEDDING_MODEL=all-mpnet-base-v2

# Increase search results
export MAX_SEARCH_RESULTS=10

# Lower similarity threshold
export SIMILARITY_THRESHOLD=0.6
```

#### For Production Scaling
```bash
# Scale horizontally
docker-compose up --scale pdf-processor=3 --scale action-server=2

# Use external databases
export CHROMA_HOST=external-chroma-server.com
export REDIS_HOST=external-redis-server.com
```

## 🧪 Testing Your System

### Automated Testing
```bash
# Run comprehensive system test
./test-system.sh

# Expected output:
# ✅ PDF Processor: healthy - chroma: ok, redis: ok
# ✅ Action Server: healthy
# ✅ ChromaDB: heartbeat responding  
# ✅ All services running
```

### Creating Test Documents

Since you'll need PDF documents for testing, here are some quick ways to create test files:

```bash
# Create a simple text file and convert to PDF (macOS/Linux)
echo "This is a test document for the RAG chatbot system. 
It contains information about artificial intelligence and machine learning.
The system can answer questions about the content in this document." > test.txt

# Convert to PDF using system tools
# macOS: textutil -convert rtf test.txt -output test.rtf && textutil -convert pdf test.rtf
# Linux: pandoc test.txt -o test.pdf
# Or use online converters like pdf24.org or smallpdf.com

# Alternatively, save any webpage as PDF using your browser
# Or download research papers from arxiv.org, papers with abstracts work well
```

### Manual Testing Scenarios

#### Scenario 1: Single Document Upload & Query
```bash
# 1. Upload test document (replace with your PDF file)
curl -X POST -F "file=@your-document.pdf" http://localhost:8001/upload-pdf

# 2. Wait for processing (check status)
curl http://localhost:8001/documents

# 3. Ask questions
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender": "test", "message": "What is RAG?"}'
```

#### Scenario 2: Interactive Chat Session
```bash
# Start interactive session
python3 chat.py

# Try these conversation flows:
# User: Hello
# Bot: Hello! I'm your AI assistant...

# User: What does the document say about Rasa?
# Bot: Based on the uploaded documents: Rasa is...

# User: List documents  
# Bot: 📚 Uploaded Documents: [list of files]

# User: Goodbye
# Bot: Goodbye! Feel free to ask me anything...
```

#### Scenario 3: API Integration Test
```python
import requests
import json

def test_full_workflow():
    # 1. Check system health
    health = requests.get("http://localhost:8001/health")
    assert health.json()["status"] == "healthy"
    
    # 2. Upload document (replace with your PDF file)
    with open("your-document.pdf", "rb") as f:
        upload = requests.post("http://localhost:8001/upload-pdf", 
                              files={"file": f})
    assert upload.status_code == 200
    
    # 3. Wait for processing
    import time
    time.sleep(5)
    
    # 4. Ask question
    chat_response = requests.post("http://localhost:5005/webhooks/rest/webhook",
        json={"sender": "test", "message": "What is this document about?"})
    
    assert len(chat_response.json()) > 0
    print("✅ Full workflow test passed!")

test_full_workflow()
```

## 🚧 Troubleshooting Guide

### Common Issues & Solutions

#### 1. Services Won't Start
**Symptoms**: `docker-compose up` fails or services keep restarting

**Solutions**:
```bash
# Check Docker is running
docker --version
docker-compose --version

# Verify port availability  
lsof -i :5005 :5055 :8000 :8001 :6379

# Clean up previous containers
docker-compose down -v
docker system prune -f

# Check logs for specific errors
docker-compose logs [service-name]
```

#### 2. "No relevant documents found"
**Symptoms**: Bot always responds with no results

**Solutions**:
```bash
# Verify documents are uploaded and processed
curl http://localhost:8001/documents

# Check document processing status
curl http://localhost:8001/status/FILE_ID

# Test direct search API
curl "http://localhost:8001/search?query=test"

# Verify question relates to document content
# Lower similarity threshold in .env if needed
```

#### 3. PDF Processing Failures
**Symptoms**: Documents fail to process or extract text

**Solutions**:
```bash
# Ensure PDF contains text (not just images)
# Check file size is under limit (50MB default)
# Verify PDF isn't password protected

# Test with simple text PDF first
# Check processing logs
docker-compose logs pdf-processor
```

#### 4. Memory/Performance Issues
**Symptoms**: Services crash or slow responses

**Solutions**:
```bash
# Increase Docker memory allocation (Docker Desktop settings)
# Reduce concurrent processing:
export CHUNK_SIZE=500
export MAX_SEARCH_RESULTS=3

# Monitor resource usage
docker stats

# Scale down if needed
docker-compose down
docker-compose up -d --scale pdf-processor=1
```

#### 5. ChromaDB Connection Issues
**Symptoms**: "Could not connect to ChromaDB" errors

**Solutions**:
```bash
# Check ChromaDB container health
docker-compose logs chroma

# Restart ChromaDB service
docker-compose restart chroma

# Verify network connectivity
docker-compose exec pdf-processor ping chroma

# Check version compatibility (using ChromaDB 0.4.15)
```

### Debug Commands

#### Container Debugging
```bash
# Enter container for investigation
docker-compose exec pdf-processor bash
docker-compose exec rasa bash
docker-compose exec chroma bash

# Check internal network connectivity
docker-compose exec pdf-processor curl http://chroma:8000/api/v1/heartbeat
docker-compose exec rasa curl http://action-server:5055/health
```

#### Database Inspection
```bash
# Check ChromaDB collections
curl http://localhost:8000/api/v1/collections

# Check Redis keys
docker-compose exec redis redis-cli keys "*"

# Monitor real-time logs
docker-compose logs -f --tail=50
```

## 🚀 Production Deployment

### Security Checklist
- [ ] Change default passwords in `.env`
- [ ] Enable authentication on ChromaDB and Redis
- [ ] Set up SSL/TLS certificates for HTTPS
- [ ] Configure firewall rules for service ports
- [ ] Use Docker secrets for sensitive data
- [ ] Enable audit logging
- [ ] Set up rate limiting on APIs
- [ ] Configure CORS policies appropriately

### Performance Optimization
- [ ] Use external databases (PostgreSQL + pgvector)
- [ ] Implement Redis clustering for caching
- [ ] Add load balancing for multiple instances
- [ ] Configure CDN for static assets
- [ ] Set up monitoring and alerting (Prometheus + Grafana)
- [ ] Implement proper backup strategies
- [ ] Use container orchestration (Kubernetes)

### Monitoring Setup
```yaml
# docker-compose.monitoring.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    
  node-exporter:
    image: prom/node-exporter
    ports:
      - "9100:9100"
```

## 📖 Example Conversations

### Basic Interaction
```
👤 User: Hello!
🤖 Bot: Hello! I'm your AI assistant with access to uploaded documents. 
       I can help you find information from your PDF files. How can I assist you today?

👤 User: What can you tell me about machine learning?
🤖 Bot: Based on the uploaded documents, machine learning is a subset of artificial 
       intelligence that enables computer systems to automatically improve their 
       performance on specific tasks through experience, without being explicitly 
       programmed for each scenario. The documents describe several key approaches 
       including supervised learning, unsupervised learning, and reinforcement learning, 
       each suited for different types of problems and data structures.
       
       📚 Sources: ML_Guide.pdf, AI_Research.pdf

👤 User: Can you be more specific about neural networks?
🤖 Bot: From your documents, neural networks are computational models inspired by 
       biological neural networks in the human brain. They consist of interconnected 
       nodes (neurons) organized in layers that process and transmit information. 
       The documents explain that these networks learn by adjusting the strength of 
       connections between neurons based on training data, making them particularly 
       effective for pattern recognition, image classification, and natural language 
       processing tasks.
       
       📚 Sources: Deep_Learning.pdf, Neural_Networks_Guide.pdf
```

### Document Management
```
👤 User: List my documents
🤖 Bot: 📚 Your Uploaded Documents:
       
       ✅ ML_Guide.pdf (completed) - 45 chunks, uploaded 2 hours ago
       ✅ AI_Research.pdf (completed) - 32 chunks, uploaded 1 hour ago  
       ⏳ Deep_Learning.pdf (processing) - 28% complete
       
       Total: 3 documents, 77 processed chunks

👤 User: Can you upload PDFs for me?
🤖 Bot: I can't directly upload files, but I can guide you! Here's how:
       
       📋 Via API:
       curl -X POST "http://localhost:8001/upload-pdf" -F "file=@your-file.pdf"
       
       📋 Via Python:
       requests.post("http://localhost:8001/upload-pdf", files={"file": open("file.pdf", "rb")})
       
       Once uploaded, I'll automatically process and index the content for searching!

👤 User: Clear all my documents
🤖 Bot: I've cleared all documents from your knowledge base. Your document 
       collection is now empty and ready for new uploads.
```

### Advanced Queries
```
👤 User: Compare the approaches to deep learning mentioned in my documents
🤖 Bot: Based on your documents, I found several approaches to deep learning:
       
       🔹 **Supervised Learning Approach** (ML_Guide.pdf):
       Uses labeled training data to learn input-output mappings...
       
       🔹 **Unsupervised Learning Approach** (AI_Research.pdf):  
       Discovers patterns in data without explicit labels...
       
       🔹 **Reinforcement Learning Approach** (Deep_Learning.pdf):
       Learns through interaction with environment and rewards...
       
       📚 Sources: 3 documents, 8 relevant sections

👤 User: What questions can I ask you?
🤖 Bot: Great question! Here are the types of queries I can help with:
       
       📋 **Document Content Questions**:
       - "What does the document say about X?"
       - "Explain the concept of Y"
       - "How does Z work according to the documents?"
       
       📋 **Comparative Analysis**:
       - "Compare A and B from my documents"
       - "What are the differences between X and Y?"
       
       📋 **Document Management**:
       - "List my documents" 
       - "Clear all documents"
       - "What's in document X?"
       
       📋 **Factual Lookups**:
       - "Define term X"
       - "What are the key points about Y?"
       
       I work best with specific questions about content in your uploaded PDFs!
```