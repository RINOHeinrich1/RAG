import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8001";

export default function FineTunePage() {
  const [question, setQuestion] = useState("");
  const [results, setResults] = useState([]);
  const [selected, setSelected] = useState([]);
  const [status, setStatus] = useState("");
  const [showAllDocs, setShowAllDocs] = useState(false);
  const [allDocs, setAllDocs] = useState([]);
  const [selectedAllDocs, setSelectedAllDocs] = useState([]);

  const askQuestion = async () => {
    setStatus("Recherche...");
    try {
      const res = await axios.post(`${API_URL}/ask`, {
        question: question,
        top_k: 3,
      });
      setResults(res.data.results);
      setSelected([]);
      setStatus("Résultats reçus.");
      setShowAllDocs(false); // réinitialise vue
    } catch (err) {
      console.error(err);
      setStatus("❌ Erreur lors de la requête.");
    }
  };

  const fetchAllDocs = async () => {
    try {
      const res = await axios.get(`${API_URL}/documents`);
      setAllDocs(res.data.documents);
      setSelectedAllDocs([]);
      setShowAllDocs(true);
    } catch (err) {
      console.error(err);
      setStatus("❌ Erreur lors de la récupération des documents.");
    }
  };

  const submitFeedback = async (useAllDocs = false) => {
    const positives = useAllDocs
      ? selectedAllDocs.map((i) => allDocs[i])
      : selected.map((i) => results[i].doc);

    const negatives = useAllDocs
      ? allDocs.filter((_, i) => !selectedAllDocs.includes(i))
      : results.filter((_, i) => !selected.includes(i)).map((r) => r.doc);

    setStatus("Envoi du feedback...");
    try {
      const res = await axios.post(`${API_URL}/feedback`, {
        question: question,
        positive_docs: positives,
        negative_docs: negatives,
      });
      setStatus(res.data.message || "✅ Feedback envoyé !");
      setShowAllDocs(false); // fermer l'interface après envoi
    } catch (err) {
      console.error(err);
      setStatus("❌ Erreur lors de l’envoi du feedback.");
    }
  };
  const deployModel = async () => {
    setStatus("📦 Déploiement du modèle en cours...");
    try {
      const res = await axios.post(`${API_URL}/deploy`);
      const msg = res.data.message || "✅ Modèle déployé avec succès !";
      setStatus(msg);
    } catch (err) {
      console.error(err);
      setStatus("❌ Erreur lors du déploiement du modèle.");
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <h1>🎓 Assistant ESTI (RAG Fine-Tuning)</h1>

      <input
        type="text"
        value={question}
        placeholder="Pose une question..."
        onChange={(e) => setQuestion(e.target.value)}
        style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
      />

      <button onClick={askQuestion} style={{ padding: "10px 20px" }}>
        🔍 Chercher
      </button>

      {results.length > 0 && !showAllDocs && (
        <div style={{ marginTop: "20px" }}>
          <h2>📚 Résultats proposés</h2>
          {results.map((r, i) => (
            <div key={i} style={{ marginBottom: "8px" }}>
              <label>
                <input
                  type="checkbox"
                  checked={selected.includes(i)}
                  onChange={() =>
                    setSelected((prev) =>
                      prev.includes(i)
                        ? prev.filter((x) => x !== i)
                        : [...prev, i]
                    )
                  }
                  style={{ marginRight: "8px" }}
                />
                <strong>(score: {r.score.toFixed(4)})</strong> {r.doc}
              </label>
            </div>
          ))}

          <div style={{ marginTop: "15px" }}>
            <button
              onClick={() => submitFeedback(false)}
              style={{ padding: "10px 20px", marginRight: "10px" }}
            >
              🧠 Envoyer le feedback
            </button>

            <button
              onClick={fetchAllDocs}
              style={{
                padding: "10px 20px",
                backgroundColor: "#f44336",
                color: "white",
              }}
            >
              🚫 Aucun document n’est correct
            </button>
          </div>
        </div>
      )}

      {showAllDocs && (
        <div style={{ marginTop: "20px" }}>
          <h2>📋 Tous les documents</h2>
          {allDocs.map((doc, i) => (
            <div key={i} style={{ marginBottom: "8px" }}>
              <label>
                <input
                  type="checkbox"
                  checked={selectedAllDocs.includes(i)}
                  onChange={() =>
                    setSelectedAllDocs((prev) =>
                      prev.includes(i)
                        ? prev.filter((x) => x !== i)
                        : [...prev, i]
                    )
                  }
                  style={{ marginRight: "8px" }}
                />
                {doc}
              </label>
            </div>
          ))}

          <button
            onClick={() => submitFeedback(true)}
            style={{
              marginTop: "10px",
              padding: "10px 20px",
              backgroundColor: "#4CAF50",
              color: "white",
            }}
          >
            ✅ Envoyer les bons documents
          </button>
        </div>
      )}

      {status && (
        <p
          style={{
            marginTop: "20px",
            color: status.includes("❌") ? "red" : "green",
          }}
        >
          📝 {status}
        </p>
      )}
      <div
        style={{
          marginTop: "30px",
          borderTop: "1px solid #ccc",
          paddingTop: "20px",
        }}
      >
        <h2>🚀 Déploiement</h2>
        <button
          onClick={deployModel}
          style={{
            padding: "10px 25px",
            backgroundColor: "#2196F3",
            color: "white",
          }}
        >
          🚀 Déployer le modèle actuel
        </button>
      </div>
    </div>
  );
}
