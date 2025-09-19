# � Sipsty RAG Chatbot - Multilingual Online Store Assistant

> **Status: ✅ FULLY OPERATIONAL** - A complete Retrieval-Augmented Generation (RAG) chatbot built with Rasa for Sipsty beverages. This is an **example implementation** of a multilingual online store chatbot supporting **English, French, and Arabic** languages.

## 🌟 Project Overview

This project demonstrates how to build a sophisticated **multilingual e-commerce chatbot** for an online beverage store. It showcases:

- 🌍 **Multilingual Support**: Native English, French, and Arabic conversation handling
- 🛒 **Product Inquiries**: Smart product discovery and information retrieval
- 💰 **Pricing Information**: Automated pricing and availability responses  
- 🥗 **Ingredient Questions**: Natural, vegan, and dietary information handling
- 🏢 **Business Inquiries**: Professional partnership and B2B communication
- 📱 **Web Dashboard**: Complete management interface with real-time monitoring

## 🎯 **Sipsty Business Context**

**Sipsty** is a premium beverage company specializing in natural, elegant, and creative sparkling drinks:

- **Product Lines**: Classics (70s-inspired) and Signatures (exclusive creations)
- **Key Products**: Cola Sipsty, Bellini, Girly, Punchy, Blue Hawaii, Piña Colada, and more
- **Values**: 100% Natural, Vegan-Friendly, Low-Calorie, Premium Quality
- **Markets**: Europe-wide distribution with multilingual customer support
- **Format**: 4-pack bottles (€3.96 per pack)

## 🌐 **Web Management Dashboard**

Access the complete management interface at: **http://localhost:8002**

### **Dashboard Features:**
- 📊 **System Status**: Real-time health monitoring of all services
- 📁 **Document Management**: Upload and manage PDF knowledge base
- 🗂️ **Collection Viewer**: Browse ChromaDB vector database collections  
- 💬 **Chat Interface**: Test conversations directly in the browser
- 🔍 **Search Functionality**: Query your document database visually
- 📈 **Service Monitoring**: Track all 6 running containers status

### **Multilingual Interface:**
The web UI automatically detects and responds in the user's language:
- **English**: Professional, innovation-focused responses
- **French**: Elegant and sophisticated communication style  
- **Arabic**: Culturally-aware responses with proper RTL support

## 🌟 Core Features

- ✅ **External LLM Integration** - Uses OpenRouter DeepSeek Chat v3.1 Free model
- ✅ **PDF Document Processing** - Automatic text extraction and intelligent chunking
- ✅ **Vector Search** - ChromaDB for semantic similarity search
- ✅ **Conversational Interface** - Natural language interaction via Rasa
- ✅ **Web Management UI** - Complete dashboard at port 8002
- ✅ **Multilingual Support** - English, French, and Arabic languages
- ✅ **RESTful APIs** - Easy integration with other applications
- ✅ **Persistent Storage** - Documents and embeddings stored locally
- ✅ **Multi-Document Support** - Handle multiple PDFs simultaneously
- ✅ **Real-time Processing** - Background document processing
- ✅ **Source Attribution** - Answers include source document references
- ✅ **Production Ready** - Docker-based deployment with proper error handling

## 🏗 System Architecture

The system consists of **6 Docker services** working together:

### Core Services
- **Rasa Core** (Port 5005): Conversational AI engine with multilingual support
- **Action Server** (Port 5055): Custom RAG actions with DeepSeek LLM integration
- **PDF Processor** (Port 8000): Document processing and embedding service
- **ChromaDB** (Port 8003): Vector database for embeddings
- **Redis** (Port 6379): Caching and session storage
- **Web UI Dashboard** (Port 8002): Management interface with real-time monitoring

### Technologies Stack
- **Rasa 3.6.20-full**: Conversational AI framework with multilingual NLU
- **ChromaDB 0.4.15**: Vector database for similarity search
- **FastAPI**: PDF processing REST API and web dashboard backend
- **Bootstrap 5**: Responsive web UI framework
- **OpenRouter DeepSeek API**: External LLM for intelligent answer generation
- **sentence-transformers**: Self-hosted embedding models
- **Redis 7**: High-performance caching
- **Docker Compose**: Service orchestration

