from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import chromadb
from chromadb.config import Settings
import redis
import os
import logging
import uuid
import aiofiles
from typing import List, Dict, Any
from pdf_processor import PDFProcessor
from embeddings import EmbeddingManager
import httpx
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="PDF Processing Service", version="1.0.0")

# Configuration
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
UPLOAD_DIR = "/app/uploads"
COLLECTION_NAME = "pdf_documents"

# Initialize ChromaDB client (for vector embeddings) - will be initialized on startup
chroma_client = None
redis_client = None
embedding_manager = None
pdf_processor = None

@app.on_event("startup")
async def startup_event():
    """Initialize all services on startup with proper retries"""
    global chroma_client, redis_client, embedding_manager, pdf_processor
    
    # Initialize Redis client
    try:
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        redis_client.ping()
        logger.info(f"Redis client initialized: {REDIS_HOST}:{REDIS_PORT}")
    except Exception as e:
        logger.error(f"Failed to initialize Redis client: {e}")
        raise
    
    # Initialize PDF processor
    try:
        pdf_processor = PDFProcessor()
        logger.info("PDF processor initialized")
    except Exception as e:
        logger.error(f"Failed to initialize PDF processor: {e}")
        raise
    
    # Initialize embedding manager  
    try:
        embedding_manager = EmbeddingManager()
        logger.info("Embedding manager initialized")
    except Exception as e:
        logger.error(f"Failed to initialize embedding manager: {e}")
        raise
    
    # Initialize ChromaDB client with retries
    retries = 10
    for attempt in range(retries):
        try:
            chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
            # Test connection
            chroma_client.heartbeat()
            logger.info(f"ChromaDB client initialized: {CHROMA_HOST}:{CHROMA_PORT}")
            break
        except Exception as e:
            if attempt == retries - 1:
                logger.error(f"Failed to initialize ChromaDB client after {retries} attempts: {e}")
                raise
            else:
                logger.warning(f"Failed to initialize ChromaDB client (attempt {attempt + 1}/{retries}): {e}")
                await asyncio.sleep(2)
    
    # Initialize collection with retries
    for attempt in range(retries):
        try:
            collection = chroma_client.get_or_create_collection(
                name=COLLECTION_NAME,
                metadata={"description": "PDF document embeddings for RAG"}
            )
            logger.info(f"Collection '{COLLECTION_NAME}' ready")
            return
        except Exception as e:
            if attempt == retries - 1:
                logger.error(f"Failed to initialize collection after {retries} attempts: {e}")
                raise
            else:
                logger.warning(f"Failed to initialize collection (attempt {attempt + 1}/{retries}): {e}")
                await asyncio.sleep(2)

@app.get("/")
async def root():
    return {"message": "PDF Processing Service is running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check ChromaDB
        chroma_client.heartbeat()
        
        # Check Redis
        redis_client.ping()
        
        return {"status": "healthy", "services": {"chroma": "ok", "redis": "ok"}}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "error": str(e)}

