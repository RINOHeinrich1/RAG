from datasets import Dataset
import pandas as pd
from transformers import AutoTokenizer, AutoModel, pipeline
import torch
import numpy as np
import faiss

# 1. Préparation de la base de connaissances (en français)
data = {
    "texte": [
        "La capitale de la France est Paris.",
        "Le Mont Everest est la plus haute montagne du monde.",
        "La Tour Eiffel se trouve à Paris.",
        "La Grande Muraille de Chine est visible depuis l'espace.",
        "Python est un langage de programmation populaire."
    ]
}
knowledge_base = Dataset.from_pandas(pd.DataFrame(data))

# 2. Chargement du tokenizer et modèle pour créer les embeddings
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def get_embedding(texts):
    # Accepte une liste de textes
    inputs = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)  # pooling par moyenne
    return embeddings.cpu().numpy()

# 3. Création des embeddings pour la base de connaissances
embeddings = []
batch_size = 16
texts = knowledge_base["texte"]
for i in range(0, len(texts), batch_size):
    batch_texts = texts[i:i+batch_size]
    batch_emb = get_embedding(batch_texts)
    embeddings.append(batch_emb)
embeddings = np.vstack(embeddings)

# 4. Création de l’index FAISS pour la recherche rapide
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# 5. Chargement du pipeline de génération de texte (modèle léger)
generator = pipeline("text-generation", model="distilgpt2")

# 6. Fonction pour récupérer les documents pertinents
def retrieve_documents(query, k=2):
    query_emb = get_embedding([query])
    distances, indices = index.search(query_emb, k)
    results = [knowledge_base[int(idx)]["texte"] for idx in indices[0]]
    return results

# 7. Fonction pour générer la réponse à partir des documents récupérés
def generate_answer(query, retrieved_docs):
    contexte = " ".join(retrieved_docs)
    prompt = f"Contexte : {contexte}\nQuestion : {query}\nRéponse :"
    outputs = generator(prompt, max_new_tokens=50, num_return_sequences=1)
    generated_text = outputs[0]["generated_text"]
    # Extraction de la réponse après "Réponse :"
    answer = generated_text.split("Réponse :")[-1].strip()
    return answer

# 8. Exemple d’utilisation
if __name__ == "__main__":
    question_utilisateur = "Où se trouve la Tour Eiffel ?"
    docs = retrieve_documents(question_utilisateur, k=2)
    print("Documents récupérés :", docs)
    reponse = generate_answer(question_utilisateur, docs)
    print("Réponse générée :", reponse)
