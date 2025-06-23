import React, { useState } from "react";
import { askQuestion } from "../api";

export default function ChatPage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    try {
      const res = await askQuestion(question);
      setAnswer(res.answer);
      setDocuments(res.documents);
    } catch (err) {
      console.error("Erreur lors de l'appel API :", err);
      setAnswer("Erreur lors de la génération de la réponse.");
      setDocuments([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-blue-50 flex items-center justify-center p-4">
      <div className="bg-white shadow-lg rounded-xl p-8 max-w-2xl w-full mx-auto">
        <h1 className="text-3xl font-bold text-blue-800 mb-6 text-center">
          Pose ta question
        </h1>

        <input
          type="text"
          placeholder="Ex: Qu'est-ce que l'ESTI ?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
          className="w-full border border-blue-300 rounded px-4 py-2 mb-4"
        />

        <button
          onClick={handleAsk}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded w-full"
        >
          {loading ? "Chargement..." : "Envoyer"}
        </button>

        {documents.length > 0 && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold text-blue-600 mb-2">
              📄 Documents :
            </h2>
            <ul className="list-disc list-inside space-y-1 text-gray-700">
              {documents.map((doc, idx) => (
                <li key={idx}>{doc}</li>
              ))}
            </ul>
          </div>
        )}

        {answer && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold text-blue-600 mb-2">
              🤖 Réponse :
            </h2>
            <p className="text-gray-800 bg-blue-100 p-4 rounded">{answer}</p>
          </div>
        )}
      </div>
    </div>
  );
}
