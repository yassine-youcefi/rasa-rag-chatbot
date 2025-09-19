"""
DeepSeek API Generator for RAG Answer Generation
External API integration using DeepSeek's official API
"""

import httpx
import asyncio
import logging
import os
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class DeepSeekAPIGenerator:
    """DeepSeek API integration for intelligent answer generation"""
    
    def __init__(self, 
                 api_key: str,
                 base_url: str = "https://api.deepseek.com/v1",
                 model_name: str = "deepseek-chat",
                 temperature: float = 0.1,
                 max_tokens: int = 500,
                 timeout: float = 30.0):
        """
        Initialize DeepSeek API generator
        
        Args:
            api_key: DeepSeek API key
            base_url: DeepSeek API base URL
            model_name: DeepSeek model identifier
            temperature: Response creativity (0.0-1.0)
            max_tokens: Maximum response length
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        
        if not self.api_key or self.api_key == "your_deepseek_api_key_here":
            logger.warning("DeepSeek API key not configured. LLM features will be disabled.")
            self.enabled = False
        else:
            self.enabled = True
            logger.info(f"Initialized DeepSeek API generator: {model_name} @ {base_url}")
    
    async def generate_answer(self, question: str, context: str, max_retries: int = 3) -> str:
        """
        Generate intelligent answer using DeepSeek API
        
        Args:
            question: User's question
            context: Retrieved document context
            max_retries: Maximum retry attempts
            
        Returns:
            Generated answer string
        """
        
        if not self.enabled:
            return self._fallback_response(question, context)
        
        # Create optimized messages for DeepSeek Chat API
        messages = self._build_messages(question, context)
        
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": self.model_name,
                            "messages": messages,
                            "temperature": self.temperature,
                            "max_tokens": self.max_tokens,
                            "stream": False,
                            "stop": None
                        }
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        if "choices" in result and len(result["choices"]) > 0:
                            generated_text = result["choices"][0]["message"]["content"].strip()
                            
                            if generated_text:
                                return self._clean_response(generated_text)
                            else:
                                logger.warning(f"Empty response from DeepSeek API (attempt {attempt + 1})")
                        else:
                            logger.error(f"Invalid response format from DeepSeek API (attempt {attempt + 1})")
                    else:
                        error_msg = f"DeepSeek API error: {response.status_code}"
                        if response.status_code == 401:
                            error_msg += " - Invalid API key"
                        elif response.status_code == 429:
                            error_msg += " - Rate limit exceeded"
                        elif response.status_code == 500:
                            error_msg += " - Server error"
                        
                        logger.error(f"{error_msg} (attempt {attempt + 1})")
                        
                        # If it's an auth error, don't retry
                        if response.status_code == 401:
                            break
                            
            except httpx.TimeoutException:
                logger.warning(f"DeepSeek API request timeout (attempt {attempt + 1})")
            except Exception as e:
                logger.error(f"DeepSeek API generation error (attempt {attempt + 1}): {e}")
            
            if attempt < max_retries - 1:
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        
        # Fallback response
        logger.warning("All DeepSeek API attempts failed, using fallback response")
        return self._fallback_response(question, context)
    
    def _build_messages(self, question: str, context: str) -> list:
        """Build optimized messages for DeepSeek Chat API"""
        
        # Truncate context if too long (keep within token limits)
        max_context_length = 2000
        if len(context) > max_context_length:
            context = context[:max_context_length] + "..."
        
        system_message = """You are a helpful AI assistant that answers questions based on provided document context.

Instructions:
- Answer based ONLY on the provided context
- Be concise, accurate, and informative
- If the context doesn't contain relevant information, say "I cannot find information about this in the provided documents"
- Provide specific details when available
- Do not make up information not present in the context
- Keep responses clear and well-structured"""

        user_message = f"""Context from documents:
{context}

Question: {question}

Please provide a helpful answer based on the context above."""
        
        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    
    def _clean_response(self, response: str) -> str:
        """Clean and format the API response"""
        
        response = response.strip()
        
        # Remove common artifacts if they appear at the start
        artifacts = [
            "Based on the provided context:",
            "According to the context:",
            "From the document context:",
            "The context shows that:"
        ]
        
        for artifact in artifacts:
            if response.startswith(artifact):
                response = response[len(artifact):].strip()
        
        # Ensure proper capitalization
        if response and response[0].islower():
            response = response[0].upper() + response[1:]
        
        return response
    
    def _fallback_response(self, question: str, context: str) -> str:
        """Generate fallback response when API fails"""
        
        logger.info("Using fallback response generation")
        
        # Simple extractive summarization as fallback
        sentences = context.split('.')[:3]  # First 3 sentences
        summary = '. '.join(s.strip() for s in sentences if s.strip())
        
        if summary:
            return f"Based on the available documents: {summary}"
        else:
            return "I found relevant information in the documents, but cannot generate a detailed response at the moment. Please try rephrasing your question."
    
    async def health_check(self) -> Dict[str, Any]:
        """Check if DeepSeek API is accessible and working"""
        
        if not self.enabled:
            return {
                "status": "disabled",
                "message": "API key not configured",
                "api_accessible": False
            }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout * 0.33) as client:
                # Test with a simple request
                test_messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Say 'Hello' if you can hear me."}
                ]
                
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model_name,
                        "messages": test_messages,
                        "max_tokens": 10,
                        "temperature": 0
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if "choices" in result and len(result["choices"]) > 0:
                        return {
                            "status": "healthy",
                            "message": "API is accessible and responsive",
                            "api_accessible": True,
                            "model": self.model_name
                        }
                    else:
                        return {
                            "status": "error",
                            "message": "Invalid response format",
                            "api_accessible": True
                        }
                else:
                    return {
                        "status": "error",
                        "message": f"API returned status {response.status_code}",
                        "api_accessible": False
                    }
                    
        except Exception as e:
            return {
                "status": "error",
                "message": f"Health check failed: {str(e)}",
                "api_accessible": False
            }

# Factory function for easy initialization
def create_deepseek_generator() -> DeepSeekAPIGenerator:
    """Create DeepSeek API generator with environment configuration"""
    
    api_key = os.getenv("DEEPSEEK_API_KEY", "")
    
    if not api_key:
        logger.warning("DEEPSEEK_API_KEY not found in environment variables")
    
    return DeepSeekAPIGenerator(
        api_key=api_key,
        base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
        model_name=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        temperature=float(os.getenv("LLM_TEMPERATURE", "0.1")),
        max_tokens=int(os.getenv("LLM_MAX_TOKENS", "500")),
        timeout=float(os.getenv("LLM_TIMEOUT", "30.0"))
    )