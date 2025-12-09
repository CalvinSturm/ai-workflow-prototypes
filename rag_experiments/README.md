# Local-Writer: Privacy-First RAG Pipeline

## Why this Architecture?

In enterprise environments—particularly within financial, healthcare, and legal sectors—data privacy is paramount. Many organizations cannot leverage public cloud LLMs due to strict compliance requirements (GDPR, HIPAA, SOC2) that forbid sensitive data from leaving their secure perimeter.

This project implements a **Local-Writer** pattern to address these constraints:

*   **Privacy-First Design:** By using `Ollama` for local inference and `ChromaDB` for local vector storage, this pipeline ensures **0% data egress**. No documents or prompts are sent to external APIs (like OpenAI or Anthropic).
*   **Cost-Control:** Local inference eliminates token-based pricing, allowing for unlimited iterations of document Q&A without accruing operational costs (OpEx).
*   **Latency vs. Security Tradeoff:** While local CPU inference (Llama 3 8B) introduces higher latency compared to cloud clusters, it provides the absolute data sovereignty required for highly regulated use cases.

This architecture serves as a prototype for a **"Private Cloud" RAG deployment**, mirroring the security needs of Fortune 500 clients who require bespoke AI solutions within their own VPCs (Virtual Private Clouds).

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
*   **Why Local?** To eliminate data exfiltration risks for sensitive financial/HR documents.
*   **Why Nomic Embed?** Chosen over standard BERT models for better semantic retrieval performance on technical documentation.
*   **Dual-Model Setup:** Decoupled inference and embedding to allow for independent scaling of retrieval accuracy vs. generation speed.

## ⚠️ Limitations & Future Work

As a prototype designed for local feasibility testing, this architecture makes specific trade-offs. A production-grade deployment for a Fortune 500 client would address the following:

### 1. Inference Latency (CPU vs. GPU)
*   **Current Limitation:** Running Llama 3 (8B) on consumer CPUs results in higher token generation latency.
*   **Production Solution:** Deploy inference endpoints on GPU-accelerated infrastructure (NVIDIA A100s or H100s) using **vLLM** or **TGI** to maximize throughput and minimize time-to-first-token (TTFT).

### 2. Retrieval Accuracy (Vector vs. Graph)
*   **Current Limitation:** Semantic search (Vector RAG) struggles with multi-hop reasoning or connecting disparate concepts across large document sets.
*   **Future Work (In Progress):** Integrating **Knowledge Graphs (GraphRAG)** to map entity relationships. This ensures that when a user asks about "Project X," the system retrieves not just keyword matches, but also connected stakeholders and dependencies.

### 3. Hallucination Mitigation
*   **Current Limitation:** The model answers based on retrieved chunks but lacks a robust verification layer.
*   **Production Solution:** Implement "Citation" constraints (forcing the model to reference source chunks) and a **Re-ranking** step (using Cross-Encoders) to filter out irrelevant chunks before they reach the LLM context window.

---
**Author:** Calvin Sturm
*AI Solutions Developer & Technical Consultant*
[LinkedIn](in\calvinsturm) | [Portfolio/Email](CalvinSturm@gmail.com)