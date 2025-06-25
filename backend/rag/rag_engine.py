from rag.index import build_or_load_index
from rag.embedding import get_embedding
from rag.generation import generate
from rag.cache import get_cache, set_cache
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, SearchParams

def retrieve_documents(client: QdrantClient, collection_name: str, query: str, k=3, threshold=None):
    query_vector = get_embedding(query)  # pas besoin de []
    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=k,
        with_payload=True,
        search_params=SearchParams(hnsw_ef=128)  # Optionnel
    )

    filtered = []
    for r in results:
        if threshold is None or r.score >= threshold:  # Qdrant retourne la similarité (cosine) → plus c’est haut, mieux c’est
            filtered.append(r.payload["text"])

    return filtered

def generate_answer(query, docs):
    cached = get_cache(query, docs)
    if cached:
        return cached

    if not docs:
        return "Je ne dispose pas d'informations pertinentes pour répondre à cette question."

    contexte = "\n---\n".join(docs)

    result= contexte
    set_cache(query, docs, result)
    return result
