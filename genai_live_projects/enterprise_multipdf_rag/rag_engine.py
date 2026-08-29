from pathlib import Path
from typing import List, Dict, Optional
import chromadb
from openai import OpenAI
from pypdf import PdfReader

from config import OPENAI_API_KEY, EMBEDDING_MODEL, CHAT_MODEL

DB_PATH = Path("chroma_db")
COLLECTION_NAME = "enterprise_knowledge_base"

client = OpenAI(api_key=OPENAI_API_KEY)
chroma = chromadb.PersistentClient(path=str(DB_PATH))


def get_collection(reset: bool = False):
    if reset:
        try:
            chroma.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
    return chroma.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "Enterprise multi-PDF RAG knowledge base"},
    )


def extract_pdf(file_bytes: bytes, filename: str) -> List[Dict]:
    temp = Path(".tmp_uploaded.pdf")
    temp.write_bytes(file_bytes)
    try:
        reader = PdfReader(str(temp))
        pages = []
        for page_no, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append({"text": text.strip(), "page": page_no, "source": filename})
        return pages
    finally:
        temp.unlink(missing_ok=True)


def recursive_split(text: str, chunk_size: int = 900, overlap: int = 150) -> List[str]:
    separators = ["\n\n", "\n", ". ", " "]

    def split_level(value: str, level: int = 0) -> List[str]:
        if len(value) <= chunk_size:
            return [value.strip()] if value.strip() else []

        sep = separators[min(level, len(separators) - 1)]
        parts = value.split(sep)
        out, current = [], ""
        for part in parts:
            candidate = (current + sep + part).strip() if current else part.strip()
            if len(candidate) <= chunk_size:
                current = candidate
            else:
                if current:
                    out.append(current)
                if len(part) > chunk_size and level < len(separators) - 1:
                    out.extend(split_level(part, level + 1))
                    current = ""
                else:
                    current = part
        if current:
            out.append(current)
        return out

    raw = split_level(text)
    chunks = []
    for i, chunk in enumerate(raw):
        if i == 0 or not overlap:
            chunks.append(chunk)
        else:
            prefix = raw[i - 1][-overlap:]
            chunks.append((prefix + " " + chunk)[:chunk_size + overlap])
    return chunks


def embed(texts: List[str]) -> List[List[float]]:
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    return [item.embedding for item in response.data]


def ingest(files, chunk_size=900, overlap=150, reset=False):
    collection = get_collection(reset=reset)
    all_chunks = []

    for uploaded in files:
        for page in extract_pdf(uploaded.getvalue(), uploaded.name):
            for idx, chunk in enumerate(recursive_split(page["text"], chunk_size, overlap), 1):
                all_chunks.append({
                    "text": chunk, "source": page["source"],
                    "page": page["page"], "chunk": idx
                })

    if not all_chunks:
        return {"documents": 0, "chunks": 0, "collection": COLLECTION_NAME}

    for start in range(0, len(all_chunks), 64):
        batch = all_chunks[start:start + 64]
        vectors = embed([x["text"] for x in batch])
        ids = [f'{x["source"]}::p{x["page"]}::c{x["chunk"]}' for x in batch]
        collection.upsert(
            ids=ids,
            documents=[x["text"] for x in batch],
            embeddings=vectors,
            metadatas=[{"source": x["source"], "page": x["page"], "chunk": x["chunk"]} for x in batch],
        )

    return {
        "documents": len({x["source"] for x in all_chunks}),
        "chunks": len(all_chunks),
        "collection": COLLECTION_NAME,
    }


def retrieve(query: str, top_k: int = 5, source_filter: Optional[str] = None):
    collection = get_collection()
    if collection.count() == 0:
        return []

    q_vector = embed([query])[0]
    kwargs = {
        "query_embeddings": [q_vector],
        "n_results": min(top_k, collection.count()),
        "include": ["documents", "metadatas", "distances"],
    }
    if source_filter:
        kwargs["where"] = {"source": source_filter}

    result = collection.query(**kwargs)
    return [
        {"text": d, "metadata": m, "distance": dist}
        for d, m, dist in zip(
            result["documents"][0], result["metadatas"][0], result["distances"][0]
        )
    ]


def answer_question(query: str, hits: List[Dict]) -> str:
    if not hits:
        return "I could not find relevant information in the uploaded knowledge base."

    context = "\n\n".join(
        f"[Source: {h['metadata']['source']}, Page: {h['metadata']['page']}]\n{h['text']}"
        for h in hits
    )

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content":
             "You are an enterprise knowledge assistant. Answer only from the supplied context. "
             "Do not invent facts. If context is insufficient, say so. Cite source filename and page inline."},
            {"role": "user", "content": f"Question:\n{query}\n\nRetrieved context:\n{context}"},
        ],
    )
    return response.choices[0].message.content
