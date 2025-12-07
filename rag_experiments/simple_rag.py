import os
import sys
import time
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter  # <--- NEW TOOL

# --- CONFIGURATION ---
MODEL_NAME = "llama3"
EMBEDDING_MODEL = "nomic-embed-text"
PDF_FILE = "handbook.pdf"

def main():
    if not os.path.exists(PDF_FILE):
        print(f"❌ ERROR: Could not find '{PDF_FILE}'.")
        return

    print(f"--- 🚀 Initializing Local RAG with {MODEL_NAME} ---")

    # 1. LOAD
    print("--- 📄 Loading PDF... ---")
    loader = PyPDFLoader(PDF_FILE)
    raw_pages = loader.load() # Load raw pages first
    print(f"   ✅ Raw document loaded ({len(raw_pages)} pages).")

    # 2. SPLIT (The Fix: Cut it into small pieces)
    print("--- ✂️  Splitting text into chunks... ---")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,       # Smaller chunks = Safer for local machine
        chunk_overlap=50      # Overlap ensures sentences aren't cut in half
    )
    chunks = text_splitter.split_documents(raw_pages)
    print(f"   ✅ Created {len(chunks)} text chunks.")

    # 3. EMBED
    print(f"--- 🧠 Creating Embeddings (via Ollama: {EMBEDDING_MODEL})... ---")
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    
    # Create DB from chunks
    db = Chroma.from_documents(
        documents=chunks, 
        embedding=embeddings, 
        persist_directory="./chroma_db"
    )
    print("   ✅ Vector Database Created.")

    # 4. CHAT
    print("--- 🔗 Connecting to Local LLM... ---")
    llm = ChatOllama(model=MODEL_NAME)
    
    prompt_template = """
    Use the following pieces of context to answer the question at the end. 
    If the context doesn't contain the answer, say "I don't see that in the document."
    
    Context: {context}
    
    Question: {question}
    
    Answer:"""
    
    PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=db.as_retriever(search_kwargs={"k": 5}), # Retrieve more chunks since they are smaller
        chain_type_kwargs={"prompt": PROMPT},
        return_source_documents=True
    )

    print("\n✅ SYSTEM READY. Type 'exit' to quit.\n")

    while True:
        query = input("You: ")
        if query.lower() in ["exit", "quit"]: break
        
        print("   🤖 Thinking...")
        try:
            result = qa_chain.invoke({"query": query})
            print(f"\nAI: {result['result']}\n")
            
            print("[Sources Used:]")
            for doc in result['source_documents']:
                print(f" - {doc.page_content[:60].replace(chr(10), ' ')}...")
            print("-" * 50)
        except Exception as e:
            print(f"❌ Error during chat: {e}")

if __name__ == "__main__":
    main()