#!/bin/bash

echo "🚀 Starting RAG System with Web UI..."
echo "📦 Building and starting all services..."

# Stop any existing containers
docker-compose down

# Build and start all services including web UI
docker-compose up --build -d

echo "⏳ Waiting for services to be ready..."

# Wait for ChromaDB
echo "Waiting for ChromaDB..."
while ! curl -sf http://localhost:8000/api/v1/heartbeat > /dev/null 2>&1; do
    sleep 2
done
echo "✅ ChromaDB is ready"

# Wait for Redis
echo "Waiting for Redis..."
while ! nc -z localhost 6379 > /dev/null 2>&1; do
    sleep 2
done
echo "✅ Redis is ready"

# Wait for PDF Processor
echo "Waiting for PDF Processor..."
while ! curl -sf http://localhost:8001/health > /dev/null 2>&1; do
    sleep 2
done
echo "✅ PDF Processor is ready"

# Wait for Action Server
echo "Waiting for Action Server..."
while ! curl -sf http://localhost:5055/health > /dev/null 2>&1; do
    sleep 2
done
echo "✅ Action Server is ready"

# Wait for Rasa Server
echo "Waiting for Rasa Server..."
while ! curl -sf http://localhost:5005/ > /dev/null 2>&1; do
    sleep 2
done
echo "✅ Rasa Server is ready"

# Wait for Web UI
echo "Waiting for Web UI..."
while ! curl -sf http://localhost:8002/api/system-status > /dev/null 2>&1; do
    sleep 2
done
echo "✅ Web UI is ready"

echo ""
echo "🎉 All services are ready!"
echo ""
echo "📊 Access your RAG System Dashboard at: http://localhost:8002"
echo "🤖 Direct Rasa API access at: http://localhost:5005"
echo "📄 PDF Processor API docs at: http://localhost:8001/docs"
echo ""
echo "💡 You can now:"
echo "   1. Open http://localhost:8002 in your browser"
echo "   2. Upload PDF documents through the web interface"
echo "   3. View and explore your document collections"
echo "   4. Chat with the RAG system"
echo "   5. Search through your documents"
echo ""