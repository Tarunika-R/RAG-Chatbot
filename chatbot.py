import streamlit as st
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import faiss
import numpy as np

# --- Initialize Model and Index ---
st.set_page_config(page_title="RAG Chatbot", layout="centered")

@st.cache_resource
def load_models_and_index():
    documents = [
        "RAG stands for Retrieval-Augmented Generation.",
        "RAG allows chatbots to answer questions based on external documents.",
        "You can use FAISS to store and retrieve documents using vector similarity.",
        "Transformers like GPT can be used to generate human-like responses.",
        "The retriever finds relevant documents and the generator creates the answer.",
        "GPT-2 is a language model developed by OpenAI."
    ]
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    doc_embeddings = embedder.encode(documents)
    index = faiss.IndexFlatL2(doc_embeddings.shape[1])
    index.add(np.array(doc_embeddings))
    generator = pipeline("text-generation", model="gpt2")
    return embedder, generator, index, documents

embedder, generator, index, documents = load_models_and_index()

# --- Define Retrieval and Generation ---
def retrieve(query, top_k=1):
    query_vec = embedder.encode([query])
    distances, indices = index.search(np.array(query_vec), top_k)
    return [documents[i] for i in indices[0]]

def generate_answer(query):
    retrieved_docs = retrieve(query)
    context = " ".join(retrieved_docs)
    prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"
    response = generator(prompt, max_length=100, num_return_sequences=1)
    return response[0]["generated_text"].replace(prompt, "").strip()

# --- Streamlit UI ---
st.title("🧠 Simple RAG Chatbot")
st.markdown("Ask a question based on the internal knowledge base.")

user_input = st.text_input("You:", placeholder="Type your question here...")

if user_input:
    response = generate_answer(user_input)
    st.markdown("**Bot:** " + response)