@app.post("/upload-pdf")
async def upload_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """Upload and process a PDF file"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        # Generate unique file ID
        file_id = str(uuid.uuid4())
        filename = f"{file_id}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        # Save uploaded file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Store processing status in Redis
        redis_client.hset(f"pdf:{file_id}", mapping={
            "filename": file.filename,
            "status": "processing",
            "file_path": file_path
        })
        
        # Add background task to process PDF
        background_tasks.add_task(process_pdf_background, file_id, file_path, file.filename)
        
        return JSONResponse(content={
            "file_id": file_id,
            "filename": file.filename,
            "status": "processing",
            "message": "PDF uploaded successfully and is being processed"
        })
        
    except Exception as e:
        logger.error(f"Error uploading PDF: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to upload PDF: {str(e)}")

async def process_pdf_background(file_id: str, file_path: str, filename: str):
    """Background task to process PDF and create embeddings"""
    try:
        logger.info(f"Starting to process PDF: {filename}")
        
        # Extract text from PDF
        text_chunks = pdf_processor.extract_and_chunk_text(file_path)
        
        if not text_chunks:
            redis_client.hset(f"pdf:{file_id}", "status", "failed")
            redis_client.hset(f"pdf:{file_id}", "error", "No text found in PDF")
            return
        
        # Generate embeddings
        embeddings = embedding_manager.generate_embeddings(text_chunks)
        
        # Store in ChromaDB
        collection = chroma_client.get_collection(COLLECTION_NAME)
        
        # Prepare data for ChromaDB
        ids = [f"{file_id}_{i}" for i in range(len(text_chunks))]
        metadatas = [{"file_id": file_id, "filename": filename, "chunk_id": i} 
                    for i in range(len(text_chunks))]
        
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=text_chunks,
            metadatas=metadatas
        )
        
        # Update status in Redis
        redis_client.hset(f"pdf:{file_id}", mapping={
            "status": "completed",
            "chunks_count": len(text_chunks)
        })
        
        logger.info(f"Successfully processed PDF: {filename} ({len(text_chunks)} chunks)")
        
    except Exception as e:
        logger.error(f"Error processing PDF {filename}: {e}")
        redis_client.hset(f"pdf:{file_id}", "status", "failed")
        redis_client.hset(f"pdf:{file_id}", "error", str(e))

@app.get("/status/{file_id}")
async def get_processing_status(file_id: str):
    """Get processing status of a PDF file"""
    try:
        status_data = redis_client.hgetall(f"pdf:{file_id}")
        if not status_data:
            raise HTTPException(status_code=404, detail="File not found")
        
        return status_data
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/search")
async def search_documents(query: str, max_results: int = 5):
    """Search through processed documents"""
    try:
        # Generate query embedding
        query_embedding = embedding_manager.generate_embeddings([query])[0]
        
        # Search in ChromaDB
        collection = chroma_client.get_collection(COLLECTION_NAME)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=max_results
        )
        
        if not results["documents"][0]:
            return {"results": [], "message": "No relevant documents found"}
        
        # Format results
        formatted_results = []
        for i in range(len(results["documents"][0])):
            formatted_results.append({
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i] if results["distances"] else None
            })
        
        return {"results": formatted_results, "query": query}
        
    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def list_documents():
    """List all processed documents"""
    try:
        # Get all unique file IDs from Redis
        keys = redis_client.keys("pdf:*")
        documents = []
        
        for key in keys:
            doc_data = redis_client.hgetall(key)
            if doc_data:
                documents.append({
                    "file_id": key.split(":")[1],
                    "filename": doc_data.get("filename"),
                    "status": doc_data.get("status"),
                    "chunks_count": doc_data.get("chunks_count", 0)
                })
        
        return {"documents": documents}
        
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/documents/{file_id}")
async def delete_document(file_id: str):
    """Delete a document and its embeddings"""
    try:
        # Check if document exists
        doc_data = redis_client.hgetall(f"pdf:{file_id}")
        if not doc_data:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Delete from ChromaDB
        collection = chroma_client.get_collection(COLLECTION_NAME)
        
        # Get all chunk IDs for this file
        results = collection.get(where={"file_id": file_id})
        if results["ids"]:
            collection.delete(ids=results["ids"])
        
        # Delete from Redis
        redis_client.delete(f"pdf:{file_id}")
        
        # Delete file from filesystem
        file_path = doc_data.get("file_path")
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        
        return {"message": f"Document {file_id} deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/documents")
async def clear_all_documents():
    """Clear all documents from the knowledge base"""
    try:
        # Reset ChromaDB collection
        chroma_client.delete_collection(COLLECTION_NAME)
        chroma_client.create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "PDF document embeddings for RAG"}
        )
        
        # Clear Redis
        keys = redis_client.keys("pdf:*")
        if keys:
            redis_client.delete(*keys)
        
        # Clear upload directory
        for filename in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        return {"message": "All documents cleared successfully"}
        
    except Exception as e:
        logger.error(f"Error clearing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)