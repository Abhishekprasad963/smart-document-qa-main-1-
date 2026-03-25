# vector_store_free.py
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List
import os

class VectorStore:
    def __init__(self):
        """Initialize the vector store with ChromaDB and free Hugging Face embeddings"""
        self.client = chromadb.Client(Settings(anonymized_telemetry=False))
        self.collection_name = "documents"
        self.collection = None
        
        # Use a free, high-quality embedding model from Hugging Face
        print("Loading embedding model (this may take a moment on first run)...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Embedding model loaded!")
    
    def create_collection(self):
        """Create or get existing collection"""
        try:
            # Try to create new collection
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            print(f"Created new collection: {self.collection_name}")
        except Exception as e:
            # Collection might already exist, try to get it
            try:
                self.collection = self.client.get_collection(name=self.collection_name)
                print(f"Using existing collection: {self.collection_name}")
            except Exception as e2:
                print(f"Error with collection: {e2}")
                raise e2
    
    def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Get embeddings using free Hugging Face model
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            # Use Sentence Transformers to generate embeddings
            embeddings = self.embedding_model.encode(texts, convert_to_tensor=False)
            
            # Convert to list of lists (ChromaDB format)
            embeddings_list = [embedding.tolist() for embedding in embeddings]
            
            print(f"Generated {len(embeddings_list)} embeddings using free model")
            return embeddings_list
            
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            raise e
    
    def add_documents(self, chunks: List[str], filename: str):
        """
        Add document chunks to vector store
        
        Args:
            chunks: List of text chunks
            filename: Source filename for metadata
        """
        if not chunks:
            print("No chunks to add")
            return
        
        try:
            print(f"Adding {len(chunks)} chunks from {filename}")
            
            # Generate embeddings for all chunks
            embeddings = self.get_embeddings(chunks)
            
            # Create unique IDs and metadata for each chunk
            ids = [f"{filename}_{i}" for i in range(len(chunks))]
            metadatas = [
                {
                    "source": filename, 
                    "chunk_id": i,
                    "text_length": len(chunk)
                } 
                for i, chunk in enumerate(chunks)
            ]
            
            # Add to ChromaDB collection
            self.collection.add(
                embeddings=embeddings,
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            
            print(f"✅ Successfully added {len(chunks)} chunks to vector store")
            
        except Exception as e:
            print(f"Error adding documents: {e}")
            raise e
    
    def search(self, query: str, n_results: int = 3) -> List[str]:
        """
        Search for relevant chunks using semantic similarity
        
        Args:
            query: Search query string
            n_results: Number of results to return
            
        Returns:
            List of relevant text chunks
        """
        if not self.collection:
            print("No collection available for search")
            return []
        
        try:
            print(f"Searching for: '{query}'")
            
            # Generate embedding for the query
            query_embedding = self.get_embeddings([query])[0]
            
            # Search the collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            # Extract documents from results
            documents = results['documents'][0] if results['documents'] else []
            
            print(f"Found {len(documents)} relevant chunks")
            return documents
            
        except Exception as e:
            print(f"Error during search: {e}")
            return []
    
    def get_collection_info(self):
        """Get information about the current collection"""
        if not self.collection:
            return "No collection initialized"
        
        try:
            count = self.collection.count()
            return f"Collection '{self.collection_name}' contains {count} documents"
        except Exception as e:
            return f"Error getting collection info: {e}"

# Test the vector store (optional)
if __name__ == "__main__":
    vector_store = VectorStore()
    vector_store.create_collection()
    
    # Test with sample documents
    test_chunks = [
        "Machine learning is a subset of artificial intelligence.",
        "Deep learning uses neural networks with multiple layers.",
        "Natural language processing helps computers understand text."
    ]
    
    vector_store.add_documents(test_chunks, "test_document.txt")
    
    # Test search
    results = vector_store.search("What is machine learning?", n_results=2)
    print("Search results:")
    for i, result in enumerate(results):
        print(f"{i+1}. {result}")

