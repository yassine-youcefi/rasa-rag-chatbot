// RAG System Dashboard JavaScript
let currentDocuments = [];
let currentCollections = [];

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', function() {
    checkSystemStatus();
    loadDocuments();
    loadCollections();
    
    // Set up event listeners
    document.getElementById('chatInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendChatMessage();
        }
    });
    
    document.getElementById('searchQuery').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchDocuments();
        }
    });
    
    // Refresh data every 30 seconds
    setInterval(checkSystemStatus, 30000);
    setInterval(loadDocuments, 60000);
});

// System status check
async function checkSystemStatus() {
    try {
        const response = await fetch('/api/system-status');
        const status = await response.json();
        
        let overallStatus = 'healthy';
        let healthyCount = 0;
        let totalCount = Object.keys(status).length;
        
        for (const [service, info] of Object.entries(status)) {
            if (info.status === 'healthy') {
                healthyCount++;
            } else if (info.status === 'error' || info.status === 'unhealthy') {
                overallStatus = 'unhealthy';
            }
        }
        
        if (healthyCount === 0) {
            overallStatus = 'unhealthy';
        } else if (healthyCount < totalCount) {
            overallStatus = 'partial';
        }
        
        const statusElement = document.getElementById('system-status');
        statusElement.className = `badge bg-${getStatusColor(overallStatus)}`;
        statusElement.textContent = `${healthyCount}/${totalCount} Services Healthy`;
    } catch (error) {
        console.error('Failed to check system status:', error);
        const statusElement = document.getElementById('system-status');
        statusElement.className = 'badge bg-danger';
        statusElement.textContent = 'Status Unknown';
    }
}

function getStatusColor(status) {
    switch(status) {
        case 'healthy': return 'success';
        case 'partial': return 'warning';
        case 'unhealthy': return 'danger';
        default: return 'secondary';
    }
}

// Load documents
async function loadDocuments() {
    try {
        const response = await fetch('/api/documents');
        const data = await response.json();
        currentDocuments = data.documents || [];
        renderDocuments();
    } catch (error) {
        console.error('Failed to load documents:', error);
        document.getElementById('documentsContainer').innerHTML = 
            '<div class="alert alert-danger">Failed to load documents</div>';
    }
}

function renderDocuments() {
    const container = document.getElementById('documentsContainer');
    
    if (currentDocuments.length === 0) {
        container.innerHTML = `
            <div class="text-center text-muted p-4">
                <i class="fas fa-file-pdf fa-3x mb-3"></i>
                <p>No documents uploaded yet</p>
                <small>Upload a PDF file to get started</small>
            </div>
        `;
        return;
    }
    
    const documentsHtml = currentDocuments.map(doc => `
        <div class="card document-card mb-3">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h6 class="mb-0">
                    <i class="fas fa-file-pdf text-danger"></i> ${doc.filename}
                </h6>
                <div>
                    <span class="badge ${getDocumentStatusColor(doc.status)} status-badge me-2">
                        ${doc.status}
                    </span>
                    <button class="btn btn-sm btn-outline-danger" onclick="deleteDocument('${doc.file_id}')">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-6">
                        <small class="text-muted">File ID:</small><br>
                        <code>${doc.file_id}</code>
                    </div>
                    <div class="col-md-6">
                        <small class="text-muted">Upload Time:</small><br>
                        ${formatDate(doc.upload_time)}
                    </div>
                </div>
                ${doc.chunks ? `
                    <div class="mt-2">
                        <small class="text-muted">Chunks: <strong>${doc.chunks}</strong></small>
                    </div>
                ` : ''}
                ${doc.processing_time ? `
                    <div class="mt-1">
                        <small class="text-muted">Processing Time: <strong>${doc.processing_time}</strong></small>
                    </div>
                ` : ''}
            </div>
        </div>
    `).join('');
    
    container.innerHTML = documentsHtml;
}

function getDocumentStatusColor(status) {
    switch(status) {
        case 'completed': return 'bg-success';
        case 'processing': return 'bg-warning';
        case 'failed': return 'bg-danger';
        default: return 'bg-secondary';
    }
}

// Load ChromaDB collections
async function loadCollections() {
    try {
        const response = await fetch('/api/collections');
        const data = await response.json();
        currentCollections = data.collections || [];
        renderCollections();
    } catch (error) {
        console.error('Failed to load collections:', error);
        document.getElementById('collectionsContainer').innerHTML = 
            '<div class="alert alert-danger">Failed to load collections</div>';
    }
}

