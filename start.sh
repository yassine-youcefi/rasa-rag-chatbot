#!/bin/bash

# Rasa RAG Chatbot - Quick Start Script
# This script builds and starts all services

set -e

echo "🚀 Starting Rasa RAG Chatbot..."

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

echo "📦 Building and starting services..."
docker-compose up --build -d

echo "⏳ Waiting for services to be ready..."

# Wait for ChromaDB
echo "Waiting for ChromaDB..."
for i in {1..30}; do
    if curl -s http://localhost:8000/api/v1/heartbeat > /dev/null 2>&1; then
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
    if docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
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
    if curl -s http://localhost:8001/health > /dev/null 2>&1; then
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
    if curl -s http://localhost:5055/webhook > /dev/null 2>&1; then
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
    if curl -s http://localhost:5005/ > /dev/null 2>&1; then
        echo "✅ Rasa Server is ready"
        break
    fi
    if [ $i -eq 60 ]; then
        echo "❌ Rasa Server failed to start"
        exit 1
    fi
    sleep 2
done

echo ""
echo "🎉 All services are running!"
echo ""
echo "📋 Service URLs:"
echo "   Rasa Server:     http://localhost:5005"
echo "   PDF Processor:   http://localhost:8001"
echo "   ChromaDB:        http://localhost:8000"
echo "   Action Server:   http://localhost:5055"
echo ""
echo "📚 To upload a PDF:"
echo "   curl -X POST http://localhost:8001/upload-pdf -F 'file=@your-document.pdf'"
echo ""
echo "💬 To chat with the bot:"
echo "   curl -X POST http://localhost:5005/webhooks/rest/webhook \\"
echo "        -H 'Content-Type: application/json' \\"
echo "        -d '{\"sender\": \"user1\", \"message\": \"Hello!\"}'"
echo ""
echo "📖 Check README.md for detailed usage instructions."
echo ""
echo "🔍 View logs with: docker-compose logs [service-name]"
echo "🛑 Stop with: docker-compose down"