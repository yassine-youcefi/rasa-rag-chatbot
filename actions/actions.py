from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import httpx
import logging
import os
import redis

# Import DeepSeek LLM generator
from deepseek_generator import create_deepseek_generator

logger = logging.getLogger(__name__)

# Configuration
PDF_PROCESSOR_HOST = os.getenv("PDF_PROCESSOR_HOST", "localhost")
PDF_PROCESSOR_PORT = int(os.getenv("PDF_PROCESSOR_PORT", "8001"))
REDIS_HOST = os.getenv("REDIS_HOST", "localhost") 
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
USE_LLM = os.getenv("LLM_TYPE", "").lower() == "deepseek_api"
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
MAX_RELEVANT_SENTENCES = int(os.getenv("MAX_RELEVANT_SENTENCES", "2"))
CONTEXT_SUMMARY_WORDS = int(os.getenv("CONTEXT_SUMMARY_WORDS", "100"))

# Initialize Redis client
try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    logger.info("Redis client initialized")
except Exception as e:
    logger.error(f"Failed to initialize Redis: {e}")
    redis_client = None

# Initialize DeepSeek LLM generator if enabled
deepseek_generator = None
if USE_LLM:
    try:
        deepseek_generator = create_deepseek_generator()
        logger.info("DeepSeek LLM generator initialized")
    except Exception as e:
        logger.error(f"Failed to initialize DeepSeek generator: {e}")
        deepseek_generator = None

class ActionAnswerQuestion(Action):
    """Custom action to answer questions using RAG"""
    
    def name(self) -> Text:
        return "action_answer_question"
    
    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # Get the user's question
            user_message = tracker.latest_message.get('text', '')
            
            if not user_message:
                dispatcher.utter_message(text="I didn't receive a question. What would you like to know?")
                return []
            
            logger.info(f"Processing question: {user_message}")
            
            # Check if there are any documents in the knowledge base
            async with httpx.AsyncClient() as client:
                # Search for relevant documents
                search_response = await client.get(
                    f"http://{PDF_PROCESSOR_HOST}:{PDF_PROCESSOR_PORT}/search",
                    params={"query": user_message, "max_results": MAX_SEARCH_RESULTS}
                )
                
                if search_response.status_code != 200:
                    dispatcher.utter_message(text="Sorry, I'm having trouble accessing the knowledge base. Please try again later.")
                    return []
                
                search_data = search_response.json()
                results = search_data.get("results", [])
                
                if not results:
                    dispatcher.utter_message(text="I couldn't find any relevant information in the uploaded documents. Please make sure you have uploaded PDFs that might contain the answer to your question.")
                    return []
                
                # Extract relevant context
                context_parts = []
                sources = set()
                
                for result in results:
                    context_parts.append(result["content"])
                    filename = result["metadata"].get("filename", "Unknown")
                    sources.add(filename)
                
                context = " ".join(context_parts)
                
                # Generate answer using DeepSeek LLM or fallback
                if USE_LLM and deepseek_generator:
                    answer = await self.generate_llm_answer(user_message, context)
                else:
                    answer = self.generate_simple_answer(user_message, context)
                
                # Format response with sources
                source_list = ", ".join(sources)
                response = f"{answer}\n\n📚 Sources: {source_list}"
                
                dispatcher.utter_message(text=response)
                
                # Store context in slot for potential follow-up questions
                return [SlotSet("context", context)]
                
        except Exception as e:
            logger.error(f"Error in ActionAnswerQuestion: {e}")
            dispatcher.utter_message(text="Sorry, I encountered an error while processing your question. Please try again.")
            return []
    
    async def generate_llm_answer(self, question: str, context: str) -> str:
        """Generate answer using DeepSeek LLM"""
        try:
            logger.info("Generating answer using DeepSeek LLM")
            answer = await deepseek_generator.generate_answer(question, context)
            return answer
        except Exception as e:
            logger.error(f"Error generating LLM answer: {e}")
            # Fallback to simple generation
            return self.generate_simple_answer(question, context)
    
    def generate_simple_answer(self, question: str, context: str) -> str:
        """
        Generate an answer based on the question and context
        This is a simple implementation - in production, you might want to use
        a language model like GPT or a local LLM for better answer generation
        """
        try:
            # Simple keyword-based answer generation
            # This is a basic implementation - you can enhance this with LLMs
            
            question_lower = question.lower()
            context_lower = context.lower()
            
            # Look for direct answers in the context
            sentences = context.split('.')
            relevant_sentences = []
            
            question_words = set(question_lower.split())
            question_words.discard('what')
            question_words.discard('how')
            question_words.discard('when')
            question_words.discard('where')
            question_words.discard('why')
            question_words.discard('is')
            question_words.discard('are')
            question_words.discard('the')
            question_words.discard('a')
            question_words.discard('an')
            
            for sentence in sentences:
                sentence_words = set(sentence.lower().split())
                # Check if sentence contains question keywords
                if question_words.intersection(sentence_words):
                    relevant_sentences.append(sentence.strip())
            
            if relevant_sentences:
                # Return the most relevant sentences
                answer = '. '.join(relevant_sentences[:MAX_RELEVANT_SENTENCES])
                if answer:
                    return f"Based on the uploaded documents: {answer}"
            
            # Fallback: return first part of context
            context_words = context.split()
            if len(context_words) > CONTEXT_SUMMARY_WORDS:
                summary = ' '.join(context_words[:CONTEXT_SUMMARY_WORDS]) + "..."
            else:
                summary = context
                
            return f"Here's what I found in the documents: {summary}"
            
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            return "I found relevant information in the documents, but had trouble formatting the answer. Please try rephrasing your question."


