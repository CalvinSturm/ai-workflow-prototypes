# Local-Writer: Privacy-First RAG Pipeline

A completely offline, air-gapped Retrieval-Augmented Generation (RAG) system. 
Built to demonstrate how Enterprise data can be queried securely without API calls leaving the infrastructure.

## 🏗 Architecture

*   **Ingestion:** Python `langchain` pipeline to parse unstructured PDFs.
*   **Chunking:** Recursive character splitting (500 chars) to optimize context window retention.
*   **Vector Store:** ChromaDB (Persistent local storage).
*   **Embeddings:** `nomic-embed-text` (Running locally via Ollama).
*   **Inference:** `llama3` (Running locally via Ollama).
*   **UI:** Streamlit for chat interface.

## ⚙️ Prerequisites

1.  **Install Ollama:** [Download here](https://ollama.com/)
2.  **Pull the Models:**
    ```bash
    ollama pull llama3
    ollama pull nomic-embed-text
    ```

## 🛠️ Installation

1. Clone the repo
    ```bash
    git clone <your-repo-url>
    cd local-writer
    ```

2. Create virtual environment
    ```bash
    python -m venv venv
    ```
3. Activate environment

# Windows:
   ```bash
    venv\Scripts\activate
    ```

# Mac/Linux:
   ```bash
    source venv/bin/activate
    ```

4. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
    
## 🚀 How to Run
**Step 1: Start the Backend**
Ensure the Ollama app is running in the background (check your system tray).  

**Step 2: Generate Test Data (Optional)**
If you don't have a PDF handy, generate 3 synthetic enterprise documents:
   ```bash
    python generate_data.py
    ```
**Step 3: Launch the UI**
   ```bash
    streamlit run app.py
    ```
This will open the interface in your web browser at http://localhost:8501.

**Step 4: Use the System**
1. Drag and drop a PDF into the sidebar.
2. Wait for the "✅ Indexed" message.
3. Chat with your document.

## 🧠 Engineering Decisions
+ Why Local? To eliminate data exfiltration risks for sensitive financial/HR documents.
+ Why Nomic Embed? Chosen over standard BERT models for better semantic retrieval performance on technical documentation.
+ Dual-Model Setup: Decoupled inference and embedding to allow for independent scaling of retrieval accuracy vs. generation speed.