function renderCollections() {
    const container = document.getElementById('collectionsContainer');
    
    if (currentCollections.length === 0) {
        container.innerHTML = `
            <div class="text-center text-muted p-4">
                <i class="fas fa-database fa-3x mb-3"></i>
                <p>No collections found</p>
                <small>Collections will appear after uploading documents</small>
            </div>
        `;
        return;
    }
    
    const collectionsHtml = currentCollections.map(collection => `
        <div class="card collection-card mb-3">
            <div class="card-header">
                <h6 class="mb-0">
                    <i class="fas fa-database text-primary"></i> ${collection.name}
                    <button class="btn btn-sm btn-outline-info float-end" onclick="viewCollection('${collection.name}')">
                        <i class="fas fa-eye"></i> View Details
                    </button>
                </h6>
            </div>
            <div class="card-body">
                <div class="collection-stats">
                    <span class="stat-item">
                        <i class="fas fa-file"></i> ${collection.count} documents
                    </span>
                    <span class="stat-item">
                        <i class="fas fa-tag"></i> ID: ${collection.id}
                    </span>
                </div>
                
                ${collection.error ? `
                    <div class="alert alert-warning mt-2">
                        <small><strong>Error:</strong> ${collection.error}</small>
                    </div>
                ` : ''}
                
                ${collection.sample_documents && collection.sample_documents.length > 0 ? `
                    <div class="mt-3">
                        <small class="text-muted">Sample Documents:</small>
                        <div class="document-content">
                            ${collection.sample_documents.slice(0, 2).map(doc => 
                                `<div class="border-bottom pb-1 mb-1"><small>${doc.substring(0, 200)}...</small></div>`
                            ).join('')}
                        </div>
                    </div>
                ` : ''}
            </div>
        </div>
    `).join('');
    
    container.innerHTML = collectionsHtml;
}

