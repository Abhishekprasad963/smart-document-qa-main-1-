# qa_engine_free.py
from typing import List
import requests
import json

class QAEngine:
    def __init__(self, use_ollama=False):
        """
        Initialize the QA engine with free alternatives
        
        Args:
            use_ollama: If True, use local Ollama. If False, use Hugging Face API (free)
        """
        self.use_ollama = use_ollama
        
        # Always initialize these attributes
        self.base_url = "http://localhost:11434/api/generate"
        self.model = "llama3.2"  # You can change this to any model you have installed
        
        if use_ollama:
            print("Using Ollama for Q&A (make sure Ollama is running)")
        else:
            print("Using simple text processing for Q&A (no API calls)")
    
    def generate_answer_simple(self, question: str, context_chunks: List[str]) -> str:
        """
        Generate answer using simple text processing (no API needed)
        """
        if not context_chunks:
            return "I cannot find relevant information in the provided documents to answer your question."
        
        # Combine all context
        full_context = " ".join(context_chunks)
        
        # Simple keyword matching approach
        question_lower = question.lower()
        
        # Look for specific patterns in questions
        if any(word in question_lower for word in ["what", "who", "where", "when", "how"]):
            # Try to find sentences that might contain answers
            sentences = full_context.split('.')
            relevant_sentences = []
            
            # Simple relevance scoring based on question words
            question_words = set(question_lower.split())
            question_words.discard("what")
            question_words.discard("who") 
            question_words.discard("where")
            question_words.discard("when")
            question_words.discard("how")
            question_words.discard("is")
            question_words.discard("the")
            question_words.discard("a")
            question_words.discard("an")
            
            for sentence in sentences:
                sentence_lower = sentence.lower()
                score = sum(1 for word in question_words if word in sentence_lower)
                if score > 0:
                    relevant_sentences.append((sentence.strip(), score))
            
            # Sort by relevance and take top sentences
            relevant_sentences.sort(key=lambda x: x[1], reverse=True)
            top_sentences = [s[0] for s in relevant_sentences[:3] if s[0]]
            
            if top_sentences:
                answer = "Based on the document, here's what I found:\n\n"
                answer += ". ".join(top_sentences)
                if not answer.endswith('.'):
                    answer += "."
                return answer
        
        # Fallback: return first few sentences of most relevant chunk
        if context_chunks:
            first_chunk = context_chunks[0]
            sentences = first_chunk.split('.')[:3]  # First 3 sentences
            return "Based on the document: " + ". ".join(sentences).strip() + "."
        
        return "I found some related information but cannot generate a specific answer. Please try rephrasing your question."
    
    def generate_answer_ollama(self, question: str, context_chunks: List[str]) -> str:
        """
        Generate answer using local Ollama model
        """
        if not context_chunks:
            return "I cannot find relevant information in the provided documents to answer your question."
        
        context = "\n\n".join([f"Chunk {i+1}:\n{chunk}" for i, chunk in enumerate(context_chunks)])
        
        prompt = f"""Based on the following context from documents, answer the question accurately and concisely.

If the answer cannot be found in the context, say "I cannot find this information in the provided documents."

Context:
{context}

Question: {question}

Answer:"""

        try:
            response = requests.post(
                self.base_url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.1,
                        "top_p": 0.9,
                        "max_tokens": 500
                    }
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "Error generating response")
            else:
                return f"Error: Ollama server responded with status {response.status_code}"
                
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Make sure Ollama is running locally."
        except Exception as e:
            return f"Error generating answer with Ollama: {str(e)}"
    
    def generate_answer(self, question: str, context_chunks: List[str]) -> str:
        """
        Main method to generate answers
        """
        if self.use_ollama:
            return self.generate_answer_ollama(question, context_chunks)
        else:
            return self.generate_answer_simple(question, context_chunks)
    
    def generate_followup_questions(self, question: str, answer: str, context_chunks: List[str]) -> List[str]:
        """
        Generate simple follow-up questions based on context
        """
        if not context_chunks:
            return []
        
        # Simple rule-based follow-up generation
        followups = []
        
        context_text = " ".join(context_chunks).lower()
        
        # Generate questions based on common entities/topics found
        if "experience" in context_text or "work" in context_text:
            followups.append("What work experience is mentioned?")
        
        if "skill" in context_text or "technology" in context_text:
            followups.append("What skills or technologies are discussed?")
        
        if "education" in context_text or "degree" in context_text:
            followups.append("What educational background is mentioned?")
        
        if "project" in context_text:
            followups.append("What projects are described?")
        
        if "company" in context_text or "organization" in context_text:
            followups.append("Which companies or organizations are mentioned?")
        
        return followups[:3]  # Return max 3 questions

# Test the QA engine
if __name__ == "__main__":
    qa_engine = QAEngine(use_ollama=False)  # Use simple approach
    
    # Test with sample context
    sample_context = [
        "John Smith has 5 years of experience as a software engineer. He worked at Google and Microsoft.",
        "He specializes in Python, JavaScript, and machine learning. John has a Computer Science degree from MIT."
    ]
    
    question = "What programming languages does John know?"
    answer = qa_engine.generate_answer(question, sample_context)
    print(f"Q: {question}")
    print(f"A: {answer}")
    
    # Test follow-up questions
    followups = qa_engine.generate_followup_questions(question, answer, sample_context)
    print(f"\nFollow-up questions:")
    for i, fq in enumerate(followups, 1):
        print(f"{i}. {fq}")

