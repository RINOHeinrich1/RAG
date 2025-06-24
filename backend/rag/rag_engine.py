from rag.index import build_or_load_index
from rag.embedding import get_embedding
from rag.generation import generate
from rag.knowledge_base import load_knowledge_base
from rag.cache import get_cache, set_cache

def retrieve_documents(index, dataset, query, k=3, threshold=40):
    query_emb = get_embedding([query])
    print("➡️ Dimension embedding requête :", query_emb.shape)
    print("➡️ Dimension index FAISS :", index.d)
    distances, indices = index.search(query_emb, k)
    print("📏 Distances :", distances[0])
    return [
        dataset[int(idx)]["texte"]
        for dist, idx in zip(distances[0], indices[0])
        if idx != -1 and dist <= threshold
    ]

def generate_answer(query, docs):
    cached = get_cache(query, docs)
    if cached:
        return cached

    if not docs:
        return "Je ne dispose pas d'informations pertinentes pour répondre à cette question."

    #contexte = "\n---\n".join(docs)
    contexte = docs[0]
    prompt = f"{contexte}\nQuestion: {query}\Answer:"

    result = generate(prompt)
    if "Réponse :" in result:
        result = result.split("Réponse :")[-1].strip()

    set_cache(query, docs, result)
    return result