// View collection details
async function viewCollection(collectionName) {
    try {
        const response = await fetch(`/api/collection/${collectionName}?limit=20`);
        const data = await response.json();
        
        const modalHtml = `
            <div class="modal fade" id="collectionModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-database"></i> Collection: ${data.name}
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="mb-3">
                                <span class="badge bg-info">Total Documents: ${data.count}</span>
                                <span class="badge bg-secondary">Has Embeddings: ${data.has_embeddings ? 'Yes' : 'No'}</span>
                            </div>
                            
                            <div class="table-responsive">
                                <table class="table table-sm">
                                    <thead>
                                        <tr>
                                            <th>ID</th>
                                            <th>Content</th>
                                            <th>Metadata</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${data.documents.map((doc, index) => `
                                            <tr>
                                                <td><code>${data.ids[index]}</code></td>
                                                <td>
                                                    <div class="chunk-text">
                                                        ${doc.substring(0, 200)}...
                                                    </div>
                                                </td>
                                                <td>
                                                    <small>${JSON.stringify(data.metadatas[index] || {}, null, 2)}</small>
                                                </td>
                                            </tr>
                                        `).join('')}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Remove existing modal if any
        const existingModal = document.getElementById('collectionModal');
        if (existingModal) {
            existingModal.remove();
        }
        
        // Add new modal
        document.body.insertAdjacentHTML('beforeend', modalHtml);
        const modal = new bootstrap.Modal(document.getElementById('collectionModal'));
        modal.show();
        
    } catch (error) {
        console.error('Failed to load collection details:', error);
        alert('Failed to load collection details');
    }
}

// File upload
async function uploadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a file to upload');
        return;
    }
    
    if (!file.type.includes('pdf')) {
        alert('Please select a PDF file');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    const statusDiv = document.getElementById('uploadStatus');
    statusDiv.innerHTML = '<div class="alert alert-info"><i class="fas fa-spinner fa-spin"></i> Uploading...</div>';
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            statusDiv.innerHTML = '<div class="alert alert-success"><i class="fas fa-check"></i> Upload successful!</div>';
            fileInput.value = '';
            
            // Refresh documents after a delay
            setTimeout(() => {
                loadDocuments();
                statusDiv.innerHTML = '';
            }, 2000);
        } else {
            throw new Error(result.detail || 'Upload failed');
        }
    } catch (error) {
        console.error('Upload failed:', error);
        statusDiv.innerHTML = `<div class="alert alert-danger"><i class="fas fa-exclamation-triangle"></i> ${error.message}</div>`;
    }
}

// Search documents
async function searchDocuments() {
    const query = document.getElementById('searchQuery').value.trim();
    if (!query) {
        alert('Please enter a search query');
        return;
    }
    
    const resultsContainer = document.getElementById('searchResultsContainer');
    resultsContainer.innerHTML = '<div class="text-center"><i class="fas fa-spinner fa-spin"></i> Searching...</div>';
    
    // Switch to search results tab
    const searchTab = new bootstrap.Tab(document.getElementById('search-results-tab'));
    searchTab.show();
    
    try {
        const response = await fetch(`/api/search?query=${encodeURIComponent(query)}&limit=10`);
        const data = await response.json();
        
        if (data.results && data.results.length > 0) {
            const resultsHtml = data.results.map((result, index) => `
                <div class="card search-result mb-3">
                    <div class="card-body">
                        <h6 class="card-title">
                            <i class="fas fa-search text-success"></i> Result ${index + 1}
                            <span class="badge bg-info float-end">Score: ${result.score?.toFixed(3) || 'N/A'}</span>
                        </h6>
                        <div class="chunk-text mb-2">${result.content}</div>
                        <div class="metadata-info">
                            <small class="text-muted">
                                <strong>Source:</strong> ${result.metadata?.filename || 'Unknown'} |
                                <strong>Chunk:</strong> ${result.metadata?.chunk_index || 'N/A'}
                            </small>
                        </div>
                    </div>
                </div>
            `).join('');
            
            resultsContainer.innerHTML = `
                <div class="mb-3">
                    <h5>Search Results for: "${query}"</h5>
                    <span class="badge bg-success">${data.results.length} results found</span>
                </div>
                ${resultsHtml}
            `;
        } else {
            resultsContainer.innerHTML = `
                <div class="text-center text-muted p-4">
                    <i class="fas fa-search fa-2x mb-3"></i>
                    <p>No results found for "${query}"</p>
                    <small>Try different keywords or upload relevant documents</small>
                </div>
            `;
        }
    } catch (error) {
        console.error('Search failed:', error);
        resultsContainer.innerHTML = '<div class="alert alert-danger">Search failed</div>';
    }
}

// Chat functionality
async function sendChatMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    
    if (!message) return;
    
    const messagesContainer = document.getElementById('chatMessages');
    
    // Add user message
    addChatMessage(message, 'user');
    input.value = '';
    
    // Add loading message
    const loadingId = 'loading-' + Date.now();
    addChatMessage('<i class="fas fa-spinner fa-spin"></i> Thinking...', 'bot', loadingId);
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: `message=${encodeURIComponent(message)}`
        });
        
        const data = await response.json();
        
        // Remove loading message
        document.getElementById(loadingId)?.remove();
        
        if (data.responses && data.responses.length > 0) {
            data.responses.forEach(response => {
                addChatMessage(response.text || response.message || 'No response', 'bot');
            });
        } else {
            addChatMessage('Sorry, I could not process your message.', 'bot');
        }
    } catch (error) {
        console.error('Chat failed:', error);
        document.getElementById(loadingId)?.remove();
        addChatMessage('Sorry, there was an error processing your message.', 'bot');
    }
}

function addChatMessage(message, sender, id = null) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${sender}`;
    if (id) messageDiv.id = id;
    messageDiv.innerHTML = message;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Delete document
async function deleteDocument(fileId) {
    if (!confirm('Are you sure you want to delete this document?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/documents/${fileId}`, {method: 'DELETE'});
        
        if (response.ok) {
            alert('Document deleted successfully');
            loadDocuments();
            loadCollections();
        } else {
            throw new Error('Delete failed');
        }
    } catch (error) {
        console.error('Delete failed:', error);
        alert('Failed to delete document');
    }
}

// Clear all documents
async function clearAllDocuments() {
    if (!confirm('Are you sure you want to clear ALL documents? This cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch('/api/collections/clear', {method: 'DELETE'});
        
        if (response.ok) {
            alert('All documents cleared successfully');
            loadDocuments();
            loadCollections();
        } else {
            throw new Error('Clear failed');
        }
    } catch (error) {
        console.error('Clear failed:', error);
        alert('Failed to clear documents');
    }
}

// Utility functions
function formatDate(dateString) {
    if (!dateString) return 'Unknown';
    return new Date(dateString).toLocaleString();
}