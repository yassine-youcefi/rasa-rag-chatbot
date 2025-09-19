import PyPDF2
import logging
from typing import List

logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize PDF processor
        
        Args:
            chunk_size: Maximum size of text chunks
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                
                return text.strip()
                
        except Exception as e:
            logger.error(f"Error extracting text from PDF {pdf_path}: {e}")
            raise

    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into chunks with overlap
        
        Args:
            text: Text to be chunked
            
        Returns:
            List of text chunks
        """
        if not text:
            return []
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # If this isn't the last chunk, try to end at a sentence boundary
            if end < len(text):
                # Look for the last sentence ending within the chunk
                sentence_endings = ['.', '!', '?', '\n']
                for i in range(end - 1, start + self.chunk_size // 2, -1):
                    if text[i] in sentence_endings:
                        end = i + 1
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            if start <= 0:
                break
                
        return chunks

    def extract_and_chunk_text(self, pdf_path: str) -> List[str]:
        """
        Extract text from PDF and split into chunks
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of text chunks
        """
        try:
            logger.info(f"Extracting text from PDF: {pdf_path}")
            
            # Extract text
            text = self.extract_text_from_pdf(pdf_path)
            
            if not text:
                logger.warning(f"No text extracted from PDF: {pdf_path}")
                return []
            
            # Chunk text
            chunks = self.chunk_text(text)
            
            logger.info(f"Successfully extracted and chunked PDF: {pdf_path} ({len(chunks)} chunks)")
            return chunks
            
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {e}")
            raise

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        
        Args:
            text: Text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        cleaned = " ".join(text.split())
        
        # Remove special characters that might interfere
        cleaned = cleaned.replace('\x00', '')  # Remove null characters
        
        return cleaned