## 🤖 **AI Models & Integration**

### **Large Language Model (LLM) - OpenRouter DeepSeek Chat v3.1 Free**

Your system uses **OpenRouter's DeepSeek Chat v3.1 Free model** for intelligent answer generation:

**🧠 Model Details:**
- **Provider**: OpenRouter (DeepSeek Chat v3.1 Free)
- **Model**: `deepseek/deepseek-chat-v3.1:free`
- **Parameters**: 671B total, 37B active
- **Context Length**: 163,840 tokens (163K)
- **Cost**: 100% Free ($0/M input/output tokens)
- **Features**: Advanced reasoning, code generation, tool use
- **Performance**: High-quality responses with minimal latency

**⚙️ Configuration:**
```bash
# In .env file:
LLM_TYPE=deepseek_api
DEEPSEEK_API_KEY=your_openrouter_api_key_here
DEEPSEEK_BASE_URL=https://openrouter.ai/api/v1
DEEPSEEK_MODEL=deepseek/deepseek-chat-v3.1:free
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=1000
LLM_TIMEOUT=30.0
```

**📋 Setup Instructions:**
1. **Get API Key**: Visit [OpenRouter.ai](https://openrouter.ai) and create an account
2. **Generate API Key**: Navigate to API Keys section and create a new key
3. **Configure Environment**: Add your API key to `.env` file:
   ```bash
   DEEPSEEK_API_KEY=your_openrouter_api_key_here
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
- **DeepSeek API**: ~0MB (external service via OpenRouter)
- **Embedding Models**: ~1GB RAM for model loading
- **ChromaDB**: ~500MB for vector storage
- **Total System**: ~4GB RAM recommended

**⚡ Performance Characteristics:**
- **Answer Generation**: 1-3 seconds (OpenRouter DeepSeek API)
- **Embedding Generation**: 100ms per document chunk
- **Vector Search**: <50ms for similarity queries
- **PDF Processing**: 2-5 seconds per MB of PDF content

**🔐 Privacy & Security:**
- **LLM**: External API via OpenRouter (data sent to OpenRouter/DeepSeek)
- **Embeddings**: Fully local (no data leaves your server)
- **Documents**: Stored locally in ChromaDB
- **Cache**: All embeddings cached locally for privacy

## 📋 Prerequisites

- **Docker & Docker Compose**: Latest version installed
- **Hardware Requirements**: 
  - At least 4GB RAM (8GB recommended for production)
  - 2GB free disk space (more for document storage)
- **Network**: Ports 5005, 5055, 8000, 8001, 6379 available
- **OpenRouter API Key**: Free account at [OpenRouter.ai](https://openrouter.ai)

## 🚀 Quick Start Guide

### 1. Get OpenRouter API Key (Required)
Before starting, you need an OpenRouter API key for the DeepSeek model:

1. **Visit OpenRouter**: Go to [https://openrouter.ai](https://openrouter.ai)
2. **Create Account**: Sign up for a new account
3. **Generate API Key**: 
   - Navigate to "API Keys" in your dashboard
   - Click "Create new key"
   - Copy the generated key
4. **Add to Environment**: 
   ```bash
   # Edit .env file
   DEEPSEEK_API_KEY=your_openrouter_api_key_here
   ```

### 2. System Startup
```bash
# Navigate to project directory
cd /Users/Yassine/Desktop/rasa

# Configure OpenRouter API key (REQUIRED)
# Edit .env file and add: DEEPSEEK_API_KEY=your_openrouter_api_key_here

# Start all services with Web UI (recommended)
./start-with-ui.sh

# OR start manually with docker-compose
docker-compose up --build -d

# Check all services are running (should show 6 containers)
docker-compose ps

# Run system health check
./test-system.sh
```

### 3. Access Web Dashboard 🌟
```bash
# Open the Web Management Dashboard
open http://localhost:8002

# Or visit directly in your browser:
# http://localhost:8002
```

**Dashboard Features:**
- 📊 System status monitoring
- 📁 Document upload and management
- 💬 Interactive chat interface
- 🗂️ Vector database exploration
- 🌍 Multilingual conversation testing

### 4. Upload Your First PDF
```bash
# Method 1: Via Web Dashboard (Recommended)
# 1. Open http://localhost:8002
# 2. Go to "Document Management" tab
# 3. Drag & drop your PDF files

# Method 2: Via API
curl -X POST "http://localhost:8000/upload-pdf" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/sipsty-document.pdf"

# Check processing status
curl "http://localhost:8000/documents"
```

### 5. Test Multilingual Conversations
```bash
# Method 1: Via Web Dashboard (Recommended)
# 1. Open http://localhost:8002
# 2. Use the chat interface in any language:
#    English: "Hello, tell me about Sipsty products"
#    French: "Bonjour, parlez-moi des produits Sipsty"
#    Arabic: "مرحباً، أخبرني عن منتجات سيبستي"

# Method 2: Interactive terminal chat
python3 chat.py

# Method 3: Direct API testing
# English conversation
curl -X POST "http://localhost:5005/webhooks/rest/webhook" \
     -H "Content-Type: application/json" \
     -d '{"sender": "user", "message": "Hello, what Sipsty products do you have?"}'

# French conversation  
curl -X POST "http://localhost:5005/webhooks/rest/webhook" \
     -H "Content-Type: application/json" \
     -d '{"sender": "user", "message": "Bonjour, quels produits Sipsty avez-vous?"}'

# Arabic conversation
curl -X POST "http://localhost:5005/webhooks/rest/webhook" \
     -H "Content-Type: application/json" \
     -d '{"sender": "user", "message": "مرحباً، ما هي منتجات سيبستي المتوفرة؟"}'
```

**Example Conversations to Try:**
- 🇺🇸 **English**: "What ingredients are in Cola Sipsty?" / "How much does a 4-pack cost?"
- 🇫🇷 **French**: "Quels sont les ingrédients du Cola Sipsty?" / "Combien coûte un pack de 4?"
- 🇸🇦 **Arabic**: "ما مكونات كولا سيبستي؟" / "كم سعر العبوة من 4 زجاجات؟" \
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

## � **Multilingual Training Data**

This project includes comprehensive **multilingual training data** specifically designed for Sipsty:

### **📚 Training Data Structure**
- **17 Total Intents**: Including 8 new Sipsty-specific intents
- **300+ Training Examples**: Across English, French, and Arabic languages
- **7 Entities**: Product names, categories, and business contexts
- **15+ Conversation Stories**: Real customer journey scenarios

### **🎯 Sipsty-Specific Intents**
1. **`product_inquiry`** - Ask about specific products (Cola Sipsty, Bellini, Girly, etc.)
2. **`pricing_inquiry`** - Questions about €3.96 pricing and 4-pack format
3. **`ingredient_question`** - Natural, vegan, low-calorie ingredient queries
4. **`availability_question`** - Store locations, distribution, online purchase
5. **`professional_inquiry`** - HoReCa partnerships, retailer information
6. **`contact_info`** - Website, social media, customer service contacts
7. **`out_of_scope`** - Proper handling of non-Sipsty related questions

### **🏷️ Multilingual Entity Recognition**
- **Product Names**: Cola Sipsty, Bellini, Girly, Punchy, Lady, Baby, etc.
- **Categories**: Classics vs Signatures product lines
- **Languages**: Automatic detection and appropriate cultural responses
- **Business Context**: Professional inquiries vs consumer questions

### **🗣️ Cultural Adaptation**
- **English**: Focus on innovation, quality, and premium positioning
- **French**: Emphasis on elegance, sophistication, and artisanal craftsmanship  
- **Arabic**: Cultural sensitivity for consumption occasions and family preferences

## �🎯 Usage Guide
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
# LLM Configuration (OpenRouter DeepSeek Chat v3.1 Free)
LLM_TYPE=deepseek_api
DEEPSEEK_API_KEY=your_openrouter_api_key_here
DEEPSEEK_BASE_URL=https://openrouter.ai/api/v1
DEEPSEEK_MODEL=deepseek/deepseek-chat-v3.1:free
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=1000
LLM_TIMEOUT=30.0

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
UPLOAD_DIR=/app/uploads

# Search & RAG Configuration  
MAX_SEARCH_RESULTS=5
SIMILARITY_THRESHOLD=0.7
MAX_RELEVANT_SENTENCES=2
CONTEXT_SUMMARY_WORDS=100
COLLECTION_NAME=pdf_documents

# Redis Configuration
REDIS_TTL=3600
CACHE_ENABLED=true

# Logging
LOG_LEVEL=INFO
```

## 🔍 Monitoring & Troubleshooting

### Health Monitoring
```bash
# Comprehensive system test
./test-system.sh

# Individual service checks
curl http://localhost:8001/health  # PDF Processor
curl http://localhost:5055/health  # Action Server  
curl http://localhost:8000/api/v1/heartbeat  # ChromaDB

# View service status
docker-compose ps

# View logs
docker-compose logs -f --tail=50
```

### Common Issues & Solutions

#### 1. Services Won't Start
```bash
# Check Docker is running and ports are available
lsof -i :5005 :5055 :8000 :8001 :6379

# Clean up and restart
docker-compose down -v
docker-compose up --build -d
```

#### 2. "No relevant documents found"
```bash
# Verify documents are uploaded and processed
curl http://localhost:8001/documents

# Test direct search API
curl "http://localhost:8001/search?query=test"
```

#### 3. PDF Processing Failures
- Ensure PDF contains text (not just images)
- Check file size is under limit (50MB default)
- Verify PDF isn't password protected

#### 4. API Key Issues
- Verify OpenRouter API key is correct in `.env`
- Check API key has sufficient credits/permissions
- Restart services after changing API key

## 🧪 Testing Your System

### Quick Test
```bash
# Run comprehensive system test
./test-system.sh

# Upload test document and interact
./upload-and-test.sh

# Interactive chat
python3 chat.py
```

### API Testing
```bash
# 1. Upload document
curl -X POST -F "file=@your-document.pdf" http://localhost:8001/upload-pdf

# 2. Check processing status
curl http://localhost:8001/documents

# 3. Ask questions via API
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender": "test", "message": "What is this document about?"}'
```

##  Example Conversations

### Basic Interaction
```
👤 User: Hello!
🤖 Bot: Hello! I'm your AI assistant with access to uploaded documents. 
       I can help you find information from your PDF files. How can I assist you today?

👤 User: What can you tell me about machine learning?
🤖 Bot: Based on the uploaded documents, machine learning is a subset of artificial 
       intelligence that enables computer systems to automatically improve their 
       performance on specific tasks through experience...
       
       📚 Sources: ML_Guide.pdf, AI_Research.pdf

👤 User: List my documents
🤖 Bot: 📚 Your Uploaded Documents:
       
       ✅ ML_Guide.pdf (completed) - 45 chunks, uploaded 2 hours ago
       ✅ AI_Research.pdf (completed) - 32 chunks, uploaded 1 hour ago  
       
       Total: 2 documents, 77 processed chunks
```

### Supported Questions
- **Document Content**: "What does the document say about X?"
- **Comparisons**: "Compare A and B from my documents"
- **Document Management**: "List documents", "Clear all documents"
- **General Help**: "What can you do?", "How do I upload files?"

---

## 🚀 Getting Started Checklist

1. **✅ Prerequisites**: Docker & Docker Compose installed
2. **✅ API Key**: Get free OpenRouter API key from [openrouter.ai](https://openrouter.ai)
3. **✅ Configuration**: Add API key to `.env` file
4. **✅ Start System**: Run `docker-compose up --build -d`
5. **✅ Test**: Run `./test-system.sh` to verify everything works
6. **✅ Upload**: Add your first PDF document
7. **✅ Chat**: Start interacting with `python3 chat.py`

**Need Help?** Check the troubleshooting section above or create an issue in the repository.

---

*Built by  @yassine-youcefi with ❤️ using Rasa, OpenRouter DeepSeek, ChromaDB, and Docker*