# app_free.py
import streamlit as st
import os
from dotenv import load_dotenv
from document_processor import DocumentProcessor
from vector_store import VectorStore
from qa_engine import QAEngine

# Load environment variables (optional now)
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Smart Document Q&A (Free Version)",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components (cached to avoid recreation)
@st.cache_resource
def initialize_components():
    """Initialize and cache the main components"""
    try:
        processor = DocumentProcessor(chunk_size=1000, chunk_overlap=200)
        vector_store = VectorStore()
        vector_store.create_collection()
        qa_engine = QAEngine(use_ollama=False)  # Set to True if you have Ollama running
        return processor, vector_store, qa_engine
    except Exception as e:
        st.error(f"Error initializing components: {e}")
        return None, None, None

def main():
    st.title("📚 Smart Document Q&A System (Free Version)")
    st.markdown("Upload documents and ask questions about their content using **completely free** AI!")
    
    # Info about the free version
    with st.expander("ℹ️ About this Free Version"):
        st.markdown("""
        **This version uses completely free alternatives:**
        - 🤖 **Embeddings**: Hugging Face Sentence Transformers (free)
        - 🔍 **Vector Search**: ChromaDB (free, local)
        - 💬 **Q&A**: Simple text processing (free) or Local Ollama (free)
        - 💰 **Cost**: $0 - No API keys required!
        
        **Note**: First time loading might be slow while downloading the embedding model.
        """)
    
    # Initialize components
    processor, vector_store, qa_engine = initialize_components()
    
    if not all([processor, vector_store, qa_engine]):
        st.error("Failed to initialize components. Please check your setup.")
        st.stop()
    
    # Sidebar for document management
    with st.sidebar:
        st.header("📄 Document Management")
        
        # File upload
        uploaded_files = st.file_uploader(
            "Choose files to upload",
            type=['pdf', 'txt'],
            accept_multiple_files=True,
            help="Upload PDF or text files to ask questions about them"
        )
        
        # Process uploaded files
        if uploaded_files:
            if st.button("🔄 Process Documents", type="primary"):
                process_documents(uploaded_files, processor, vector_store)
        
        # Display collection info
        st.divider()
        st.subheader("📊 Collection Info")
        if vector_store and vector_store.collection:
            info = vector_store.get_collection_info()
            st.info(info)
        else:
            st.info("No documents processed yet")
        
        # Settings
        st.divider()
        st.subheader("⚙️ Settings")
        
        # Number of chunks to retrieve
        n_results = st.slider(
            "Results to retrieve",
            min_value=1,
            max_value=10,
            value=3,
            help="How many document chunks to use for answering"
        )
        
        # Show sources toggle
        show_sources = st.checkbox(
            "Show source chunks",
            value=True,
            help="Display the source chunks used for answers"
        )
        
        # AI Method selection
        st.divider()
        st.subheader("🧠 AI Method")
        ai_method = st.radio(
            "Choose Q&A method:",
            ["Simple Text Processing", "Ollama (if running)"],
            help="Simple is always available, Ollama gives better results if you have it running"
        )

    # Main chat interface
    st.header("💬 Ask Questions")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources if available
            if message["role"] == "assistant" and "sources" in message and show_sources:
                display_sources(message["sources"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching documents and generating answer..."):
                
                # Check if we have any documents
                if not vector_store.collection or vector_store.collection.count() == 0:
                    answer = "❌ No documents have been uploaded yet. Please upload some documents first!"
                    sources = []
                else:
                    # Update QA engine method based on user choice
                    qa_engine.use_ollama = (ai_method == "Ollama (if running)")
                    
                    # Search for relevant chunks
                    relevant_chunks = vector_store.search(prompt, n_results=n_results)
                    
                    if relevant_chunks:
                        # Generate answer
                        answer = qa_engine.generate_answer(prompt, relevant_chunks)
                        sources = relevant_chunks
                        
                        # Add method info to answer
                        method_used = "Ollama" if qa_engine.use_ollama else "Simple Processing"
                        answer += f"\n\n*Answer generated using: {method_used}*"
                    else:
                        answer = "❌ No relevant information found in the uploaded documents for your question."
                        sources = []
                
                # Display answer
                st.markdown(answer)
                
                # Show sources if enabled and available
                if show_sources and sources:
                    display_sources(sources)
            
            # Add assistant response to chat history
            st.session_state.messages.append({
                "role": "assistant", 
                "content": answer,
                "sources": sources if show_sources else []
            })

def process_documents(uploaded_files, processor, vector_store):
    """Process uploaded documents and add them to the vector store"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_files = len(uploaded_files)
    processed_count = 0
    
    for i, uploaded_file in enumerate(uploaded_files):
        try:
            status_text.text(f"Processing {uploaded_file.name}...")
            
            # Process the file
            text, chunks = processor.process_file(uploaded_file)
            
            if chunks:
                # Add to vector store
                vector_store.add_documents(chunks, uploaded_file.name)
                processed_count += 1
                st.success(f"✅ Processed {uploaded_file.name}: {len(chunks)} chunks created")
            else:
                st.warning(f"⚠️ No text extracted from {uploaded_file.name}")
            
            # Update progress
            progress_bar.progress((i + 1) / total_files)
            
        except Exception as e:
            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
    
    # Final status
    status_text.text(f"✅ Processing complete! {processed_count}/{total_files} files processed successfully.")
    progress_bar.progress(1.0)

def display_sources(sources):
    """Display source chunks in an expandable section"""
    if not sources:
        return
    
    with st.expander(f"📖 View {len(sources)} source chunks used for this answer"):
        for i, chunk in enumerate(sources):
            st.markdown(f"**Source {i+1}:**")
            # Use a more unique key with timestamp to avoid duplicates
            import time
            unique_key = f"source_{i}_{len(st.session_state.messages)}_{int(time.time() * 1000)}"
            st.text_area(
                f"Chunk {i+1}",
                value=chunk,
                height=100,
                key=unique_key,
                disabled=True
            )
            if i < len(sources) - 1:  # Don't add divider after last chunk
                st.divider()

# Clear chat history button
if st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# Instructions
with st.sidebar:
    st.divider()
    st.subheader("📖 Quick Start")
    st.markdown("""
    1. **Upload** a PDF or text file
    2. **Click** "Process Documents"
    3. **Ask** questions about the content
    4. **Switch** between AI methods to compare results
    """)

if __name__ == "__main__":
    main()

