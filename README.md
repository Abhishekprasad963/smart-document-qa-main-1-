# 📚 Smart Document Q&A System

A **completely free** AI-powered document question-answering system built with Python, Streamlit, and open-source models. Upload your documents (PDFs, text files) and ask questions about their content using local AI - no API keys or cloud services required!

![Demo](https://img.shields.io/badge/Status-Working-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## 🌟 Features

- **📄 Document Processing**: Upload and process PDF and text files
- **🧠 Free AI**: Uses Hugging Face transformers (no OpenAI API required)
- **🔍 Semantic Search**: Find relevant content using vector embeddings
- **💬 Interactive Chat**: Ask questions in natural language
- **🏠 100% Local**: Everything runs on your machine, completely private
- **⚡ Fast**: Cached models and efficient vector search
- **🎛️ Configurable**: Adjust search parameters and AI methods

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/smart-document-qa.git
   cd smart-document-qa
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run app_free.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## 📖 How to Use

1. **Upload Documents**: Use the sidebar to upload PDF or text files
2. **Process Documents**: Click "Process Documents" to analyze and embed your files
3. **Ask Questions**: Type questions about your documents in the chat interface
4. **View Sources**: Expand source chunks to see which parts of your documents were used for answers

### Example Questions

- "What programming languages are mentioned?"
- "Summarize the main qualifications"
- "What work experience is described?"
- "What companies are mentioned?"

## 🛠️ Technical Architecture

### Core Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Document       │    │  Vector Store    │    │  Q&A Engine     │
│  Processor      ├───►│  (ChromaDB)      ├───►│  (Local AI)     │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        ▲                         ▲                       ▲
        │                         │                       │
   ┌────────┐              ┌─────────────┐         ┌─────────────┐
   │ PDFs   │              │ Embeddings  │         │ Text        │
   │ Texts  │              │ (HuggingFace│         │ Processing  │
   └────────┘              │ Transformers│         │ or Ollama   │
                           └─────────────┘         └─────────────┘
```

### Key Technologies

- **[Streamlit](https://streamlit.io/)**: Web interface
- **[ChromaDB](https://www.trychroma.com/)**: Vector database for embeddings
- **[Sentence Transformers](https://www.sbert.net/)**: Free text embeddings
- **[PyPDF2](https://pypdf2.readthedocs.io/)**: PDF text extraction
- **[Tiktoken](https://github.com/openai/tiktoken)**: Token counting for optimal chunking

### How It Works

1. **Document Processing**: 
   - Extracts text from PDFs/text files
   - Splits into overlapping chunks (1000 tokens each)
   - Maintains context with 200-token overlap

2. **Embedding Generation**:
   - Uses `all-MiniLM-L6-v2` model from Sentence Transformers
   - Creates vector representations of text chunks
   - Stores in ChromaDB for fast similarity search

3. **Question Answering**:
   - Converts questions to embeddings
   - Finds most relevant document chunks
   - Generates answers using either:
     - Simple text processing (rule-based)
     - Local Ollama models (if available)

## ⚙️ Configuration

### Chunk Settings

Adjust in `document_processor.py`:
```python
processor = DocumentProcessor(
    chunk_size=1000,      # Tokens per chunk
    chunk_overlap=200     # Overlap between chunks
)
```

### Search Settings

Configure in the Streamlit sidebar:
- **Results to retrieve**: Number of chunks to use for answers (1-10)
- **Show source chunks**: Toggle to view source material
- **AI Method**: Choose between simple processing or Ollama

### Adding Ollama (Optional)

For better AI responses, install [Ollama](https://ollama.ai/):

1. **Install Ollama:**
   ```bash
   # macOS
   brew install ollama
   
   # Or download from https://ollama.ai
   ```

2. **Start Ollama service:**
   ```bash
   ollama serve
   ```

3. **Pull a model:**
   ```bash
   ollama pull llama3.2
   ```

4. **Select "Ollama" in the app settings**

## 📁 Project Structure

```
smart-document-qa/
├── app_free.py              # Main Streamlit application
├── document_processor.py    # PDF/text processing and chunking
├── vector_store.py         # ChromaDB vector database management
├── qa_engine.py            # Question answering logic
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🔧 Dependencies

```
streamlit>=1.28.0
chromadb>=0.4.0
sentence-transformers>=2.2.0
pypdf2>=3.0.0
python-dotenv>=1.0.0
tiktoken>=0.5.0
torch>=2.0.0
transformers>=4.30.0
requests>=2.31.0
```

## 🐛 Troubleshooting

### Common Issues

**1. "No module named 'sentence_transformers'"**
```bash
pip install sentence-transformers
```

**2. "Error processing PDF"**
- Ensure PDF is not password-protected
- Try with different PDF files
- Check file is not corrupted

**3. "ChromaDB connection error"**
```bash
pip install --upgrade chromadb
```

**4. Model download slow on first run**
- The embedding model (~90MB) downloads on first use
- Subsequent runs will be much faster

**5. Ollama connection error**
```bash
# Make sure Ollama is running
ollama serve

# Check if models are installed
ollama list
```

### Performance Tips

- **Chunk size**: Larger chunks (1500+ tokens) for longer documents
- **Overlap**: More overlap (300+ tokens) for better context preservation  
- **Results**: Retrieve more chunks (5-7) for complex questions
- **Memory**: Close other applications if running out of memory

## 🚀 Future Enhancements

### Planned Features
- [ ] Support for Word documents (.docx)
- [ ] Web scraping for URLs
- [ ] Conversation memory across sessions
- [ ] Multiple document collections
- [ ] Advanced chunking strategies
- [ ] Export chat history

### Advanced Configurations
- [ ] Custom embedding models
- [ ] Hybrid search (semantic + keyword)
- [ ] Document metadata filtering
- [ ] Multi-language support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Hugging Face** for free transformer models
- **ChromaDB** for the excellent vector database
- **Streamlit** for the amazing web framework
- **Sentence Transformers** for semantic search capabilities

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [Issues](https://github.com/YOUR_USERNAME/smart-document-qa/issues)
3. Create a new issue with detailed description

## ⭐ Star This Project

If you find this project helpful, please consider giving it a star on GitHub!

---

**Built with ❤️ using completely free and open-source tools**

