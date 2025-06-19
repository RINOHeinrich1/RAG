import React, { useState } from "react";
import { askQuestion } from "./api";

function App() {
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
    <div style={{ padding: "2rem", fontFamily: "sans-serif", maxWidth: 800, margin: "auto" }}>
      <h1>🧠 Assistant RAG</h1>
      <input
        type="text"
        placeholder="Pose ta question ici..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && handleAsk()}
        style={{ width: "100%", padding: "0.75rem", fontSize: "1rem", marginBottom: "1rem" }}
      />
      <button
        onClick={handleAsk}
        disabled={loading}
        style={{ padding: "0.5rem 1rem", fontSize: "1rem", cursor: "pointer" }}
      >
        {loading ? "Chargement..." : "Envoyer"}
      </button>

      {documents.length > 0 && (
        <div style={{ marginTop: "2rem" }}>
          <h2>📄 Documents récupérés :</h2>
          <ul>
            {documents.map((doc, idx) => (
              <li key={idx}>{doc}</li>
            ))}
          </ul>
        </div>
      )}

      {answer && (
        <div style={{ marginTop: "2rem" }}>
          <h2>🤖 Réponse :</h2>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default App;
