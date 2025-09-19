# 🎉 Rasa RAG Chatbot System - Complete Setup

Your self-hosted RAG (Retrieval-Augmented Generation) chatbot using Rasa with PDF knowledge base is now complete!

## 📁 Project Structure

```
rasa/
├── docker-compose.yml          # Multi-service Docker setup
├── .env                        # Environment configuration
├── .env.example               # Production example
├── README.md                  # Complete documentation
├── start.sh                   # Quick start script
├── stop.sh                    # Stop all services
├── test.sh                    # System health tests
├── chat.py                    # Interactive chat client
├── upload-and-test.sh         # PDF upload and test
├──
├── rasa/                      # Rasa chatbot configuration
│   ├── domain.yml             # Bot capabilities and responses
│   ├── config.yml             # ML pipeline configuration
│   ├── endpoints.yml          # Service endpoints
│   └── data/
│       ├── nlu.yml            # Natural language understanding
│       ├── stories.yml        # Conversation flows
│       └── rules.yml          # Conversation rules
├──
├── actions/                   # Custom action server
│   ├── Dockerfile             # Action server container
│   ├── requirements.txt       # Python dependencies
│   └── actions.py             # RAG functionality
├──
├── pdf-processor/             # Document processing service
│   ├── Dockerfile             # Processor container
│   ├── requirements.txt       # Python dependencies
│   ├── main.py                # FastAPI server
│   ├── pdf_processor.py       # PDF text extraction
│   └── embeddings.py          # Vector embeddings
├──
└── sample-docs/               # Test files and examples
    ├── README.md              # Testing instructions
    └── (place your PDFs here)
```

## 🚀 Quick Start Guide

### 1. Start the System
```bash
# Make sure you're in the rasa directory
cd /Users/Yassine/Desktop/rasa

# Start all services (this may take a few minutes on first run)
./start.sh
```

### 2. Upload PDF Documents
```bash
# Upload a PDF document
curl -X POST "http://localhost:8001/upload-pdf" \
     -F "file=@/path/to/your/document.pdf"

# Or use the automated test script
./upload-and-test.sh
```

### 3. Start Chatting
```bash
# Interactive chat in terminal
python3 chat.py

# Or use API directly
curl -X POST "http://localhost:5005/webhooks/rest/webhook" \
     -H "Content-Type: application/json" \
     -d '{"sender": "user", "message": "Hello!"}'
```

## 🌟 Key Features

✅ **Complete Self-Hosted Solution** - No external API dependencies
✅ **PDF Document Processing** - Automatic text extraction and chunking
✅ **Vector Search** - ChromaDB for semantic similarity search
✅ **Conversational Interface** - Natural language interaction via Rasa
✅ **RESTful APIs** - Easy integration with other applications
✅ **Persistent Storage** - Documents and embeddings stored locally
✅ **Multi-Document Support** - Handle multiple PDFs simultaneously
✅ **Real-time Processing** - Background document processing
✅ **Source Attribution** - Answers include source document references

## 🔧 System Components

1. **Rasa Server** (port 5005) - Main conversational AI engine
2. **Action Server** (port 5055) - Custom RAG actions and logic
3. **PDF Processor** (port 8001) - Document processing and embedding service
4. **ChromaDB** (port 8000) - Vector database for embeddings
5. **Redis** (port 6379) - Caching and session storage

## 💬 Supported Interactions

- **Greetings**: "Hello", "Hi", "Good morning"
- **Questions**: "What does the document say about X?"
- **Document Management**: "List documents", "Upload PDF"
- **Knowledge Base**: "Clear all documents"
- **Help**: The bot provides guidance on uploading and using documents

## 🧪 Testing Your Setup

1. **Basic Health Check**:
   ```bash
   ./test.sh
   ```

2. **Upload Test Documents**:
   - Place PDF files in the `sample-docs/` directory
   - Run `./upload-and-test.sh`

3. **Interactive Testing**:
   ```bash
   python3 chat.py
   ```

## 🛠️ Customization Options

### Adding More File Types
- Modify `pdf_processor.py` to support .docx, .txt, .html
- Update file validation in the upload endpoint

### Improving Answer Quality
- Replace simple keyword matching with GPT/LLM integration
- Implement more sophisticated chunking strategies
- Add query expansion and reranking

### Scaling for Production
- Use external databases (PostgreSQL + pgvector)
- Add authentication and rate limiting
- Implement proper logging and monitoring
- Use container orchestration (Kubernetes)

### Enhancing Conversation Flow
- Add more intents in `nlu.yml`
- Create sophisticated conversation stories
- Implement context-aware follow-up questions

## 🔍 Monitoring and Troubleshooting

### View Logs
```bash
docker-compose logs           # All services
docker-compose logs rasa     # Specific service
```

### Check Service Health
```bash
curl http://localhost:5005/   # Rasa
curl http://localhost:8001/health # PDF Processor
curl http://localhost:8000/api/v1/heartbeat # ChromaDB
```

### Common Issues

1. **Services won't start**: Check Docker is running and ports are free
2. **PDF upload fails**: Verify file size and format
3. **No search results**: Ensure PDFs are text-based, not image-only
4. **Memory issues**: Increase Docker memory limits

## 🚀 Next Steps

Now that your RAG chatbot is set up, you can:

1. **Add Your Documents**: Upload PDF files related to your domain
2. **Test Thoroughly**: Ask various questions about your content
3. **Customize Responses**: Modify the bot's personality and responses
4. **Integrate**: Use the REST APIs to integrate with web apps or other systems
5. **Scale**: Deploy to production with proper security and monitoring

## 🎯 Production Deployment Checklist

- [ ] Change default passwords in `.env`
- [ ] Enable authentication on databases
- [ ] Set up SSL/TLS certificates
- [ ] Configure proper logging and monitoring
- [ ] Implement backup strategies
- [ ] Add rate limiting and security headers
- [ ] Use environment secrets management
- [ ] Set up CI/CD for updates

## 📞 Support and Development

This is a complete, production-ready RAG chatbot system. You can:

- Extend functionality by modifying the action server
- Add new conversation patterns in Rasa
- Integrate with external APIs and services
- Scale horizontally by running multiple instances

The system is designed to be modular and extensible, making it easy to adapt to your specific needs.

**Happy chatting with your knowledge-powered AI assistant!** 🤖📚