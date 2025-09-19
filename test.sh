#!/bin/bash

# Test script for Rasa RAG Chatbot
# This script tests the main functionality

set -e

BASE_URL="http://localhost"
RASA_PORT="5005"
PDF_PORT="8001"

echo "🧪 Testing Rasa RAG Chatbot..."

# Check if services are running
echo "📋 Checking service health..."

# Test PDF Processor
if ! curl -s "${BASE_URL}:${PDF_PORT}/health" > /dev/null; then
    echo "❌ PDF Processor is not responding"
    exit 1
fi
echo "✅ PDF Processor is healthy"

# Test Rasa Server  
if ! curl -s "${BASE_URL}:${RASA_PORT}/" > /dev/null; then
    echo "❌ Rasa Server is not responding"
    exit 1
fi
echo "✅ Rasa Server is healthy"

echo ""
echo "🔍 Testing core functionality..."

# Test 1: Basic chat
echo "Test 1: Basic greeting"
RESPONSE=$(curl -s -X POST "${BASE_URL}:${RASA_PORT}/webhooks/rest/webhook" \
    -H "Content-Type: application/json" \
    -d '{"sender": "test_user", "message": "hello"}')

if echo "$RESPONSE" | grep -q "Hello"; then
    echo "✅ Basic chat works"
else
    echo "❌ Basic chat failed"
    echo "Response: $RESPONSE"
fi

# Test 2: Document listing (should be empty initially)
echo "Test 2: List documents"
RESPONSE=$(curl -s -X POST "${BASE_URL}:${RASA_PORT}/webhooks/rest/webhook" \
    -H "Content-Type: application/json" \
    -d '{"sender": "test_user", "message": "list documents"}')

if echo "$RESPONSE" | grep -q "No documents\|Documents"; then
    echo "✅ Document listing works"
else
    echo "❌ Document listing failed"
    echo "Response: $RESPONSE"
fi

# Test 3: Question without documents
echo "Test 3: Ask question without documents"
RESPONSE=$(curl -s -X POST "${BASE_URL}:${RASA_PORT}/webhooks/rest/webhook" \
    -H "Content-Type: application/json" \
    -d '{"sender": "test_user", "message": "what is artificial intelligence?"}')

if echo "$RESPONSE" | grep -q "documents\|upload"; then
    echo "✅ Question handling works (no documents case)"
else
    echo "❌ Question handling failed"
    echo "Response: $RESPONSE"
fi

# Test 4: PDF upload instructions
echo "Test 4: Upload PDF instructions"
RESPONSE=$(curl -s -X POST "${BASE_URL}:${RASA_PORT}/webhooks/rest/webhook" \
    -H "Content-Type: application/json" \
    -d '{"sender": "test_user", "message": "upload pdf"}')

if echo "$RESPONSE" | grep -q "upload\|POST"; then
    echo "✅ Upload instructions work"
else
    echo "❌ Upload instructions failed"
    echo "Response: $RESPONSE"
fi

# Test 5: PDF Processor API
echo "Test 5: PDF Processor documents endpoint"
RESPONSE=$(curl -s "${BASE_URL}:${PDF_PORT}/documents")

if echo "$RESPONSE" | jq -e '.documents' > /dev/null 2>&1; then
    echo "✅ PDF Processor API works"
else
    echo "❌ PDF Processor API failed"
    echo "Response: $RESPONSE"
fi

# Test 6: Search endpoint (should work even with no documents)
echo "Test 6: Search endpoint"
RESPONSE=$(curl -s "${BASE_URL}:${PDF_PORT}/search?query=test")

if echo "$RESPONSE" | jq -e '.results' > /dev/null 2>&1; then
    echo "✅ Search endpoint works"
else
    echo "❌ Search endpoint failed"
    echo "Response: $RESPONSE"
fi

echo ""
echo "🎯 Core functionality tests completed!"
echo ""
echo "📁 To test with a real PDF file:"
echo "1. Create a sample PDF or use an existing one"
echo "2. Upload it:"
echo "   curl -X POST ${BASE_URL}:${PDF_PORT}/upload-pdf -F 'file=@your-file.pdf'"
echo "3. Wait for processing to complete"
echo "4. Ask questions about the content"
echo ""
echo "🔍 Manual testing examples:"
echo "   List documents: curl -X POST ${BASE_URL}:${RASA_PORT}/webhooks/rest/webhook -H 'Content-Type: application/json' -d '{\"sender\": \"user\", \"message\": \"list documents\"}'"
echo "   Ask question: curl -X POST ${BASE_URL}:${RASA_PORT}/webhooks/rest/webhook -H 'Content-Type: application/json' -d '{\"sender\": \"user\", \"message\": \"what does the document say about X?\"}'"