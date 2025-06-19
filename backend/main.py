from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from rag.knowledge_base import load_knowledge_base
from rag.index import build_or_load_index
from rag.rag_engine import retrieve_documents, generate_answer

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

# --- Chargement initial de la base et de l'index ---
knowledge_base = load_knowledge_base()
index = build_or_load_index(knowledge_base)

# --- Schémas Pydantic ---
class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    documents: List[str]
    answer: str

# --- Route principale ---
@app.post("/ask", response_model=AnswerResponse)
def ask_question(req: QuestionRequest):
    question = req.question
    docs = retrieve_documents(index, knowledge_base, question, k=3, threshold=34)
    answer = generate_answer(question, docs)
    return AnswerResponse(documents=docs, answer=answer)

# --- Mode CLI (facultatif) ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
