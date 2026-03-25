# document_processor.py
import PyPDF2
from typing import List, Tuple
import tiktoken
import io

class DocumentProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the document processor
        
        Args:
            chunk_size: Maximum number of tokens per chunk
            chunk_overlap: Number of tokens to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # Use tiktoken to count tokens accurately
        self.encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """
        Extract text from uploaded PDF file
        
        Args:
            pdf_file: Streamlit uploaded file object
            
        Returns:
            str: Extracted text from PDF
        """
        try:
            # Reset file pointer to beginning
            pdf_file.seek(0)
            # Create a BytesIO object from the uploaded file
            pdf_bytes = io.BytesIO(pdf_file.read())
            reader = PyPDF2.PdfReader(pdf_bytes)
            
            text = ""
            for page_num, page in enumerate(reader.pages):
                try:
                    page_text = page.extract_text()
                    if page_text.strip():  # Only add non-empty pages
                        text += f"\n--- Page {page_num + 1} ---\n"
                        text += page_text
                except Exception as e:
                    print(f"Error extracting page {page_num + 1}: {e}")
                    continue
            
            return text.strip()
        
        except Exception as e:
            print(f"Error processing PDF: {e}")
            return ""
    
    def extract_text_from_txt(self, txt_file) -> str:
        """
        Extract text from uploaded text file
        
        Args:
            txt_file: Streamlit uploaded file object
            
        Returns:
            str: File content as string
        """
        try:
            # Reset file pointer to beginning
            txt_file.seek(0)
            # Read as bytes and decode
            content = txt_file.read()
            if isinstance(content, bytes):
                text = content.decode('utf-8')
            else:
                text = str(content)
            return text.strip()
        except Exception as e:
            print(f"Error processing text file: {e}")
            return ""
    
    def count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text string"""
        return len(self.encoding.encode(text))
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks based on token count
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of text chunks
        """
        if not text.strip():
            return []
        
        # Encode the entire text into tokens
        tokens = self.encoding.encode(text)
        
        if len(tokens) <= self.chunk_size:
            # If text is smaller than chunk size, return as single chunk
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(tokens):
            # Get chunk of tokens
            end = start + self.chunk_size
            chunk_tokens = tokens[start:end]
            
            # Decode back to text
            try:
                chunk_text = self.encoding.decode(chunk_tokens)
                chunks.append(chunk_text)
            except Exception as e:
                print(f"Error decoding chunk: {e}")
                # Skip this chunk if there's a decoding error
                pass
            
            # Move start position, accounting for overlap
            start = end - self.chunk_overlap
            
            # Prevent infinite loop
            if start >= len(tokens):
                break
        
        # Remove empty chunks
        chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
        
        return chunks
    
    def process_file(self, uploaded_file) -> Tuple[str, List[str]]:
        """
        Process an uploaded file and return extracted text and chunks
        
        Args:
            uploaded_file: Streamlit uploaded file object
            
        Returns:
            Tuple of (extracted_text, chunks)
        """
        file_type = uploaded_file.type
        filename = uploaded_file.name
        
        print(f"Processing file: {filename} (type: {file_type})")
        
        # Extract text based on file type
        if file_type == "application/pdf":
            text = self.extract_text_from_pdf(uploaded_file)
        elif file_type == "text/plain":
            text = self.extract_text_from_txt(uploaded_file)
        else:
            print(f"Unsupported file type: {file_type}")
            return "", []
        
        if not text:
            print(f"No text extracted from {filename}")
            return "", []
        
        # Create chunks
        chunks = self.chunk_text(text)
        
        print(f"Extracted {len(text)} characters, created {len(chunks)} chunks")
        print(f"Token count: {self.count_tokens(text)}")
        
        return text, chunks

# Test the processor (you can run this to test)
if __name__ == "__main__":
    processor = DocumentProcessor()
    
    # Test with sample text
    sample_text = "This is a sample document. " * 100  # Repeat to make it long
    chunks = processor.chunk_text(sample_text)
    
    print(f"Sample text length: {len(sample_text)} characters")
    print(f"Token count: {processor.count_tokens(sample_text)}")
    print(f"Number of chunks: {len(chunks)}")
    print(f"First chunk: {chunks[0][:100]}...")

