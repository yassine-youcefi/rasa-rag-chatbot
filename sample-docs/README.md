# Sample Documents for Testing

This directory contains sample documents and scripts to help you test the RAG functionality.

## Quick Test Commands

### Upload a PDF
```bash
# Upload a PDF file
curl -X POST "http://localhost:8001/upload-pdf" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@sample-docs/your-document.pdf"
```

### Check Processing Status
```bash
# Get the file_id from upload response, then check status
curl "http://localhost:8001/status/FILE_ID_HERE"
```

### List All Documents
```bash
curl "http://localhost:8001/documents"
```

### Ask Questions
```bash
# After documents are processed, ask questions
curl -X POST "http://localhost:5005/webhooks/rest/webhook" \
     -H "Content-Type: application/json" \
     -d '{
       "sender": "test_user",
       "message": "What does the document say about artificial intelligence?"
     }'
```

## Sample Questions to Try

Once you upload PDF documents, try these questions:

- "What is machine learning?"
- "Tell me about neural networks"
- "How does deep learning work?"
- "What are the applications of AI?"
- "Explain natural language processing"
- "What does the document say about data science?"

## Creating Test PDFs

If you don't have PDF documents ready, you can:

1. **Convert text to PDF**: Use online tools to convert text documents to PDF
2. **Save web pages as PDF**: Use your browser's "Save as PDF" option
3. **Create from Word**: Save any Word document as PDF
4. **Use research papers**: Download academic papers related to your domain

## Test Scenarios

### Scenario 1: Single Document
1. Upload one PDF about a specific topic
2. Ask detailed questions about that topic
3. Verify the bot provides relevant answers with correct source attribution

### Scenario 2: Multiple Documents
1. Upload 2-3 PDFs on related topics
2. Ask questions that might span multiple documents
3. Check that sources are correctly identified

### Scenario 3: Document Management
1. Upload several documents
2. Use "list documents" to see all files
3. Use "clear all documents" to reset
4. Verify the knowledge base is properly cleared

## Troubleshooting Tests

### If PDF Upload Fails
- Check file size (must be under 50MB by default)
- Ensure file is actually a PDF
- Verify the PDF contains text (not just images)

### If Questions Return No Results
- Confirm the PDF processing completed successfully
- Try broader or simpler questions
- Check if your question relates to the document content

### If Bot Doesn't Respond
- Verify all services are running: `docker-compose ps`
- Check logs: `docker-compose logs rasa`
- Test basic greeting first: "hello"

## Interactive Testing

Use the provided chat client for easier testing:

```bash
# Start interactive chat
python3 chat.py

# Or with custom server URL
python3 chat.py http://localhost:5005 your_user_id
```