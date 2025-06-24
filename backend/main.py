from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from fastapi import Request
from fastapi.responses import JSONResponse
import os
import shutil
import tempfile
import requests
import numpy as np
import faiss
import zipfile
from rag.embedding import get_embedding, get_latest_model_path  # <-- modèle SentenceTransformer à jour
from rag.index import build_or_load_index,get_embedding,EMB_FILE,INDEX_FILE
from rag.rag_engine import retrieve_documents, generate_answer
from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from dotenv import load_dotenv
load_dotenv()

# --- Initialisation de l'application ---
app = FastAPI(title="RAG API")

# Autoriser le frontend React (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
collection_name=os.getenv("COLLECTION_NAME")
# --- Schémas Pydantic ---
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    documents: List[str]
    answer: str
    
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY"),
)

# --- Route principale ---
@app.post("/ask", response_model=AnswerResponse)
def ask_question(req: QuestionRequest):
    question = req.question
    docs = retrieve_documents(client, collection_name, question, k=1, threshold=0)
    print(docs)
    answer = generate_answer(question, docs)
    return AnswerResponse(documents=docs, answer=answer)

@app.get("/reload-model")
def reload_model(version: str = None, url: str = None):
    global collection_name, doc_embeddings, index

    if not url:
        return JSONResponse(status_code=400, content={"error": "Missing 'url' param"})

    try:
        # 1. Télécharger et extraire le zip
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "model.zip")

            r = requests.get(url)
            r.raise_for_status()
            with open(zip_path, "wb") as f:
                f.write(r.content)

            target_dir = f"./models/{version}"
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            os.makedirs(target_dir, exist_ok=True)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(target_dir)

        return {
            "status": "success",
            "message": f"✅ Modèle '{version}' rechargé avec succès.",
            "version": version,
            "model_used": get_latest_model_path()
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})   
# --- Mode CLI (facultatif) ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
