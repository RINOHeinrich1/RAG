import faiss
import numpy as np
import os
from rag.embedding import get_embedding

EMB_FILE = "embeddings/embeddings.npy"
INDEX_FILE = "embeddings/faiss.index"

def build_or_load_index(dataset):
    if os.path.exists(EMB_FILE) and os.path.exists(INDEX_FILE):
        print("🔄 Chargement des embeddings et de l'index FAISS depuis disque...")
        embeddings = np.load(EMB_FILE)
        index = faiss.read_index(INDEX_FILE)
    else:
        print("⚙️ Génération des embeddings et de l'index FAISS...")
        texts = dataset["texte"]
        embeddings = get_embedding(texts)
        os.makedirs("embeddings", exist_ok=True)
        np.save(EMB_FILE, embeddings)

        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        faiss.write_index(index, INDEX_FILE)
    return index
