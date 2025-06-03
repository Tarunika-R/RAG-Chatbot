import streamlit as st

# Must be the first Streamlit command
st.set_page_config(page_title="College Helpdesk Chatbot", page_icon="🎓")

from sentence_transformers import SentenceTransformer
from transformers import pipeline
import faiss
import numpy as np

# Sample knowledge base
documents = [
    "The admission process begins in March every year.",
    "You must submit your original documents during counseling.",
    "Hostel facilities are available for both boys and girls.",
    "Scholarships are provided based on merit and need.",
    "The placement cell invites companies from various industries.",
    "Attendance requirement is at least 75% per semester.",
    "The college library is open from 9 AM to 8 PM on weekdays.",
    "Online classes are available for some courses during vacations.",
    "Students can apply for internships through the training portal.",
    "Ragging is strictly prohibited and punishable by law."
]

# Load embedding model
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

# Embed documents (fix: underscore _model to skip caching it)
@st.cache_resource
def embed_documents(_model, docs):
    embeddings = _model.encode(docs, convert_to_tensor=False)
    dim = embeddings[0].shape[0]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))
    return index, np.array(embeddings)

# Load language model
@st.cache_resource
def load_generator():
    return pipeline("text-generation", model="gpt2")

# Load models
embedding_model = load_embedding_model()
index, doc_embeddings = embed_documents(embedding_model, documents)
generator = load_generator()

# UI
st.title("🎓 College Helpdesk Chatbot")
st.markdown("Ask me anything about admissions, hostels, placements, etc.")

# Input
user_query = st.text_input("Your Question")

if user_query:
    # Get query embedding
    query_embedding = embedding_model.encode([user_query])[0]
    D, I = index.search(np.array([query_embedding]), k=2)

    # Get top context
    retrieved_docs = [documents[i] for i in I[0]]
    context = " ".join(retrieved_docs)

    # Build prompt
    prompt = f"Context: {context}\n\nQuestion: {user_query}\nAnswer:"

    # Generate response
    response = generator(prompt, max_length=100, do_sample=True, temperature=0.7)[0]['generated_text']
    answer = response.split("Answer:")[-1].strip()

    # Display response
    st.markdown(f"**Answer:** {answer}")
