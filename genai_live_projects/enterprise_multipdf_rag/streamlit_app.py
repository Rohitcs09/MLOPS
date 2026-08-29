import streamlit as st
from rag_engine import ingest, retrieve, answer_question, get_collection

st.set_page_config(page_title="Enterprise Multi-PDF RAG", page_icon="📚", layout="wide")

st.title("📚 Enterprise Multi-PDF RAG Assistant")
st.caption("PDF → Chunking → Embeddings → ChromaDB → Retrieval → LLM")

with st.sidebar:
    st.header("Knowledge Base")
    uploaded = st.file_uploader("Upload PDF documents", type=["pdf"], accept_multiple_files=True)
    chunk_size = st.slider("Chunk size", 400, 1600, 900, 100)
    overlap = st.slider("Chunk overlap", 0, 300, 150, 25)
    top_k = st.slider("Top-K results", 1, 10, 5)

    if st.button("🧹 Reset Knowledge Base", use_container_width=True):
        get_collection(reset=True)
        st.success("Knowledge base reset.")
        st.rerun()

if uploaded:
    st.subheader("Selected Documents")
    for f in uploaded:
        st.write(f"📄 {f.name}")

    if st.button("🚀 Build / Update Knowledge Base", type="primary"):
        with st.spinner("Extracting PDFs, chunking text and creating embeddings..."):
            stats = ingest(uploaded, chunk_size, overlap)
        st.success(f"{stats['documents']} PDFs processed → {stats['chunks']} chunks stored in ChromaDB.")

count = get_collection().count()
a, b, c = st.columns(3)
a.metric("Vector Records", count)
b.metric("Chunk Size", chunk_size)
c.metric("Top-K", top_k)

st.divider()
st.subheader("💬 Ask the Knowledge Base")
query = st.text_input("Ask a question", placeholder="Example: What is the work from home policy?")

if st.button("🔎 Search & Answer", type="primary", disabled=not query.strip()):
    with st.spinner("Searching ChromaDB and generating answer..."):
        hits = retrieve(query, top_k)
        answer = answer_question(query, hits)

    st.markdown("### 🤖 Answer")
    st.write(answer)

    st.markdown("### 📚 Retrieved Sources")
    if not hits:
        st.warning("No relevant sources found.")
    for i, hit in enumerate(hits, 1):
        m = hit["metadata"]
        with st.expander(f"{i}. {m['source']} — Page {m['page']} — Chunk {m['chunk']}"):
            st.write(hit["text"])
            st.caption(f"ChromaDB distance: {hit['distance']:.4f}")

st.divider()
st.caption("Learning project: production-style Multi-PDF RAG architecture.")
