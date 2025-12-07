from langchain_community.embeddings import OllamaEmbeddings

print("--- 🧪 Testing Embedding Engine ---")
try:
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vector = embeddings.embed_query("Hello, is this thing on?")
    print(f"✅ Success! Generated a vector of length: {len(vector)}")
    print("The engine is healthy.")
except Exception as e:
    print(f"❌ Failure: {e}")