class ActionUploadPdf(Action):
    """Custom action to handle PDF upload requests"""
    
    def name(self) -> Text:
        return "action_upload_pdf"
    
    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # In a real implementation, you would need to handle file upload
            # This action provides instructions for uploading files
            
            message = f"""To upload a PDF document:

1. **Via API**: Send a POST request to:
   `http://{PDF_PROCESSOR_HOST}:{PDF_PROCESSOR_PORT}/upload-pdf`
   
2. **Via cURL**: 
   ```bash
   curl -X POST "http://{PDF_PROCESSOR_HOST}:{PDF_PROCESSOR_PORT}/upload-pdf" \\
        -H "accept: application/json" \\
        -H "Content-Type: multipart/form-data" \\
        -F "file=@/path/to/your/document.pdf"
   ```

3. **Programmatically**: Use any HTTP client to send a multipart form-data request with your PDF file.

After uploading, I'll process the document and you can ask questions about its content! 📄✨"""
            
            dispatcher.utter_message(text=message)
            return []
            
        except Exception as e:
            logger.error(f"Error in ActionUploadPdf: {e}")
            dispatcher.utter_message(text="Sorry, I encountered an error. Please try again.")
            return []


class ActionListPdfs(Action):
    """Custom action to list uploaded PDFs"""
    
    def name(self) -> Text:
        return "action_list_pdfs"
    
    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"http://{PDF_PROCESSOR_HOST}:{PDF_PROCESSOR_PORT}/documents")
                
                if response.status_code != 200:
                    dispatcher.utter_message(text="Sorry, I couldn't retrieve the document list. Please try again later.")
                    return []
                
                data = response.json()
                documents = data.get("documents", [])
                
                if not documents:
                    dispatcher.utter_message(text="No documents have been uploaded yet. Upload some PDFs to get started!")
                    return []
                
                # Format document list
                doc_list = "📚 **Uploaded Documents:**\n\n"
                for doc in documents:
                    status = doc.get("status", "unknown")
                    filename = doc.get("filename", "Unknown")
                    chunks = doc.get("chunks_count", 0)
                    
                    status_emoji = "✅" if status == "completed" else "⏳" if status == "processing" else "❌"
                    doc_list += f"{status_emoji} **{filename}** ({status})"
                    
                    if status == "completed" and chunks:
                        doc_list += f" - {chunks} chunks"
                    
                    doc_list += "\n"
                
                dispatcher.utter_message(text=doc_list)
                return []
                
        except Exception as e:
            logger.error(f"Error in ActionListPdfs: {e}")
            dispatcher.utter_message(text="Sorry, I encountered an error while retrieving the document list.")
            return []


class ActionClearKnowledgeBase(Action):
    """Custom action to clear all documents from knowledge base"""
    
    def name(self) -> Text:
        return "action_clear_knowledge_base"
    
    async def run(self, dispatcher: CollectingDispatcher,
                  tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.delete(f"http://{PDF_PROCESSOR_HOST}:{PDF_PROCESSOR_PORT}/documents")
                
                if response.status_code == 200:
                    dispatcher.utter_message(text="✅ All documents have been cleared from the knowledge base!")
                else:
                    dispatcher.utter_message(text="❌ Failed to clear the knowledge base. Please try again later.")
                
                return []
                
        except Exception as e:
            logger.error(f"Error in ActionClearKnowledgeBase: {e}")
            dispatcher.utter_message(text="Sorry, I encountered an error while clearing the knowledge base.")
            return []