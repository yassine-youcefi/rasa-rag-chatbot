#!/bin/bash

# Stop all services
echo "🛑 Stopping Rasa RAG Chatbot services..."

docker-compose down

echo "✅ All services stopped!"
echo ""
echo "🧹 To also remove volumes (WARNING: This deletes all data):"
echo "   docker-compose down -v"
echo ""
echo "🗑️ To remove Docker images:"
echo "   docker-compose down --rmi all"