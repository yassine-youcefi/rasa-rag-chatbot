#!/bin/bash

# Sample PDF Upload Script
# This script demonstrates how to upload PDFs and test the system

set -e

BASE_URL="http://localhost:8001"
RASA_URL="http://localhost:5005"

echo "📄 Sample PDF Upload and Test Script"
echo "===================================="

# Check if services are running
if ! curl -s "${BASE_URL}/health" > /dev/null; then
    echo "❌ PDF Processor is not running. Start services first with: ./start.sh"
    exit 1
fi

if ! curl -s "${RASA_URL}/" > /dev/null; then
    echo "❌ Rasa Server is not running. Start services first with: ./start.sh"
    exit 1
fi

echo "✅ Services are running!"
echo ""

# Function to upload a PDF
upload_pdf() {
    local file_path="$1"
    local filename=$(basename "$file_path")
    
    echo "📤 Uploading: $filename"
    
    if [ ! -f "$file_path" ]; then
        echo "❌ File not found: $file_path"
        return 1
    fi
    
    response=$(curl -s -X POST "${BASE_URL}/upload-pdf" \
        -H "accept: application/json" \
        -H "Content-Type: multipart/form-data" \
        -F "file=@$file_path")
    
    echo "Response: $response"
    
    # Extract file_id
    file_id=$(echo "$response" | jq -r '.file_id // empty')
    
    if [ -n "$file_id" ]; then
        echo "✅ Upload successful! File ID: $file_id"
        
        # Wait for processing
        echo "⏳ Waiting for processing to complete..."
        for i in {1..30}; do
            status_response=$(curl -s "${BASE_URL}/status/${file_id}")
            status=$(echo "$status_response" | jq -r '.status // empty')
            
            if [ "$status" = "completed" ]; then
                echo "✅ Processing completed!"
                chunks=$(echo "$status_response" | jq -r '.chunks_count // 0')
                echo "📊 Document split into $chunks chunks"
                break
            elif [ "$status" = "failed" ]; then
                echo "❌ Processing failed"
                echo "$status_response"
                break
            elif [ $i -eq 30 ]; then
                echo "⚠️ Processing is taking longer than expected"
                echo "Current status: $status"
                break
            fi
            
            echo "Status: $status (attempt $i/30)"
            sleep 2
        done
        
        return 0
    else
        echo "❌ Upload failed"
        return 1
    fi
}

# Function to ask a question
ask_question() {
    local question="$1"
    echo ""
    echo "❓ Asking: $question"
    
    response=$(curl -s -X POST "${RASA_URL}/webhooks/rest/webhook" \
        -H "Content-Type: application/json" \
        -d "{\"sender\": \"test_user\", \"message\": \"$question\"}")
    
    echo "$response" | jq -r '.[].text // empty' | while read -r line; do
        echo "🤖 Bot: $line"
    done
}

# Check for PDF files in sample-docs directory
echo "🔍 Looking for PDF files to upload..."

pdf_files=(sample-docs/*.pdf)
if [ ! -f "${pdf_files[0]}" ]; then
    echo ""
    echo "📝 No PDF files found in sample-docs/ directory."
    echo ""
    echo "To test the system:"
    echo "1. Add some PDF files to the sample-docs/ directory"
    echo "2. Run this script again"
    echo ""
    echo "Or upload manually:"
    echo "   curl -X POST ${BASE_URL}/upload-pdf -F 'file=@your-file.pdf'"
    echo ""
    echo "💡 You can download sample PDFs from:"
    echo "   - Research papers (arxiv.org, scholar.google.com)"
    echo "   - Documentation (any project's documentation as PDF)"
    echo "   - Convert web pages to PDF using your browser"
    exit 0
fi

# Upload found PDFs
uploaded_count=0
for pdf_file in "${pdf_files[@]}"; do
    if [ -f "$pdf_file" ]; then
        if upload_pdf "$pdf_file"; then
            ((uploaded_count++))
        fi
        echo ""
    fi
done

if [ $uploaded_count -eq 0 ]; then
    echo "❌ No PDFs were successfully uploaded"
    exit 1
fi

echo "🎉 Successfully uploaded $uploaded_count PDF(s)!"
echo ""

# List all documents
echo "📚 Current documents in knowledge base:"
curl -s "${BASE_URL}/documents" | jq -r '.documents[] | "• \(.filename) (\(.status)) - \(.chunks_count // 0) chunks"'

echo ""
echo "🧪 Testing with sample questions..."

# Sample questions
questions=(
    "Hello!"
    "List documents"
    "What topics are covered in the documents?"
    "Can you summarize the main points?"
    "What does the document say about the first topic mentioned?"
)

for question in "${questions[@]}"; do
    ask_question "$question"
    echo ""
    sleep 1
done

echo ""
echo "✨ Testing completed!"
echo ""
echo "🔧 Try your own questions:"
echo "   python3 chat.py"
echo ""
echo "🌐 Or use the API directly:"
echo "   curl -X POST ${RASA_URL}/webhooks/rest/webhook \\"
echo "        -H 'Content-Type: application/json' \\"
echo "        -d '{\"sender\": \"user\", \"message\": \"your question here\"}'"