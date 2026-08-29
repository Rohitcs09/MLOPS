# Enterprise Multi-PDF RAG AI Assistant

## Architecture
PDFs → extraction → recursive chunking → OpenAI embeddings → ChromaDB → Top-K retrieval → LLM → answer + sources

## Run
1. Create and activate a virtual environment.
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`
4. Add your OpenAI API key.
5. `streamlit run streamlit_app.py`

Sample PDFs are included in `data/`.

This is a course/demo project. Production systems should additionally address authentication, authorization, document versioning, ingestion queues, observability, evaluation, backups and deployment security.
