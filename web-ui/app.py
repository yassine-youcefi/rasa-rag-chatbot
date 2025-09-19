#!/usr/bin/env python3
"""
RAG System Web UI - Document Management and Visualization Interface
Provides a web interface to view documents, collections, and interact with the RAG system
"""

from fastapi import FastAPI, Request, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import os
import asyncio
import chromadb
from typing import List, Dict, Any
import json
from datetime import datetime

app = FastAPI(title="RAG System UI", description="Web interface for RAG document management")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Configuration
PDF_PROCESSOR_URL = os.getenv("PDF_PROCESSOR_URL", "http://localhost:8001")
RASA_SERVER_URL = os.getenv("RASA_SERVER_URL", "http://localhost:5005")
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main dashboard with document overview"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/api/documents")
async def get_documents():
    """Get all documents from PDF processor"""
    try:
        response = requests.get(f"{PDF_PROCESSOR_URL}/documents")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch documents: {str(e)}")

@app.get("/api/collections")
async def get_chroma_collections():
    """Get ChromaDB collections information"""
    try:
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        collections = client.list_collections()
        
        collections_info = []
        for collection in collections:
            try:
                coll_obj = client.get_collection(collection.name)
                count = coll_obj.count()
                
                # Get some sample documents
                samples = coll_obj.peek(limit=3)
                
                collections_info.append({
                    "name": collection.name,
                    "id": collection.id,
                    "count": count,
                    "metadata": collection.metadata or {},
                    "sample_documents": samples.get("documents", [])[:3] if samples else []
                })
            except Exception as e:
                collections_info.append({
                    "name": collection.name,
                    "id": collection.id,
                    "count": "Error",
                    "metadata": {},
                    "sample_documents": [],
                    "error": str(e)
                })
        
        return {"collections": collections_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch collections: {str(e)}")

@app.get("/api/collection/{collection_name}")
async def get_collection_details(collection_name: str, limit: int = 50):
    """Get detailed information about a specific collection"""
    try:
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        collection = client.get_collection(collection_name)
        
        # Get documents with metadata
        results = collection.get(limit=limit, include=["documents", "metadatas", "embeddings"])
        
        return {
            "name": collection_name,
            "count": collection.count(),
            "documents": results.get("documents", []),
            "metadatas": results.get("metadatas", []),
            "ids": results.get("ids", []),
            "has_embeddings": len(results.get("embeddings", [])) > 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch collection details: {str(e)}")

@app.get("/api/search")
async def search_documents(query: str, limit: int = 10):
    """Search documents using the PDF processor API"""
    try:
        response = requests.get(f"{PDF_PROCESSOR_URL}/search", params={"query": query, "limit": limit})
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a document via the PDF processor"""
    try:
        files = {"file": (file.filename, file.file, file.content_type)}
        response = requests.post(f"{PDF_PROCESSOR_URL}/upload-pdf", files=files)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/api/chat")
async def chat_with_rasa(message: str):
    """Send message to Rasa chatbot"""
    try:
        payload = {
            "sender": "web-ui-user",
            "message": message
        }
        response = requests.post(f"{RASA_SERVER_URL}/webhooks/rest/webhook", json=payload)
        response.raise_for_status()
        return {"responses": response.json()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@app.delete("/api/documents/{file_id}")
async def delete_document(file_id: str):
    """Delete a document"""
    try:
        response = requests.delete(f"{PDF_PROCESSOR_URL}/documents/{file_id}")
        response.raise_for_status()
        return {"message": "Document deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")

@app.delete("/api/collections/clear")
async def clear_all_documents():
    """Clear all documents from the knowledge base"""
    try:
        response = requests.delete(f"{PDF_PROCESSOR_URL}/clear-knowledge-base")
        response.raise_for_status()
        return {"message": "Knowledge base cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clear failed: {str(e)}")

@app.get("/api/system-status")
async def get_system_status():
    """Get overall system health status"""
    services = {
        "pdf_processor": {"url": f"{PDF_PROCESSOR_URL}/health", "status": "unknown"},
        "rasa_server": {"url": f"{RASA_SERVER_URL}/", "status": "unknown"},
        "chroma_db": {"url": f"http://{CHROMA_HOST}:{CHROMA_PORT}/api/v1/heartbeat", "status": "unknown"}
    }
    
    # Check each service
    for service_name, service_info in services.items():
        try:
            response = requests.get(service_info["url"], timeout=5)
            if response.status_code == 200:
                services[service_name]["status"] = "healthy"
                services[service_name]["response"] = response.json() if service_name != "rasa_server" else "OK"
            else:
                services[service_name]["status"] = "unhealthy"
        except Exception as e:
            services[service_name]["status"] = "error"
            services[service_name]["error"] = str(e)
    
    return services

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002, reload=True)