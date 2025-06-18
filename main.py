from datasets import Dataset
import pandas as pd
from transformers import CamembertTokenizer,AutoTokenizer, AutoModel, AutoModelForSeq2SeqLM, pipeline
import torch
import numpy as np
import faiss
import os

# --- 1. Préparation de la base de connaissances ---
data = {
    "texte": [
        "La capitale de la France est Paris.",
        "Le Mont Everest est la plus haute montagne du monde.",
        "Le Mont Everest mesure 8,849 m",
        "La Tour Eiffel se trouve à Paris.",
        "La Grande Muraille de Chine est visible depuis l'espace.",
        "Python est un langage de programmation populaire."
    ]
}
knowledge_base = Dataset.from_pandas(pd.DataFrame(data))

# --- 2. Chargement du modèle de vecteurs ---
tokenizer_emb = CamembertTokenizer.from_pretrained("dangvantuan/sentence-camembert-large")
model_emb = AutoModel.from_pretrained("dangvantuan/sentence-camembert-large")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_emb.to(device)

def get_embedding(texts):
    inputs = tokenizer_emb(texts, return_tensors="pt", padding=True, truncation=True).to(device)
    with torch.no_grad():
        outputs = model_emb(**inputs)
        embeddings = outputs.pooler_output  # Utilisation de pooler_output
    return embeddings.cpu().numpy()

# --- 3. Génération ou chargement des embeddings ---
EMB_FILE = "embeddings.npy"
INDEX_FILE = "faiss.index"

if os.path.exists(EMB_FILE) and os.path.exists(INDEX_FILE):
    print("🔄 Chargement des embeddings et de l'index FAISS depuis disque...")
    embeddings = np.load(EMB_FILE)
    index = faiss.read_index(INDEX_FILE)
else:
    print("⚙️ Génération des embeddings et de l'index FAISS...")
    texts = knowledge_base["texte"]
    embeddings = get_embedding(texts)
    np.save(EMB_FILE, embeddings)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    faiss.write_index(index, INDEX_FILE)

# --- 4. Chargement du modèle de génération francophone ---
model_name = "moussaKam/barthez"
tokenizer_gen = AutoTokenizer.from_pretrained(model_name)
model_gen = AutoModelForSeq2SeqLM.from_pretrained(model_name)
generator = pipeline("text2text-generation", model=model_gen, tokenizer=tokenizer_gen, device=0 if torch.cuda.is_available() else -1)

# --- 5. Recherche sémantique ---
def retrieve_documents(query, k=3, threshold=1):
    query_emb = get_embedding([query])
    distances, indices = index.search(query_emb, k)
    
    # 👇 Debug : Afficher les distances
    print("📏 Distances :", distances[0])
    
    return [
        knowledge_base[int(idx)]["texte"]
        for dist, idx in zip(distances[0], indices[0])
        if idx != -1 and dist <= threshold
    ]

# --- 6. Génération de réponse ---
cache = {}

def generate_answer(query, retrieved_docs):
    key = (query, tuple(retrieved_docs))
    if key in cache:
        return cache[key]

    if not retrieved_docs:
        return "Je ne dispose pas d'informations pertinentes pour répondre à cette question."

    contexte = "\n---\n".join(retrieved_docs)
    prompt = (
        f"{contexte}\n"
        f"Question: {query}\n"
        f"Réponse:"
    )


    outputs = generator(
        prompt,
        max_new_tokens=100,
        do_sample=True,
        temperature=0.5,
        num_return_sequences=1
    )
    answer = outputs[0]['generated_text'].strip()
    if "Réponse :" in answer:
        answer = answer.split("Réponse :")[-1].strip()

    cache[key] = answer
    return answer

# --- 7. Exemple d'utilisation ---
if __name__ == "__main__":
    question = "quelle est le plus haut sommet du monde?"
    documents = retrieve_documents(question, k=3, threshold=28)
    print("📄 Documents récupérés :", documents)
    reponse = generate_answer(question, documents)
    print("🤖 Réponse générée :", reponse)
