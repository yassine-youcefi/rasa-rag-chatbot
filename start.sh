#!/bin/bash

# Sipsty RAG Chatbot - Complete System Startup
# Builds and starts all services including the Web UI Dashboard

set -e

echo "🚀 Starting Sipsty RAG Chatbot with Web UI..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install docker-compose."
    exit 1
fi

echo "📦 Building and starting all services (including Web UI)..."

# Stop any existing containers to ensure clean start
docker-compose down

# Build and start all services
docker-compose up --build -d

echo "⏳ Waiting for services to be ready..."
echo ""

# Wait for ChromaDB
echo "Waiting for ChromaDB..."
for i in {1..30}; do
    if curl -sf http://localhost:8003/api/v1/heartbeat > /dev/null 2>&1; then
        echo "✅ ChromaDB is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ ChromaDB failed to start"
        exit 1
    fi
    sleep 2
done

# Wait for Redis
echo "Waiting for Redis..."
for i in {1..30}; do
    if nc -z localhost 6379 > /dev/null 2>&1; then
        echo "✅ Redis is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Redis failed to start"
        exit 1
    fi
    sleep 2
done

# Wait for PDF Processor
echo "Waiting for PDF Processor..."
for i in {1..60}; do
    if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ PDF Processor is ready"
        break
    fi
    if [ $i -eq 60 ]; then
        echo "❌ PDF Processor failed to start"
        exit 1
    fi
    sleep 2
done

# Wait for Action Server
echo "Waiting for Action Server..."
for i in {1..60}; do
    if curl -sf http://localhost:5055/health > /dev/null 2>&1; then
        echo "✅ Action Server is ready"
        break
    fi
    if [ $i -eq 60 ]; then
        echo "❌ Action Server failed to start"
        exit 1
    fi
    sleep 2
done

# Wait for Rasa Server
echo "Waiting for Rasa Server..."
for i in {1..60}; do
    if curl -sf http://localhost:5005/ > /dev/null 2>&1; then
        echo "✅ Rasa Server is ready"
        break
    fi
    if [ $i -eq 60 ]; then
        echo "❌ Rasa Server failed to start"
        exit 1
    fi
    sleep 2
done

# Wait for Web UI
echo "Waiting for Web UI..."
for i in {1..30}; do
    if curl -sf http://localhost:8002/api/system-status > /dev/null 2>&1; then
        echo "✅ Web UI is ready"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Web UI failed to start"
        exit 1
    fi
    sleep 2
done

echo ""
echo "🎉 All services are running successfully!"
echo ""
echo "🌐 WEB DASHBOARD (Primary Interface):"
echo "   📊 Management Dashboard: http://localhost:8002"
echo "   💬 Chat Interface:       Available in dashboard"
echo "   📁 Document Management:  Available in dashboard"
echo "   �️  Collection Explorer:  Available in dashboard"
echo ""
echo "🔧 API ENDPOINTS (Advanced Users):"
echo "   🤖 Rasa Server:         http://localhost:5005"
echo "   📄 PDF Processor:       http://localhost:8000"
echo "   🔍 ChromaDB:            http://localhost:8003"
echo "   ⚡ Action Server:       http://localhost:5055"
echo "   📊 Redis:               localhost:6379"
echo ""
echo "💡 QUICK START:"
echo "   1. Open http://localhost:8002 in your browser"
echo "   2. Upload Sipsty knowledge base PDFs (Document Management tab)"
echo "   3. Test multilingual conversations (Chat tab)"
echo "   4. Explore vector database (Collections tab)"
echo ""
echo "🌍 TEST MULTILINGUAL CONVERSATIONS:"
echo "   English: 'Hello, tell me about Sipsty products'"
echo "   French:  'Bonjour, parlez-moi des produits Sipsty'"
echo "   Arabic:  'مرحباً، أخبرني عن منتجات سيبستي'"
echo ""
echo "� For detailed instructions, see README.md"
echo ""
echo "🔍 View logs: docker-compose logs [service-name]"
echo "🛑 Stop system: docker-compose down"
echo ""