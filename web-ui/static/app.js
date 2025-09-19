// Sipsty AI Dashboard - Enhanced JavaScript
class SipstyDashboard {
    constructor() {
        this.currentDocuments = [];
        this.currentCollections = [];
        this.chatHistory = [];
        this.searchResults = [];
        this.systemStatus = {};
        this.refreshInterval = 10000; // 10 seconds
        this.languages = { en: 0, fr: 0, ar: 0 };
        this.messagesCount = 0;
        
        this.init();
    }

    // Initialize dashboard
    async init() {
        console.log('🚀 Initializing Sipsty AI Dashboard...');
        
        // Set up event listeners
        this.setupEventListeners();
        
        // Load initial data
        await this.loadInitialData();
        
        // Start real-time updates
        this.startRealTimeUpdates();
        
        // Setup drag & drop
        this.setupDragAndDrop();
        
        console.log('✅ Dashboard initialized successfully!');
    }

    // Event listeners setup
    setupEventListeners() {
        // Chat functionality
        const chatInput = document.getElementById('chat-input');
        if (chatInput) {
            chatInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    this.sendMessage();
                }
            });
        }

        // Search functionality
        const searchQuery = document.getElementById('searchQuery');
        if (searchQuery) {
            searchQuery.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    this.performSearch();
                }
            });
        }

        // File input
        const fileInput = document.getElementById('fileInput');
        if (fileInput) {
            fileInput.addEventListener('change', (e) => {
                this.handleFileUpload(e.target.files);
            });
        }

        // Tab switching
        document.querySelectorAll('[data-bs-toggle="tab"]').forEach(tab => {
            tab.addEventListener('shown.bs.tab', (e) => {
                this.onTabSwitch(e.target.getAttribute('data-bs-target'));
            });
        });
    }

    // Drag and drop setup
    setupDragAndDrop() {
        const uploadArea = document.getElementById('uploadArea');
        if (!uploadArea) return;

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            });
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.add('drag-active');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.remove('drag-active');
            });
        });

        uploadArea.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            this.handleFileUpload(files);
        });

        // Make upload area clickable
        uploadArea.addEventListener('click', () => {
            document.getElementById('fileInput').click();
        });
    }

    // Load initial data
    async loadInitialData() {
        const loadingPromises = [
            this.checkSystemStatus(),
            this.loadDocuments(),
            this.loadCollections(),
            this.loadActivityFeed(),
            this.loadAnalytics()
        ];

        await Promise.all(loadingPromises);
    }

    // Real-time updates
    startRealTimeUpdates() {
        // System status updates
        setInterval(() => this.checkSystemStatus(), this.refreshInterval);
        
        // Connection indicator
        this.updateConnectionIndicator();
        setInterval(() => this.updateConnectionIndicator(), 5000);
    }

    // Connection indicator
    updateConnectionIndicator() {
        const indicator = document.getElementById('connection-indicator');
        if (indicator) {
            indicator.className = 'fas fa-circle-dot text-success';
            setTimeout(() => {
                indicator.className = 'fas fa-circle text-success';
            }, 200);
        }
    }

    // System status check
    async checkSystemStatus() {
        try {
            const response = await fetch('/api/system-status');
            const status = await response.json();
            this.systemStatus = status;
            
            let healthyCount = 0;
            let totalCount = Object.keys(status).length;
            
            // Count healthy services
            Object.values(status).forEach(service => {
                if (service.status === 'healthy') healthyCount++;
            });
            
            // Update status badge
            const badge = document.getElementById('system-status-badge');
            if (badge) {
                const statusText = `${healthyCount}/${totalCount} Services`;
                const statusClass = healthyCount === totalCount ? 'status-healthy' : 
                                   healthyCount > 0 ? 'status-warning' : 'status-unhealthy';
                
                badge.className = `status-badge ${statusClass}`;
                badge.innerHTML = `<i class="fas fa-heartbeat me-1"></i><span>${statusText}</span>`;
            }
            
            // Update system status grid
            this.updateSystemStatusGrid(status);
            
        } catch (error) {
            console.error('Failed to check system status:', error);
            this.showNotification('System status check failed', 'error');
        }
    }

    // Update system status grid
    updateSystemStatusGrid(status) {
        const grid = document.getElementById('system-status-grid');
        if (!grid) return;

        const services = [
            { key: 'rasa', name: 'Rasa Server', icon: 'fas fa-robot', port: '5005' },
            { key: 'pdf_processor', name: 'PDF Processor', icon: 'fas fa-file-pdf', port: '8000' },
            { key: 'chromadb', name: 'ChromaDB', icon: 'fas fa-database', port: '8003' },
            { key: 'redis', name: 'Redis Cache', icon: 'fas fa-memory', port: '6379' },
            { key: 'action_server', name: 'Action Server', icon: 'fas fa-cogs', port: '5055' },
            { key: 'web_ui', name: 'Web UI', icon: 'fas fa-globe', port: '8002' }
        ];

        grid.innerHTML = services.map(service => {
            const serviceStatus = status[service.key] || { status: 'unknown' };
            const statusClass = serviceStatus.status === 'healthy' ? 'status-healthy' : 
                               serviceStatus.status === 'error' ? 'status-unhealthy' : 'status-unknown';
            
            return `
                <div class="col-lg-4 col-md-6">
                    <div class="card service-status-card">
                        <div class="card-body text-center">
                            <i class="${service.icon} fa-2x mb-2 text-primary"></i>
                            <h6 class="card-title">${service.name}</h6>
                            <div class="status-badge ${statusClass}">
                                ${serviceStatus.status}
                            </div>
                            <div class="small text-muted mt-1">:${service.port}</div>
                            ${serviceStatus.response_time ? `<div class="small text-muted">${serviceStatus.response_time}ms</div>` : ''}
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    // Load documents
    async loadDocuments() {
        try {
            const response = await fetch('/api/documents');
            this.currentDocuments = await response.json();
            this.renderDocuments();
        } catch (error) {
            console.error('Failed to load documents:', error);
            this.showNotification('Failed to load documents', 'error');
        }
    }

    // Render documents
    renderDocuments() {
        const container = document.getElementById('documents-list');
        if (!container) return;

        if (this.currentDocuments.length === 0) {
            container.innerHTML = `
                <div class="col-12">
                    <div class="text-center text-muted py-5">
                        <i class="fas fa-folder-open fa-3x mb-3 opacity-50"></i>
                        <h6>No documents uploaded yet</h6>
                        <p class="small">Upload your first PDF to get started</p>
                    </div>
                </div>
            `;
            return;
        }

        container.innerHTML = this.currentDocuments.map(doc => `
            <div class="col-lg-6">
                <div class="document-card animate-bounce-in">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h6 class="card-title text-truncate">${doc.filename}</h6>
                        <div class="status-badge status-healthy">
                            <i class="fas fa-check me-1"></i>Ready
                        </div>
                    </div>
                    <div class="document-stats mb-3">
                        <div class="row g-2 text-center">
                            <div class="col-4">
                                <div class="small text-muted">Chunks</div>
                                <div class="fw-bold">${doc.chunks || 0}</div>
                            </div>
                            <div class="col-4">
                                <div class="small text-muted">Size</div>
                                <div class="fw-bold">${this.formatFileSize(doc.size || 0)}</div>
                            </div>
                            <div class="col-4">
                                <div class="small text-muted">Uploaded</div>
                                <div class="fw-bold">${this.formatDate(doc.uploaded_at || new Date())}</div>
                            </div>
                        </div>
                    </div>
                    <div class="d-flex gap-2">
                        <button class="btn btn-sm btn-outline-light flex-fill" onclick="dashboard.searchDocuments('${doc.filename}')">
                            <i class="fas fa-search me-1"></i>Search
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="dashboard.deleteDocument('${doc.filename}')">
                            <i class="fas fa-trash me-1"></i>Delete
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    // Handle file upload
    async handleFileUpload(files) {
        if (!files || files.length === 0) return;

        const progressContainer = document.getElementById('upload-progress');
        const resultsContainer = document.getElementById('upload-results');
        const progressBar = document.getElementById('progress-bar');
        const statusSpan = document.getElementById('upload-status');
        const percentageSpan = document.getElementById('upload-percentage');

        progressContainer.style.display = 'block';
        resultsContainer.innerHTML = '';

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            
            if (!file.type.includes('pdf')) {
                this.showNotification(`${file.name} is not a PDF file`, 'error');
                continue;
            }

            try {
                statusSpan.textContent = `Uploading ${file.name}...`;
                progressBar.style.width = '0%';
                percentageSpan.textContent = '0%';

                const formData = new FormData();
                formData.append('file', file);

                const xhr = new XMLHttpRequest();
                
                // Progress tracking
                xhr.upload.addEventListener('progress', (e) => {
                    if (e.lengthComputable) {
                        const percentComplete = (e.loaded / e.total) * 100;
                        progressBar.style.width = percentComplete + '%';
                        percentageSpan.textContent = Math.round(percentComplete) + '%';
                    }
                });

                const uploadPromise = new Promise((resolve, reject) => {
                    xhr.onload = () => {
                        if (xhr.status === 200) {
                            resolve(JSON.parse(xhr.responseText));
                        } else {
                            reject(new Error(`Upload failed: ${xhr.statusText}`));
                        }
                    };
                    xhr.onerror = () => reject(new Error('Upload failed'));
                });

                xhr.open('POST', '/api/upload-pdf');
                xhr.send(formData);

                const result = await uploadPromise;
                
                resultsContainer.innerHTML += `
                    <div class="alert alert-success alert-dismissible fade show">
                        <i class="fas fa-check-circle me-2"></i>
                        <strong>${file.name}</strong> uploaded successfully!
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                `;

                this.showNotification(`${file.name} uploaded successfully!`, 'success');

            } catch (error) {
                console.error(`Upload failed for ${file.name}:`, error);
                resultsContainer.innerHTML += `
                    <div class="alert alert-danger alert-dismissible fade show">
                        <i class="fas fa-exclamation-circle me-2"></i>
                        <strong>${file.name}</strong> upload failed: ${error.message}
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    </div>
                `;
                this.showNotification(`Upload failed: ${error.message}`, 'error');
            }
        }

        progressContainer.style.display = 'none';
        await this.loadDocuments();
    }

    // Enhanced search functionality
    async performSearch() {
        const query = document.getElementById('searchQuery')?.value.trim();
        if (!query) {
            this.showNotification('Please enter a search query', 'warning');
            return;
        }

        const loadingIndicator = document.getElementById('search-loading');
        const resultsContainer = document.getElementById('search-results');
        const countBadge = document.getElementById('search-results-count');

        // Show loading state
        loadingIndicator.style.display = 'block';
        resultsContainer.innerHTML = '<div class="text-center py-4"><div class="loading-spinner"></div><p class="mt-2">Searching...</p></div>';

        try {
            // Get search filters
            const language = document.getElementById('searchLanguage')?.value || '';
            const limit = parseInt(document.getElementById('searchLimit')?.value) || 10;
            const sort = document.getElementById('searchSort')?.value || 'score';

            const params = new URLSearchParams({
                query,
                limit: limit.toString(),
                ...(language && { language }),
                ...(sort && { sort })
            });

            const response = await fetch(`/api/search?${params}`);
            const results = await response.json();
            
            this.searchResults = results;
            this.renderSearchResults(results);
            
            // Update count badge
            countBadge.textContent = results.length;
            countBadge.style.display = results.length > 0 ? 'inline' : 'none';

            this.showNotification(`Found ${results.length} results`, 'info');

        } catch (error) {
            console.error('Search failed:', error);
            resultsContainer.innerHTML = `
                <div class="text-center text-danger py-4">
                    <i class="fas fa-exclamation-triangle fa-2x mb-3"></i>
                    <h6>Search Failed</h6>
                    <p class="small">${error.message}</p>
                </div>
            `;
            this.showNotification('Search failed', 'error');
        } finally {
            loadingIndicator.style.display = 'none';
        }
    }

    // Render search results with enhanced display
    renderSearchResults(results) {
        const container = document.getElementById('search-results');
        if (!container) return;

        if (results.length === 0) {
            container.innerHTML = `
                <div class="text-center text-muted py-4">
                    <i class="fas fa-search fa-2x mb-3 opacity-50"></i>
                    <h6>No results found</h6>
                    <p class="small">Try different keywords or check your spelling</p>
                </div>
            `;
            return;
        }

        container.innerHTML = results.map((result, index) => `
            <div class="search-result" style="animation-delay: ${index * 0.1}s">
                <div class="search-result-score">${(result.score * 100).toFixed(1)}%</div>
                
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <h6 class="mb-1">
                        <i class="fas fa-file-pdf me-2 text-danger"></i>
                        ${result.document || 'Unknown Document'}
                    </h6>
                    <div class="badge bg-primary">${result.chunk_id || 'N/A'}</div>
                </div>
                
                <div class="search-result-content mb-3">
                    <p class="mb-2">${this.highlightSearchTerms(result.content, document.getElementById('searchQuery').value)}</p>
                </div>
                
                <div class="search-result-metadata">
                    <div class="row g-2">
                        <div class="col-md-4">
                            <small class="text-muted">
                                <i class="fas fa-hashtag me-1"></i>
                                Chunk: ${result.chunk_id || 'N/A'}
                            </small>
                        </div>
                        <div class="col-md-4">
                            <small class="text-muted">
                                <i class="fas fa-ruler me-1"></i>
                                Length: ${result.content?.length || 0} chars
                            </small>
                        </div>
                        <div class="col-md-4">
                            <small class="text-muted">
                                <i class="fas fa-chart-bar me-1"></i>
                                Relevance: ${(result.score * 100).toFixed(1)}%
                            </small>
                        </div>
                    </div>
                </div>
                
                <div class="d-flex gap-2 mt-3">
                    <button class="btn btn-sm btn-outline-light" onclick="dashboard.viewFullDocument('${result.document}')">
                        <i class="fas fa-eye me-1"></i>View Document
                    </button>
                    <button class="btn btn-sm btn-outline-light" onclick="dashboard.askAboutResult('${result.content}')">
                        <i class="fas fa-question me-1"></i>Ask About This
                    </button>
                    <button class="btn btn-sm btn-outline-light" onclick="dashboard.copyToClipboard(\`${result.content.replace(/`/g, '\\`')}\`)">
                        <i class="fas fa-copy me-1"></i>Copy
                    </button>
                </div>
            </div>
        `).join('');
    }

    // Highlight search terms in results
    highlightSearchTerms(text, searchQuery) {
        if (!searchQuery) return text;
        
        const terms = searchQuery.split(' ').filter(term => term.length > 2);
        let highlightedText = text;
        
        terms.forEach(term => {
            const regex = new RegExp(`(${term})`, 'gi');
            highlightedText = highlightedText.replace(regex, '<mark>$1</mark>');
        });
        
        return highlightedText;
    }

    // Enhanced chat functionality
    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (!message) return;

        // Clear input
        input.value = '';
        
        // Add user message to chat
        this.addChatMessage(message, 'user');
        
        // Update statistics
        this.messagesCount++;
        this.updateChatStats();
        
        // Detect language
        const detectedLanguage = this.detectLanguage(message);
        if (detectedLanguage) {
            this.languages[detectedLanguage]++;
        }

        try {
            // Show typing indicator
            this.addTypingIndicator();

            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    language: detectedLanguage
                })
            });

            const data = await response.json();
            
            // Remove typing indicator
            this.removeTypingIndicator();
            
            // Add bot response
            if (data.response) {
                this.addChatMessage(data.response, 'bot');
                this.messagesCount++;
                this.updateChatStats();
            }

        } catch (error) {
            console.error('Chat error:', error);
            this.removeTypingIndicator();
            this.addChatMessage('Sorry, I encountered an error. Please try again.', 'bot');
            this.showNotification('Chat error occurred', 'error');
        }
    }

    // Add chat message
    addChatMessage(message, sender) {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return;

        // Remove welcome message if it exists
        const welcomeMessage = messagesContainer.querySelector('.text-center');
        if (welcomeMessage) {
            welcomeMessage.remove();
        }

        const messageElement = document.createElement('div');
        messageElement.className = `chat-message ${sender}`;
        messageElement.innerHTML = this.formatChatMessage(message);
        
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Store in chat history
        this.chatHistory.push({ message, sender, timestamp: new Date() });
    }

    // Format chat message with markdown-like formatting
    formatChatMessage(message) {
        return message
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
    }

    // Language detection (simple implementation)
    detectLanguage(text) {
        const arabicRegex = /[\u0600-\u06FF]/;
        const frenchWords = ['le', 'la', 'les', 'de', 'du', 'des', 'et', 'est', 'pour', 'avec', 'sur', 'dans', 'par', 'que', 'qui', 'quoi', 'comment', 'où', 'quand', 'pourquoi'];
        
        if (arabicRegex.test(text)) {
            return 'ar';
        }
        
        const words = text.toLowerCase().split(' ');
        const frenchWordsFound = words.filter(word => frenchWords.includes(word)).length;
        
        if (frenchWordsFound >= 2) {
            return 'fr';
        }
        
        return 'en'; // Default to English
    }

    // Update chat statistics
    updateChatStats() {
        const messagesCountElement = document.getElementById('messages-count');
        const languagesDetectedElement = document.getElementById('languages-detected');
        
        if (messagesCountElement) {
            messagesCountElement.textContent = this.messagesCount;
        }
        
        if (languagesDetectedElement) {
            const uniqueLanguages = Object.values(this.languages).filter(count => count > 0).length;
            languagesDetectedElement.textContent = uniqueLanguages;
        }
    }

    // Utility functions
    formatFileSize(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    }

    formatDate(date) {
        return new Date(date).toLocaleDateString();
    }

    // Show notification
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; max-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    // Additional utility methods
    addTypingIndicator() {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return;

        const typingElement = document.createElement('div');
        typingElement.className = 'chat-message bot typing-indicator';
        typingElement.innerHTML = `
            <div class="typing-dots">
                <span></span><span></span><span></span>
            </div>
        `;
        typingElement.id = 'typing-indicator';
        
        messagesContainer.appendChild(typingElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // Tab switching
    switchTab(tabName) {
        const tabElement = document.querySelector(`[data-bs-target="#${tabName}"]`);
        if (tabElement) {
            const tab = new bootstrap.Tab(tabElement);
            tab.show();
        }
    }

    // Event handlers for new features
    handleSearchKeyPress(event) {
        if (event.key === 'Enter') {
            this.performSearch();
        }
    }

    handleChatKeyPress(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            this.sendMessage();
        }
    }

    // Placeholder methods for new features
    async loadActivityFeed() {
        // Implementation for activity feed
    }

    async loadAnalytics() {
        // Implementation for analytics
    }

    async loadCollections() {
        try {
            const response = await fetch('/api/collections');
            this.currentCollections = await response.json();
            // Render collections
        } catch (error) {
            console.error('Failed to load collections:', error);
        }
    }

    onTabSwitch(targetTab) {
        // Handle tab-specific loading
        console.log('Switched to tab:', targetTab);
    }

    // Sample message senders
    sendSampleMessage(language) {
        const sampleMessages = {
            en: "Hello! What Sipsty products do you have?",
            fr: "Bonjour ! Quels produits Sipsty avez-vous ?",
            ar: "مرحباً! ما هي منتجات سيبستي المتوفرة؟"
        };
        
        const input = document.getElementById('chat-input');
        if (input) {
            input.value = sampleMessages[language];
            input.focus();
        }
    }

    // Additional methods for enhanced functionality
    async refreshSystemStatus() {
        await this.checkSystemStatus();
        this.showNotification('System status refreshed', 'info');
    }

    async refreshDocuments() {
        await this.loadDocuments();
        this.showNotification('Documents refreshed', 'info');
    }

    clearChat() {
        const messagesContainer = document.getElementById('chat-messages');
        if (messagesContainer) {
            messagesContainer.innerHTML = `
                <div class="text-center text-muted py-4">
                    <i class="fas fa-comments fa-2x mb-3 opacity-50"></i>
                    <h6>Welcome to Sipsty AI Assistant</h6>
                    <p class="small">Ask questions in English, French, or Arabic</p>
                </div>
            `;
        }
        this.chatHistory = [];
        this.messagesCount = 0;
        this.languages = { en: 0, fr: 0, ar: 0 };
        this.updateChatStats();
    }

    copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            this.showNotification('Copied to clipboard', 'success');
        }).catch(err => {
            console.error('Copy failed:', err);
            this.showNotification('Copy failed', 'error');
        });
    }
}

// Initialize dashboard
let dashboard;
document.addEventListener('DOMContentLoaded', function() {
    dashboard = new SipstyDashboard();
});

// Global functions for backward compatibility
function uploadFile() { dashboard.handleFileUpload(document.getElementById('fileInput').files); }
function sendMessage() { dashboard.sendMessage(); }
function performSearch() { dashboard.performSearch(); }
function handleSearchKeyPress(event) { dashboard.handleSearchKeyPress(event); }
function handleChatKeyPress(event) { dashboard.handleChatKeyPress(event); }
function switchTab(tabName) { dashboard.switchTab(tabName); }
function refreshSystemStatus() { dashboard.refreshSystemStatus(); }
function refreshDocuments() { dashboard.refreshDocuments(); }
function clearChat() { dashboard.clearChat(); }
function sendSampleMessage(lang) { dashboard.sendSampleMessage(lang); }

