import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- PAGE SETUP ---
st.set_page_config(page_title="Local-Writer", page_icon="📝")
st.title("📝 Local-Writer (Private RAG)")

# --- SIDEBAR CONFIG ---
with st.sidebar:
    st.header("Configuration")
    model_name = st.selectbox("LLM Model", ["llama3"])
    embed_model = st.selectbox("Embedding Model", ["nomic-embed-text"])
    st.info("Files are processed locally. No data leaves this machine.")

# --- SESSION STATE (Memory) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_db" not in st.session_state:
    st.session_state.vector_db = None

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Upload a PDF to start", type=("pdf"))

# --- PROCESSING ENGINE ---
if uploaded_file and st.session_state.vector_db is None:
    with st.spinner("🧠 Ingesting document... (This runs on your GPU)"):
        # Save uploaded file to temp
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        # Load & Split
        loader = PyPDFLoader(tmp_path)
        raw_pages = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = text_splitter.split_documents(raw_pages)

        # Embed & Store
        embeddings = OllamaEmbeddings(model=embed_model)
        db = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db_web")
        
        st.session_state.vector_db = db
        st.success(f"✅ Indexed {len(chunks)} chunks from {uploaded_file.name}")
        os.remove(tmp_path) # Clean up

# --- CHAT INTERFACE ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about your document..."):
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AI Response
    if st.session_state.vector_db:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking...")
            
            # Setup Chain
            llm = ChatOllama(model=model_name)
            retriever = st.session_state.vector_db.as_retriever(search_kwargs={"k": 4})
            
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever,
                return_source_documents=True
            )
            
            # Run Query
            response = qa_chain.invoke({"query": prompt})
            result = response["result"]
            
            # Show Sources
            sources = "\n\n**Sources:**\n"
            for doc in response["source_documents"]:
                sources += f"- {doc.page_content[:50]}...\n"
            
            full_response = result + sources
            message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    else:
        st.error("Please upload a PDF first!")