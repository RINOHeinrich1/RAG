from datasets import Dataset
import pandas as pd
from transformers import AutoTokenizer, AutoModel, AutoModelForSeq2SeqLM, pipeline
import torch
import numpy as np
import faiss

# --- 1. Préparation de la base de connaissances en français ---
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

# --- 2. Chargement du tokenizer et modèle pour créer les embeddings ---
tokenizer_emb = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model_emb = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def get_embedding(texts):
    inputs = tokenizer_emb(texts, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model_emb(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.cpu().numpy()

# --- 3. Création des embeddings pour la base de connaissances ---
embeddings = []
batch_size = 16
texts = knowledge_base["texte"]
for i in range(0, len(texts), batch_size):
    batch_texts = texts[i:i+batch_size]
    batch_emb = get_embedding(batch_texts)
    embeddings.append(batch_emb)
embeddings = np.vstack(embeddings)

# --- 4. Création de l’index FAISS pour la recherche rapide ---
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# --- 5. Chargement du modèle francophone pour la génération de texte ---
model_name = "moussaKam/barthez"
tokenizer_gen = AutoTokenizer.from_pretrained(model_name)
model_gen = AutoModelForSeq2SeqLM.from_pretrained(model_name)
generator = pipeline("text2text-generation", model=model_gen, tokenizer=tokenizer_gen)

# --- 6. Fonction pour récupérer les documents pertinents ---
def retrieve_documents(query, k=1):
    query_emb = get_embedding([query])
    distances, indices = index.search(query_emb, k)
    results = []
    for idx in indices[0]:
        if idx == -1:
            continue
        results.append(knowledge_base[int(idx)]["texte"])
    return results

# --- 7. Fonction pour générer la réponse ---
def generate_answer(query, retrieved_docs):
    if not retrieved_docs:
        return "Je ne dispose pas d'informations pertinentes pour répondre à cette question."
    contexte = "\n---\n".join(retrieved_docs)
    prompt = (
        f"Voici un contexte en français :\n{contexte}\n\n"
        "Utilise uniquement ce contexte pour répondre à la question suivante en français. "
        "Si la réponse n'est pas dans ce contexte, réponds 'Je ne sais pas'.\n"
        f"Question : {query}\n"
        f"Réponse :"
    )
    outputs = generator(prompt, max_new_tokens=100)
    answer = outputs[0]['generated_text'].strip()
    return answer

# --- 8. Exemple d’utilisation ---
if __name__ == "__main__":
    question_utilisateur = "Parle du grand muraille de chine ?"
    docs = retrieve_documents(question_utilisateur, k=1)
    print("Documents récupérés :", docs)
    reponse = generate_answer(question_utilisateur, docs)
    print("Réponse générée :", reponse)
