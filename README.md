# 📚 Smart Document Q&A System

A simple AI-powered app where you can **upload documents (PDF/text)** and **ask questions about them**.  
The system reads your document and gives answers using AI — all running locally (no paid APIs required).

---

## 🚀 Features

- 📄 Upload PDF or text files  
- 🔍 Ask questions about your documents  
- 🧠 Uses free AI models (no API key needed)  
- 💻 Runs completely on your system  
- ⚡ Fast search using embeddings  

---

## 🛠️ Tech Stack

- Python  
- Streamlit (UI)  
- ChromaDB (Vector Database)  
- Sentence Transformers (Embeddings)  
- PyPDF2 (PDF Processing)  
- Transformers / Torch (AI Models)  

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/smart-document-qa.git
cd smart-document-qa
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
# OR
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app_free.py
```

---

## ▶️ How to Use

1. Upload your document (PDF or text file)  
2. Click **Process Documents**  
3. Ask any question related to the document  
4. Get AI-generated answers  

---

## 💡 Example Questions

- What is this document about?  
- Summarize the content  
- What skills are mentioned?  
- Who is the author?  

---

## 📁 Project Structure

```
smart-document-qa/
├── app_free.py
├── document_processor.py
├── vector_store.py
├── qa_engine.py
├── requirements.txt
└── README.md
```

---

## 🎯 Key Concept

- Documents are split into small chunks  
- Each chunk is converted into vector embeddings  
- System finds relevant chunks based on your query  
- AI generates answers from those chunks  

---

## ⭐ Why This Project?

- Uses AI for document understanding  
- Fully free and runs locally  
- Good for learning AI + backend systems  
- Strong project for resume and internships  

---

## 📄 License

MIT License
